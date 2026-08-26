# Evidence index

What each member of this package is, what it supports, and — the column that
matters — what it does **not** prove. A reviewer who reads only this file should
be able to tell which claims rest on evidence and which rest on a lane's word.

Two disciplines are carried forward from earlier rounds because earlier rounds
broke them. An earlier version of this file said the packaged journals carried
ownership rows they did not contain; nothing here claims support a member does
not carry, and where a member's support depends on what a run produced, the
mechanism that produces it is named instead of the outcome. And an earlier
package printed a mechanical completeness verdict that tested nothing this file
describes; the verdict is not repeated here, because a map that also grades the
territory is no longer a map.

**No figure appears in this file.** Every count, size, digest and identity is in
`claims.json` and its rendering `DERIVED-CLAIMS.md`. Where a number would belong
here, the member that carries it is named instead.

This file names itself, and it names every member. `MANIFEST.sha256` covers
every member except itself; the archive digest and byte size live in the sidecar
beside the archive, never inside it.

## The argument

| Member | State | Supports | Does not prove |
| --- | --- | --- | --- |
| `HANDOFF.md` | staged | The ten required contents of the handoff protocol, as content. | Nothing on its own; every claim in it is carried by a member below. |
| `CLAIM-CLOSURE.md` | staged | The technical argument: what the review found, what the parent actually does when one owner's request is held, the five clauses of the ownership contract, the closure inventory, the observation accounting stated exactly, what the shape costs, and what proves it. Two of its sections bound the claim by naming the vectors that close proof gaps rather than defects. | That the argument is right. It is prose; the vectors are in `changes.patch` and their runs are in the logs. |
| `REVIEW_REQUEST.md` | staged | The blocking questions this lane cannot answer for itself, each naming the acceptance decision it gates, and the optional notes beside them — including whether the corrected command record now reads end to end, which is a verdict on this lane's own tooling and therefore not this lane's to give. | Nothing. It asks; it does not answer. |
| `PROVENANCE.md` | staged | The review link this lane has and the older one it does not; the eight evidence defects with their root causes; the attempt state machine; the post-P8 authority ordering; the ledger and log-root rules; what the history may and may not be called; that no cohort was set aside; the post-seal rows, the slice beside the archive that now carries them and the sealed member that structurally cannot; which bytes ran; and the derived workspace provenance. | Its own accuracy — the lane ledger is the authority, and where the two could disagree the ledger is right and that file is a defect. |
| `LIMITATIONS.md` | staged | The boundaries of what this lane did, stated by the lane that did it, each in a section of its own. | That the list is complete. A limitation nobody noticed is not in it. |
| `UNRESOLVED-BLOCKERS.md` | staged | Every blocker left open on purpose, with its owner and its state after this lane. | That the enumeration is complete. A blocker nobody noticed is not in it. |
| `PRIVACY-AUDIT.md` | staged | What the sanitizer looks for, where it looked, what it does not cover, and what a reviewer can run to reproduce it — including why a classifier change that makes more command text visible does not widen what may leak. | That these bytes are clean — that is the seal transcript's claim, not that file's. |

## The derived record

| Member | State | Supports | Does not prove |
| --- | --- | --- | --- |
| `claims.json` | declared, pending — P4 | Every identity, count, size and digest, derived mechanically from the repository and the frozen member inventory — including, for the first time in this series, the three symbolic workspace-provenance fields that say what kind of checkout produced this package. | Anything about the archive: the ZIP does not exist when this is written. |
| `DERIVED-CLAIMS.md` | declared, pending — P4 | The same dict, rendered. Byte-reproducible from `claims.json` by the final verification, which is why the renderer subscripts its keys rather than defaulting them. | Nothing beyond `claims.json`; it is a rendering, not a second source. |
| `checks.txt` | staged | Every command that ran, with its exit, order, start, end, tree state before and after, attempt and log — and, per row, whether the recorded string is the exact one a shell was handed, a real invocation with this lane's values elided, or a description. | That a command's *result* was correct — only that it ran, and what it exited with. |
| `commits.txt` | staged | The exact commit range from the reviewed parent to this head. | That the range is the whole change; `changed-files.txt` and `changes.patch` carry that. |
| `changed-files.txt` | staged | Every path this range touches, with its status and the diff stat. | Intent. It shows what moved, not why. |
| `changes.patch` | staged | The complete diff: the settled-only path map and the settle-handler insertion, the per-owner request held against the transport owner, the frozen shared value, the first-settled-answer rule, the body application bound at its sink, the one substitute record per unreadable spine, the new model entry points and their witnessing, the three relocated paragraphs, and the nineteen new methods with the harness capabilities they need. | That the regressions are sufficient. The parent replay is what argues that. |
| `MANIFEST.sha256` | declared, pending — P6 | A digest for every member except itself. | The archive's own identity, which is in the sidecar. |
| `EVIDENCE-INDEX.md` | staged | This table. | Anything. It is a map. |

## The runs

Two validation batteries — one at this head, one at the exact reviewed parent —
and the assembly. Each writes beneath its own log root, named by the ordinal the
lane ledger allocated to it, so a failed attempt's transcripts stay with that
attempt and cannot be overwritten by the attempt that replaces it.

**`logs/LOG-INDEX.md` is the correct entry point.** It is derived mechanically
from what is on disk, with the attempt that owns each log, and it is the
authority on which log file carries which run. The rows below name logs by role
rather than by path for that reason.

| Member | State | Supports | Does not prove |
| --- | --- | --- | --- |
| `logs/attempts.json` | declared, pending — P5 | This lane's ledger rows, copied as late as the phase contract allows so the sealing attempt's own row is inside it, each terminal or post-terminal row carrying its reason. | That it is the whole ledger. The complete ledger is a sibling; the authority gate reads that one and refuses a package whose copy disagrees with it, and the post-seal phase's rows are in the sibling and not here. |
| `logs/LOG-INDEX.md` | declared, pending — P1 | Every log in this package, its attempt and its role, derived from what is on disk. | That a log's contents are what its name says. |
| `logs/named-commits.json` | staged | Every commit and digest this package discusses but was not produced from, each with the reason a reviewer meets it. It is the allowlist the identity audit reads, so an undeclared SHA in a claim-bearing member is a refusal rather than a silent stale head. | That a named commit is what its entry says it is. The entry is prose; the commit is fetchable and the reviewer can look. |
| `logs/order-head.txt`, `logs/order-parent.txt` | staged | Each battery's own ledger: preflight identity and expected SHA, then per step the order, the log, the tree state before and after, the recorded command and the exit, then postflight with its SHA drift. `checks.txt` is composed from these rather than written beside them. | Anything a step did not record. A battery ledger is a record of asking, not of understanding. |
| the focused Catena logs | staged | The focused Catena suite at each endpoint. | That a difference between them is this lane's. Only the pair, read together, says that. |
| the head-tests-against-parent log | staged | **The non-vacuity proof of the whole lane**: this head's test file replayed against the uncorrected parent, failing where the correction is absent — including the corrected late-answer oracle, which the previous lane's version could not fail because it asserted the leak as correct. Its command is recorded verbatim. | That the corrections are complete — only that they are not vacuous. |
| the structural-check logs | staged | The generator-side structural check at each endpoint. | Anything about the browser surface. |
| the promise-ledger logs | staged | The promise ledger validates at each endpoint. | That a promise is *met* — only that the ledger is internally valid. |
| the full-discovery logs | staged | The whole suite at each endpoint, including the inherited failures, so the failure sets can be compared. | That a failure is inherited, from either log alone. Only the pair can say that. |
| the `make -k check` logs | staged | Which targets are red at each endpoint. | Which of them this lane caused. The comparison answers that. |
| the release-bindings logs | staged | The stale release bindings, fail-closed and unsigned. | That they are this lane's to fix. They are not, and none was re-signed. |
| the public-site build logs | staged | The built artifact the browser gate runs over. | That the artifact is publishable; `public-alpha verify` is a separate gate and was not run. |
| the browser-gate logs and their reports | staged | That the gate ran, at each endpoint, and the full real-Chromium report it produced. | That headless Chromium is a device or an assistive technology. It is neither. |
| the gate-comparison log | staged | The two gate reports compared object for object under named volatile exclusions, as a recorded step with its own exit rather than as an assertion in prose. | That a difference is a regression. The exit is recorded, not judged. |
| the browser-static log | staged | The static browser-surface assertions. | Runtime behaviour. |
| the gzip-size logs | staged | The measured payloads against their ceilings, at each endpoint — the page against a ceiling it is under, the model against none. | That the unbudgeted model's growth is acceptable; that question is open and re-asked. |
| the packaged ownership journals | staged | Per request: its sequence, its scenario, the route as it stood when the request was made, the owning projection, the owning **row**, the transport owner the row was given, the path, the kind, the owning step, the outcome, the cache disposition, the body applied and what it was applied under. The roster is derived from the test file itself, so every scenario the file declares is journalled. | Anything a journal does not record, and anything about a scenario the test file does not declare. |
| the sealer's own test logs | staged | That the refusals this package depends on actually fire. | That a gate refuses a contradiction it does not model. |

## The pipeline, shipped as members

The tools that assembled this package, and the ones that gate it, are shipped
under `logs/` so a reviewer can read what produced the evidence rather than take
its word. They are read as bytes by the final verification and are never
executed from inside the archive.

**The complete enumeration is mechanical, not written here.** The sibling
tool-bytes record carries every tool with its executed, trusted and shipped
digest and its class — shipped and executed, shipped and not executed, external
system tool, or reviewer-only helper — and `logs/LOG-INDEX.md` indexes their
transcripts. Among them are the assembler, the battery driver, the checks
renderer, the claims deriver, the head-consistency auditor, the sanitizer, the
final verifier, the inventory tool, the gate comparer, the gate summariser, the
payload measurer, the journal dumper and the authority gate.

**Some of them changed for this lane, and the tool-byte record is where which
ones is established rather than here.** A reviewer who wants the identity first-hand
digests each shipped tool in this package against its copy in the previous one:
a tool this lane corrected differs, every other is byte-identical, and the
classes and digests are in the executed-tool record and the P8 comparison table
named in `HANDOFF.md` §10. What each correction was and why is in
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
what the page's own change alters is *when* an answer is applied and *to whom*,
not what the page draws. The visible difference is therefore not a layout: it is
which owner's document stands under which row, and it appears only while one
owner's request is held.

That difference is asserted at the DOM by the replay harness — the rendered
holding state, the rendered body text, the row count, the refusal, the tally,
the spoken status line and the route — and journalled per request in the
packaged ownership journals, which record what rendered, which row asked, which
owner the work was held against and what came back. A raster of two chapters
showing sentences would not distinguish the corrected page from the parent at
all: at the parent the wrong document renders *cleanly*, with no marker and no
seam, which is precisely why the defect survived a review.

The limit of the substitution is stated rather than hidden: nothing in this
package shows a held transport rendered by a browser engine, and
`LIMITATIONS.md` says so. `HANDOFF.md` §10 records the omission and its reason
among the conditional artifact classes.

## The siblings, which are not members

They live beside this directory because none of them can exist until after the
manifest is taken, and because the archive must not contain the record that
names its own digest. Each is named by exact filename in `HANDOFF.md` §10: the
archive, its digest-and-size sidecar, the outer invocation log, the read-only P8
transcript, the post-P8 final authority record, the contemporaneous
executed-tool digests, the P8 tool-byte comparison table, this lane's complete
attempt and battery history, the pre-publication authority gate's transcript,
and the handoff inventory's transcript.

The outer-sanitization pass's own transcripts are the exception, and
`HANDOFF.md` §10 states why: that pass runs after the inventory and the
authority gate, so that it can rewrite and re-scan their transcripts too, and
its own two records therefore do not exist at the moment the inventory is
checked. They are described there by their suffixes rather than asserted as
present.

The inventory tool discovers and stats every one of them, including its own
output, rather than taking them from arguments — which is how an earlier package
came to omit its own inventory log while scoring ten of ten. What it now also
checks is described in `PROVENANCE.md` §1: an empty command slot, a transcript
with no command row, an elided or described command where a verbatim one was
claimed, an executed-tool status the transcripts contradict, a named cohort with
no ledger row, and an append-only claim that cannot be true of the file it is
made about.

**Two of those siblings are the in-package record that the post-seal phase ran
at all, and the sibling ledger now carries its rows.** The member sealed inside
the archive is written before the two gates run and cannot be reopened
afterwards without rewriting a sealed archive, so it stops where it stops. The
slice beside the archive is not sealed, and every row appended after it is
derived is copied into it — the two gate rows among them. So a reviewer reads
that the gates ran in their own transcripts, and reads their rows in the
sibling ledger. `PROVENANCE.md` §9 states which record carries what and why the
sealed one cannot, and `LIMITATIONS.md` records the remaining boundary.
