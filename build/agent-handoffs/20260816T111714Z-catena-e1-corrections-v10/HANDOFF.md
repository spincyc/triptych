# Catena E1 — V10 refused-prefix presentation closure handoff

## 1. Task and intended outcome

Answer the fresh independent review of V9 — **CHANGES REQUIRED** — with
exactly the review's stated next action and nothing else: preserve the V9
request-layer closure; carry and render the distinct refused-prefix state
truthfully and fail closed on contradictory prefix claims; exact-pin the
complete cold, prewarmed, late, and present-valid request/terminal vectors;
and create a new unique immutable package with clean exact-SHA/cwd
preflights, unique non-overwriting logs and targets, accurate
method/failure labels, complete handoff/request structure, and a P8
transcript bound to the ZIP name, digest, size, member partition, totals,
and duplicate checks.

The intended outcome is a reviewable head, not an accepted one. **This lane
records no acceptance of its own work and does not review it.** Every other
finding remains open and untouched; `UNRESOLVED-BLOCKERS.md` lists them,
and the reviews' own records on their review branches remain the
authoritative statement of each.

This package mutates nothing. It names, and does not touch, the sealed
V7–V9 packages on the evidence branch. It supersedes the V9 package
`20260816T044924Z-catena-e1-corrections-v9` in the protocol sense the
review required — the V9 review's package findings are corrected here, in a
new uniquely timestamped package, while the sealed V9 artifact stands
unmodified as its review left it.

## 2. Identity

Branch: `impl/catena-wave-1-e1-corrections-v10`.
Head: `ea15d16d22d7ceaed989ed9907c236f967738a03`.
Base (task parent, the exact reviewed V9 candidate):
`3c5b78249193df065c4e1c2ee5a98e5989c6e582`.
Review answered: `55df5c236a1dfda12bb974efdbb9f46d0aeb3436` on
`review/catena-wave-1-e1-corrections-v9-independent`, published review head
`4f00e04bdd1fd63702a51bfdafef256b468bef77`.
The reviewed state is the committed head with **no uncommitted changes**:
both battery ledgers open with a contemporaneous `sha=`/`porcelain=clean`
preflight (`logs/order-head.txt`, `logs/order-parent.txt`).

Every one of these identities is also derived mechanically:
`DERIVED-CLAIMS.md` and `claims.json`, computed from the frozen member
inventory by `logs/derive-claims.py`, are the authority wherever prose and
derivation could disagree, and `logs/head-consistency.py` refuses a package
whose prose names a commit those claims do not entitle it to name; the
commits this package discusses without being produced from them are
declared, each with its reason, in `logs/named-commits.json`.

The head is the parent plus three commits — the renderer/model presentation
closure, the exact terminal vectors with the ownership-recording harness,
and the durable-record update. The diff is in `changes.patch`, its
inventory in `changed-files.txt` and `commits.txt`, all regenerated at the
sealed head.

## 3. Focused files changed

Production: `src/web/browser/catena/catena.js` (the refusal consumed before
the request sink), `src/web/browser/catena/catena-model.js` (the exported
`TEXT_REFUSED` sentence and the closed claim boundary). Tests:
`tools/tests/test_catena_wave_1.py`. Durable records: `PROJECT-WORK.md`,
`guidance/corpus-browser-roadmap.md`, `promised-deliverables.toml`.
`src/web/browser/catena/catena.css`,
`src/web/browser/catena/index.html`, `scripts/_catena.py`, and all of
`src/web/data/` are byte-identical to the parent — `changed-files.txt` is
the derived inventory.

## 4. Startup and route state

From the repository root: `make public-site`, then serve
`build/public-alpha/site` with any static server (for example
`python3 -m http.server --directory build/public-alpha/site 8000`) and open
`/catena/#book=Gen&chapter=1&bible=douay-rheims`. The production corpus is
entirely present-valid, so the refused state is visible only through the
adversarial replay: `python3 -m unittest discover -s tools/tests -p
'test_catena_wave_1.py'` drives it, and `logs/11-request-journals-head.log`
prints each scenario's journal and terminal sinks.

## 5. What was wrong, and what was done

The V9 review proved the model's third prefix state stopped at the model:
`src/web/browser/catena/catena.js` never read `text_refused`, sent the
refused row's empty path
through the same `ABSENT` sentinel as genuine absence, and told the reader
the fragment `carries no text file` — false of a fragment whose spine
stated a reference this page declined, and doubly false prewarmed, where
the reviewer's exact carried file had already been fetched. The exported
claim boundary accepted the contradictory `{stated: false, trail: <valid>}`
as absence; the terminal proofs were materially incomplete; and the V9
package protocol was short in the seven ways §1 lists.

`PRESENTATION-CLOSURE.md` states the two-sentence contract, the three edits
that enforce it, and the evidence — the four terminal vectors pinned to
expected values with request ownership and `history.state` captured, the
claim boundary driven directly, and the distinction pinned with a positive
control each way. The package protocol corrections are in the pipeline
itself: `logs/battery.sh` (unique refusing logs, contemporaneous
provenance), `logs/checks.py` (provenance surfaced per block),
`logs/assemble.sh` (a reused timestamp refused, never deleted),
`logs/derive-claims.py` (accurate lane labels, the parent decomposition
reported un-collapsed), and `logs/verify-final-package.py` (the transcript
bound to the exact ZIP with duplicate-row checks and derived final-byte
totals).

## 6. How to verify

Start with `checks.txt` — every command of the two batteries, its exact
invocation, exit, ledger timestamps, unique log, and the battery's own
`sha`/`clean`/`cwd` preflight, composed by `logs/checks.py` from the
ordering ledgers `logs/order-head.txt` and `logs/order-parent.txt` that
`logs/battery.sh` wrote as the batteries ran. Then:

1. `claims.json` / `DERIVED-CLAIMS.md` — every derived figure, one pass.
2. `logs/10-head-tests-against-parent.log` — the head's test file against
   the parent's production files; the distinguishing methods by name.
3. `logs/11-request-journals-parent.log` against
   `logs/11-request-journals-head.log` — the false absence sentence
   standing at the parent beside the truthful refused terminal at the head.
4. `MANIFEST.sha256`, then `logs/sanitize-and-seal.py --verify` — the
   member proof; `logs/verify-final-package.py` — the read-only post-seal
   verification, bound to the exact ZIP basename, digest and size;
   `PRIVACY-AUDIT.md` describes the sanitization and its transcripts.
5. `EVIDENCE-INDEX.md` — every member, what it supports, what it does not.

`REVIEW_REQUEST.md` is questions only, structured as Blockers and Optional
feedback. `LIMITATIONS.md` states what this package does not prove.

## 7. Known limitations and unresolved decisions

`LIMITATIONS.md` in full; `REVIEW_REQUEST.md` carries every question that
needs external judgment; `UNRESOLVED-BLOCKERS.md` lists every finding left
open with its owner.

## 8. Artifact inventory

Core: `HANDOFF.md`, `REVIEW_REQUEST.md`, `changes.patch`, `checks.txt`.
The argument: `PRESENTATION-CLOSURE.md`, `PROVENANCE.md`,
`UNRESOLVED-BLOCKERS.md`, `LIMITATIONS.md`, `PRIVACY-AUDIT.md`. The
derived record: `claims.json`, `DERIVED-CLAIMS.md`, `MANIFEST.sha256`.
Git-derived: `commits.txt`, `changed-files.txt`. Logs and tooling: the
`logs/` tree — two battery ledgers, every uniquely indexed battery log, the
two whole browser-gate JSON reports and their comparison, the request
journals at both ends, the head-tests-against-parent run, and the pipeline
scripts that produced all of it, each named in `EVIDENCE-INDEX.md`.

Conditional classes omitted, with reasons: **screenshots/** — the
stylesheet and markup are byte-identical to the parent and the change is a
terminal sentence swap on adversarial fixtures; the rendered difference is
the sentence itself, pinned byte-exactly in the replay, and no
before/after raster pair would show anything the journals do not
(`LIMITATIONS.md` §3). **The conditional sources record** — this lane
consumed no external sources: every input is the repository's own review
records, code, and tests. **logs/ of a discarded run** — nothing was discarded; every run is
retained (`PROVENANCE.md`).
