# Provenance

This package was produced by this lane's authoritative package attempt. That
attempt's identity is fixed BEFORE the run rather than minted during it, so a
member authored beforehand and frozen at the manifest can refer to it: an
attempt id carrying a nonce invented at the first phase could never appear in a
document written in advance, and a package whose prose cannot say which attempt
it is cannot settle the question it exists to settle. **The id and the ordinal
are not typed here.** `logs/attempts.json` carries both, and the ordinal in them
was allocated by the lane ledger and would have been refused if the lane had
ever spent it.

What makes the attempt authoritative is not a sentence in this file: it is the
post-verification authority record, a sibling named in `HANDOFF.md` §10, written
only after the read-only final verification passed and bound to the archive's
recomputed size and digest. The shipped `logs/attempts.json` says `sealed`,
which is the most a member written before that verification may say about
itself.

What ran, where it ran, in what order, with what arguments, and which record
wins where two could disagree.

**The authority is the lane ledger, and the lane ledger ships beside this
package.** `logs/attempts.json` is the copy of this lane's rows taken as late as
the phase contract allows; the live ledger is a sibling, named in
`HANDOFF.md` §10. That sibling is not the whole history and this file does not
pretend it is: this lane retired an earlier ledger and opened that one in its
place, §15 names both files with their digests and the reason, and
`logs/attempt-history.json` derives every attempt this lane made across the
pair — so a reviewer reads the history in full without reaching for a record
outside the handoff. Where this file and the ledger could
be read as disagreeing, the ledger is right and this file is a defect.

No figure here is typed. `checks.txt` carries each command with its working
directory, its argument vector, its environment bindings, its exit code, its
start and end, its tree state before and after, its attempt and its log;
`claims.json` carries the identity arithmetic; `DERIVED-CLAIMS.md` renders both.

## 0. The links this lane has, and the one it still does not

**This lane can name the review it answers.** It is
`67247ecc39a6e5f6224c64ca3ab1af163ee023b1`, on
`review/catena-wave-1-e1-corrections-v15-independent`, and it answered SEMANTIC
CHANGES REQUIRED, EVIDENCE CHANGES REQUIRED and CHANGES REQUIRED overall at the
exact parent `b9202882badbbbc364f1dd3d9057d2710ee47552`. So `claims.json`
carries `review_addressed` as that commit rather than as the empty string,
`DERIVED-CLAIMS.md` renders it, and this lane's account of the disposition is
checkable against the disposition itself.

**The reviewed package is named by its bytes, not by its name.** The V15
immutable handoff is on `evidence/catena-e1-corrections-v15-handoff` at
`db5f651e4eb2d10a15d1a594a4286ac7048f612c`, and the sealed archive it carries is
1,400,092 bytes over 69 members with ZIP SHA-256
`711b598ab43543113ccb924234fc8ef4ddb76370ff74d24c72a549da574204ac`. The review
re-verified those bytes against the digest that package's own post-verification
authority record carries, which is the property the whole authority ordering
exists to produce.

**The older gap is not filled, and this lane does not fill it.** `origin` still
carries no `review/catena-wave-1-e1-corrections-v13-independent`. That review's
identity is truthfully absent, this lane cannot publish another lane's review,
and it does not invent one: the chain is intact from V14 forward and broken at
the link before it. `LIMITATIONS.md` and `UNRESOLVED-BLOCKERS.md` both record
it, and neither presents it as closed.

The tool behaviour an earlier lane introduced for that gap stands and is not
undone. The assembler reads its review argument as `${REVIEW-}` rather than
`${REVIEW:-…}`, because `:-` substitutes a default for an **empty** value as
well as an unset one, and a lane answering an unpublished review would silently
have claimed to answer the previous lane's.

## 1. The evidence defects, and what actually caused each

The review found the previous package materially defective, and this lane
answers it with thirteen evidence closures. They are listed with their root
causes, because a defect whose cause is not stated is a defect that recurs under
a different name. Each fix is in a tool this package ships under `logs/`, so a
reviewer reads the correction rather than taking its word; the resulting
verdicts are in `checks.txt`, in the executed-tool record and in the tool-byte
comparison table named in `HANDOFF.md` §10.

**1. Executable command representation.** V15's `checks.txt` recorded each
command as one string and called all twenty-four rows `LITERAL`. A string is not
an invocation: it carries no working directory of its own, its quoting is
already resolved, and a reader cannot tell a paraphrase from a transcript. The
representation here records the working directory, the argument vector as a
list, and the environment bindings a shell was actually handed, so that no
authoritative row is a paraphrase, a fragment missing its arguments, or text
that cannot be run as written. What the shipped form is exactly is in
`checks.txt` and in the tool that renders it, not asserted here.

**2. Unambiguous repository variables.** Seven of V15's twenty-four rows
single-quote `'$WORKSPACE/...'` or `'$REPO/...'` paths, which cannot expand, and
no assignments are supplied anywhere in the package — the parent `browser-gate`,
`gzip-sizes`, `head-tests-against-parent` and `request-journals` rows, and the
head `browser-gate`, `gzip-sizes` and `request-journals` rows. Worse than the
quoting: the parent replay overloads `$REPO` for BOTH the parent working
directory and the distinct head test source, so unquoting alone cannot recover
the recorded execution; and the package-comparison row is the only one of the
twenty-four with no `cwd` slot at all, claiming `$REPO` where the package
directory is what ran. No member of that package defines `$REPO`, `$WORKSPACE`
or `$EVIDENCE`, and one directory carries two different tokens. Only sixteen of
twenty-four rows were replayable with their recorded context. This lane's
variables are distinct by construction — the candidate repository, the parent
repository and the package root are three tokens, never one — and the package
ships a legend that binds each token to what it stood for, so a row is
resolvable from inside the package rather than from a reader's guess.

**3. Prefix-prose rejection.** V15's classifier decided whether a command was
literal by `str.startswith(tuple)` over a list of command heads. That accepts
`format`, `installing`, `zipcode`, `testing`, `iframe`, `setting`, `makefile`,
`envelope` and `node_modules` as commands, and two escape-hatch disjuncts —
`"/" in first` and `"=" in first` — pass any prose whose first token contains a
slash or an equals sign. The whole classifier had one test with three
single-string fixtures, and the `=` clause V15 itself added had no coverage at
all. A prefix match is not a parse, and the completeness checker compounded it
by trusting the precomputed `LITERAL` label instead of testing the row. Both
halves are corrected: the classification is not a prefix test, and the checker
does not take the label's word for it.

**4. Mechanically derived tool execution.** V15 maintained execution state
beside the invocations rather than deriving it from them, so six "not executed"
rows are synthesized with a fabricated `at` — the render instant — a fabricated
`phase` and a fabricated `log`, three fields a tool that never ran cannot have.
Execution state here is derived from the authoritative attempt logs, and a tool
that did not run carries no field that only a run could produce.

**5. Executed drivers classified correctly.** V15 marked both the assembler and
the battery driver not executed although they drove the entire build, because
neither recorder can see itself. A record whose blind spot is the two programs
that produced it is not a record of what ran. Both are classified as what they
are.

**6. A complete predecessor-history statement.** §9 states it.

**7. A complete history of this lane — across two ledger files, not inside
one.** This lane retired its first ledger and opened a successor in its place;
no row in either was rewritten or deleted, each file is append-only within
itself, one ordinal allocation per attempt and one terminal row per attempt hold
across both, and no ordinal was reissued across the move. §6 states the
allocation rule that makes that guarantee rather than a habit, §15 names both
files with their digests and the reason the first was set down, §8 states the
wording rule that keeps the claim honest, and `logs/attempt-history.json` is the
derivation taken across the pair.

**8. The example figure, derived mechanically and never stated without its
build state.** §16 below carries the mechanical reconciliation, derived into the
member `logs/divergence-reconciliation.json`, and §9 of `CLAIM-CLOSURE.md`
carries the argument; the short form has three parts. **The review's finding stands:** V15's prose asserted a bare
thirty, naming no measure and no build state, while V15's own shipped
transcripts — members of THAT package and
of no part of this one, at
`build/agent-handoffs/20260826T195656Z-catena-e1-corrections-v15/logs/attempt-01/make-check-parent.log`
and
`build/agent-handoffs/20260826T195656Z-catena-e1-corrections-v15/logs/attempt-02/make-check-head.log`
on `evidence/catena-e1-corrections-v15-handoff` — each report twenty-eight `DIFF` rows
over twenty-seven distinct commands and each summarise `28 diverged … 2 volatile
line(s) declared`, the tool's own summary field quoted verbatim rather than a
phrasing this package adopts. No artifact in that package supported thirty.
**Those V15 figures are HISTORICAL, inferred from shipped V15 evidence taken on
a warm tree, and are never presented here as a fresh V16 replay.**

**The review's diagnosis does not stand:** "twenty-eight plus the two declared volatile lines"
cannot be a decomposition of thirty, because the volatile figure is a static
constant at `scripts/replay_examples.py:734` over the two-entry table at
`:182-185`, counting DECLARED LINES for two `tools/pdf-review` captures that are
masked at `:405` and appear in every transcript as `ok` and `absent`, never as
`DIFF` rows — they were never in the set they are supposed to be subtracted
from. **The cause is BUILD STATE, and the difference is a MEASUREMENT-SURFACE
difference rather than a V16 parent/head behaviour delta:** thirty divergent
rows over twenty-eight distinct divergent identities on a cold `build/`,
twenty-eight rows over twenty-seven identities on a warm one, the entire delta
being two captures of
`tools/mass-ordinary check --out build/example-ordinary`, whose comparison
directory a later capture in the same target writes. The two authoritative V16
cold cohorts, the parent under ordinal 15 and the head under ordinal 16, agree
exactly on all four measures, so no part of this gap is a behaviour change
between the endpoints this package ships. In V15's shipped
transcripts both of those captures read `ok`, the warm signature; V15 quoted a
cold figure while shipping a warm log, and the record never said which tree it
measured. Twenty-eight is also reachable as distinct DIFF command strings —
twenty-eight rows over twenty-seven commands warm, thirty over twenty-eight cold
— which is a row-versus-name conflation of the kind the same review rightly
criticised in `logs/compare-gate.py`, and the fifth instance of that shape this lane
records. **What this package takes from it is a rule rather than a number: a
count is meaningless without the state it was taken in, and this package states
both.** It derives the figure from the run's own log, reports divergent ROWS and
distinct COMMAND STRINGS separately, keeps the volatile figure apart as the
static declaration it is and never sums it with either, records
`build-state=COLD|WARM` at preflight, and **pins no constant at all** — a check
pinning thirty, or twenty-eight, would be wrong in one state or the other. It
refuses the unsound SHAPE, refuses a prose figure this package's own transcript
does not support, and refuses a summary line that disagrees with its own `DIFF`
rows. This lane corrected the durable records to twenty-eight plus two on the
review's authority, discovered by experiment that the decomposition was
impossible, and corrected its own correction; both steps stand in
`PROJECT-WORK.md` and the roadmap rather than one silently replacing the other.

**9. Compare-gate diagnostic granularity.** V15's `walk()` keyed assertions on
the NAME alone, so **2,290 assertion ROWS collapsed onto 17 diagnostic NAMES**
under last-write-wins and 2,273 rows were discarded before the per-row
diagnostics ran — while the output called them assertion objects. **The
mitigating half is recorded with it:** the verdict line was sound, because the
final comparison is over the whole report object, all 2,290 assertion rows
included, minus four named volatile fields. The whole-report equality proof
stands. Only the localising diagnostics were degenerate, and they are rebuilt so
that a row is identified by something two rows cannot share.

**And the general lesson is taken rather than the particular fix.** The
ROW-versus-NAME conflation occurs in four places in this evidence, and a fifth
time in the parent-discrimination figure. The review found two of them — the
gate's 2,290 rows over 17 names, and the classifier's own prose. This lane found
the other two — the example replay's divergent rows against its distinct command
strings, and full discovery's 27 result ROWS over 22 distinct identities, where
V15's "27 identities" was the row count wearing the identity count's name (two
methods emit multiple `subTest` rows:
`test_tool_registry.WorkedExampleTests.test_every_verb_shows_at_least_two_real_invocations`
yields five and `test_tool_registry.ToolSmokeTests.test_shell_smoke_tests_pass`
yields two). The parent-discrimination replay repeats it at **288 failure ROWS
over 39 distinct METHODS**, one method alone contributing 192 `subTest` rows.
**Wherever this evidence quotes a count, it now says what is being counted.**
Fixing only the one artifact the review named would have left three live
instances of the same error in the same package.

**10. Final completeness after the outer sanitize and scan.** V15's recorded
`COMPLETE` verdict is stale: re-running its own shipped checker against the
extracted package with every committed sibling present gives `handoff inventory:
INCOMPLETE`, because the outer-sanitize and outer-scan siblings are written
after the gate that produced the verdict, and `HANDOFF.md` named them by suffix
rather than by filename. The verdict this package ships is taken at the final
state, after those two records exist, and both outer logs are named by EXACT
FILENAME rather than by suffix, which is what made V15's verdict stale.

**The new checks are calibrated against the real package, not only against a
fixture built to pass them.** Run over the actual V15 archive and its actual
siblings, the rebuilt checker reports `handoff inventory: INCOMPLETE` with
**14 problems**: the seven false-`LITERAL` rows, each named by transcript path;
the two unnamed outer logs; and the unsupported example figure. Run over a
corrected fixture — the two logs named exactly, the figure repaired, the seven
rows made executable — it reports **`problems: 0` / `COMPLETE`**, with zero
non-executable rows remaining. That is the calibration the review asked for, and
it is the strongest statement this package can make about its own checks: they
turn the shipped V15 package's own `COMPLETE` into a correctly-explained
`INCOMPLETE`.

**11. Named outer logs.** They are named by exact filename in `HANDOFF.md` §10,
which is the record the checker reads.

**12. Direct authority bindings.** §4 states them: each binding is recomputed
from the archive rather than carried forward from an earlier phase, and each is
named in the record that asserts it rather than inferred from an ordering.

**13. The shipped-versus-local retained-artifact privacy boundary.** §11 and
`PRIVACY-AUDIT.md` state it. The published archive and its named siblings are
scanned and re-scanned; four builder-local classes are not, and no broader claim
is made about them.

**What this lane does not claim about any of them.** That a classifier which no
longer prefix-matches is thereby correct; that a checker which models these
failures models every failure of its kind; or that this lane's verdict on its
own tooling is independent. `REVIEW_REQUEST.md` puts exactly that to the
reviewer.

## 2. The command record, and what makes a row re-runnable

A recorded command has one job: a reviewer with the package and a checkout must
be able to run it and get the same kind of answer. V15's record could not do
that for a third of its rows, and the rows it failed on were the load-bearing
ones — the parent replay that is the non-vacuity proof of the whole lane, and
both browser gates.

Three properties are required of every authoritative row, and they are
properties of the representation rather than of any particular row's luck:

- **The invocation is separable from its context.** The working directory is a
  slot of its own, present on every row, so a row cannot claim a directory by
  implication and cannot omit one. The package-comparison row, which had no
  `cwd` slot at all in V15, has one here like every other.
- **A token stands for exactly one thing.** The candidate repository, the parent
  repository and the package root are distinct tokens. No token stands for two
  directories, and no directory carries two tokens. The package ships a legend
  binding each token to what it stood for, derived rather than typed, so the
  binding is checkable from inside the package.
- **What a shell was handed is recorded as what a shell was handed.** The
  argument vector is a list, not a re-quoted string, so quoting cannot silently
  make a variable inert. A row that cannot be represented this way is not
  recorded as `LITERAL`.

The privacy mechanism is unchanged and is not weakened by any of this: values
are recorded as tokens, and the value-keyed scans in `PRIVACY-AUDIT.md` run
independently of whether any rule fired, so a record that says more about the
shape of an invocation says no more about the machine it ran on.

## 3. Two vocabularies, because there are two facts — and two axes, because there are two questions

"This validation battery ran to completion" and "this is the package to review"
are different facts, and writing both `authoritative` makes the authoritative
count uncountable by construction. That much V13 established and this lane
keeps.

**What V16 corrects is a second conflation living inside the first.** How an
attempt ENDED, and whether a completed attempt's MEASUREMENTS are the ones a
package carries, are two different questions, and the previous machine answered
them on one axis. That is why it drew `complete ──▶ set-aside` as though
setting a cohort aside were a later terminal state. It is not one and it cannot
be one: whether a cohort's figures are carried is not knowable while it runs.
Setting a cohort aside does not alter, amend or replace its `complete` terminal
row. It appends a separate, later row, on a different axis, and the terminal
row still says exactly what it said.

**The EXECUTION axis — how the attempt itself terminated.** Terminal,
irreversible, and exactly one per attempt.

    A validation battery (`side: head`, `side: parent`)

        started ──▶ complete
                ├─▶ failed
                └─▶ abandoned

    A package attempt (`side: package`)

        started ──▶ sealing ──▶ sealed
                            └─▶ discarded

**The EVIDENCE axis — whether a terminated attempt's measurements remain
authoritative.** It is meaningful only for an attempt that reached a successful
execution disposition; it is carried by a later `record=state` row that leaves
the terminal row where it is; and the absence of such a row IS a state,
`unevidenced`, which is never written to a row because the absence is the whole
of it.

    A battery cohort's evidence (execution disposition must be `complete`)

        unevidenced ──▶ authoritative ──▶ superseded
                    └─▶ set-aside

    A package attempt's evidence (execution disposition must be `sealed`)

        unevidenced ──▶ authoritative ──▶ superseded
                    └────────────────────▶ superseded

**`failed` and `abandoned` are permanently `unevidenced`.** They measured
nothing that could be carried or declined, so the evidence axis has no move to
make from either, and both `--authoritative-evidence` and `--set-aside-attempt`
refuse them by name and say why rather than failing by omission.

**The two evidence machines admit the SAME one succession, and V16 is the
version that stopped treating that as an asymmetry.** Neither axis is
reopenable: a cohort's figures are carried or they are declined, once;
`set-aside` is terminal and `authoritative` cannot follow it; and no second row
of either kind is admitted. What an attempt that WAS authoritative may become,
on either side, is SUPERSEDED — a battery cohort when a later cohort measures
the same endpoint and the package carries that one instead, a package attempt
when a later assembly replaces it. **The one shortcut is on the package side
only**: an attempt that sealed and then failed a post-seal phase never held
authority at all, and the assembler writes its `superseded` row directly, which
is the `sealed → superseded` edge above and is how ordinals 13 and 14 of this
lane are recorded. A battery cohort has no such edge: a cohort with no evidence
row is `unevidenced`, and it is carried or declined, never superseded, because
superseding it would assert it had once been carried. Refusing the succession
proper would leave deleting the predecessor's history as the only available
remedy, which is the
V12 defect rather than the cure. `superseded` is terminal, nothing follows it,
and the `authoritative` row it follows is left exactly as written, because that
attempt really did hold that disposition for the time it held it. **`set-aside`
is not superseded and cannot be**, because superseding it would assert that a
cohort had once been carried when it never was.

**The battery half of that machine was not written from theory; V16 found the
case in its own run, and found it the hard way.** The cohorts of ordinals 04
and 07 were recorded `authoritative` the moment their batteries ended — before
any package had been sealed from them. Assembly then reached P8, which compares
each tool's EXECUTED digest against the trusted anchor and against the copy the
archive SHIPS, and refused: those cohorts had executed `logs/battery.sh` at
`04ca35cb5969aea92d983c9793b5dc2d0d427c8a0ca356fa91db95bb8cc58c9c` while the
package shipped that driver at
`cca4d2840116e2e101c68d9bdf8db1305f545b838015a837514f4464b73b947c`. What ran
was not what shipped, and the difference was header comment prose alone —
rewritten in that very driver when this lane split execution disposition from
evidence disposition. The check was right anyway: an archive whose shipped
driver is not the driver that took its measurements cannot say which copy any
of its figures is about. The endpoints had to be measured again; the ledger
correctly refused to reopen an evidence disposition; and the record was left
with no way to state what had plainly happened. §13 carries both rows with
their reasons and §15 says where those transcripts are kept.

**The lesson, stated here rather than in the incident, because it is the part a
later lane needs.** An evidence disposition of `authoritative` belongs AFTER a
seal has proved that a cohort's tools are the shipped ones — not at the moment
a battery ends. That a package is shipping a cohort's figures is knowable
early; that the bytes which produced them are the bytes beside them is knowable
only once the executed record has been compared against the archive, and P8 is
where that comparison is made. Recording the disposition before the comparison
is what made this correction necessary, and this package states that rather
than presenting its shipping cohorts as though they had always been the only
ones.

**The PACKAGE side has walked its own edge for real too.** §9 records the V15
attempt that was sealed, briefly held AUTHORITATIVE after its final
verification, and was then superseded when the authority-coherence gate refused
it; §13 records two package attempts of THIS lane that sealed and were
superseded in turn. Existing tests pin the edge on both sides.

**`authoritative` means two different things on the two sides, and this is the
version that stopped pretending it meant one.** On the PACKAGE side it means
"this is the package to review": it is post-terminal, it may be written in one
place only — the live external ledger, after the final verification passes
— at most one package attempt in a lane may hold it, and this package's records
must resolve to exactly one. On the BATTERY side it means "these are the
figures this package reports", which is a different claim, is what
`--authoritative-evidence` records, and is truthfully recordable only once the
executed-versus-shipped comparison has been made — which is the correction the
paragraphs above state, and which cost this lane two cohorts to learn. Until
this lane there was no verb for the battery sense at all: a
cohort could only ever be DECLINED out loud, so an attempt whose measurements
the package actually carries was indistinguishable in the record from one
nobody had got round to classifying. Both read `complete`, and the difference
between them lived in prose. The two senses are held apart by scope rules
rather than by two vocabularies, because a vocabulary that cannot spell a true
fact forces the pipeline to delete the fact — and §14 records what happened
when one of this pipeline's own gates still held the older vocabulary.

`set-aside` is the battery-side evidence word, and it exists so that a cohort
which ran, completed, and whose figures are not used can be RECORDED rather
than deleted. It does not overwrite the verdict it follows: the battery did
complete, and the terminal row still says so.

**`refused` is not a state, in either axis.** Attempts 01 and 02 of this lane
were described in passing as "refused". Their execution disposition is
`failed`, and `guard refusal` is the CAUSE, recorded in the reason on the row
that states the disposition. A cause is not a disposition; a machine carrying
both would let one attempt be counted twice, or neither, depending on which
word a reader reached for. `logs/checks.py` therefore names the words that would
introduce such a state — `refused`, `refusal`, `refusing` — and maps each to
the disposition it is not, so an audit meeting one can say in those terms what
the truthful disposition is instead of silently accepting a sixth word.

**Every non-successful terminal or post-terminal state carries its reason**, on
the row that states it and in the summary the package ships. A row that ends
`failed`, `discarded`, `superseded` or `set-aside` with an empty reason is
refused.

No attempt may be authoritative and superseded, unresolved and final, or
discarded and authoritative. Each is a distinct refusal in the coherence gate,
and each has a test that proves the refusal fires.

**The V15 lane exercised the `sealed → authoritative → superseded` edge for
real**, and it is worth naming here because it is the edge a reader assumes is
theoretical: one V15 attempt was sealed, briefly held AUTHORITATIVE after its
final verification, and was then superseded when the authority-coherence gate
refused it. The state machine did what it exists to do, and the record of it is
in that lane's ledgers rather than in its prose — which is the defect §9
addresses.

## 4. Authority is established after verification, and it binds the archive

**The package attempt that reached final authority is `package-20260827T230425Z-3238tjpk`.** That is
the assembly whose archive this is: the run that staged these members, froze
them, built the archive, passed the final verification read-only over the
archive alone, and had its authority record written afterwards from the
archive's own recomputed bytes. Every other assembly attempt of this lane is in
the history with its own terminal execution disposition and its own reason, and
none of them produced these bytes.

That identity is written here by the assembler and could not have been written
by an author. The id is minted at the attempt's own preflight and carries a
random suffix precisely so that two attempts can never collide, so no document
staged before the run could name it and any document that guessed would be
wrong on every run but one. The source of this member carries a token; this
phase resolves it, once, into the staged copy, before the freeze that makes
these bytes evidence. It is the same shape as the package basename, one field
along, and for the same reason: a name chosen per attempt is written per
attempt, by whatever knows it.

Note that `authoritative` says two different things in this package, on two
different axes, and both are correct. The sentence above is about the PACKAGE
attempt that sealed. Elsewhere this record says a battery cohort's EVIDENCE
disposition is `authoritative`, which means the package derives its figures
from that cohort's transcripts. A battery never seals an archive and a package
attempt never measures an endpoint; the word is shared and the questions are
not. The authority gate reads only the first sense, and it was taught the
difference after refusing eleven true sentences of this record that named the
cohorts its numbers come from.

The order is:

1. the attempt starts and is recorded started;
2. the package directory is sealed, and the strongest thing any in-package row
   may claim is `sealed`;
3. the manifest is taken and the archive is built;
4. the final verification runs over the archive, read-only, executing no archive
   code;
5. the archive's byte size and SHA-256 are recomputed after that verification;
6. **and only then** is final authority established.

The authority record is a structured sidecar naming the attempt, the exact head,
the archive's basename, its byte size and SHA-256, the verification result and
the post-verification rehash result — **each recomputed from the archive rather
than carried forward from an earlier phase, and each named in the record that
asserts it.** That directness is the twelfth evidence closure: a binding that is
inferred from an ordering is a binding a reader has to reconstruct, and a
reconstruction is where a stale figure survives. If the verification fails, the
attempt stays non-authoritative and no record anywhere calls it otherwise.

The binding runs one way and the archive carries no such record, so there is no
self-reference and no ordering problem. What it costs is that an authoritative
package cannot be self-describing: an archive cannot contain its own digest.
That is why this file names no size and no digest of its own package, and why
the figures live in the sidecar named in `HANDOFF.md` §10.

**The same structural limit applies once more, to the evidence commit, and it is
recorded here rather than left to be found.** The evidence commit cannot be
bound INSIDE the authority record, because naming the commit in the record
changes the record's bytes and therefore changes the commit. Everything that
commit CONTAINS is bound instead — the archive by digest, the manifest, the
verification and rehash results — and the authority record carries a required
note saying exactly that. A reviewer who expects to find the evidence commit
bound in the record and does not find it should find the reason already written
down, in the same shape as V15's correct statement that an archive cannot
contain its own digest. This is a limit of the construction, not a gap in it,
and no lane can close it by trying harder.

## 5. What the authority gate consumes, and what it refuses

The gate consumes the archive, the digest-and-size sidecar, the verification
transcript, the live external ledger, the sibling markers and the package's
own prose. Its negative roster covers each contradiction an earlier gate
accepted: a second authoritative state row, an authoritative winner followed by
a discarded state, multiline and uppercase contradictory prose, a wrong package
on the authoritative outer-log line, and prose that never names the winner.

This lane did not reopen that roster and does not claim to have re-derived it.
The V13 `authority-negative-fixtures` requirement stays **open** in the promise
ledger rather than marked passed: the review this lane answers did not raise it,
and disposing of a promise a review did not raise would be this lane answering a
question nobody asked. `LIMITATIONS.md` records it.

## 6. One ledger, one lane, ordinals that are never reused

**This lane's ledger opened as a new file**, with the allocator's `--fresh`
assertion, which refuses to open over an existing ledger; and the allocator
refuses to append to, or read as its own, a ledger declaring a different lane.
The previous lane's ledger is neither reused nor extended, and it is not
modified by this lane at all. **This lane then retired that first file and
opened a second, once, deliberately, and §15 records both files with their
digests and the reason.** A lane that says it never moved a ledger and moved
one is the defect; a lane that moved one and says so, and can show that no
ordinal was reissued across the move, is the disposition this section is
about.

There is one allocator. It is called by the assembler and by the battery driver
alike, no tool computes a local maximum, and it refuses an ordinal any row has
ever carried, however that attempt ended. An attempt id is
`<side>-<UTC stamp>-<ordinal><nonce>`, and the nonce is drawn from an alphabet
with no hex letter in it, so an attempt id can never be misread as an
abbreviated commit SHA by the identity audit.

**And that rule was only as strong as the file it was scoped to, which is why
this lane changed where it is scoped.** The V15 lane reissued ordinals across
one lane, because allocation read the file it was handed and the ledger was
moved aside twice: each fresh ledger began allocating from the beginning again,
so ordinal 01 in that lane names three different attempts in three different
files. Monotonic-within-a-file is not never-reused-in-a-lane, and the
difference is invisible from inside any one of the files. §9 states V15's.

**This lane retired a ledger too, and reissued nothing, because allocation is
no longer file-scoped.** The retirement verb writes the predecessor's spent
ordinals into the successor's opening lane row — `ordinals_already_spent`
alongside a `retired_predecessors` entry carrying the old file's path, digest,
byte count, row count, reason and the attempt ids it held — and the allocator
unions those into the spent set before it proposes a number. So the second
ledger of this lane opened at ordinal 04 rather than at 01, the retired file's
ordinals stay spent, and `reused_ordinal_count` is derived across both files
rather than asserted about either. That is the difference between a guarantee
and a habit: V15's ledgers each carried an identity row saying an ordinal "is
never reissued", and each was telling the truth about itself while the lane
around them was not.

**Chronology is checked.** A row whose time precedes the row before it, an
attempt whose embedded timestamp postdates its own last row, and a supersession
stamped inside a file that claims to have been frozen before it are each refused
rather than left for a reader to notice. That rule is what caught the V15
operator's backdated package timestamp and retired a whole ledger, and it was
not relaxed.

**The previous lane's package is not modified by this one.** Its ledger slice is
published evidence on `evidence/catena-e1-corrections-v15-handoff`, and
appending a supersession row to it would rewrite an artifact a reviewer may
already hold. Each lane keeps its own ledger; the cross-lane disposition — that
the V15 candidate received CHANGES REQUIRED and that this candidate answers it —
is recorded where cross-lane dispositions have always been recorded, in the
durable records, and in `HANDOFF.md` §3.

## 7. One log root per attempt

Every attempt writes beneath its own root, named by the ordinal the ledger
allocates. An existing log target is refused outright, never overwritten, so a
failed attempt's transcripts stay with that attempt and cannot be destroyed by
the attempt that replaces it. `logs/LOG-INDEX.md` is derived mechanically from
what is on disk rather than written by hand.

Package validation refuses an unexplained zero-byte log claimed by an attempt; a
log an attempt claims that is not there; a log claimed by two attempts; a log
present in the package that no attempt claims; and an attempt referencing a log
outside its own root. Each has a focused test.

## 8. What this lane's attempt history contains, in the words that are true of it

**This document does not certify the history; the history certifies itself.**
`logs/attempts.json` is this lane's rows taken as late as the phase contract
allows, so the sealing attempt's own row is inside it; the live ledger is a
sibling, and the ledger it succeeded is named beside it in §15 so that neither
file is mistaken for the whole; the inventory tool counts the rows
mechanically; and the authority gate reads the external ledger, so a package whose in-package copy and external
ledger disagree is refused rather than published. A reviewer counts those rows
rather than reading a count here.

What this file owes the reviewer is the **wording rule**, because the previous
lane's defect was a word and not a row:

- `append-only` is said of a history only where it is literally true of the file
  it is said about. A ledger that has ever had a line taken out and rewritten is
  **not** append-only, whatever the rewrite was for, and the truthful phrase for
  such a file is `complete disclosed attempt history with one documented row
  replacement` — naming the replacement, its reason and the row that replaced
  it.
- `complete` is said only of a record that omits nothing a reader would count:
  not of a slice that omits a phase's rows (§10), not of a history that omits a
  cohort that ran (§9), and **not of a single ledger where a lane kept three**.
- **The case this lane is actually in is neither of those, and it takes its own
  phrase rather than borrowing one.** No row of either of this lane's ledgers
  was rewritten or deleted, so each file is append-only within itself; what
  changed is which file the lane was appending to. The truthful phrase, and the
  one every member of this package now uses, is: *each ledger is append-only
  within itself and no row in either was rewritten; the lane's history spans two
  files because one was retired; the retirement is recorded in the successor's
  opening `lane` row with the predecessor's digest and spent ordinals; and the
  complete history is derived across both.* It is never said without naming
  where the retirement is recorded, which is §15 and `logs/attempt-history.json`.
- The two claims cannot be made independently of each other. The completeness
  checker refuses an append-only claim standing beside a disclosed replacement,
  so a package can no longer say one thing in one member and the other in
  another — and this lane's own package was refused by that check, on these
  files, before the wording above replaced the unqualified one.

Where the history and this file could be read as disagreeing, the history is
right and this file is the defect.

## 9. Set-aside cohorts, and the complete V15 predecessor history

**The V15 predecessor history was not five refusals followed by a sixth seal.**
That is one slice of one ledger. The history below was DERIVED mechanically
across all three V15 ledgers by `checks.py --history-table --lane V15` over the
two retired files and the shipped one, rather than recalled from any single
slice:

| # | attempt | ord | ledger | start | disposition | reason |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `package-20260826T180457Z-03qyvspp` | 3 | 02-retired | 18:55:49Z | discarded | normalize pass 1 failed, exit 1 |
| 2 | `package-…-04jzwm3k` | 4 | 02-retired | 18:58:52Z | discarded | attempt-log audit exit 1 |
| 3 | `package-…-058sn2j5` | 5 | 02-retired | 19:01:27Z | discarded | attempt-log audit exit 1 |
| 4 | `package-…-067xmgxg` | 6 | 02-retired | 19:04:00Z | discarded | aborted in P4 derive, exit 1 |
| 5 | `package-…-07z8rv48` | 7 | 02-retired | 19:06:30Z | superseded, after sealing | ledger audit exit 1 |
| 6 | `package-20260826T194118Z-033jkh3w` | 3 | shipped | 19:41:18Z | superseded, after sealing | P8 final verification exit 1 |
| 7 | `package-20260826T195048Z-04wzq5x4` | 4 | shipped | 19:50:48Z | sealed, **AUTHORITATIVE 19:52:06Z**, superseded 19:52:07Z | authority-coherence exit 1 |
| 8 | `package-20260826T195411Z-05e1bu7n` | 5 | shipped | 19:54:21Z | discarded | attempt-log audit exit 1 |
| 9 | `package-20260826T195656Z-06v11wpe` | 6 | shipped | 19:56:56Z | **AUTHORITATIVE** | — |

Derived totals: `package_attempts 9`, `package_authoritative 1`,
`package_non_authoritative 8`, `battery_attempts 5`,
`attempts_with_no_terminal_row 1` — that one being
`parent-20260826T181908Z-01rwghhk`, which has no terminal row because nothing
terminated it; the operator stopped it — `ledger_replacements 2`, and
`reused_ordinals 6`. **Ordinal 1 was issued three times in one lane**, because
allocation was file-scoped and the ledger was moved aside twice (§6).

Ledger digests, so each can be identified independently: 01-retired, 2,501
bytes over 5 rows, SHA-256
`64683c0b8bb9624278cb136e8e8cbcbd4875bff571a1a128a870bdb6cb01ed90`; 02-retired,
45,619 bytes over 80 rows, SHA-256
`5b0c380cf7fab7b507dfedd6bdc0a6ade71cea38522937bf1a6bf851565ec117`; shipped,
61,929 bytes over 107 rows, SHA-256
`3990ff6c05a5a53d4b3a835e92259bd40f94847cfa3ce7e2de300ed66d034640`.

**The disjointness check that makes the count sound is stated rather than
assumed: no ledger is a prefix of a later one, and no attempt id is shared
between any pair.** These are therefore nine distinct attempts and not one set
counted twice — which is exactly the objection a reviewer should raise against a
number derived by unioning three files, and it is answered before it is raised.

Every package attempt in the retired second ledger shares one timestamp by
construction, so no later attempt in it could ever have passed, and the ledger
was set down rather than argued with. Attempt 7 is worth reading twice: it was
sealed, **became AUTHORITATIVE at 19:52:06Z, and was superseded one second
later** when the authority-coherence gate refused.

**And that lane's `PROVENANCE.md` declared, at lines 296 to 297, that it set no
cohort aside, while two green retired batteries had their figures declined.**
That is the definition of the word. A battery that ran to completion and whose
numbers were not used is a set-aside cohort whether or not the file it was
recorded in survived, and a lane that retires the ledger a cohort lived in does
not thereby un-run the cohort. The classification is corrected here, in the
package that answers that review, rather than left as a discrepancy for the next
reviewer to find again.

**No archive was produced by either retired V15 ledger, and no figure in the
shipped V15 package came from one.** That much of V15's account holds and is
repeated because it is true.

**What is true of THIS lane, stated in the same terms and without the
flattering version.** Its ledger is two files, one retired and one live, and
§15 names both with their digests and the reason the first was set down. It DID
set cohorts aside, and it says which and why on their own rows rather than in
prose; §13 is the whole history *because it is rendered across both of this
lane's ledgers rather than out of the live one*, and
`logs/attempt-history.json` is the derivation. What it did not do is reissue an ordinal, and that is a derived
figure across both files rather than a claim about either. **An empty table is
a pass, not a check that did not run:** the completeness checker prints
a "set-aside cohorts against the shipped attempt history" section whatever it
finds and renders `(none)` when it finds nothing, which is the same distinction
between "did not run" and "ran and found nothing" that the executed-tool record
exists to make. And the rule that makes an absence checkable is the one an
earlier review forced: **a commit named as a set-aside cohort must have a
matching ledger row, or the package is refused.**

Neither retired V15 file is shipped here. They are evidence for nothing in this
lane, their `command` fields hold raw pre-sanitization absolute paths, and
shipping them would put unscanned bytes into a sealed archive. Their digests are
above so a reviewer handed either can tell which it is. `LIMITATIONS.md` states
the same boundary in its own words.

## 10. The post-seal rows, the slice that carries them and the member that cannot

Half of this is fixed and half of it cannot be, and the boundary between the two
halves is structural rather than a matter of effort.

**The in-package member cannot carry them, and never will.**
`logs/attempts.json` is written before the manifest is taken and sealed into the
archive. The final verification, the authority record and the publication gates
all run after that. The rows for those phases do not exist when that member is
written, and adding them afterwards would mean rewriting a sealed archive and
re-taking a manifest already verified against the archive's own bytes. Nothing
in this lane mutates a sealed archive, so that member stops where it stops.

**The slice beside the archive does carry them.** It is derived after the
verification and is inside nothing sealed, and each row appended to the lane
ledger after that point is copied into it. It is safe on each of the terms the
gates depend on: before it exists the mirror does nothing, so what the earlier
phases read is unchanged; the publication gates read the slice BEFORE their own
rows are appended, so no gate is handed a row about itself; the rows carry no
disposition, which is what the authority gate's external fold selects on; they
arrive before the outer sanitize pass, so they are sanitized with the rest of the
file; and each row is copied rather than recomposed, so both files carry the
same bytes for the same fact.

A reviewer who wants the gates' rows reads the sibling; the in-package record
that they ran is the pair of gate transcripts named in `HANDOFF.md` §10.
`LIMITATIONS.md` states the remaining boundary in its own words.

## 11. Which bytes actually ran

**Every tool invocation records the SHA-256 of the exact bytes immediately
before it runs**, and the execution state of every tool is derived from those
records rather than maintained beside them. A tool that shipped without running
says so instead of borrowing the claim of one that ran; a tool that ran says so
because a run recorded it, not because a table asserted it; and the record
refuses outright if one logical tool was ever executed as two different sets of
bytes, because then "the tool that ran" is not a single thing.

**The counts are separated by kind, and the schema is labelled by phase.** V15
sealed two unlabelled count sets in one package: its verification log and its
tool-byte sidecar said one thing, its assembly log said another, they were taken
at different phases, neither was labelled by phase, and nothing in the package
reconciled them. A reader meeting both had no way to tell which was wrong, and
in fact neither was — they were answers to different questions wearing one set
of words. So the quantities are named apart: tools referenced, tools executed,
execution invocations, tools shipped, and tools trusted but not executed. What
each is in this package is in the executed-tool record and the tool-byte
comparison table, both siblings named in `HANDOFF.md` §10, and in neither case
is it stated here.

**The drivers are classified as what they are.** The assembler and the battery
driver drove this build, and they are recorded executed. V15 recorded them not
executed because neither recorder can see itself, which made the record's blind
spot the two programs that produced it.

**A tool that did not run carries no field only a run could produce.** V15
synthesized six not-executed rows with an `at` set to the render instant, a
`phase` and a `log`. A time, a phase and a transcript are things an execution
has. Their presence on a row that denies an execution is the record contradicting
itself in three fields at once, and it is not done here.

**The trust anchor is out of package, versioned and clean.** The only code the
final verification executes is taken from a git checkout outside the archive,
whose working tree is empty, so the anchor check reports it versioned and clean
at a commit rather than raising an unversioned-anchor problem — and the commit is
in the verification transcript, not in this sentence. That anchor was seeded
byte-exactly from the previous package's shipped `logs/` and then carries this
lane's tool corrections as commits on top, which is why a tool this lane changed
differs from its predecessor by a digest a reviewer can compute from both
packages, and every tool it did not change does not. The anchor is identified in
every record by its symbol, never by a path: an anchor's location is an account
name and a workspace topology, and the sanitizer refuses to seal a package that
carries either.

## 12. Two endpoints, the checkout they were measured in, and what is not claimed

Every validation ran twice: once at this head, once at the exact reviewed parent
`b9202882badbbbc364f1dd3d9057d2710ee47552`. That is the only way to tell an
inherited failure from a caused one, and this repository's own guidance requires
comparing failure sets rather than exit codes.

The parent battery additionally replays **this head's test file against the
parent**, which is the non-vacuity proof of the whole lane: regressions that pass
everywhere prove nothing, and these fail where the correction is absent. That
step is recorded with its own working directory and its own argument vector, and
the two repositories it touches carry two distinct tokens, because V15's version
of this row overloaded one token for both and is the single clearest reason its
command record could not be re-run. The substituted file is copied in and
restored by the battery's own recorded steps, and a battery refuses to start on a
tree that is not clean, naming the files that made it dirty, because a battery
measures a commit and the commit it names is only its subject if the tree is that
commit's.

**And it must be told which commit.** The battery requires an expected SHA and
refuses terminally when the checkout's HEAD does not match it, so a clean
checkout of the wrong commit cannot be labelled `parent`; it also refuses
terminally on a dirty postflight rather than recording the dirt and continuing.
Both refusals go through the discard path and leave a terminal ledger row
carrying its reason. Tree state is read **per command**, before and after, rather
than inherited from one preflight.

**What kind of checkout this was is derived, not asserted.** `claims.json`
carries three fields under `identity` and `DERIVED-CLAIMS.md` renders them: for
this lane `workspace_mode` is `fresh-clone`, `worktree` is false, and
`git_dir_kind` is `directory` — a real repository directory with nothing linked
to it, rather than a linked worktree sharing another tree's object store. **Every
one of those values is symbolic or boolean and none is a path**, deliberately:
they ship inside `claims.json`, the final verification re-renders
`DERIVED-CLAIMS.md` from the shipped copy and byte-compares, and a path here
would be rewritten by the sanitizer after the freeze and would break an otherwise
honest package — besides leaking the thing the sanitizer exists to remove. A
reviewer checks them against `git rev-parse --git-dir` in their own copy.

**What is not claimed here.** That the V13 review can be checked — it cannot; see
§0. That any earlier package was corrected — none was touched; the V12 through
V15 packages remain exactly as their reviews left them on their own evidence
branches, and this lane appended nothing to any of them. That this lane's
post-seal rows are in the archive — they are not; see §10. That the retired V15
ledgers can be audited from this package — they cannot; §9 offers their digests
and nothing more. That every retained builder-local artifact is privacy-clean —
that claim is declined; see `PRIVACY-AUDIT.md`. That the classifier, the
completeness checker or the coherence gate models every failure of its kind —
each models the failures it has been shown, and a contradiction a gate does not
model is not a contradiction a gate disproves. That this lane's tooling
corrections have been independently verified — they have not; this lane wrote
them and this lane's verdict on them is not independent, which is why
`REVIEW_REQUEST.md` asks for that verdict rather than recording one. That any
figure here derives from the abandoned battery of ordinal 06, or from the
set-aside batteries of ordinals 03 and 05, or from the superseded cohorts of
ordinals 04 and 07 — none does, and §13 states each of them in full. That the
retained cohorts of §15 can be audited from this package — they cannot; they
are local-only, they are offered by digest and file count, and no claim here
rests on one. That this lane never retired a ledger — it retired one, once,
and §6 and §15 say so with the digest of the file it set down. And that this
lane reviewed itself — it did not.

**Sections 13 through 17 follow this one** and were written after it: the
attempt history and its two axes, the state-machine work and its guards, the
retained cohorts and ledgers, the example-figure reconciliation, and the two
`$NAME` vocabularies with their legend. They are appended rather than
interleaved because this file's section numbers are cited by other members, and
renumbering a record to make it read more tidily is the disposition this
package spends most of its length arguing against.

## 13. This lane's attempt history, derived rather than recalled

**No figure in this section is typed.** Every one is read from
`logs/attempt-history.json`, which `checks.py --history-table
--assert-invariants` produced by reading both of this lane's ledgers and
folding their rows; a reviewer who distrusts the table reads the JSON, and a
reviewer who distrusts the JSON reads the ledgers it names. The Execution and
Evidence columns are the two axes of §3, and they are not one column wearing
two hats: no row's evidence disposition alters, replaces or supersedes its
execution disposition, and the pair `complete` / `set-aside` is two rows in the
ledger and never a transition.

| Ord | Attempt | Ledger | Side | Execution | Evidence | What it was |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | `parent-20260827T135733Z-01m83vq7` | retired | parent | `failed` | `unevidenced` | the exec-record guard refused a row whose recorded command could not be replayed as written |
| 02 | `parent-20260827T141358Z-02sh6373` | retired | parent | `failed` | `unevidenced` | the log target already existed; nothing was run and nothing was overwritten |
| 03 | `parent-20260827T141439Z-038xp4y2` | retired | parent | `complete` | `set-aside` | a green parent cohort measured against a `build/` the refused attempt of ordinal 01 had warmed; its figures were declined and the cohort re-run cold |
| 04 | `parent-20260827T143106Z-04hy5j4v` | live | parent | `complete` | `authoritative`, then **`superseded`** | the first cold parent cohort; carried when its battery ended, and replaced once P8 found it had executed a `logs/battery.sh` this package does not ship |
| 05 | `head-20260827T144631Z-05qmtgwx` | live | head | `complete` | `set-aside` | a green head cohort that measured head `251900b14`, superseded by `cc1f2fb86` |
| 06 | `head-20260827T150233Z-06zg9rhq` | live | head | **`abandoned`** | `unevidenced` | externally interrupted after three green steps |
| 07 | `head-20260827T154350Z-079xrp6n` | live | head | `complete` | `authoritative`, then **`superseded`** | the first cold shipping-head cohort, replaced for the same cause and by the same remedy as ordinal 04 |
| 08 | `package-20260827T185118Z-084t4236` | live | package | `discarded` | `unevidenced` | the first assembly; normalize pass 1 failed |
| 09 | `package-20260827T190747Z-09sn82rr` | live | package | `discarded` | `unevidenced` | the consistency audit refused: a member disagreed with the frozen inventory or with the claims derived from it |
| 10 | `package-20260827T191122Z-10x52qgn` | live | package | `discarded` | `unevidenced` | the attempt-log audit refused: a transcript was not accounted for by exactly one row of exactly one attempt |
| 11 | `package-20260827T191528Z-1196tyyp` | live | package | `discarded` | `unevidenced` | the attempt-log audit refused again, on the same rule |
| 12 | `package-20260827T191825Z-12gkk5s8` | live | package | `discarded` | `unevidenced` | and a third time, on the same rule |
| 13 | `package-20260827T192021Z-13qt4xks` | live | package | `sealed` | **`superseded`** | it sealed, and then the executed-tool record could not be rendered: one logical tool had been executed as two different sets of bytes, so the record could not say which copy a claim was about |
| 14 | `package-20260827T192515Z-14vwr9zy` | live | package | `sealed` | **`superseded`** | it sealed, and the final verification then refused: the archive did not answer for the claims the package made about itself, so no authority record was written |
| 15 | `parent-20260827T193049Z-15pnpphq` | live | parent | `complete` | **`authoritative`** | the cold parent cohort every parent-side figure in this package derives from, executed at the exact tool digests this package ships |
| 16 | `head-20260827T194839Z-166gh2tz` | live | head | `complete` | **`authoritative`** | the cold shipping-head cohort every head-side figure in this package derives from, on the same terms |
| 17 | `package-20260827T200754Z-17ss7m5n` | live | package | `discarded` | `unevidenced` | the consistency audit refused again: a member disagreed with the frozen inventory or with the claims derived from it |
| 18 | `package-20260827T205127Z-189y3zrv` | live | package | `discarded` | `unevidenced` | normalize pass 1 failed |
| 19 | `package-20260827T205242Z-19k4x433` | live | package | `sealed` | **`superseded`** | it sealed, and the authority-coherence gate then refused: the records beside the package did not agree on which attempt was authoritative |
| 20 | `package-20260827T205659Z-2099y7ym` | live | package | `sealed` | **`superseded`** | it sealed, and the authority-coherence gate refused on the same rule |
| 21 | `package-20260827T205923Z-213p3n74` | live | package | `sealed` | **`superseded`** | and a third time, on the same rule |
| 22 | `package-20260827T221649Z-224yt5pr` | live | package | `sealed` | **`superseded`** | it sealed, and the outer siblings did not reach a clean sanitizer fixpoint: a tracked file beside the package would still have been rewritten by the sanitizer |
| 23 | `package-20260827T222021Z-23tzjtsz` | live | package | `discarded` | `unevidenced` | the attempt-log audit refused: a transcript was not accounted for by exactly one row of exactly one attempt |

**The counts are derived, not pinned, and that is deliberate.** Assembly may
create further attempts on the package side, and a figure hard-coded here would
be wrong the moment it did — which is the shape of defect this package exists
to stop repeating. At the state this file describes:

    attempt_count                          23
    terminal_execution_disposition_count   23
    unresolved_count                        0
    reused_ordinal_count                    0
    failed_count                            2
    abandoned_count                         1
    complete_count                          6
    authoritative_evidence_count            2
    set_aside_count                         2

**Three invariants are asserted over those counts rather than read off them**,
and `--assert-invariants` exits non-zero if any fails:

    attempt_count == terminal_execution_disposition_count    PASS
    unresolved_count == 0                                    PASS
    reused_ordinal_count == 0                                PASS

The first says every attempt reached exactly one terminal execution
disposition — the defect V15 shipped, where one interrupted battery reached
none and stayed unresolved because the vocabulary could express the absence of
a row but not the fact the absence stood for. The second says none is still
open. The third says no ordinal is carried by two attempts, and it is computed
across BOTH of this lane's ledgers, which is the only scope at which it means
anything (§6).

**`authoritative_evidence_count` is 2 and not 4, and that is the count doing
its job.** It counts the attempts whose evidence disposition IS
`authoritative`, and ordinals 04 and 07 no longer hold it; their `authoritative`
rows stand in the ledger and their `superseded` rows follow. Eight rows in the
table above read `superseded` — the two battery cohorts and six package
attempts that sealed and were then refused by a later gate — and the derivation
carries no count key for them, so the table and the ledger are what a reader
counts.

**A history this long is not a tidy one and this section does not apologise
for it.** Every attempt reached exactly one terminal execution disposition; no
ordinal was ever reused, across the retired ledger and the live one alike;
nothing was renumbered and nothing was deleted; each discarded assembly carries
its own row naming the audit that refused it, and §15 names where each retained
tree is kept; and the two superseded cohorts say so on their rows rather than
vanishing from the count. That is a stronger record than a short one. V15 shipped a history naming
six attempts where nine existed, and left one battery with no terminal row at
all.

### Attempt 06, stated in full because a killed run is exactly what a record hides

**It was stopped from outside itself.** The background process running that
battery was terminated by something that was not the battery, after three steps
had passed green. No step failed. No guard refused. Its execution disposition
is terminally **`abandoned`**, its evidence disposition is **`unevidenced`** and
permanently so, and its reason, verbatim from the ledger row:

> the background process running this battery was stopped from outside the
> battery after three green steps; no step failed and no figure of this attempt
> is carried anywhere, and the head cohort was measured again from the
> beginning under a later ordinal

**It contributes no validation result to any authoritative V16 claim.** Not a
count, not a size, not a digest, not a pass or a fail. The head cohort was
measured again from the beginning under ordinal 07, and then — once P8 had
refused that cohort's driver bytes — from the beginning again under ordinal 16;
every head-side figure this package reports is derived from the transcripts of
`head-20260827T194839Z-166gh2tz`. Attempt 06 is retained for history and audit
only: its partial cohort is kept outside this package, with a digest listing
every file it wrote, and §15 records it. That
retention is not a hedge — it is the difference between a record and a
narrative, and the one thing it must never do is support a figure.

**Why `abandoned` and not `failed`.** `failed` asserts that the run reached a
decision and that the record can name the step that made it. Nothing here
reached a decision; something outside removed the process. Collapsing that into
`failed` would assert a decision nothing made, and leaving it with no terminal
row at all — which is what the previous lane's vocabulary forced — leaves a
reader unable to tell an abandoned attempt from a lost one, and leaves the audit
saying only `unresolved`. §14 states the guards that keep the softer word from
covering a real refusal.

### Attempt 05, stated in full because a measurement of a head that moved is the other thing a record hides

    execution disposition = complete
    evidence disposition  = set-aside
    reason                = it measured a superseded V16 head

That battery ran to completion and every step of it passed. What changed is
what it was measuring: it measured head `251900b14`, and `cc1f2fb86` then
removed from the lane record the figures a record cannot truthfully state about
itself, so the head this package reports is not the head that cohort measured.
**No final validation figure in this package derives from attempt 05.** The
head cohort was measured again, cold and from the beginning, under ordinal 07,
and then again under ordinal 16 for the reason the next subsection states;
**attempt 16 is the shipping-head measurement source exactly as attempt 15 is
the shipping-parent source.**

The `complete` row is untouched. Setting the cohort aside appended a later row
on the evidence axis and altered nothing about how the attempt ended, because
the attempt ended the way it ended and no later knowledge changes that. A
record that overwrote the terminal row instead would be a record that cannot
tell "this ran and we declined its figures" from "this did not run".

### Attempts 04 and 07, stated in full because a cohort that was carried and then replaced is the third thing a record hides

    execution disposition = complete   (unchanged; both rows still say complete)
    evidence disposition  = authoritative, and then superseded
    reason                = what ran was not what shipped

Both cohorts ran cold, completed with every step recorded, and were recorded
`authoritative` the moment their batteries ended — **before any package had
been sealed from them**, which is the whole of the mistake and is stated first
because everything else follows from it.

**P8 is what caught it, and it is worth naming precisely, because it is
evidence that this protocol works rather than a story about a lane that
stumbled.** The final verification compares, for every tool, three digests: the
one recorded immediately before the tool EXECUTED, the one held by the
out-of-package TRUSTED anchor, and the one the archive SHIPS. Those cohorts had
executed `logs/battery.sh` at
`04ca35cb5969aea92d983c9793b5dc2d0d427c8a0ca356fa91db95bb8cc58c9c`; this
package ships that driver at
`cca4d2840116e2e101c68d9bdf8db1305f545b838015a837514f4464b73b947c`; the
comparison refused the archive on the ground that what ran is not what shipped.
**The entire difference between those two files is header comment prose** — the
driver's header was rewritten in this very lane, when execution disposition was
split from evidence disposition — and the gate refused anyway, which is exactly
what a byte-identity gate is for. A gate that accepted a difference because the
difference looked harmless would be a gate that never refuses anything, and no
reader could then tell which copy of a driver produced a figure.

The reason recorded on both `superseded` rows, quoted with its two digests
written out in full and its tool name set as code, because the ledger records
the digests abbreviated and this package's identity audit refuses an
abbreviated hex token that prefixes no commit the package may name:

> this cohort executed `logs/battery.sh` at digest
> `04ca35cb5969aea92d983c9793b5dc2d0d427c8a0ca356fa91db95bb8cc58c9c` while the
> package ships that driver at
> `cca4d2840116e2e101c68d9bdf8db1305f545b838015a837514f4464b73b947c`; the
> difference is header prose from the execution-versus-evidence split, and P8
> refuses an archive whose executed bytes are not its shipped bytes, so the
> endpoint was measured again under a later ordinal and this cohort's figures
> are not carried

**Why this could not simply be recorded, and what changed so that it could.**
The evidence disposition had already been written, and a battery's evidence
axis was strictly irreversible: the cohorts could not be set aside, because
they had been carried, and they could not be un-recorded without deleting a row
that was true at the moment it was written. That left the record unable to say
what had plainly happened — which is the V12 defect arriving from a new
direction. The battery axis therefore gained the one succession the package
axis already had, on the same reasoning and with the same terminal shape; §3
states the machine and §14 states the verb and its guards.

**What was done instead of explaining the difference away.** Both endpoints
were measured again, cold, from the beginning, against frozen drivers, under
ordinals 15 and 16. Every tool those batteries executed — `logs/battery.sh`,
`logs/gate-summary.py`, `logs/gzip-sizes.py` and `logs/journal-dump.py` — matches its shipped
copy byte for byte, and that identity was established BEFORE either evidence
disposition was recorded the second time. Both re-runs report, on a cold
`build/`, the same `divergent_rows`, the same `distinct_divergent_identities`,
the same `volatile_rows` and the same `total_differing_rows` that §16
reconciles, which is what a byte-identical driver measuring the same two commits
should report.

**The superseded cohorts reproduced those same cold counts, and that is
recorded as a CONTROL rather than as a source.** Two independent pairs of cold
runs landing on the same four measures is a small check that the figure is a
property of the measurement surface rather than of one run, and it is worth
recording for exactly that. It is not authority: authority for every V16
example figure in this package derives from the cold cohorts under ordinals 15
and 16, which are the members `logs/attempt-15/make-check-parent.log` and
`logs/attempt-16/make-check-head.log`, and from nothing else.

**No figure in this package derives from attempt 04 or attempt 07.** Their
transcripts are not members; they are retained local-only, in one tree because
one cause superseded both, and §15 records the tree with its file count and the
sidecar that digests every file in it. Their `complete` rows are untouched and
their `authoritative` rows are untouched, because both were true when they were
written, and a record that rewrote them could no longer tell "this was carried
and then replaced" from "this was never carried at all".

### A divergence from the final instruction, disclosed rather than reconciled away: `authoritative → superseded` where the instruction says `set-aside`

**What this lane did.** The final assembly instructions this lane was given fix
the evidence-disposition vocabulary at three words — `authoritative`, `set-aside`, `unevidenced` — and
direct that a completed assembly later superseded should take a separate
evidence `set-aside` record. **This lane had already recorded cohorts 04 and 07
as `authoritative → superseded` before that instruction existed**, using a
succession the package evidence axis already carried, and both of those rows are
irreversible by design. Rewriting them is forbidden by the same rule that makes
them worth anything, so they stand as written and this lane declares the
difference here rather than quietly conforming the prose to a vocabulary its
ledger does not contain.

**Why it was recorded that way.** `set-aside` asserts that a cohort's figures
were declined **without ever having been carried**. That would be false of 04
and 07: they were recorded `authoritative` the moment their batteries ended,
they were carried, and they were then replaced when P8 refused the archive on
the ground that what ran was not what shipped. A record that said `set-aside`
of them would be a record that cannot tell "this was carried and then replaced"
from "this was never carried at all" — and that erasure, deleting or flattening
a superseded predecessor's history, is precisely the V12 defect this whole
sequence exists to correct rather than the cure for it. The package evidence
axis already had exactly this succession, added for exactly this reason; the
battery axis gained the same one succession and no other.

**The effect is identical either way, and that is the point.** Under
`superseded` and under `set-aside` alike, **neither cohort is an authoritative
source of any V16 figure**. No figure in this package derives from either. The
disagreement is about which word truthfully records how they stopped being
carried, not about what they support — which is nothing.

**The question is put to the reviewer rather than defended.** Is `superseded`
right here, on the ground that a carried-then-replaced cohort is a different
fact from a never-carried one and a record that cannot distinguish them is the
defect? Or should the vocabulary have been held to the three words the
instructions name, with the distinction carried in the reason text of a
`set-aside` row instead — accepting a coarser axis in exchange for a vocabulary
no lane extends mid-run? This lane's answer is the first; it is a judgment made
inside the lane about the lane's own state machine, which is the kind of
judgment least safe to make unreviewed, so it is written here in full rather
than left for a reviewer to notice from the ledger.

## 14. The state-machine work: the verbs, every guard, and the two defects it found in this pipeline's own gates

The vocabulary of §3 is only worth what its refusals are worth, so the
refusals are stated here and each is pinned by a test.

**`--abandon-attempt ID --attempts LEDGER --lane LANE --reason WHY`** appends
one terminal execution row. It refuses unless:

- the ledger exists and carries that attempt;
- the attempt belongs to the named lane, and the lane is either given or
  declared by the ledger itself;
- the reason is substantive — at least forty characters over at least eight
  words, because an attempt abandoned without a stated reason is the defect the
  verb exists to close and a token reason is a shorter way to write the same
  silence;
- the attempt has NOT already reached a terminal disposition, because every
  attempt reaches exactly one and rewriting that is what an append-only ledger
  forbids;
- and **no row of that attempt carries a battery-written `failed` or
  `discarded` status, or a result beginning `REFUSED:` or `FAILED:`.** An
  attempt whose own run reached a decision is failed or discarded, and the
  disposition that names the decision is the truthful one.

**Abandonment does NOT key on step exit codes, and that is the guard's most
important property rather than a loophole in it.** Four gates in the repository
under test are inherited-red by design and return 2, 2, 1 and 2 at BOTH
endpoints; a battery that ran all of them and finished is `complete`. A guard
that read a non-zero step exit as a failed step would make this verb unusable
on every real battery this lane ran, and would record a false statement about
the ones it did accept. What says a run reached a decision is a DISPOSITION —
a row a guard or the battery itself wrote — and that is the only thing the
guard reads. A test pins each direction: an attempt with red-but-expected exits
is abandonable, and an attempt carrying a written refusal is not.

**`--set-aside-attempt`** and **`--authoritative-evidence`** are the two
answers to one question — what became of a completed cohort's measurements —
and they are the same shape because they are the same axis. Each refuses
unless:

- the attempt is a BATTERY attempt; a package attempt is superseded, never set
  aside, and a package attempt's authority is established after the final
  verification by the sidecar bound to the archive, never by hand;
- the attempt has reached a terminal execution disposition, and that
  disposition is `complete`. `failed` and `abandoned` are refused by name, with
  the reason given: only a battery that COMPLETED has measurements to carry or
  to decline, and calling one authoritative would assert a result its run never
  reached;
- the attempt carries no evidence disposition already — not a second one of the
  same kind and not one of the other kind, in either order;
- the lane matches and the reason is substantive on the same terms as above.

**Neither verb touches the terminal row.** Both print the execution disposition
back with `(unchanged; this row does not replace it)` beside it, because the
one thing a reader must be able to see is that the two facts are two rows.

**`--supersede-evidence` is the third answer, and it was added in this lane
because this lane needed it.** It records that a cohort or a package attempt
which really was authoritative has been replaced. It refuses unless:

- the ledger exists, carries that attempt, and the lane matches;
- the attempt actually HOLDS `authoritative`. Superseding anything else is
  refused by name and with the reason given — superseding a `set-aside` cohort,
  or one with no evidence row at all, would assert that it had once been
  carried when it never was. The package side's `sealed → superseded` shortcut
  is not this verb: it is written by the assembler on the run that failed a
  post-seal phase, for an attempt that never held authority, and §3 states
  which edge is which;
- the attempt is not already superseded, because `superseded` is terminal and
  a second such row would make the record say the same thing twice with two
  reasons;
- the reason is substantive on the same terms as above, at least forty
  characters over at least eight words. The refusal message says why: a figure
  withdrawn with no account of what replaced it is the defect, not the record
  of it.

It appends and never rewrites. The `authoritative` row it follows is left
exactly as written, and the verb prints that back too, because the succession
is only honest if the disposition it succeeds is still legible.

**The tests are six suites and they are green.** They went from 451 to 545
across those suites for this lane's work: `logs/test-attempt-history.py` 169,
`logs/test-authority-coherence.py` 91, `logs/test-compare-gate.py` 13,
`logs/test-handoff-inventory.py` 65, `logs/test-sanitize-and-seal.py` 169 and
`logs/test-verify-final-package.py` 38. Every one of them ships as a member so a
reviewer runs the refusals rather than reading about them.

### And two defects this lane found in its own gates, before assembly rather than during it

**`logs/authority-coherence.py` held a stale copy of the vocabulary, and it would
have refused this package for telling the truth.** Its battery state set
contained `started`, `complete`, `failed` and `set-aside` — `abandoned`
appeared **in no vocabulary at all**, on either side. So a package shipping the
honest record of attempt 06 would have been rejected by this lane's own
publication gate *because* it shipped that record, and the only way past the
gate would have been to delete or soften the row. That is the shape of defect
that produces a clean history: not a lie anyone tells, but a check that only
accepts one. It is fixed, the fix is a vocabulary the two axes are read out of
rather than one flat set, and the module now asserts at import that every
terminal state is covered by exactly one of the reason-required and successful
partitions.

**The same gate faulted twice on a battery cohort recorded `authoritative`**,
for the neighbouring reason: it assumed the word could only ever mean "the
package to review". A cohort marked authoritative under
`--authoritative-evidence` would have deadlocked assembly at P5. Both defects
were found and fixed before assembly ran, both are pinned by tests among the
counts above, and both are recorded here rather than quietly repaired, because
a gate that would have refused an honest package is a finding about the gate
and not a chore.

## 15. Every retained cohort and every ledger, with the rule that governs them

**The rule first, because it is what makes the list checkable: no authoritative
claim in this package may require an unsanitized, builder-local artifact.**
Everything below that is local-only is retained so that the history is not
destroyed, and nothing below that is local-only supports a figure. The figures
this package reports come from the two shipped cohorts, which are members,
scanned and re-scanned like every other member.

**Shipped, and therefore members of the manifest:**

| Cohort | Attempt | Files | What it is |
| --- | --- | --- | --- |
| `logs/attempt-15/` | `parent-20260827T193049Z-15pnpphq` | 13 | the cold parent cohort; evidence disposition `authoritative` |
| `logs/attempt-16/` | `head-20260827T194839Z-166gh2tz` | 12 | the cold shipping-head cohort; evidence disposition `authoritative` |

**Local-only, never shipped, retained under `spincyc/v16-retired/` outside this
package**, each beside a sibling `.sha256` listing every file it holds so a
reviewer handed one can tell which it is:

| Cohort | Files | Bytes | Evidence status | Why it is retained |
| --- | --- | --- | --- | --- |
| `attempt-01-refused` | 12 | 785,632 | `unevidenced` | the exec-record guard refused a non-replayable row; the directory name predates the terminology correction of §3 and the attempt's execution disposition is `failed` |
| `attempt-03-warm` | 14 | 10,112,329 | `set-aside` | a green parent cohort measured on a warm `build/`; its figures were declined and the cohort re-run cold |
| `attempt-04-07-driver-drift` | 27 | 19,669,322 | `superseded` | the cold parent cohort of ordinal 04 and the cold head cohort of ordinal 07, in one tree because one cause replaced both: each was recorded `authoritative` when its battery ended, and P8 then found they had executed a `logs/battery.sh` this package does not ship |
| `attempt-05-superseded-head` | 13 | 9,556,761 | `set-aside` | a green head cohort that measured a superseded head |
| `attempt-06-abandoned` | 5 | 110,007 | `unevidenced` | externally interrupted; retained for history and audit only and supporting no figure anywhere |

**The ledgers.** The retired one is immutable and is bound by digest;
the live one is not, and saying why is the point.

| Ledger | State | Bytes | Rows | Bound by |
| --- | --- | --- | --- | --- |
| `build/agent-handoffs/attempt-ledger.jsonl` | retired, ordinals 1–3 | 21,536 | 29 | SHA-256 `d7fd68ce256f94d1efca59d3248960a5d6d6999ea4aa2d06c60cf6cb2c901d87` |
| `build/agent-handoffs/attempt-ledger-02.jsonl` | live, ordinals 4 onward | — | — | **name and row count at seal, not a digest** |
| `build/agent-handoffs/executed-tools.jsonl` | live, lane-wide | — | — | name; it is the lane-wide execution journal, outside every sanitize walk |

**A live ledger cannot be bound by digest and it is dishonest to pretend
otherwise.** Its bytes move every time an attempt appends a row, and assembly
appends rows — so a digest written here would be stale before the package
sealed, and a reader checking it would find a mismatch that means nothing. What
binds it is its name and its row count at the moment of seal, recorded by the
gate that reads it, and the in-package copy `logs/attempts.json` which the
authority gate compares against the external file and refuses on disagreement.
The retired ledger has the opposite property: nothing will ever append to it
again, so its digest is a real identity and is given.

**None of the local-only artifacts above is a member, a named sibling, or
committed to any evidence branch**, and none is inside any sanitize walk —
the retired ledger's `command` fields hold raw pre-sanitization absolute paths,
which is one of the reasons it is not shipped. `PRIVACY-AUDIT.md` states that
boundary in its own words and `LIMITATIONS.md` records the class. What a
reviewer can do with them is identify them by digest and file count; what a
reviewer cannot do is audit their contents from this package, and no claim here
asks them to.

## 16. The example-divergence figure, reconciled mechanically against the review that raised it

**The full derivation is `logs/divergence-reconciliation.json`, which is a
member.** It carries the parsing rule and its soundness argument, all four
transcripts field by field, the identity set-differences in both directions,
the volatile check, the root cause with its controlled experiment and its live
reproduction, and the reconciliation against the V15 review. Nothing in this
section is typed that is not in that file, and where the two could be read as
disagreeing the file is right.

**The four measures this section uses, named apart, because collapsing them is
the defect it exists to correct.** `divergent_rows` is the count of captured
rows the replay marked `DIFF`, and a command captured twice contributes two of
them. `distinct_divergent_identities` is the count of distinct command strings
among those rows. `volatile_rows` is the count of lines declared volatile in a
static source table and masked BEFORE comparison; they are never `DIFF` rows and
are no part of `divergent_rows`. `total_differing_rows` is the sum of the first
and third, stated only as that sum and never as a count of anything. Every
figure below is one of those four and says which.

**The authoritative basis, and the historical basis, kept apart.** The
authoritative V16 measurement basis is the pair of COLD cohorts under ordinals
15 and 16 — `logs/attempt-15/make-check-parent.log` at the parent
`b9202882badbbbc364f1dd3d9057d2710ee47552` and
`logs/attempt-16/make-check-head.log` at the head
`cc1f2fb8625f044558c26edd358b99cd7dcc7646` — carried in
`logs/divergence-reconciliation.json` under `figures.v16_parent`,
`figures.v16_head` and `authoritative_basis`, with `v16_endpoints_equal` true.
**Everything this section says about V15 is HISTORICAL, inferred from shipped
V15 evidence taken on a warm tree, and is never a fresh V16 replay**; V15's own
ordering ledgers carry no build-state line, so even the warmth of that tree is
an inference from V15's own transcript rather than a recorded fact, and the
member records it as one. **The superseded cohorts under ordinals 04 and 07
reproduced the same cold counts and are recorded as a CONTROL on this figure,
never as a source of it**; the member says so in `cohort_note` and
`authoritative_basis.note`.

**The V15 review's OBSERVATION stands and is not softened.** V15's durable
prose claimed a bare thirty at both endpoints, naming no measure and no build
state; V15's own shipped transcripts report twenty-eight `DIFF` rows over
twenty-seven distinct commands and summarise `28 diverged … 2 volatile line(s)
declared`, which is the tool's own summary field quoted verbatim. No artifact
in the V15 package supported the durable figure. That was correctly caught and
this lane does not relitigate it.

**The review's DIAGNOSIS does not stand, and this lane says so rather than
inheriting it.** The review's sentence is quoted once, here, in its own words,
so that what is being refused is on the record rather than paraphrased into
agreement — and it is quoted in order to be refused, not adopted:

> The authoritative logs report 28 divergent examples plus two separately
> declared volatile lines, not the durable producer claim of 30 divergences.

That reading presents thirty as decomposing into twenty-eight and two, and it
cannot decompose that way. Its governing noun is not one of the four measures
above: "divergent examples" names neither `divergent_rows` nor
`distinct_divergent_identities`, and that ambiguity is load-bearing rather than
stylistic, because twenty-eight is true of BOTH — of `divergent_rows` in the
V15 warm transcripts the review was reading, and of
`distinct_divergent_identities` at the authoritative V16 cold endpoints — and
those are two different facts about two different runs. A word that can stand
for either is a word that lets a reader carry a figure from one to the other
without noticing, which is why this package retires it. The volatile figure is a
STATIC constant computed as `sum(len(lines) for lines in VOLATILE.values())`
over a two-entry module-level table; it counts DECLARED LINES over the source
tree, never a run outcome. Both of the captures that table names are masked
before comparison, and in all four transcripts they appear as `ok` and
`absent` — never as `DIFF` rows. They were never in the set they are supposed
to be subtracted from, so they can be neither added to it nor taken out of it.
The equality is an arithmetic coincidence, and it closed the question on the
wrong cause.

**The cause is BUILD STATE.** `build/example-ordinary` is written by a later
capture in the same target — `tools/mass-ordinary structure --out
build/example-ordinary`, at tool line 211 — and it is never cleaned up, because
`mass-ordinary` appears in neither the `SCRATCH` table nor the `PREPARE` table
of `scripts/replay_examples.py`. On a cold tree the two `check` captures run
before anything has created that directory and both report that files would be
rewritten; on every later run in the same tree they match. `typeset-bible` has
exactly this shape and IS handled, with a `PREPARE` entry whose comment
describes the identical problem. That missing entry belongs to another owner
and this lane does not fix it; `LIMITATIONS.md` discloses it and
`UNRESOLVED-BLOCKERS.md` records the owner.

**There is ONE additional identity, and it contributes TWO rows.** This is the
correction that matters most, because getting it wrong would have been this
lane committing, in the very sentence that fixes a row-versus-name conflation,
the row-versus-name conflation. Set-differencing the divergent command
identities in both directions: exactly one identity is present in the V16 cold
set and absent from the V15 warm set, and NOTHING is present in the V15 set and
absent from the V16 set — the V16 cold set is a strict superset. That one
identity is `tools/mass-ordinary check --out build/example-ordinary`, and it is
captured TWICE in `tools/mass-ordinary`, at lines 116 and 201, replayed as rows
96 and 102. So one new NAME contributes two new ROWS. Distinct diverging
commands go twenty-seven to twenty-eight, not twenty-six to twenty-eight, and
**the phrase "the two additional identities" is itself the conflation and is
not repeated here.**

**The controlled evidence that the tree is not the variable, and why this is a
measurement-surface difference rather than a behaviour delta.** V15's head
commit IS V16's parent commit, `b9202882badbbbc364f1dd3d9057d2710ee47552`, and
that one commit reports twenty-eight divergent rows warm and thirty divergent
rows cold. The same commit, the same command, the same bytes: nothing about the
tree under test moved, only the state of `build/` the measurement was taken
against. That is the whole force of the word SURFACE here, and it is what makes
the V15-to-V16 change a difference in how the figure was taken and not a
difference in what the code does. The two authoritative V16 cold cohorts, the
parent under ordinal 15 and the head under ordinal 16, agree exactly on
`divergent_rows`, on `distinct_divergent_identities`, on `volatile_rows` and on
`total_differing_rows`, so no V16 parent/head behaviour delta is being reported
at all. `tools/mass-ordinary`
and `scripts/replay_examples.py` are byte-identical blobs at all three commits
involved — `69f25754`, `b9202882` and `cc1f2fb8`. The transition was then
reproduced live in a throwaway extract, replaying that tool alone: two
divergent rows cold, none warm, none warm again, and two divergent rows again
after the directory was removed. It is deterministic and reversible by exactly one filesystem
condition.

**A parsing subtlety, stated because a reader who checks will meet it.** The
producer's `N diverged` field is `len(diverged) + len(recovered)` — that is,
`DIFF` rows together with `FIXED` rows. `FIXED` is zero in all four
transcripts, so the field coincides with the `DIFF` row count here, but the two
are not the same quantity and a later run in which anything recovers would
separate them. This package reports the row count and the distinct-command
count as two derived figures and does not lean on the summary field for either.

**So the sentence this package ships, and the shape of every sentence like
it.** The authoritative V16 parent and head cold cohorts agree exactly. Each
contains **30 `divergent_rows`** representing **28 `distinct_divergent_identities`**, plus **2 `volatile_rows`**, for **32 `total_differing_rows`**.
Historical V15 shipped warm evidence contained **28 `divergent_rows`** representing **27 `distinct_divergent_identities`**, plus **2 `volatile_rows`**, for **30 `total_differing_rows`**.
The V16 cold set is a
strict superset of the V15 warm set by exactly one distinct identity,
`tools/mass-ordinary check --out build/example-ordinary`, which contributes two
captured divergent rows; nothing is in the V15 set and absent from the V16 one.
The V15 figures are historical reconciliation evidence only, and V16
authoritative validation derives from attempts 15 and 16.

**The bare phrase "30 divergences" is never shipped, and neither is "28
divergences"**, because on their own they omit the build state without which
the figure does not reproduce, because neither names which of the four measures
it means, and because the first silently endorses a decomposition this lane has
refuted. Thirty is a count of ROWS. Twenty-eight is a count of IDENTITIES. A
sentence that lets a reader take either for the other is the defect, not the
shorthand.

`logs/divergence-reconciliation.json` also records the directions' fourth
measure, `total_differing_rows`, under `figures.v16_parent` and
`figures.v16_head` beside the other three. It is
an arithmetic sum of two quantities of different kinds, it is recorded because
the directions ask for it, and it is not a count of anything — which is exactly
why it lives in a JSON field with a name that says what it is rather than in a
sentence that would read as a defect count.

### The path policy this artifact holds to, stated because it is a design decision and not an omission

**All artifact member names and evidence references in
`logs/divergence-reconciliation.json` are package-root-relative, and
builder-local absolute filesystem paths are excluded because they are not part
of the portable evidence identity.** An absolute path read at derivation time is
a fact about one machine's filesystem and not a fact about the evidence; the
only root that exists once the archive is unpacked is the package root, and a
reviewer resolves every name against it. The member states this in its own
`path_policy` field, so the rule travels with the artifact rather than only with
this sentence.

**Local absolute paths are NOT tokenised into placeholders merely to preserve
them.** A token standing where a builder path used to be still records that a
builder path was thought worth keeping, and it invites a reader to believe a
reference is resolvable that is not; the sanitizer's tokens exist to redact
paths that must appear, not to memorialise paths that need not. Nothing is lost
by the exclusion, because nothing in the derivation depends on where the builder
happened to keep a file. **This is deliberate evidence design.** An earlier
cross-lane note in this package's narrative said that this member carried raw
host paths and should be looked at on that ground; it no longer describes the
regenerated artifact and it has been removed rather than left standing, and
`PRIVACY-AUDIT.md` records both the removal and the one thing that remains — two
`local_path_read` fields under the HISTORICAL V15 transcript entries, recording
where the predecessor package's logs were extracted to be parsed, retained as
historical derivation context for figures this package derives nothing from.

### The row-versus-name conflation, in five places, and the rule taken from it

This lane has now found the same error five times in one body of evidence, and
each instance was a real count wearing another count's name:

1. the browser gate — **2,290 assertion ROWS across 17 diagnostic NAMES**,
   found by the V15 review;
2. the example replay — **30 `divergent_rows` over 28
   `distinct_divergent_identities`** cold, found here;
3. full discovery — **27 result ROWS spanning 22 distinct IDENTITIES**, which
   the V15 record called "27 identities";
4. the parent replay — **288 failure ROWS over 39 distinct METHODS**, one
   method alone contributing 192 `subTest` rows;
5. and this lane's own first framing of the divergence figure, above, which
   said "two additional identities" where there is one.

**The rule, which is the part that generalises: wherever this evidence quotes a
count, it says what is being counted, and no figure is stated without the state
it was taken in.** Fixing only the artifact the review named would have left
three live instances in the same package, and the fifth instance says plainly
that finding the shape is not the same as being immune to it.

### The compare gate, reported at its own granularity

Three figures, kept apart, because collapsing them is the same error again:

    total_gate_rows                            2,290
    normalized_reports_equal                     yes
    distinct_diagnostic_names_or_categories       17

**Three quantities, reported separately, never folded into one.**
`total_gate_rows` is the identity universe: 2,290 assertion rows.
`normalized_reports_equal` is a verdict and not a count at all — the equality is
over the whole report object, all of the rows included, minus the named volatile
fields, and that half of the previous lane's gate was sound and is unchanged in
kind. `distinct_diagnostic_names_or_categories` is the diagnostic vocabulary the
localiser reports in, and **it is not a row-identity count**: nothing here should
be read as implying that a small diagnostic category count equals the full
2,290-row identity universe. Seventeen categories do not enumerate 2,290 rows,
and the sentence that let them appear to is the defect this gate's rebuild
closes.

## 17. Two vocabularies of `$NAME`, one derived legend, and no name meaning two directories

Two disjoint sets of `$NAME` tokens reach this package, from subsystems that
never meet, and the package ships a legend covering both rather than leaving a
reviewer to work out which is which.

**REPLAY ROOTS are BINDINGS**, written by the battery driver and the assembler
into command records. Supplying one — `replay-command.py --root NAME=/path` —
is what makes a recorded command run. They are `$CANDIDATE_REPO`,
`$PARENT_REPO`, `$PACKAGE_ROOT`, `$TOOLS_ANCHOR` and `$EVIDENCE_ROOT`, and
their meanings are declared at run time on `root=` lines in the ordering
ledgers, from which the legend is built.

**SANITIZATION TOKENS are SUBSTITUTIONS**, written by the sealer into
transcript prose: a private path was removed and the token stands where it was.
They are `$REPO`, `$WORKSPACE`, `$EVIDENCE`, `$SCRATCH` and `$HOME`. Nothing
binds them, and no recorded command may use one —
`catena_command.RESERVED_VARIABLES` refuses exactly these names in a record.

**The two scopes never meet, and the legend enforces that in both directions.**
A replay root that no ledger defines is a refusal; a sanitization token the
sealer can emit and the legend does not explain is a refusal; and a name that
is BOTH is a refusal, because that is V15's defect under a new spelling. The
token list is derived from the sealer's own substitution tables by three
independent readings unioned together, so a token added to any of them appears
in the legend without the legend being edited.

**Where a token and a replay root name the same directory, the legend says so
with `==` rather than leaving it to be inferred.** `$REPO == $CANDIDATE_REPO`:
the candidate checkout is `$CANDIDATE_REPO` in `commands.json` and `$REPO` in a
transcript, which is one directory with two spellings in two subsystems and is
not ambiguity. V15's defect was the opposite and much worse — ONE token, `$REPO`,
meaning TWO directories inside a single row, so unquoting alone could not
recover what had run.

**Two corrections to statements a reader might otherwise carry forward.**
`$WORKSPACE` is the workspace root that CONTAINS the checkouts and the anchor:
it is a PREFIX of the replay roots and equal to none of them. And **`$EVIDENCE`
is NOT `$TOOLS_ANCHOR`** — the sealer's rule matches the `.agents/<segment>`
directory segment and nothing else, so `$EVIDENCE` names this lane's agent
evidence directory, not the out-of-package tools anchor. The V15 review landed
on that pairing because the PREDECESSOR package's own siblings disagreed with
each other:
`build/agent-handoffs/20260826T195656Z-catena-e1-corrections-v15.verify-final.log`
said `$WORKSPACE/…` where
`build/agent-handoffs/20260826T195656Z-catena-e1-corrections-v15.executed-tools.json`
said `$EVIDENCE` for the one anchor. Neither is an artifact of this package —
both sit beside the V15 package on `evidence/catena-e1-corrections-v15-handoff`
and are named here by the repository path they occupy there, so that no reader
takes the defect for one of this package's own siblings. This package answers
the finding in its own bytes rather than leaving a reviewer to work it out.
