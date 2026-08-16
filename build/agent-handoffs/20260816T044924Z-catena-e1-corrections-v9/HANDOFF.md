# Catena E1 — V9 composed prefix/fallback closure handoff

## 1. Task and intended outcome

Answer the fresh independent review of V8 — **CHANGES REQUIRED** — with
exactly the review's stated next action and nothing else: preserve the
absent / present-valid / present-invalid `text_prefix` distinction through
composition, permit the carried fallback only on genuine absence, prove the
closure cold, prewarmed and genuinely late at the production request sinks
with complete terminal assertions, and produce a package whose machine
claims describe the final sealed bytes.

The intended outcome is a reviewable head, not an accepted one. **This lane
records no acceptance of its own work and does not review it.** Every other
finding of the V7 review, as the V8 review left it, remains open and
untouched; `UNRESOLVED-BLOCKERS.md` lists them, and the reviews' own records
on their review branches remain the authoritative statement of each.

This package mutates nothing. It names, and does not touch, the sealed V7
and V8 packages on the evidence branch, and it supersedes none of them: it
is the record of a new head, not a correction of an old package.

## 2. Identity

**Every SHA, count, size and identity claim in this package is in
`DERIVED-CLAIMS.md` and `claims.json`, computed from the frozen member
inventory by `logs/derive-claims.py`.** No identity or figure is typed into
this file. `logs/head-consistency.py` refuses a package whose prose names a
commit those claims do not entitle it to name; the commits this package
discusses without being produced from them are declared, each with its
reason, in `logs/named-commits.json`.

The lineage in words: the parent is the exact V8 candidate the independent
review reviewed; the review it answers is that review's commit on its own
review branch; the head is the parent plus three commits — the three-state
composition closure, its cold/prewarmed/late production-sink regressions,
and the durable-record update. The diff is in `changes.patch`, its inventory
in `changed-files.txt` and `commits.txt`, all regenerated at the sealed
head.

## 3. What was wrong, and what was done

The V8 review proved the composed escape the isolated validators could not
see: a prefix the file stated and the page refused collapsed into the same
`''` as a prefix the file never stated, and the carried-fallback door opened
on that one `''` — so a refused `structure/paragraphs/` prefix still
fetched the valid same-stem carried `structure/catena/text/` file it stood
beside, and the planted body rendered as an ordinary success. It also
proved the V8 package's machine inventory was captured before the final
sealing writes, understating the final uncompressed total with five stale
member rows.

`COMPOSED-CLOSURE.md` states the three-state contract, the two functions
that now enforce it, and the evidence — the valid-corpus preservation kept
deliberately apart from the adversarial half, and both driven at the
request journal the replay harness records. The journals themselves are
`logs/request-journals-head.log` and, for the defect demonstrated at the
parent, `logs/request-journals-parent.log`. The package correction is the
sealing protocol itself: the inventory is frozen before derivation, derived
members are named and never sized or hashed, and a read-only post-seal
verification proves every claim against the final ZIP alone.

## 4. How to verify

Start with `checks.txt` — every command of the two batteries, its exact
invocation, exit, ledger timestamps and log, composed by `logs/checks.py`
from the ordering ledgers `logs/order-head.txt` and `logs/order-parent.txt`
that `logs/battery.sh` wrote as the batteries ran. Then:

1. `claims.json` / `DERIVED-CLAIMS.md` — every derived figure, one pass.
2. `logs/v8-tests-against-parent.log` — the head's test file against the
   parent's production files; the classes that distinguish the heads, by
   name.
3. `logs/request-journals-parent.log` against
   `logs/request-journals-head.log` — the defect's own fetch journal beside
   the closed one.
4. `MANIFEST.sha256`, then `logs/sanitize-and-seal.py --verify` — the
   member proof; `logs/verify-final-package.py` — the read-only post-seal
   verification of every claim against the final ZIP; `PRIVACY-AUDIT.md`
   describes the sanitization and its transcripts.
5. `EVIDENCE-INDEX.md` — every member, what it supports, what it does not.

`REVIEW_REQUEST.md` is questions only. `LIMITATIONS.md` states what this
package does not prove.
