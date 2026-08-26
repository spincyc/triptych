# Provenance

This package was produced by this lane's authoritative package attempt. That
attempt's identity is fixed BEFORE the run rather than minted during it, so a
member authored beforehand and frozen at P6 can refer to it: an attempt id
carrying a nonce invented at P0 could never appear in a document written in
advance, and a package whose prose cannot say which attempt it is cannot settle
the question it exists to settle. **The id and the ordinal are not typed here.**
`logs/attempts.json` carries both, and the ordinal in them was allocated by the
lane ledger and would have been refused if the lane had ever spent it.

What makes the attempt authoritative is not a sentence in this file: it is the
post-P8 authority record, a sibling named in `HANDOFF.md` §10, written only
after P8 passed and bound to the archive's recomputed size and digest. The
shipped `logs/attempts.json` says `sealed`, which is the most a member written
before P8 may say about itself.

What ran, where it ran, in what order, and which record wins where two could
disagree.

**The authority is the lane ledger, and the lane ledger ships beside this
package.** `logs/attempts.json` is the copy of this lane's rows taken as late as
the phase contract allows; the complete ledger is a sibling, named in
`HANDOFF.md` §10, so a reviewer can read every attempt this lane made without
reaching for a record outside the handoff. Where this file and the ledger could
be read as disagreeing, the ledger is right and this file is a defect.

No figure here is typed. `checks.txt` carries each command with its exit code,
its start and end, its tree state before and after, its attempt and its log;
`claims.json` carries the identity arithmetic; `DERIVED-CLAIMS.md` renders both.

## 0. The link this lane has, and the one it still does not

**This lane can name the review it answers, and the previous lane could not.**
It is `0d11766ec232b2b4e46a7d1b0ada56ef22370004`, on
`review/catena-wave-1-e1-corrections-v14-independent`, and it answered CHANGES
REQUIRED at the exact parent `69f2575421ba976271c936b1abd4b39dbe8b98fd`. So
`claims.json` carries `review_addressed` as that commit rather than as the empty
string, `DERIVED-CLAIMS.md` renders it rather than an em dash, and this lane's
account of the disposition is checkable against the disposition itself, which
is a property the previous lane recorded that it did not have.

**The older gap is not filled, and this lane does not fill it.** `origin` still
carries no `review/catena-wave-1-e1-corrections-v13-independent`. That review's
identity is truthfully absent, this lane cannot publish another lane's review,
and it does not invent one: the chain is intact from this link forward and
broken at the one before it. `LIMITATIONS.md` and `UNRESOLVED-BLOCKERS.md` both
record it, and neither presents it as closed.

The tool change the previous lane made for that gap stands and is not undone.
`logs/assemble.sh` reads its review argument as `${REVIEW-}` rather than
`${REVIEW:-…}`, because `:-` substitutes a default for an **empty** value as
well as an unset one, and a lane answering an unpublished review would silently
have claimed to answer the previous lane's. This lane exercises the same
mechanism in the other direction: a review that is present is recorded because
it is present, not because a default happened to be right.

## 1. Eight defects in the evidence itself, and what actually caused each

The review at `0d11766ec232b2b4e46a7d1b0ada56ef22370004` found the previous
package materially defective in eight respects. They are listed here with their
root causes, because a defect whose cause is not stated is a defect that recurs
under a different name. Each fix is in a tool this package ships under `logs/`,
so a reviewer reads the correction rather than taking its word; the resulting
verdicts are in `checks.txt`, in the executed-tool record and in the P8
tool-byte comparison table named in `HANDOFF.md` §10.

**1. Two browser-gate commands were recorded `ELIDED`.** The cause was not a
private value and not the pipeline's placeholders. `logs/checks.py` reads a
standalone capitalised token as a stand-in for a value the lane held — correctly,
because that is exactly how `logs/assemble.sh` records its package-phase
commands — and the browser-gate row carried the capitalised English word `JSON`
inside a quoted `echo` note that `logs/battery.sh` composes. It was **not** the
report's filename, which is lower case and glued to a dot, a shape the
classifier already exempts; and it was **not** the `$WORKSPACE` and `$EVIDENCE`
symbols, which are exempt by design because a shell variable in a recorded
command is an expansion, not an elision. The classifier was right to be
conservative, so the fix is in the note: the word is lower case now, the row
classifies `LITERAL`, and the battery carries a comment saying that any word
added to that note must stay lower case. The placeholder rule was not weakened.

**2. The load-bearing parent-replay command was recorded `PROSE`** — "a
description of what happened, not a string a shell was handed" — about a string
a shell was handed and which re-runs verbatim. The cause was that `cp` was
missing from the classifier's list of command heads, which carried only
interpreters and version-control tools, so a real `cp … && python3 -m unittest
…` chain failed the only test the verdict turns on. The list now also carries
the coreutils and shell builtins a battery composes with. It was **not** replaced
by a `shutil.which()` PATH probe: `checks.txt` is a shipped, byte-stable member
that a reviewer re-derives off-host, and a host-dependent classifier would give a
different verdict and different bytes on a different machine. The cost of a fixed
list is that it must be extended by hand when a battery invokes a head it never
invoked before, and that cost is stated in the tool.

**3. `logs/compare-gate.py` was labelled `shipped-not-executed` although the assembly
transcript records it running and exiting**, and the same was true of
`logs/gate-summary.py`, `logs/gzip-sizes.py` and `logs/journal-dump.py`. A tool's execution
state is now derived mechanically from the invocations the run actually
recorded, rather than being maintained beside them. What each tool's state is in
this package is in the executed-tool record and the P8 tool-byte table, not
here.

**4. One label counted invocation rows while a table a few lines above it
counted unique tools**, and the two disagreed because they were counting
different things under one word. A tool that runs a dozen times is one tool and
twelve rows, and both are worth knowing. The two are separately named now, and
no combined single-fraction label is printed at all — a single label cannot be right about
both, and the honest correction was to stop printing one.

**5. The attempt history was called `complete` and `append-only` while it was
neither.** It omitted a set-aside cohort and the post-seal rows, and another
member of that same package disclosed a rewrite of two of its own malformed
entries — a rewrite, not an append, in a file it called append-only two hundred
lines later. Both of those facts are about the PREVIOUS package's history, not
this one's: nothing in this lane's ledger has been taken out, rewritten or
replaced, and §7 states what is true of it. The wording is corrected, and the
completeness checker now refuses an append-only claim standing beside a
disclosed replacement, so the two statements can no longer ship in one package.

**6. A commit was described in `logs/named-commits.json` as a set-aside cohort
that "appears only in the append-only attempt ledger's set-aside row", and no
such row existed.** A named cohort with no matching ledger row is now refused.
This lane set no cohort aside and names none; see §8.

**7. `claims.json` did not derive every figure the package prose said it
derived.** The rule this package holds itself to is that a number in its prose
is quoted from `claims.json` or is a judgement a machine cannot make and is
labelled as one, and `logs/head-consistency.py` refuses a member whose prose
disagrees with the derived record. Where the derivation had a hole, the prose
was standing on nothing. Among the figures now derived rather than asserted are
the three workspace-provenance fields in §11.

**8. The mechanical handoff-completeness result printed `COMPLETE` while testing
none of the above** — which is the worst of the eight, because a green mechanical
verdict is what a reviewer reads instead of checking. It now also detects an
empty command slot, a transcript with no command row at all, the literal tokens
`ELIDED` and `PROSE` in a recorded slot, an executed-tool status its own
transcripts contradict, a named cohort with no ledger row, and an append-only
claim that cannot be true of the file it is made about.

**What this lane does not claim about any of them.** That a classifier wrong
about three commands is right about the fourth; that a checker which now models
six failures models every failure; or that this lane's verdict on its own
tooling is independent. `REVIEW_REQUEST.md` puts exactly that to the reviewer.

## 2. Two vocabularies, because there are two facts

"This validation battery ran to completion" and "this is the package to review"
are different facts, and writing both `authoritative` makes the authoritative
count uncountable by construction. So:

**A validation battery** (`side: head`, `side: parent`):

    started ──▶ complete ──▶ set-aside
            └─▶ failed

**A package attempt** (`side: package`):

    started ──▶ sealing ──▶ sealed ──▶ authoritative ──▶ superseded
                        └─▶ discarded

`authoritative` is reserved for a package attempt, it is post-terminal, and it
may be written in one place only — the complete external ledger, after P8 passes.
At most one package attempt in a lane may hold it, and this package's records
must resolve to exactly one. A battery written `authoritative` is a refusal, not
a row.

`set-aside` is the battery-side post-terminal word, and it exists so that a
cohort which ran and completed and whose figures are not used can be recorded
rather than deleted. It does not overwrite the verdict it supersedes: the
battery did complete, and the terminal row still says so.

**Every non-successful terminal or post-terminal state carries its reason**, on
the row that states it and in the summary the package ships. A row that ends
`failed`, `discarded`, `superseded` or `set-aside` with an empty reason is
refused, so a supersession, a discard and a set-aside each say what happened in
their own row rather than in a document beside it.

No attempt may be authoritative and superseded, unresolved and final, or
discarded and authoritative. Each is a distinct refusal in the coherence gate,
and each has a test that proves the refusal fires.

## 3. Authority is established after verification, and it binds the archive

The order is:

1. the attempt starts and is recorded started;
2. the package directory is sealed, and the strongest thing any in-package row
   may claim is `sealed`;
3. the manifest is taken and the archive is built;
4. P8 verifies the archive, read-only, executing no archive code;
5. the archive's byte size and SHA-256 are recomputed after P8;
6. **and only then** is final authority established.

The authority record is a structured sidecar naming the attempt, the exact head,
the archive's basename, its byte size and SHA-256, the P8 result and the post-P8
rehash result — **each recomputed from the archive rather than carried forward
from an earlier phase.** If P8 fails, the attempt stays non-authoritative and no
record anywhere calls it otherwise.

The binding runs one way and the archive carries no such record, so there is no
self-reference and no ordering problem. What it costs is that an authoritative
package cannot be self-describing: an archive cannot contain its own digest.
That is why this file names no size and no digest of its own package, and why
the figures live in the sidecar named in `HANDOFF.md` §10.

## 4. What the authority gate consumes, and what it refuses

The gate consumes the archive, the digest-and-size sidecar, the P8 transcript,
the complete external ledger, the sibling markers and the package's own prose,
and its negative roster covers each contradiction an earlier gate accepted: a
second authoritative state row, an authoritative winner followed by a discarded
state, multiline and uppercase contradictory prose, a wrong package on the
authoritative outer-log line, and prose that never names the winner.

This lane did not reopen that roster and does not claim to have re-derived it.
The V13 `authority-negative-fixtures` requirement stays **open** in the promise
ledger rather than marked passed: the review this lane answers did not raise it,
and disposing of a promise a review did not raise would be this lane answering a
question nobody asked. `LIMITATIONS.md` records it.

## 5. One ledger, one lane, ordinals that are never reused

**This lane's ledger is a new file**, opened once with the allocator's `--fresh`
assertion, which refuses to open over an existing ledger; and the allocator
refuses to append to, or read as its own, a ledger declaring a different lane.
The previous lane's ledger is neither reused nor extended, and it is not
modified by this lane at all.

There is one allocator. `logs/checks.py --allocate-ordinal` is called by
`logs/assemble.sh` and by `logs/battery.sh` alike, no tool computes a local
maximum, and the allocator refuses an ordinal any row has ever carried, however
that attempt ended. Ordinals are **monotonic and never reused**, so a rerun
cannot reproduce a previous attempt's log identity. An attempt id is
`<side>-<UTC stamp>-<ordinal><nonce>`, and the nonce is drawn from an alphabet
with no hex letter in it, so an attempt id can never be misread as an
abbreviated commit SHA by the identity audit.

**Chronology is checked.** A row whose time precedes the row before it, an
attempt whose embedded timestamp postdates its own last row, and a supersession
stamped inside a file that claims to have been frozen before it are each refused
rather than left for a reader to notice.

**The previous lane's package is not modified by this one.** Its ledger slice is
published evidence on `evidence/catena-e1-corrections-v14-handoff`, and
appending a supersession row to it would rewrite an artifact a reviewer may
already hold. Each lane keeps its own ledger; the cross-lane disposition — that
the V14 candidate received CHANGES REQUIRED and that this candidate answers it —
is recorded where cross-lane dispositions have always been recorded, in the
durable records, and in `HANDOFF.md` §3.

## 6. One log root per attempt

Every attempt writes beneath its own root, named by the ordinal the ledger
allocates. An existing log target is refused outright, never overwritten, so a
failed attempt's transcripts stay with that attempt and cannot be destroyed by
the attempt that replaces it. `logs/LOG-INDEX.md` is derived mechanically from
what is on disk rather than written by hand.

Package validation refuses an unexplained zero-byte log claimed by an attempt; a
log an attempt claims that is not there; a log claimed by two attempts; a log
present in the package that no attempt claims; and an attempt referencing a log
outside its own root. Each has a focused test.

## 7. What this lane's attempt history contains, in the words that are true of it

**This document does not certify the history; the history certifies itself.**
`logs/attempts.json` is this lane's rows taken as late as the phase contract
allows, so the sealing attempt's own row is inside it; the complete ledger is a
sibling; the inventory tool counts the rows mechanically; and the authority gate
reads the external ledger, so a package whose in-package copy and external
ledger disagree is refused rather than published. A reviewer counts those rows
rather than reading a count here.

What this file owes the reviewer is the **wording rule**, because the previous
package's defect was a word and not a row:

- `append-only` is said of this lane's history only where it is literally true
  of the file it is said about. A ledger that has ever had a line taken out
  and rewritten is **not** append-only, whatever the rewrite was for, and the
  truthful phrase for such a file is `complete disclosed attempt history with
  one documented row replacement` — naming the replacement, its reason and the
  row that replaced it.
- `complete` is said only of a record that omits nothing a reader would count:
  not of a slice that omits a phase's rows (§9), and not of a history that omits
  a cohort that ran (§8).
- The two claims cannot be made independently of each other any more. The
  completeness checker refuses an append-only claim standing beside a disclosed
  replacement, so a package can no longer say one thing in one member and the
  other in another, which is exactly what the previous one did.

Where the history and this file could be read as disagreeing, the history is
right and this file is the defect.

## 8. Set-aside cohorts

**This lane set no cohort aside.** No battery of this lane ran green and had its
figures declined; no figure in this package comes from work that was measured
and not used. `logs/attempts.json` and the sibling ledger are the authority on
that, and the resolved state of each attempt is in the rows rather than in this
sentence.

**It did retire two ledgers, and that is a different thing, disclosed here
rather than left for a reviewer to find by counting.** Neither was rewritten: a
ledger this lane could not carry forward was set down whole and a fresh one
opened.

The first was opened when the batteries were started against a head that a
records correction then superseded — the durable records had called the review
this lane answers the first in the sequence with a published commit, which is
false, since every review from V5 to V12 was published and V13's alone was not.
It allocated attempt ordinal 1, recorded three completed parent steps, and has
no terminal row because nothing terminated it: the operator stopped it. It is
2,501 bytes over five rows, SHA-256
`64683c0b8bb9624278cb136e8e8cbcbd4875bff571a1a128a870bdb6cb01ed90`.

The second carried both batteries to completion and then five package attempts,
four discarded and one that reached its sealed terminal row. It is 45,619 bytes
over eighty rows, SHA-256
`5b0c380cf7fab7b507dfedd6bdc0a6ade71cea38522937bf1a6bf851565ec117`. It was
retired for a defect in the operator's inputs that this ledger's OWN audit
caught and would not let past: the package timestamp had been chosen an hour
before the attempts it named, and an attempt id claiming to have been minted
long before its own first row is exactly what an anti-backdating rule exists to
refuse. Every package attempt in one ledger shares one timestamp by
construction, so no later attempt in that file could ever have passed it. The
ledger was set down rather than argued with, and the rule was not relaxed.

**No archive was produced by either, and no figure in this package comes from
either.** The four discarded package attempts were refused at P2, P5, P5 and P4
— an evidence-index reference written as a bare tool name, a discarded
predecessor's log root named but not shipped, the same again, and an ambiguous
battery log created by staging a predecessor's transcripts — and the fifth was
refused by the ledger audit before P7 ever ran. Not one wrote a ZIP. Every
number this package carries was measured again, from the beginning, in the
authoritative cohorts it ships.

Neither retired file is shipped: they are evidence for nothing, and shipping a
ledger no claim rests on would invite exactly the confusion this section exists
to prevent. Their digests are above so a reviewer handed either can tell which
it is. The authoritative ledger of this lane is a third, and it is complete for
the lane it opens. `LIMITATIONS.md` states the same facts in its own words.

**An empty table here is a pass, not a check that did not run.** The
completeness checker prints a "set-aside cohorts against the shipped attempt
history" section whatever it finds, and renders `(none)` when it finds nothing.
A reviewer meeting that section empty is meeting a check that ran and had
nothing to refuse — which is the same distinction between "did not run" and
"ran and found nothing" that the executed-tool record exists to make, in
miniature.

The rule that makes the absence checkable is the one the previous review forced:
**a commit named as a set-aside cohort must have a matching ledger row, or the
package is refused.** The previous package named one that had none.
`logs/named-commits.json` in this package describes no commit as set aside, so
there is no such claim for the checker to match — which is the state a lane with
no cohort should be in, and it is now a checked state rather than an asserted
one.

## 9. The post-seal rows, the slice that carries them and the member that cannot

The previous package's history omitted the post-seal rows entirely, and called
itself complete anyway. Half of that is fixed here and half of it cannot be, and
the boundary between the two halves is structural rather than a matter of
effort.

**The in-package member cannot carry them, and never will.**
`logs/attempts.json` is written at P5, proved by the manifest at P6 and sealed
into the archive at P7. P8, P9 and P10 all run after that. The rows for the
post-seal gates do not exist when that member is written, and adding them
afterwards would mean rewriting a sealed archive and re-taking a manifest
already verified against the ZIP's own bytes. Nothing in this lane mutates a
sealed archive, so that member stops at P5.

**The slice beside the archive does carry them now.**
`<package>.attempts.jsonl` is derived at P9 and is inside nothing sealed. Each
row appended to the lane ledger after that point is copied into the slice as
well — the one-line mirror that P11 and the discard path had each been doing
separately, moved to the one place that covers every row. It is safe on each of
the terms the gates depend on: before P9 the slice does not exist and the mirror
does nothing, so what P8 and P9 read is unchanged; the P10 gates read the slice
BEFORE their own rows are appended, so no gate is handed a row about itself; the
rows carry no disposition, which is what the authority gate's external fold
selects on; they arrive before the outer sanitize pass, so they are sanitized
with the rest of the file; and each row is copied rather than recomposed, so
both files carry the same bytes for the same fact.

Now carried in the slice: P9's own derivation row, both P10 gate rows, the
executed-tool re-render row, the P10 completion row, and any row a later phase
adds. Still not carried: the in-package member, which stops at P5. A reviewer
who wants the gates' rows reads the sibling; the in-package record that P10 ran
is the pair of gate transcripts named in `HANDOFF.md` §10. `LIMITATIONS.md`
states the remaining boundary in its own words.

## 10. Which bytes actually ran

**Every tool invocation records the SHA-256 of the exact bytes immediately
before it runs.** The record distinguishes shipped-and-executed from
shipped-and-not-executed, external system tool and reviewer-only helper, so a
tool that shipped without running says so instead of borrowing the claim of one
that ran; and it refuses outright if one logical tool was ever executed as two
different sets of bytes, because then "the tool that ran" is not a single thing.
Which class each tool holds in this package is in the executed-tool record and
the P8 tool-byte comparison table, both siblings named in `HANDOFF.md` §10, and
in neither case is it stated here. P8 compares executed against trusted against
shipped and fails hard on divergence.

**The trust anchor is out of package, versioned and clean.** The only code P8
executes is taken from a git checkout outside the archive, whose working tree is
empty, so P8's anchor check reports it versioned and clean at a commit rather
than raising an unversioned-anchor problem — and the commit is in the P8
transcript, not in this sentence. That anchor was seeded byte-exactly from the
previous package's shipped `logs/` and then carries this lane's tool corrections
as commits on top, which is why a tool this lane changed differs from its
predecessor by a digest a reviewer can compute from both packages, and every
tool it did not change does not. The anchor is identified in every record by its
symbol, never by a path: an anchor's location is an account name and a workspace
topology, and the sanitizer refuses to seal a package that carries either.

## 11. Two endpoints, and the checkout they were measured in

Every validation ran twice: once at this head, once at the exact reviewed parent
`69f2575421ba976271c936b1abd4b39dbe8b98fd`. That is the only way to tell an
inherited failure from a caused one, and this repository's own guidance requires
comparing failure sets rather than exit codes.

The parent battery additionally replays **this head's test file against the
parent**, which is the non-vacuity proof of the whole lane: regressions that pass
everywhere prove nothing, and these fail where the correction is absent.
`checks.txt` names that step, its log and its exit — and, for the first time in
this series, names it as the verbatim command it was, because the classifier no
longer calls it prose. The substituted file is copied in and restored by the
battery's own recorded steps, and a battery refuses to start on a tree that is
not clean, naming the files that made it dirty, because a battery measures a
commit and the commit it names is only its subject if the tree is that commit's.

**And it must be told which commit.** The battery requires an expected SHA and
refuses terminally when the checkout's HEAD does not match it, so a clean
checkout of the wrong commit cannot be labelled `parent`; it also refuses
terminally on a dirty postflight rather than recording the dirt and continuing.
Both refusals go through the discard path and leave a terminal ledger row
carrying its reason. Tree state is read **per command**, before and after, rather
than inherited from one preflight.

**What kind of checkout this was is derived, not asserted.** The previous lane
said in prose that its evidence came from a fresh clone and nothing derived said
whether it did. `claims.json` now carries three fields under `identity`, and
`DERIVED-CLAIMS.md` renders them: for this lane `workspace_mode` is
`fresh-clone`, `worktree` is false, and `git_dir_kind` is `directory` — a real
repository directory with nothing linked to it, rather than a linked worktree
sharing another tree's object store. **Every one of those values is symbolic or
boolean and none is a path**, deliberately: they ship inside `claims.json`, P8
re-renders `DERIVED-CLAIMS.md` from the shipped copy and byte-compares, and a
path here would be rewritten by the sanitizer after the freeze and would break an
otherwise honest package — besides leaking the thing the sanitizer exists to
remove. A reviewer checks them against `git rev-parse --git-dir` in their own
copy.

## 12. What is not claimed here

That the V13 review can be checked — it cannot; see §0. That any earlier package
was corrected — none was touched; the V11 through V14 packages remain exactly as
their reviews left them on their own evidence branches, and this lane appended
nothing to any of them. That P10's rows are in the archive — they are not; see
§9. That the classifier, the completeness checker or the coherence gate models
every failure of its kind — each models the failures it has been shown, and a
contradiction a gate does not model is not a contradiction a gate disproves.
That this lane's tooling corrections have been independently verified — they have
not; this lane wrote them and this lane's verdict on them is not independent,
which is why `REVIEW_REQUEST.md` asks for that verdict rather than recording one.
And that this lane reviewed itself — it did not.
