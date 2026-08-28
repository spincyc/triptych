# Evidence index

What each member of this package is, what it supports, and — the column that
matters — what it does **not** prove. A reviewer who reads only this file should
be able to tell which claims rest on evidence and which rest on a lane's word.

Three disciplines are carried forward from earlier rounds because earlier rounds
broke them. An earlier version of this file said the packaged journals carried
ownership rows they did not contain; nothing here claims support a member does
not carry, and where a member's support depends on what a run produced, the
mechanism that produces it is named instead of the outcome. An earlier package
printed a mechanical completeness verdict that tested nothing this file
describes; the verdict is not repeated here, because a map that also grades the
territory is no longer a map. And the previous package's gate comparison was
described by its sound half alone; where a member does one thing well and
another badly, both halves are stated in its row.

**No figure appears in this file.** Every count, size, digest and identity is in
`claims.json` and its rendering `DERIVED-CLAIMS.md`. Where a number would belong
here, the member that carries it is named instead.

This file names itself, and it names every member. `MANIFEST.sha256` covers
every member except itself; the archive digest and byte size live in the sidecar
beside the archive, never inside it.

## The argument

| Member | State | Supports | Does not prove |
| --- | --- | --- | --- |
| `HANDOFF.md` | staged | The ten required contents of the handoff protocol, as content, and the artifact inventory that names every member and every sibling by exact filename — including the two outer records the previous package named only by suffix. | Nothing on its own; every claim in it is carried by a member below. |
| `CLAIM-CLOSURE.md` | staged | The technical argument: what the review found in three parts, what the parent actually does when a payload's prototype is mutated and when a foreign completion reaches a row, the six clauses of the publication-and-completion contract, the ten closures with the three categories they are kept apart from, the measured invariants of the finalized value, the corrected observation accounting, what the shape costs and what proves it. | That the argument is right. It is prose; the vectors are in `changes.patch` and their runs are in the logs. |
| `REVIEW_REQUEST.md` | staged | The blocking questions this lane cannot answer for itself — whether a per-caller envelope is the right carrier, whether an unforgeable seal is worth its opacity, whether a journal that appends nothing for an unconfirmed write is the correct disposition, and whether the rebuilt command record is re-runnable end to end — with the optional notes beside them. | Nothing. It asks; it does not answer. |
| `PROVENANCE.md` | staged | The review links this lane has and the older one it does not; the thirteen evidence closures with their root causes; what makes a recorded command re-runnable; the two state machines; the authority ordering and its direct bindings; the ledger and log-root rules and why a file-scoped ordinal allocator is not a lane-scoped one; the complete predecessor history across all three of the previous lane's ledgers, and the set-aside classification it corrects; the post-seal rows and the member that structurally cannot carry them; which bytes ran and under what phase-labelled schema; the derived workspace provenance; and what is not claimed. | Its own accuracy — the lane ledger is the authority, and where the two could disagree the ledger is right and that file is a defect. |
| `LIMITATIONS.md` | staged | The boundaries of what this lane did, stated by the lane that did it, each in a section of its own — including the two this correction newly creates: a confirmation that covers the body text and not the apparatus beside it, and a transport owner minted for a row that resolves no address. | That the list is complete. A limitation nobody noticed is not in it. |
| `UNRESOLVED-BLOCKERS.md` | staged | Every blocker left open on purpose, with its owner and its state after this lane. | That the enumeration is complete. A blocker nobody noticed is not in it. |
| `PRIVACY-AUDIT.md` | staged | What the sanitizer looks for, where it looked, what it does not cover, and what a reviewer can run to reproduce it — including why a command representation that shows more of an invocation's structure discloses no more about the machine it ran on. | That these bytes are clean — that is the seal transcript's claim, not that file's. |

## The derived record

| Member | State | Supports | Does not prove |
| --- | --- | --- | --- |
| `claims.json` | declared, pending | Every identity, count, size and digest, derived mechanically from the repository and the frozen member inventory — including the three symbolic workspace-provenance fields that say what kind of checkout produced this package. | Anything about the archive: the archive does not exist when this is written. |
| `DERIVED-CLAIMS.md` | declared, pending | The same dict, rendered. Byte-reproducible from `claims.json` by the final verification, which is why the renderer subscripts its keys rather than defaulting them. | Nothing beyond `claims.json`; it is a rendering, not a second source. |
| `checks.txt` | staged | Every command that ran, with its working directory, the argument vector a shell was handed, its environment bindings, its exit, order, start, end, tree state before and after, attempt and log — and the token legend that binds each symbol to exactly one location, so a row is resolvable from inside the package. | That a command's *result* was correct — only that it ran, in what directory, with what arguments, and what it exited with. |
| `commits.txt` | staged | The exact commit range from the reviewed parent to this head. | That the range is the whole change; `changed-files.txt` and `changes.patch` carry that. |
| `changed-files.txt` | staged | Every path this range touches, with its status and the diff stat. | Intent. It shows what moved, not why. |
| `changes.patch` | staged | The complete diff: the finalizer and its schema, the seal that makes a scalar-only null-prototype frozen record, the publication of the finished value, the completion envelope and its `WeakSet`, the three exact-object comparisons at the application, the post-write body record, the rebinding of a cached value to a later owner, the relocated page prose, and the harness seams — the publication probe over the engine's own map operations and the write that is made to fail. | That the regressions are sufficient. The parent replay is what argues that. |
| `MANIFEST.sha256` | declared, pending | A digest for every member except itself. | The archive's own identity, which is in the sidecar. |
| `EVIDENCE-INDEX.md` | staged | This table. | Anything. It is a map. |

## The runs

Two validation batteries are SHIPPED here — `logs/attempt-15/` at the exact
reviewed parent and `logs/attempt-16/` at this head — and they are the two
whose evidence disposition is `authoritative`. **They are not the only
batteries this lane ran, and the index says so rather than letting the shipped
pair stand for the history.** Two more completed and had their figures
declined. Two more completed, were recorded `authoritative` the moment they
ended, and were then SUPERSEDED: P8 found they had executed a `logs/battery.sh` this
package does not ship — what ran was not what shipped, on a difference of
header comment prose — and the remedy was to measure both endpoints again
rather than to argue the difference away. One was refused by a guard before it
ran a step, one was refused because its log target already existed, and one was
stopped from outside itself and is terminally `abandoned`.
`logs/attempt-history.json` is the derivation and `PROVENANCE.md` §13 is the
account; the cohorts that are not shipped are retained outside this package and
support nothing in it.

**The shipped pair carries one property the superseded pair did not, and it is
the property a reviewer should check first.** Every tool those two batteries
executed — the battery driver, the gate summariser, the payload measurer and
the journal dumper — is byte-identical to the copy this package ships under
`logs/`, and that identity was established BEFORE either cohort's evidence
disposition was recorded. The executed, trusted and shipped digests are in the
sibling tool-bytes record, and `PROVENANCE.md` §13 states what happened the
first time round.

Each battery writes beneath its own log root, named by the ordinal the lane
ledger allocated to it, so a failed attempt's transcripts stay with that attempt
and cannot be overwritten by the attempt that replaces it.

**`logs/LOG-INDEX.md` is the correct entry point.** It is derived mechanically
from what is on disk, with the attempt that owns each log, and it is the
authority on which log file carries which run. The rows below name logs by role
rather than by path for that reason.

| Member | State | Supports | Does not prove |
| --- | --- | --- | --- |
| `logs/attempts.json` | declared, pending | This lane's ledger rows, copied as late as the phase contract allows so the sealing attempt's own row is inside it, each terminal or post-terminal row carrying its reason. | That it is the whole ledger, and — separately — that any one ledger is the whole history. The live ledger is a sibling; the authority gate reads that one and refuses a package whose copy disagrees with it, and the post-seal phase's rows are in the sibling and not here. The live ledger is itself the successor of a ledger this lane retired after ordinal 03: no row in either was rewritten or deleted, but neither file is the history on its own, and the history is derived across the pair in `logs/attempt-history.json` and recorded with both files' digests in `PROVENANCE.md` §15. |
| `logs/LOG-INDEX.md` | declared, pending | Every log in this package, its attempt and its role, derived from what is on disk. | That a log's contents are what its name says. |
| `logs/attempt-history.json` | staged | This lane's attempt history in full — which means across BOTH of its ledgers, because the first was retired after ordinal 03 and the second opened in its place, and neither file is the whole history on its own — derived by `checks.py --history-table --assert-invariants` across both of them: every attempt with its ordinal, its ledger, its side, its EXECUTION disposition and its EVIDENCE disposition as two separate columns, each non-successful or post-terminal row's reason, the derived counts, the ledger identities, and the three invariants asserted over them with their pass state. It is the record `PROVENANCE.md` §13 is rendered from, and the reason no count in that section is typed. | That the ledgers it folds are themselves complete — the authority gate reads the external ledger and refuses a package whose in-package copy disagrees with it, and that gate's verdict is a sibling transcript, not this member. Nor that a later attempt cannot change the counts: assembly may append package-side attempts, which is why the figures are derived at seal time and pinned nowhere. |
| `logs/divergence-reconciliation.json` | staged | The mechanical reconciliation of the example-replay figure, in four measures named apart and never collapsed — `divergent_rows`, `distinct_divergent_identities`, `volatile_rows` and `total_differing_rows`: the parsing rule with its soundness argument, all four transcripts field by field with their build state and the evidence for it, the divergent-command identity sets differenced in both directions under `v16_minus_v15_distinct_identities` and `v15_minus_v16_distinct_identities`, the volatile-table check, the root cause with its controlled experiment and its live reproduction, and the point-by-point reconciliation against the V15 review — including where that review's observation is upheld and where its diagnosis is refuted. `authoritative_basis` names the cold parent and head cohorts this package ships as the sole authoritative source and `v16_endpoints_equal` records that they agree exactly; every name it gives a transcript of this package is package-root-relative. | That `check-examples` is correct, or that the underlying tool defect is fixed. It is neither; the missing `PREPARE` entry belongs to another owner and `LIMITATIONS.md` discloses it. Nor that the figure is a constant: every figure in it is stated with the build state it was taken in, because without that state it does not reproduce. Nor that its V15 entries are a V16 replay: they are historical, inferred from shipped V15 warm evidence, and no figure here derives from them — nor from the superseded cohorts under ordinals 04 and 07, which reproduced the same cold counts and are recorded as a control on the figure rather than as a source of it. |
| `logs/named-commits.json` | staged | Every commit and digest this package discusses but was not produced from, each with the reason a reviewer meets it. It is the allowlist the identity audit reads, so an undeclared SHA in a claim-bearing member is a refusal rather than a silent stale head. | That a named commit is what its entry says it is. The entry is prose; the commit is fetchable and the reviewer can look. |
| `logs/order-head.txt`, `logs/order-parent.txt` | staged | Each battery's own ledger: preflight identity and expected SHA, then per step the order, the log, the tree state before and after, the recorded invocation and the exit, then postflight with its SHA drift. `checks.txt` is composed from these rather than written beside them. | Anything a step did not record. A battery ledger is a record of asking, not of understanding. |
| the focused Catena logs | staged | The focused Catena suite at each endpoint. | That a difference between them is this lane's. Only the pair, read together, says that. |
| the head-tests-against-parent log | staged | **The non-vacuity proof of the whole lane**: this head's test file replayed against the uncorrected parent, failing where the correction is absent — including the corrected body-application oracle, which the previous lane's version could not fail because it asserted a bare row plus arbitrary content as a valid application. Its invocation is recorded with its own working directory, and the two repositories it touches carry two distinct tokens. | That the corrections are complete — only that they are not vacuous. |
| the publication-probe records | staged | What a lookup of the probed path returned at every instant the transport could have been observed: before the handler, during parsing, during normalization, before publication, after publication, and from a synchronous reentrant lookup inside the handler. | That no instant exists which nobody named. The structural fact — that the value handed to the map is the return of a function that has already run to completion — is what carries the claim; this corroborates it. |
| the structural-check logs | staged | The generator-side structural check at each endpoint. | Anything about the browser surface. |
| the promise-ledger logs | staged | The promise ledger validates at each endpoint. | That a promise is *met* — only that the ledger is internally valid. |
| the full-discovery logs | staged | The whole suite at each endpoint, including the inherited failures, so the failure sets can be compared: 27 result ROWS over 22 distinct `module.Class.method` identities, stated apart, because two methods emit multiple `subTest` rows. | That a failure is inherited, from either log alone. Only the pair can say that, and where a fresh replay differs from the sealed transcript the difference is recorded rather than reconciled away — including the `pdf-review.test` tool-registry identity, which appears only from a checkout under `/tmp`, since `tools/pdf-review:486` allows any output under `Path("/tmp").resolve()` for a non-managed worker and the asserted refusal then never happens. That is an environment precondition, not a change. |
| the `make -k check` logs | staged | Which targets are red at each endpoint, and the example replay's own line with its divergent ROWS, its distinct COMMAND STRINGS and its declared volatile lines as three separate figures, each recorded beside the BUILD STATE (`COLD`/`WARM`) the run was taken in. | Which of them this lane caused — the comparison answers that. That the divergence figure is a constant: it is 30 divergent rows over 28 distinct divergent identities cold and 28 divergent rows over 27 distinct divergent identities warm, so a figure quoted without its build state is not reproducible, and nothing here quotes one. The volatile figure is a static declaration, not a run outcome, and is never summed with either sense. Nor that four red targets is the only correct reading: `check-tool-registry` is genuinely run here because `tmt` is installed, and on a box without it only three are red. |
| the release-bindings logs | staged | The stale release bindings, fail-closed and unsigned. | That they are this lane's to fix. They are not, and none was re-signed. |
| the public-site build logs | staged | The built artifact the browser gate runs over. | That the artifact is publishable; `public-alpha verify` is a separate gate and was not run. |
| the browser-gate logs and their reports | staged | That the gate ran, at each endpoint, and the full real-Chromium report it produced. | That headless Chromium is a device or an assistive technology. It is neither, and it does not witness any vector this lane closes. |
| the gate-comparison log | staged | The two gate reports compared object for object under named volatile exclusions, as a recorded step with its own exit rather than as an assertion in prose, with per-row diagnostics keyed on something two rows cannot share — `total_gate_rows` 2,290, `normalized_reports_equal` yes and `distinct_diagnostic_names_or_categories` 17, reported as three figures because they are three quantities of three kinds and a diagnostic category count is not the row-identity universe. | That a difference is a regression. The exit is recorded, not judged. The previous lane's whole-report verdict was sound and its diagnostics were degenerate; this row is worth reading with that history in mind. |
| the browser-static log | staged | The static browser-surface assertions. | Runtime behaviour. |
| the gzip-size logs | staged | The measured payloads against their ceilings, at each endpoint — the page at 12,965/13,000 whole-gzip and 7,835/8,800 stripped, thirty-five bytes under a ceiling this lane did not raise, and the uncapped model at 44,247/10,344. | That the page's remaining headroom is workable, or that the unbudgeted model's growth is acceptable. Both questions are open and re-asked. Nor that thirty-five bytes bought everything worth buying: two identified fixes cost 37 and about 60 gzipped bytes and were deliberately deferred, which `LIMITATIONS.md` states with their costs. |
| the packaged ownership journals | staged | Per request: its sequence, its scenario, the route as it stood when the request was made, the owning projection, the owning **row**, the transport owner the row was given, the path, the kind, the owning step, the outcome, the cache disposition, and — bound to the owner object rather than to a path and a row id — the body that was applied after its write was confirmed. The roster is derived from the test file itself, so every scenario the file declares is journalled. | Anything a journal does not record, and anything about a scenario the test file does not declare. A body whose write was not confirmed appears nowhere, by design — and so does a REFUSED application: V15's `bodyAsked` witnessed every attempt including refusals, while V16 records only confirmed applications, so refusals are proved by the boundary's committed `false` and by the unchanged page rather than by a journal row. |
| the sealer's own test logs | staged | That the refusals this package depends on actually fire. | That a gate refuses a contradiction it does not model. |

## The pipeline, shipped as members

The tools that assembled this package, and the ones that gate it, are shipped
under `logs/` so a reviewer can read what produced the evidence rather than take
its word. They are read as bytes by the final verification and are never
executed from inside the archive.

**The complete enumeration is mechanical, not written here.** The sibling
tool-bytes record carries every tool with its executed, trusted and shipped
digest and its class, and `logs/LOG-INDEX.md` indexes their transcripts. Among
them are the assembler, the battery driver, the checks renderer, the claims
deriver, the head-consistency auditor, the sanitizer, the final verifier, the
inventory tool, the gate comparer, the gate summariser, the payload measurer,
the journal dumper and the authority gate.

**The execution state in that record is derived, not maintained.** The previous
package kept it beside the invocations, which is how several rows came to deny an
execution while carrying a time, a phase and a transcript — three fields only an
execution has — and how the two scripts that drove the entire build came to be
marked not executed, because neither recorder can see itself. What ships here is
derived from what the run recorded, its quantities are named apart rather than
combined into one fraction, and the schema is labelled by the phase it was taken
at. `PROVENANCE.md` §11 states the rule; the record states the values.

**Some of them changed for this lane, and the tool-byte record is where which
ones is established rather than here.** A reviewer who wants the identity
first-hand digests each shipped tool in this package against its copy in the
previous one: a tool this lane corrected differs, every other is byte-identical,
and the classes and digests are in the executed-tool record and the comparison
table named in `HANDOFF.md` §10. What each correction was and why is in
`PROVENANCE.md` §1.

The test suites among them are the ones that prove a refusal fires:
`logs/test-sanitize-and-seal.py` for the sealer and the log-and-attempt
protocol, `logs/test-authority-coherence.py` for the authority gate,
`logs/test-attempt-history.py` for the ledger's rules and for the battery's own
endpoint refusals — the wrong clean commit and the dirty postflight —
`logs/test-verify-final-package.py` for the final verification, and
`logs/test-handoff-inventory.py` for the completeness checker. A gate that has
only ever been run against a package that passes is a gate nobody has seen
refuse.

## The pictures, and why there are none

There is no `screenshots/` directory and no capture in this package, and no
empty directory stands in for one. This correction changes no HTML and no CSS —
`src/web/browser/catena/catena.css` and
`src/web/browser/catena/index.html` are byte-identical at both endpoints — and
what the page's own change alters is *when* a value becomes reachable, *what it
is made of* and *who may apply it*, not what the page draws.

The differences it does produce are not layouts and are not photographable. A
prototype's words standing as a fragment's own text look exactly like a
fragment's own text. A body applied under a row that never asked for it renders
cleanly, with no marker and no seam, which is precisely why the defect survived
a review. A write that does not take leaves the page showing what it showed
before. And a path lookup returning an unresolved promise is not a visual state
at all: it is a value, observed at an instant, inside a module nothing exports.

Those states are asserted at the DOM by the replay harness — the rendered body
text, the rendered holding state, the row count, the refusal, the tally, the
spoken status line and the route — and journalled per request, with the body
journal recording only writes the page read back. The limit of the substitution
is stated rather than hidden: nothing in this package shows any of these states
under a browser engine, and `LIMITATIONS.md` says so. `HANDOFF.md` §10 records
the omission and its reason among the conditional artifact classes.

## The siblings, which are not members

They live beside this directory because none of them can exist until after the
manifest is taken, and because the archive must not contain the record that
names its own digest. Each is named by exact filename in `HANDOFF.md` §10: the
archive, its digest-and-size sidecar, the outer invocation log, the read-only
final-verification transcript, the post-verification authority record, the
contemporaneous executed-tool digests, the tool-byte comparison table, this
lane's attempt and battery history as the live ledger carries it — the ledger
this lane opened when it retired its first, whose retirement `PROVENANCE.md` §15
records and which `logs/attempt-history.json` folds together with its
predecessor — the pre-publication authority
gate's transcript, the handoff inventory's transcript, the outer sanitization
pass's transcript, and the re-scan that clears each rewritten sibling.

**The last two were named by suffix in the previous package, and that is the
defect this one closes.** That pass runs after the inventory and the authority
gate so that it can rewrite and re-scan their transcripts too, so its own
records do not exist at the moment the inventory first runs. The previous
package described them by suffix and recorded a `COMPLETE` verdict taken before
they existed; re-run at the true final state, its own checker answers
`INCOMPLETE`. Here they are named by filename and the verdict this package ships
is the one taken after they exist.

The inventory tool discovers and stats every sibling, including its own output,
rather than taking them from arguments — which is how an earlier package came to
omit its own inventory log while scoring ten of ten. What it now also checks is
described in `PROVENANCE.md` §1: a row whose recorded invocation cannot be run
as written, a token that stands for two locations, a classification that rests
on a prefix match, an execution state the transcripts contradict, a named cohort
with no ledger row, an append-only claim that cannot be true of the file it is
made about, and a completeness verdict taken at any state but the final one.

**Two of those siblings are the record that the post-seal phases ran at all, and
the sibling ledger carries their rows.** The member sealed inside the archive is
written before those gates run and cannot be reopened afterwards without
rewriting a sealed archive, so it stops where it stops. The slice beside the
archive is not sealed, and every row appended after it is derived is copied into
it. So a reviewer reads that the gates ran in their own transcripts, and reads
their rows in the sibling ledger. `PROVENANCE.md` §10 states which record
carries what and why the sealed one cannot, and `LIMITATIONS.md` records the
remaining boundary.
