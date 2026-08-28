# Catena E1 — V16 publication atomicity and completion-envelope handoff

This package is the evidence for one bounded correction lane and nothing else.
It records no acceptance, marks no separately owned prerequisite complete, and
does not review its own work.

Every figure in this file is derived by `logs/derive-claims.py` at seal time and
rendered in `DERIVED-CLAIMS.md`; where one appears here it is repeated from
there, and `claims.json` is the machine-readable original. Where a figure came
from a command, `checks.txt` names the command, the working directory it ran
in, the argument vector a shell was handed and the log.

## 1. Task and intended outcome

Answer the V15 independent review — **CHANGES REQUIRED** at exact head
`b9202882badbbbc364f1dd3d9057d2710ee47552`, recorded at review commit
`67247ecc39a6e5f6224c64ca3ab1af163ee023b1` on
`review/catena-wave-1-e1-corrections-v15-independent` — with exactly its stated
next action and nothing else. That review answered on two axes and recorded
both: **SEMANTIC CHANGES REQUIRED** on transport and final authority, and
**EVIDENCE CHANGES REQUIRED** on the package.

The review passed a great deal, and this lane does not reopen any of it: the
row-transport owner model, which accepts only an actual projected row, returns
one stable frozen owner per row, retains the authoritative projection, mints
distinct owners for distinct same-path rows and refuses copies, literals,
scalars and `null`; the decisive A-held/B-independent behaviour with its
thirty-six-field terminal vector; the wrapper-created-authority closure and the
per-name substitute for a spine the page cannot read; one owner's failure
suppressing no other owner's request, and owner-local retry; the hostile nested
`edition` and `edition_published` accessor cases; the thirteen throwing
mutations and the downstream rerender that reconsumes the projection; and the
inherited V14 `unfetched`, one-read inventory, structural member, raw-reread,
rights and provenance, refusal, carried-path, spine-prefix and prewarm
closures. All of it is replayed here and all of it still passes. **Those are
REGRESSIONS, and this package counts them apart from its closures.** The V15
review criticised exactly that conflation, and separately criticised counting a
byte-identity hash pin and a consumer-roster audit as semantic closures. Pins,
audits, preserved behaviour and new closures are four categories here, and they
are never summed into one headline.

The review found **two decisive semantic defects and a third that follows from
the first**:

> `fragmentTexts.set(path, asked)` runs inside the fulfilment handler of the
> promise returned by `.then()`, before that handler returns, so a still-pending
> object is briefly reachable by path; publication also precedes the freeze.

> `M.bodyAsked(row, content)` authorizes any content whenever `row` occurs in
> `rowOwners`, so an actual B row accepts arbitrary A content at the boundary;
> and the body journal is recorded before the DOM write.

A promise returned by `then` cannot settle until its handler returns. The entry
published under that path was therefore `Promise { <pending> }` at the instant
it became reachable, and fulfilled only in the following microtask. Ordinary
event-loop work cannot interleave there, which is why the V15 behavioural tests
were green; a synchronous reentrant operation retrieves it. The value that
eventually stood at that path was the raw parsed JSON object, shallow-frozen at
the top level, carrying a mutable prototype — and `M.textPayload` then read its
fields at render time by ordinary prototype-sensitive lookup, so a frozen empty
object could turn from unreadable to readable between one reader and the next
by prototype mutation alone, and an own accessor answering differently on a
second read decided the page.

Beside them the review found: a provenance-specific committed `===` assertion
missing from an equality matrix that claimed the whole roster; observation
prose that omitted the `getPrototypeOf` observation its own enumeration causes
and used `has` and own-property test interchangeably; and the evidence package
materially defective in the respects `PROVENANCE.md` enumerates — a command
record that cannot be re-run as written, a classifier that accepts prose by
prefix, tool accounting with manufactured rows and two unreconciled count sets,
an incomplete predecessor history, a hand-typed example figure that appears in
no log, a compare gate whose diagnostics collapse thousands of rows onto a
handful of names, and a completeness verdict taken before the package's last
two phases had run.

The intended outcome: normalize a fragment payload once, at settlement, into an
owner-independent immutable scalar record; publish that finished value and never
the initiating owner's pending promise; carry a per-caller completion envelope
holding the exact row-transport owner to the body sink and require that owner at
application; record the body only after the write is confirmed; add the missing
provenance identity assertion and correct the observation accounting; and
rebuild the evidence with executable commands, unambiguous repository variables,
a mechanically derived tool-execution record, the complete predecessor and
current attempt histories, the corrected example figures, granular gate
diagnostics and a completeness check taken at the true final state — then stop,
for a fresh independent review.

**Not** in scope and not attempted: entering another E1 blocker, integration,
merge, deployment, re-signing any release-owned record, cutover, or any of the
broader blockers in `UNRESOLVED-BLOCKERS.md`.

## 2. Branch

`impl/catena-wave-1-e1-corrections-v16`

Not a detached HEAD. Not merged with `origin/main`, which is
`2778285849f2973ea89d1cfd5b2751ed4ae58e54`.

The immutable copy of this package is archived on
`evidence/catena-e1-corrections-v16-handoff`; that branch carries the package
and nothing else.

## 3. Current commit and base commit

| | |
| --- | --- |
| V16 head | `cc1f2fb8625f044558c26edd358b99cd7dcc7646` |
| parent, the exact candidate that review answered | `b9202882badbbbc364f1dd3d9057d2710ee47552` |
| review addressed | `67247ecc39a6e5f6224c64ca3ab1af163ee023b1` on `review/catena-wave-1-e1-corrections-v15-independent` |
| V15 evidence, carrying the reviewed package | `db5f651e4eb2d10a15d1a594a4286ac7048f612c` on `evidence/catena-e1-corrections-v15-handoff` |
| V15 package this lane supersedes | `20260826T195656Z-catena-e1-corrections-v15`, 1,400,092 bytes, ZIP SHA-256 `711b598ab43543113ccb924234fc8ef4ddb76370ff74d24c72a549da574204ac`; its own archive is the authority on how many members it holds |
| the production commit | `e34ab2b05`, which publishes only a finished value and carries its owner to the body |
| the proof commit | `208f086b5`, which proves the interval closed, the owner carried and the record earned |
| the durable-records commit | `251900b14`, the lane record and the in-place correction of what this lane first corrected wrongly |
| the disclosure commit, which is also the head | `cc1f2fb86`, removing from the lane record the figures a record cannot truthfully state about itself |
| the authoritative package attempt | **not typed here, because this file was frozen before it existed.** Its id and ordinal are allocated by the lane ledger when the assembly attempt opens, and `logs/attempts.json` carries both. What makes it authoritative is not a sentence in any member: it is the post-verification authority record beside the archive, written only after the read-only final verification passed and bound to the archive's recomputed size and digest |

The parent is an ancestor of the head, and the length of the range is derived
rather than asserted — see `claims.json` under `identity` and `commits.txt`.

**The V15 package is not modified by this lane.** Its ledger slice is published
evidence on the V15 evidence branch, and appending a supersession row to it
would rewrite an artifact a reviewer may already hold. The supersession is
recorded where cross-lane dispositions have always been recorded: the durable
records. Each lane keeps its own ledger; this lane's opened fresh for `V16`,
with one ordinal allocation per attempt and one terminal row per attempt.
`PROVENANCE.md` records what this lane's ledger history actually is, including
the replacement it made and why that replacement spent no ordinal twice.

**Which cohorts this package's figures come from, and which carry nothing.**
Every head-side figure here derives from the cold shipping-head battery of
ordinal 16, and every parent-side figure from the cold parent battery of
ordinal 15. Those are the cohorts whose evidence disposition is
`authoritative`; the cold cohorts of ordinals 04 and 07 held that disposition
first and are `superseded`, and `CLAIM-CLOSURE.md` §10a states the cause and the
remedy. Both statements are derived rather than asserted: the machine-readable
derivation is `logs/attempt-history.json`, taken across both of this lane's
ledgers because the first was retired and a successor opened in its place, and
the live ledger is a sibling. The battery of ordinal 05 ran to completion and measured a
V16 head that a later commit superseded, so its evidence disposition is
`set-aside` and no final validation figure in this package derives from it. The
battery of ordinal 06 was stopped from outside itself after three green steps;
its execution disposition is terminally `abandoned`, it **contributes no
validation result to any authoritative claim in this package**, and it is
retained for history and audit only, outside the archive, with a digest listing
of every file it wrote. Neither of those cohorts is a defect in the record; a
lane that measured a superseded head, or that had a battery killed under it,
and then said neither, is the defect.

## 4. Uncommitted changes

None. The working tree was clean at the head when this package was assembled,
and `claims.json` carries `identity.worktree_clean_at_head` derived from
`git status --porcelain` rather than asserted here. It also carries
`workspace_mode`, `worktree` and `git_dir_kind`: this lane ran in a fresh
standalone clone with a real `.git` directory and no worktree, and all three
values are symbolic or boolean, so none of them is a path the sanitizer would
have to rewrite after the freeze.

The batteries record tree state **per command**, before and after, so a step
that dirtied the tree is recorded dirty on its own row, and a battery refuses to
start on a tree that is not clean. See `checks.txt`.

## 5. Focused files changed

Seven files. **Two of them are production.** The page's own
change is about fifty lines added and about as many replaced; the model's is
larger, because the model is where the correction lives and where the page's
prose went.

| file | what it is |
| --- | --- |
| `src/web/browser/catena/catena.js` | the publication itself: the finalized value is computed to completion before `fragmentTexts.set(path, content)` runs, so nothing unresolved is ever published; the completion envelope is what travels to the body sink; a finished cached value is rebound to a later owner through that owner's own completion; the write is attempted inside a `try`, read back from the node, and only then recorded |
| `src/web/browser/catena/catena-model.js` | `textPayload` as the finalizer, `sealText`, `TEXT_SCHEMA` and `NO_TEXT`; the completion envelope `textCompleted`/`textFailed` and its `WeakSet`; `bodyAsked` on three exact-object comparisons; the new `bodyApplied`; `bodySaying` and `failureSaid`; and the page prose that moved here because the page has a ceiling and this file has none |
| `tools/tests/test_catena_wave_1.py` | the publication probe that records what a path lookup returns at every instant it could return anything, the write that is made to fail, the six-kind observation vocabulary, and the V16 methods with their scenarios |
| `PROJECT-WORK.md` | the V16 lane record, and the in-place correction of the V15 lane's hand-typed example figure |
| `guidance/corpus-browser-roadmap.md` | the V16 section, the seventeenth-candidate E1 row and the dated ledger row |
| `guidance/corpus-browser-master-plan.md` | the E1 row moves from the V14 disposition to the V15 one |
| `promised-deliverables.toml` | the V16 deliverable with its criteria |

`src/web/data/` has **zero** changes: every adversarial fixture lives in the
test file and is served by the replay harness's own stub network.
`src/web/browser/catena/catena.css` and `src/web/browser/catena/index.html` are
byte-identical at both endpoints — SHA-256
`733e84909e0e8049629187352d3800be320e469da7be200e860378bcc28851c5` and
`7779d1f19ca175fd315cd7164f5347cc3c08d68b20b3b68a9219429b02bb8fa8`. No release
binding, common gate, shared shell, Liturgy, PDF or CLI path is touched, no
ceiling is raised, and `changed-files.txt` is derived from
`git diff --name-status` rather than typed here.

## 6. Startup commands and route state

All paths are repository-relative. Run from the checkout root.

The focused suite for this route is
`python3 -m unittest discover -s tools/tests -p 'test_catena*.py'`, and this
lane's own classes are
`python3 -m unittest discover -s tools/tests -p 'test_catena_wave_1.py' -k V16`.
The generator-side structural check is `python3 scripts/_catena.py check` and
the promise ledger is `tools/tpt check-promised-deliverables`.

To see the page itself, build the public artifact with `make public-site` and
serve it with `python3 -m http.server --directory build/public-alpha/site`.
Then open the route with its required state:
`/catena/#book=Gen&chapter=1&bible=douay-rheims`. The real-browser gate over
that artifact is `node tools/tests/corpus_browser_gate.mjs`; set
`TRIPTYCH_CHROME` to the browser binary unless google-chrome-stable is the one
present.

Everything, including the inherited red targets, is `make -k check` and
`python3 -m unittest discover -s tools/tests`.

The route under review is the Catena Omnia page. Its route state is carried in
the URL hash. The states this lane closes are reached by opening a chapter whose
fragment resolves a text address and then observing what a lookup of that
address returns at each instant of the transport, and by stepping to a second
chapter that carries the same address after the first has settled.

The production corpus is entirely present-valid; no real server publishes a
document whose prototype is mutated between two reads, and no real reader
performs a synchronous reentrant lookup inside a fulfilment handler. So **the
states this lane closes are not reachable on any real route.** They are
properties of when a value becomes reachable and of what it is made of, not of
any JSON document, and this lane's cases are reachable exactly one way: through
the replay harness, which drives the real page under Node against a stub DOM and
a stub network whose answers can be parked, released and mutated one ask at a
time. Every assertion is taken at that page's own sinks — the rendered body
text, the row count, the refusal, the tally, the spoken status line, the request
journal, the ownership journal, the body journal and the route.

## 7. Implementation summary

**`src/web/browser/catena/catena-model.js`.** `M.textPayload` is no longer a
render-time projection; it is the FINALIZER, called at settlement, and what it
returns is the value the page renders. Every field is taken by own descriptor
through `ownData`, so nothing inherited is visible and no getter is ever
invoked. Every field is a scalar by construction, because `sealText` admits a
boolean or `sound()`'s string and nothing else, so there is no nested structure
in the result to mutate afterwards. The record is given a null prototype, so it
carries no inherited authority of its own; it is frozen; and its key set is
fixed and published as `M.TEXT_SCHEMA` — `present`, `unreadable`, `text`,
`basis`, `date_basis`, `acknowledgement`, `acknowledgement_broken`. `M.NO_TEXT`
is the finished value for a row that resolves no address at all, a finalized
value like any other rather than a sentinel the page recognizes by identity.

A settled transport is then sealed into one frozen envelope:

```js
if (bag(owner) !== owner || rowTransports.get(owner.row) !== owner) return null;
if (!failed && !contents.has(content)) return null;
```

`M.textCompleted(owner, content)` and `M.textFailed(owner, error)` mint an
envelope only against an owner this model is currently holding for that owner's
own row, and only around content this model itself finalized, so neither half
can be supplied **by the data**. Membership is held in a `WeakSet`, so a literal of
the same shape is not one of these. A forged owner, a scalar owner, `null` and a
null-prototype look-alike each yield `null`.

**That is the exact strength of the claim.** A hostile chapter, source record or
fragment file cannot mint either half, because neither is derivable from
anything the data carries — which is the defect the review found, and it is
closed. In-realm code is a different matter: a recorder installed through the
exported `chapterWitness` receives the page's actual row objects, and from a
real row both `M.rowTransport` and `M.textPayload` will mint valid halves in
five lines. This is therefore **not a security boundary against code already
running in the realm** — such code can write the DOM directly and needs no
envelope — and the unqualified claim that the halves cannot be supplied from
outside is refutable by a five-line probe and is not made here.

`M.bodyAsked(row, completed)` now requires three exact-object comparisons — the
completion is one this model sealed; its owner is the transport held for that
very row; the owner's projection is the projection that made the row — with no
path, no id and no string anywhere in the test. `M.bodyApplied(row, completed,
wrote)` is new and records the body AFTER the write is confirmed, binding the
owner object, the row, the projection, the address, the finalized content value
itself, whether the completion was a failure, and the post-write success state.

**`src/web/browser/catena/catena.js`.** The page publishes the FINAL VALUE and
never a promise:

```js
const content = M.textPayload(file);
if (!fragmentTexts.has(path)) fragmentTexts.set(path, content);
return M.textCompleted(owner, content);
```

`M.textPayload(file)` runs to completion before `fragmentTexts.set` is reached,
so there is no instant at which a path lookup returns unresolved or partial
work, reentrantly or otherwise. `if (!fragmentTexts.has(path))` is the
first-settled-answer rule, unchanged. A finished value already in the cache is
rebound to a later owner through that owner's own completion —
`Promise.resolve(M.textCompleted(owner, done))` — which is what keeps the cached
value owner-independent and keeps A's owner from ever crossing into B. The
envelope never becomes the cache value.

At the sink, containment is checked first, then the row's own transport, and the
write is attempted, read back and only then recorded:

```js
const wrote = (completed, write) => {
  let said = null;
  try { said = write(); } catch (problem) { said = null; }
  if (said === text.textContent) M.bodyApplied(fragment, completed, true);
};
```

A write that throws and a write that silently does not take both leave no
applied-body entry. **The retry flag is deliberately NOT reset in the `catch`,
and that is a decision with a reason rather than an omission.** An earlier
revision did reset it there. An adversarial review found that the reset created
an incoherent arm: a throw AFTER the body had already landed would leave the
body on the page, leave no journal entry, and then invite a second full
application out of the memoised completion — a page written twice and
journalled never. The reset was removed. `asked = false` occurs only in the
transport-failure arm, where it always did, because **a network failure is
retryable and a failed DOM write is not**. Both write-failure modes therefore
end identically: no entry, no false success, and no second attempt. The
consequence disclosed beside the decision is that a write which silently does
not take leaves the fragment showing its previous state with no way for the
reader to retry; no such failure is reachable in a real DOM, and it is
disclosed because the arm exists. The suite asserts the shipped behaviour in a
method that passes at BOTH endpoints, counted as a truthful-state assertion
rather than as a discriminator.

**The second half of this closure is containment, and it is the sharper
discriminator.** A throwing body write at the V15 parent escapes as an
unhandled rejection and kills the entire replay — `Ran 35 tests, 98 errors`,
every replay class down. V16's sink contains it and the page continues. The
harness proves this without weakening the probe: an `unhandledRejection`
handler RECORDS escapes into a journal rather than letting them be fatal, and a
global method asserts that journal empty across the whole plan. It is empty at
the candidate; at the parent it holds exactly one entry, for the throwing-write
scenario. This is recorded as the second half of closure 8 rather than as an
eleventh closure, because the ten-closure enumeration is fixed across the
directions, the durable records and this package, and renumbering would
desynchronise them.

**`tools/tests/test_catena_wave_1.py`** adds the two seams the review's findings
cannot be reached without, and neither is a seam in the page. `Map.prototype` is
wrapped once for every scenario and answers exactly as it did — the real method
runs first and its answer is returned — recording only a string key carrying the
probed path, only while a scenario has asked for a probe, so the page's chapter
and paragraph caches and every object-keyed map in either realm are untouched.
What it records is what a lookup of the path returns AT THE INSTANT of each
event: absent, an unresolved promise, a settling promise, a partially normalized
record, or the finalized immutable value. The second seam drops exactly one
`textContent` write carrying a named marker, on one node in one scenario, and
does not throw, because a throw inside the page's own settle handler would
become an unhandled rejection and take the replay down — the probe would be
deciding the result rather than reporting it. The observation vocabulary is
rebuilt into six kinds named for the operations they are: `value_gets`,
`getter_invocations`, `has_operator`, `own_descriptor_reads`, `enumerations` and
`prototype_observations`.

The argument is in `CLAIM-CLOSURE.md`; the figures are in `checks.txt`.

## 8. Known limitations

`LIMITATIONS.md` states them, each in a section of its own. In short: the page
ends slightly larger than V15 left it and its whole-file headroom is now too
small for the next correction of any size; more of the page's own prose has
moved into the unbudgeted model, which grew again and still carries no ceiling;
the post-write confirmation reads back the body text alone and not the
acknowledgement block or the apparatus paragraphs beside it; a projected row
that resolves no address now mints a transport owner where V15 minted none, so
the request journal carries one more row for such rows; the reentrant and
mutation vectors are reachable only through the replay harness and are not
browser-engine evidence; four stale release bindings remain unsigned;
screenshots are omitted; the browser gate is red at both endpoints; `make -k
check` is red at both endpoints; the battery of ordinal 06 was externally
interrupted, is terminally `abandoned` and contributes no validation result to
any authoritative claim here; the battery of ordinal 05 completed and its
evidence is set aside, so no final figure derives from it; every cohort this
lane did not carry is retained outside this package rather than deleted, and no
authoritative claim rests on any of them;
`tools/mass-ordinary` lacks the `PREPARE` entry that would make its `check`
captures independent of build state, which is another owner's defect and is
disclosed rather than fixed; the warm build state of the predecessor package's
own example transcripts is an inference from those transcripts rather than a
recorded fact, because that battery recorded no build state at all; and every
broader E1 blocker stays open.

## 9. Unresolved decisions

Three things this lane decided under judgment rather than under proof, and each
of them is put to the reviewer rather than settled here. Whether an envelope
minted per caller is the right carrier for ownership, or whether ownership
belongs in something the page does not hold at all. Whether a body journal that
appends nothing for an unconfirmed write is the correct disposition, or whether
an explicit not-applied record would serve a reader better. And whether the
observation seam belongs in shipped browser bytes at all, now that a third lane
in a row has added to it. `REVIEW_REQUEST.md` carries these as blocking
questions with the optional notes beside them.

It also puts questions about the RECORD rather than the code, and they are
decisions of the same kind. Whether an attempt's history is rightly modelled on
two independent axes — how the run ended, and what became of its measurements —
with `abandoned` as a terminal execution disposition for a run something outside
it stopped. And whether this lane is right to uphold the previous review's
observation about the example figure while refuting its diagnosis, having
established a different cause mechanically. That disagreement is put to the
reviewer inside the package rather than settled inside it.

`UNRESOLVED-BLOCKERS.md` lists every finding left open with its owner. None was
touched by this lane.

## 10. Artifact inventory

**In the package.** The hand-authored argument: `HANDOFF.md` (this file),
`REVIEW_REQUEST.md`, `CLAIM-CLOSURE.md`, `LIMITATIONS.md`,
`UNRESOLVED-BLOCKERS.md`, `PRIVACY-AUDIT.md`, `PROVENANCE.md` and
`EVIDENCE-INDEX.md`. The machine-derived record: `claims.json`,
`DERIVED-CLAIMS.md`, `checks.txt`, `commits.txt`, `changed-files.txt`,
`changes.patch`, `commands.json` and `MANIFEST.sha256`. Under `logs/`:
`logs/LOG-INDEX.md`, `logs/attempts.json`, `logs/attempt-history.json`,
`logs/divergence-reconciliation.json`, `logs/named-commits.json`,
`logs/order-head.txt`, `logs/order-parent.txt`, `logs/catena_command.py`,
`logs/replay-command.py`, the per-attempt transcript directories, and the
shipped copies of every tool this pipeline runs. Every one of those names is
written out rather than described, because a member a document refers to by
kind is a member the completeness checker cannot bind to a file.

**Some of those members are new in V16** and are named again here so a reviewer
looks for them rather than infers them. `commands.json` is the machine-readable
command record from which `checks.txt` is derived. `logs/catena_command.py` is
the command-classification module the derivation runs.
`logs/replay-command.py` is the parent-replay driver whose recorded invocation
carries one variable per location instead of overloading `$REPO`.
`logs/attempt-history.json` is the mechanical derivation of this lane's attempt
history in full — every attempt with its execution disposition, its evidence
disposition and its reason, the derived counts, and the invariants asserted
over them — produced by `checks.py --history-table --assert-invariants` over
the ledgers rather than transcribed from any of them. And
`logs/divergence-reconciliation.json` is the mechanical reconciliation of the
example-replay figure across this package's own transcripts and the predecessor
package's, including the identity set-difference that establishes what actually
changed and the live reproduction that establishes why. Member, log and tool
counts move accordingly, and this file states none of them: they are derived
into `claims.json`, rendered in `DERIVED-CLAIMS.md`, and `MANIFEST.sha256` is
the roster a reviewer counts.

**"In full" above means across BOTH of this lane's ledgers, because this lane's
history is not inside a single file, and a reader of this file alone should not
have to infer that.** This lane retired its first ledger and opened a successor
in its place; no row in either was rewritten or deleted and each is append-only
within itself, but neither file is the history on its own, so the derivation
reads the pair. The successor's opening `lane` row carries the retired file's
digest, byte count, row count and the ordinals it spent, no ordinal was reissued
across the move, and `PROVENANCE.md` §15 records both files with their
identities and the reason the first was set down.

**Beside the package**, and therefore *not* members of the manifest, because
each is written after the seal the manifest describes.

`20260827T230425Z-catena-e1-corrections-v16` is the archive basename — the UTC stamp the assembling attempt is
allocated, joined to `catena-e1-corrections-v16` — and every sibling below is
named as its full filename against that basename, ending included, so that none
of them is described by suffix alone. **A basename is knowable before the
archive exists, because it is a property of the attempt rather than of the
bytes: it is fixed when the attempt opens, on the same terms as the attempt id,
which is why a member frozen at the manifest can refer to either.**

**The archive's byte size, its member count and its SHA-256 are a different
kind of thing, and none of the three is written anywhere in this package.**
They are not properties of an attempt; they are properties of the finished
archive, and these bytes are inside it. Writing any of them here would change
the thing being written about. That is the structural reason V15 gave correctly
for its own digest, and it is unchanged: the size and the digest are recomputed
from the archive AFTER the read-only final verification and recorded in the
authority record named below, and the member roster is `MANIFEST.sha256`. Each
of those identities is bound by a record written *after* the bytes it binds,
which is the only order in which such a binding can be true.

- `20260827T230425Z-catena-e1-corrections-v16.zip` — the archive;
- `20260827T230425Z-catena-e1-corrections-v16.zip.sha256` — its digest and byte size;
- `20260827T230425Z-catena-e1-corrections-v16.assemble.log` — the outer invocation log;
- `20260827T230425Z-catena-e1-corrections-v16.verify-final.log` — the read-only final-verification transcript;
- `20260827T230425Z-catena-e1-corrections-v16.authority.json` — the post-verification final authority record;
- `20260827T230425Z-catena-e1-corrections-v16.executed-tools.json` — the contemporaneous executed-tool digests;
- `20260827T230425Z-catena-e1-corrections-v16.tool-bytes.json` — the tool-byte comparison table;
- `20260827T230425Z-catena-e1-corrections-v16.attempts.jsonl` — this lane's attempt and battery history;
- `20260827T230425Z-catena-e1-corrections-v16.authority-coherence.log` — the pre-publication authority gate's transcript;
- `20260827T230425Z-catena-e1-corrections-v16.handoff-inventory.log` — this inventory's own transcript;
- `20260827T230425Z-catena-e1-corrections-v16.outer-sanitize.log` — the outer sanitization pass's transcript;
- `20260827T230425Z-catena-e1-corrections-v16.outer-scan.log` — the re-scan that clears each rewritten sibling.

**That list is not the authority on what is beside the package, and it is not
supposed to be.** `logs/handoff-inventory.py` discovers every artifact sharing this
package's basename and stats it, including its own transcript, rather than
taking a declared list from arguments — which is how a predecessor package came
to omit its own inventory log while scoring full marks. A sibling this list did
not anticipate is therefore found and reported, not missed; what this list owes
the reviewer is the names of the ones the pipeline is contracted to write, and
the reason each of them cannot be a member.

**And the same structural limit reaches one step further, to the evidence
commit.** The SHA of the commit that publishes this package cannot be written
inside the package, because the package's bytes are what that commit commits
and naming the commit changes them. There is no clever ordering that closes it
and none is attempted. The model that is actually true is stated instead: the
sealed package binds every identity that exists before the evidence commit —
the head, the parent, the review, the archive by digest, the manifest, the
verification and the rehash — the evidence commit then commits exactly those
bytes, and the pushed evidence branch is what externally identifies the
resulting commit. A reviewer who expects to find the evidence commit bound
inside these bytes should find this paragraph where the binding would have
been. **No self-binding SHA is manufactured anywhere in this package**, and a
package that carried one would be asserting a fact about bytes it could not
have seen.

**The last two are named by filename here, and V15's were not.** V15 described
them by suffix, because that pass runs after the inventory and the authority
gate so that it can rewrite and re-scan their transcripts too, and its own
records therefore did not exist at the moment the inventory ran. The V15 review
found that the shipped completeness checker, re-run at the true final state,
reports both of them unnamed and answers `INCOMPLETE`. So the names are
written out, and the completeness verdict this package ships is the one taken
after the outer sanitization and its re-scan have finished — the final state,
not a state the package then leaves behind.

**Conditional artifact classes, and why any is omitted.** Screenshots are
**omitted**. This lane changes no ordinary visible composition:
`src/web/browser/catena/catena.css` and `src/web/browser/catena/index.html` are
byte-identical at both endpoints, and the page's own change is in when a value
becomes reachable, what it is made of and who is allowed to apply it, not in
what the page draws. The visible differences this correction does produce are
reachable only from a mutated payload, a reentrant lookup or a write that does
not take, and each is asserted at its exact DOM sink, by rendered text, row
count, refusal presence, tally string, spoken status line, request journal,
ownership journal, body journal and route. A sources record is **omitted**: this
lane adds no external source, edition, artifact or passage record, and
`src/web/data/` has zero changes. A `logs/` directory is **present**.
