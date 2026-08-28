# Review request — E1 Catena correction V16

**A fresh independent review is asked for, at the candidate head of
`impl/catena-wave-1-e1-corrections-v16`, against the exact parent
`b9202882badbbbc364f1dd3d9057d2710ee47552`.** Nothing in this package records
an acceptance, and no disposition is claimed by it. The review this lane
answers is `67247ecc39a6e5f6224c64ca3ab1af163ee023b1` on
`review/catena-wave-1-e1-corrections-v15-independent`, which answered
**SEMANTIC CHANGES REQUIRED**, **EVIDENCE CHANGES REQUIRED** and **CHANGES
REQUIRED** overall.

This asks only what needs judgment from outside this lane. Everything this
lane believes it proved is in `CLAIM-CLOSURE.md` with its evidence, the
figures are in `claims.json` and `DERIVED-CLAIMS.md`, and the commands are in
`checks.txt`; none of them is repeated here.

## Blockers

### 1. The completion envelope as the carrier of ownership

The defect was that the answer travelled alone. `M.bodyAsked(row, content)`
asked only whether `row` was a row this model had projected, so an actual B row
authorized any content at all — A's answer, a literal, a value no request ever
produced — and the association held in production only because one closure
happened to carry both halves. The shape chosen here is a frozen envelope,
minted by `M.textCompleted`/`M.textFailed`, carrying the exact `rowTransport`
owner beside the finalized value, sealed in a `WeakSet` so a same-shaped
literal is not one, and required at the application by three exact-object
comparisons.

Three questions, and they are separable.

**Is a per-caller envelope the right carrier, or does it put ownership in the
wrong place?** The envelope is never shared and never becomes the path-cache
value, which is what keeps the cache owner-independent; the price is that
ownership is now an object the page holds and passes, and a caller outside the
projection cannot construct one at all. That refusal is deliberate and it is
also a constraint on anything that later wants to drive this transport from
outside. Is the envelope the right identity, or should the sink take the owner
and the value as two arguments and compare them itself?

**Is `WeakSet` membership a sufficient seal?** It is unforgeable from outside
the module and it is not enumerable, which is exactly what is wanted; it is
also invisible to a reviewer reading a value in a debugger, and a value that
looks correct in every observable respect can still be refused. Is
unforgeability worth that opacity here?

**Is rebinding a cached value through a later owner's own completion sound?**
A finished value already at the path is handed to a second row inside a fresh
envelope minted for that row's owner. The value crosses an owner edge; the
envelope does not. This lane's position is that an owner-independent,
null-prototype, frozen, scalar-only record is the class of thing that may
cross, and that the whole finding is about sharing something outside that
class — so the boundary is doing real work and a reviewer should test it
rather than accept it.

### 2. Publication atomicity, and what the probe can and cannot see

The rule is that the path map receives only a value that has been finalized:
`M.textPayload(file)` runs to completion, and only then does
`fragmentTexts.set(path, content)` run. The proof is a probe over
`Map.prototype` that records what a lookup of that path returns at every
instant it could return anything — before the handler, during parsing, during
normalization, before publication, after publication, and from a synchronous
reentrant lookup inside the handler itself.

Two limits on that proof, and both are judgment calls a reviewer should weigh.

**The probe is in the harness, not in the page.** `fragmentTexts` is a
module-scope `Map` inside the page's own IIFE; nothing exported reaches it, and
adding an export so a test could look would be the test changing the thing it
asserts about. Wrapping `Map.prototype` for the whole replay realm is the
alternative, and it means the assertion is about what the engine saw rather
than about what the page published. Is that the right substitution?

**A negative about instants is proved over the instants the probe visits.**
The probe visits every event this lane could name. It cannot prove that no
instant exists which nobody named. What is claimed is the stronger structural
fact beside it — that the value passed to `set` is the return of a function
that has already run to completion, so there is no partially built value to
observe — and a reviewer is asked to judge whether the structural argument or
the probe is what carries the claim.

### 3. The body journal, and what an unconfirmed write leaves behind

`M.bodyApplied(row, completed, wrote)` appends a record only when the
completion is still owner-valid and the write is confirmed by reading the node
back. A write that throws and a write that silently does not take both leave
**no entry at all**.

**Is silence the correct disposition?** This lane's argument is that it is the
only truthful thing an append-only body journal can do: an entry saying "not
applied" is a record of an event that produced no page state, and the journal
exists to say what reached the reader. The counter-argument is that a reviewer
reading the journal cannot distinguish a body that failed to write from a body
that was never asked for, and that a separate refusal channel would carry that.

**And the confirmation is narrower than "the body was applied".** What is read
back is `text.textContent` — the fragment's words. The acknowledgement block
and the `Extent —` and `Date —` apparatus paragraphs that may be appended
beside it are not confirmed. The positive claim is therefore that the body text
reached the page; the negative claim — that a body which did not reach the page
leaves no entry saying it did — is the one this lane is entitled to, and it is
stated that way in `CLAIM-CLOSURE.md` and `LIMITATIONS.md`. Is the narrower
confirmation acceptable, or does the confirmation need to cover the apparatus?

### 4. Exact reproducible evidence, and a record that can be re-run

The previous review found the evidence defective in the respects
`PROVENANCE.md` enumerates, and most of them are defects in this pipeline's own
tools. They are fixed here rather than explained: a command representation that
carries the working directory, the argument vector and the environment a shell
was actually handed, instead of a single string whose quoting cannot expand;
distinct repository variables, so one token never stands for two directories;
a classifier that no longer accepts prose by prefix match and a completeness
checker that no longer trusts a precomputed label; tool execution derived
mechanically from the attempt logs, with the scripts that drove the build
classified as executed; one phase-labelled count schema instead of two
unreconciled sets; the complete predecessor history across all three V15
ledgers; the corrected example figures, stated as two figures of two different
kinds and never summed; gate diagnostics that no longer collapse thousands of
assertion rows onto a handful of names; and a completeness verdict taken after
the outer sanitization and its re-scan, at the final state.

**Is the command record now re-runnable end to end?** The specific ask is that
the reviewer take a row from `checks.txt`, resolve its tokens from the legend
the package ships, and run it — and confirm that no authoritative row is a
paraphrase, that no row single-quotes a variable it needs expanded, and that no
one token stands for two locations. A pipeline that was wrong about seven of
its own rows may still be wrong about an eighth, and this lane's verdict on its
own tooling is not independent.

**Is the tool accounting one kind of row, honestly labelled?** V15 sealed two
unlabelled count sets in one package and manufactured six rows with a
fabricated time, phase and log — three fields a tool that never ran cannot
have. What ships here is derived from what the run recorded. Whether the schema
distinguishes the right things — unique referenced, unique executed, execution
invocations, shipped, and trusted but not executed — is a judgment worth an
outside verdict.

**Is the disclosed history complete this time — and complete across what?**
`PROVENANCE.md` states this lane's own attempts, and states the V15 predecessor
history across all three of its ledgers rather than the single shipped slice.
Two of those ledgers are retired and unshipped, and they are disclosed by byte
count, row count and digest. Is a retired ledger disclosed by digest an
acceptable substitute for one that was never opened, and is the classification
of V15's two completed retired batteries as set-aside cohorts the right reading
of that word? **The same question is turned back on this lane, because this
lane retired a ledger too, and its own history is not inside a single file.**
`build/agent-handoffs/attempt-ledger.jsonl` spent ordinals 01 to 03 and was
retired when a parent cohort that had run green was declined for having
measured against a warm `build/`; `build/agent-handoffs/attempt-ledger-02.jsonl`
opened at ordinal 04 in its place, carrying the retired file's digest, byte
count, row count, the ordinals it spent, the attempts it held and the reason it
stopped in its own opening `lane` row. No row in either was rewritten or
deleted, each file is append-only within itself, and the retired one is retained
whole and bound by SHA-256
`d7fd68ce256f94d1efca59d3248960a5d6d6999ea4aa2d06c60cf6cb2c901d87` over 21,536
bytes and 29 rows. The history is whole only when both files are read together,
which is exactly what `logs/attempt-history.json` derives and what
`PROVENANCE.md` §15 records with both files' identities. The rest of that
history is long, and no total for it is typed here, because assembly appends
package attempts and a figure written into prose would be stale before the
archive sealed: it holds discarded assemblies, sealed package attempts later
superseded, two batteries that failed outright, one abandoned from outside
itself, cohorts set aside, and two battery cohorts that were carried and then
replaced. None was renumbered, deleted or merged, and no ordinal was reissued
across the retirement. Is a long history that accounts for every ordinal the
right thing to ship, or does its length itself now obscure the two cohorts a
reviewer actually has to check?

### 5. Two axes for an attempt's history, and a terminal disposition for a run nobody finished

The previous machine recorded how an attempt ended and what became of its
figures on ONE axis, which is why it could draw `complete → set-aside` as a
terminal transition. This lane split them. **Execution disposition** — how the
attempt itself terminated — is terminal, irreversible and exactly one per
attempt: `complete`, `failed` or `abandoned` for a battery, `sealed` or
`discarded` for a package attempt. **Evidence disposition** — whether a
terminated attempt's measurements are the ones a package reports — is a
separate, later row that never touches the terminal row:
`authoritative`, `set-aside`, `superseded`, or the unwritten `unevidenced` that
`failed` and `abandoned` carry permanently. `PROVENANCE.md` §3 states both
machines, §13 the resulting history, §14 every guard and what each closes.

Three questions.

**Is `abandoned` a disposition this record should have at all?** The case for
it: the previous lane shipped an attempt with three green steps and no terminal
row, and its vocabulary could express the ABSENCE of a row but not the fact the
absence stood for, so the audit could only say `unresolved` and a reader could
not tell an abandoned attempt from a lost one. The case against: a fourth word
is a fourth thing to get wrong, and `failed` with a truthful reason would have
carried it. This lane's position is that `failed` asserts the run reached a
decision, that nothing here reached one, and that asserting a decision nothing
made is worse than adding a word. A reviewer may reasonably disagree.

**Is the guard on abandonment keyed on the right thing?** It refuses when any
row of the attempt carries a battery-written `failed` or `discarded` status, or
a result beginning `REFUSED:` or `FAILED:` — and it deliberately does NOT look
at step exit codes, because four gates in the repository under test are
inherited-red by design and return 2, 2, 1 and 2 at both endpoints, so a
battery that ran all of them and finished is `complete`. Reading a non-zero
exit as a failure would make the verb unusable and record a false statement.
Both directions are pinned by tests. Is that the right line, or does it leave
a real refusal reachable through the softer word?

**Is `authoritative → superseded` right on the BATTERY axis, and was this lane
right to add it in the middle of its own run?** The package axis has always had
that succession: an attempt that really did pass its final verification and was
then replaced is superseded, and refusing the succession would leave DELETING
the predecessor's history as the only remedy, which is the V12 defect. This
lane gave the battery axis the same one succession, and it did so because it
needed it. Two cohorts were recorded `authoritative` the moment their batteries
ended; P8 then refused the archive, because those cohorts had executed
`logs/battery.sh` at bytes the package does not ship — the difference being header
comment prose written in that very driver when this lane split the two axes.
The endpoints were measured again, and the ledger, correctly, would not reopen
an evidence disposition, which left no way to record what had happened. The
choice was a new succession or a deleted row. `set-aside` remains terminal and
cannot be superseded, because that would assert a cohort had once been carried
when it never was. Tests pin every edge. **The ask here is threefold, and the
last part is the uncomfortable one.** Is the succession right? Is the rule
recorded beside it right — that `authoritative` may be recorded only after a
seal has proved a cohort's tools are the shipped ones? And is a lane that
extends its own state machine mid-run doing the honest thing by disclosing it
here, or should it have
shipped the defect and left the vocabulary alone for an independent hand to
change?

**And there is a fourth part, which is a plain divergence from the final
instruction rather than a design question, so it is stated as one.** The final
assembly instructions this lane was given fix the evidence-disposition
vocabulary at three words —
`authoritative`, `set-aside`, `unevidenced` — and direct that a completed
assembly later superseded should take a separate evidence `set-aside` record.
**This lane had already recorded cohorts 04 and 07 as `authoritative →
superseded` before that instruction existed**, using a succession the package
evidence axis already carried. Those rows are irreversible by design and
rewriting them is forbidden, so they stand as written.

**Why the lane recorded it that way.** `set-aside` asserts that a cohort's
figures were declined **without ever having been carried**, and that would be
false of 04 and 07: they were recorded `authoritative` when their batteries
ended, they were carried, and they were replaced only when P8 refused the
archive because what ran was not what shipped. Saying `set-aside` of them would
leave a record that cannot tell "this was carried and then replaced" from "this
was never carried at all" — and deleting or flattening a superseded
predecessor's history is the V12 defect this sequence exists to correct, not the
cure for it. The package evidence axis already had exactly this succession for
exactly this reason; the battery axis gained the same one and no other.

**The effect is identical either way.** Under `superseded` and under
`set-aside` alike, **neither cohort is an authoritative source of any V16
figure**, and none of this package's figures derives from either. The
disagreement is about which word truthfully records how they stopped being
carried, not about what they support.

**So the question, put to the reviewer rather than argued at them: is
`superseded` right here, or should the vocabulary have been held to the three
words those instructions name, with the carried-then-replaced distinction
carried in a `set-aside` row's reason text instead?** This lane's answer is
the first and its reasoning is above, but it is a lane judging its own state machine mid-run, which is the
least safe kind of judgment to leave unreviewed. `PROVENANCE.md` §13 states the
same divergence in full beside the ledger rows it concerns.

### 6. A reconciliation that upholds the previous review's observation and refutes its diagnosis

This is the one place where this package disagrees with the review it answers,
so it is put to the reviewer explicitly rather than settled in a footnote.

**The measures, named apart before any figure is quoted.** Four quantities carry
this reconciliation and none of them is interchangeable with another:
`divergent_rows`, the captured rows the replay marked `DIFF`;
`distinct_divergent_identities`, the distinct command strings among those rows;
`volatile_rows`, lines declared volatile in a static source table and masked
before comparison, which are never `DIFF` rows; and `total_differing_rows`, the
sum of the first and third and a count of nothing. **The authoritative V16
figures are the COLD cohorts under ordinals 15 and 16, which agree exactly:**
30 `divergent_rows` over 28 `distinct_divergent_identities`, plus 2 `volatile_rows`, for 32 `total_differing_rows` at each endpoint.
**The V15 figures below are HISTORICAL, inferred from shipped V15 warm evidence,
and are not a V16 replay:**
28 `divergent_rows` over 27 `distinct_divergent_identities`, plus 2 `volatile_rows`, for 30 `total_differing_rows`.
`logs/divergence-reconciliation.json` is the derivation
and carries all of it under `figures`, `authoritative_basis`,
`v16_endpoints_equal` and the two set-difference fields.

**What is upheld.** V15's durable prose claimed a bare thirty, naming no measure
and no build state, and V15's own
shipped transcripts report twenty-eight `DIFF` rows over twenty-seven distinct
commands. No artifact in that package supported the durable figure. That finding
stands entirely and this lane does not soften it.

**What is refuted.** The review's account of the gap set twenty-eight of what it
called examples beside two separately declared volatile lines, against a durable
thirty — which reads as a decomposition, and it cannot be one. Its sentence is
quoted verbatim, once, in `PROVENANCE.md` §16, in order to be refused rather
than paraphrased into agreement; the word it turns on names neither
`divergent_rows` nor `distinct_divergent_identities`. The volatile figure is a
static constant over a two-entry module-level table; it counts declared LINES
over the source tree, both of its captures are masked before comparison, and in
all four transcripts they appear as `ok` and `absent` and never as `DIFF` rows.
They were never in the set they are supposed to be taken out of. The equality is
an arithmetic coincidence.

**What the cause actually is, and how it was established.** Build state, and
therefore a MEASUREMENT-SURFACE difference rather than a V16 parent/head
behaviour delta. `build/example-ordinary` is written by a later capture in the
same target and never cleaned. The tree is provably not the variable: V15's head
commit IS V16's parent commit, that one commit reports 28 `divergent_rows` warm
and 30 `divergent_rows` cold, and
both the tool and the replay script are byte-identical blobs at every commit
involved. The transition was reproduced live and is reversible by exactly one
filesystem condition. **The two authoritative V16 cold cohorts agree exactly on
all four measures**, so nothing in this comparison reports a behaviour change
between the endpoints this package ships. And the identity set-difference runs
one way only: **one**
additional command identity, contributing **two** captured divergent rows
because the
same command is captured twice — so `distinct_divergent_identities` goes
twenty-seven to twenty-eight while `divergent_rows` goes twenty-eight to thirty,
and any phrasing about "two additional identities" is itself
the row-versus-name conflation. `logs/divergence-reconciliation.json` is the
derivation; `PROVENANCE.md` §16 is the account. **The superseded cohorts under
ordinals 04 and 07 reproduced the same cold counts; that is recorded as a
CONTROL on the figure and never as a source of it**, and no V16 figure in this
package derives from either.

**The ask is a verdict on the disagreement, not agreement with it.** Is the
refutation of the diagnosis correct? Is the build-state cause established to
the standard this package requires of its other claims? And is a lane that
corrects the review it answers doing the right thing by saying so in the
package, rather than quietly shipping a figure that happens to be right for a
reason nobody wrote down?

## Optional feedback

- **The page ends larger than V15 left it, and this is the first version in
  this sequence that cannot say otherwise.** `src/web/browser/catena/catena.js`
  moves from 12,958 to 12,965 gzipped whole against a 13,000 ceiling, leaving
  35 bytes of headroom; stripped it moves from 7,724 to 7,835 against 8,800.
  The three sentences the page may say about a body, the presentation decision
  itself and the page's paragraph on the one point-of-use acknowledgement
  channel were relocated into the uncapped model, and that paid for most of the
  change and not all of it. No ceiling was raised, and no load-bearing comment
  was trimmed to buy a smaller number. Whether that is the right trade, and
  whether 35 bytes is a ceiling anyone can work under, is a judgment this lane
  made under a budget it does not own. **Two fixes an adversarial review
  identified were costed and deliberately not made, because each costs more
  than the headroom holds**: testing the cache hit with `fragmentTexts.has(path)`
  rather than for truthiness (37 gzipped bytes against 35 available; safe on
  today's schema, since a sealed value is always a non-null object, and a
  latent trap only if the schema ever admits a falsy sealed value), and writing
  the words before the class so a throw before the body lands leaves the page
  wholly untouched (about 60 gzipped bytes, because the reorder breaks a
  repeated pattern gzip was compressing, and no such throw is reachable). Both
  are disclosed, costed and deferred rather than paid for by raising a ceiling
  or trimming load-bearing prose. Whether that is the right disposition is a
  judgment worth a reviewer's disagreement.
- **A row that resolves no address now mints a transport owner where V15 minted
  none.** `M.rowTransport(row)` is consulted unconditionally in
  `fragmentText`, because "this fragment carries no text file" is a body
  application like any other and must be owned by a completion the model sealed
  rather than applied on a bare row-membership test. The consequence is one
  more `transport` witness per such row in the request journal. It is disclosed
  here rather than left for a reviewer to find as a count that moved.
- **The observation accounting is corrected, and it is larger than V15's.**
  Six kinds are counted apart, and the `getPrototypeOf` observation that key
  enumeration causes is now among them; V15 measured it and did not disclose
  it, while calling its list exhaustive. `Object.hasOwn` is an own-property
  test performed through `[[GetOwnProperty]]`, which is why it lands in the
  descriptor count and why the per-key figure is three; V15's prose called that
  bucket `has` and covered neither question cleanly. Confirmation that the
  corrected vocabulary is right, or a correction to it, is welcome.
- **Preserved V15 behaviour is recorded as regression, not as closure.** The
  row-transport owner model, the A-held/B-independent vector, the wrapper
  closure, the failure isolation, the accessor cases and the inherited V14
  closures all still pass and none of them is counted among this lane's
  closures. If any of them reads as a claimed closure anywhere in this package,
  that is a defect in the package and worth naming.
- **A refused body application now leaves no journal entry at all.** V15's
  `bodyAsked` called `witnessed` unconditionally, so every attempt including
  every refusal left a `body` row. V16 records only confirmed applications, so
  the journal no longer positively records that a stale or cross-owner
  application was turned away. The negative cases are still proved — by the
  boundary returning `false` in a committed direct assertion and by the
  rendered page being unchanged — but the page-level journal row V15 had is
  gone. It is a deliberate consequence of taking the record AFTER the write,
  which is what the review required, and it is disclosed rather than left to be
  found. Whether that trade is acceptable is a fair question to put back to us.
- **The completion envelope's two halves cannot be supplied BY THE DATA**, and
  no stronger claim is made. In-realm code holding a recorder installed through
  the exported `chapterWitness` receives the page's actual row objects, and from
  a real row both `M.rowTransport` and `M.textPayload` will mint valid halves in
  five lines. This is not a security boundary against code already in the realm,
  which can write the DOM directly; if any sentence in this package reads as an
  unqualified impossibility, that is a defect worth naming.
- **This lane retired a ledger, and the disclosure is deliberately
  unflattering.** The V15 review's ordinal finding was that allocation had been
  file-scoped, so moving a ledger aside restarted it. This lane also retired a
  ledger, once, and says so rather than presenting itself as a lane that kept
  one file. What is different is the guarantee behind it: the retirement verb
  writes the predecessor's spent ordinals into the successor's opening lane row
  and the allocator unions them into the spent set, so the second ledger opened
  at ordinal 04 and `reused_ordinal_count` is derived across both files rather
  than asserted about either. The retired file is retained whole, no row in
  either was rewritten or deleted, and `PROVENANCE.md` §15 names both files with
  their identities while `logs/attempt-history.json` derives the history across
  the pair. Whether a retirement disclosed on those terms is
  an acceptable disposition, or whether a lane should never move a ledger at
  all, is a fair question to put back to us.
- **A defect in another owner's tool was found, argued through, and
  deliberately not fixed.** `tools/mass-ordinary` has no `PREPARE` entry, so its
  `check` captures are compared against a directory a later capture in the same
  target writes; `typeset-bible` already carries exactly such an entry, with a
  comment describing the identical problem. Adding one would remove the whole
  ambiguity this lane spent a reconciliation on. It was not added, because a
  lane answering a review about publication atomicity does not quietly change an
  unrelated tool's example fixtures. `LIMITATIONS.md` discloses it and
  `UNRESOLVED-BLOCKERS.md` records the owner. Whether that restraint is right,
  or whether the fix should simply have been made, is worth a verdict.
- **The unbudgeted model grew again**, to 44,247 gzipped whole and 10,344
  stripped, against no ceiling in either column. Whether the model and the
  combined route payload need a governed ceiling remains the budget owner's
  question, and it has now been carried forward by more lanes than have
  answered it.
