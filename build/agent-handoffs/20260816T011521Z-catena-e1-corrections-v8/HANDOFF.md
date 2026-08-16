# Catena E1 — V8 namespace-closure handoff

## 1. Task and intended outcome

Answer the fresh independent review of V7 — **CHANGES REQUIRED** — with
exactly the review's stated first bounded commit and nothing else: require
the byte-exact `structure/catena/text/` namespace for both the composed and
the carried Catena text path, with no whitespace repair, and prove it with
same-stem wrong-namespace regressions at the actual production request sink.

The intended outcome is a reviewable head, not an accepted one. **This lane
records no acceptance of its own work and does not review it.** Every other
finding of the V7 review remains open and untouched;
`UNRESOLVED-BLOCKERS.md` lists them, and the review's own record on its
review branch remains the authoritative statement of each.

This package mutates nothing. It names, and does not touch, both V7 packages
on the evidence branch, and it supersedes neither: it is the record of a new
head, not a correction of an old package.

## 2. Identity

**Every SHA, count, size and identity claim in this package is in
`DERIVED-CLAIMS.md` and `claims.json`, computed at seal time by
`logs/derive-claims.py`.** No identity or figure is typed into this file.
`logs/head-consistency.py` refuses a package whose prose names a commit those
claims do not entitle it to name; the commits this package discusses without
being produced from them are declared, each with its reason, in
`logs/named-commits.json`.

The lineage in words: the parent is the exact V7 candidate the independent
review reviewed; the review it answers is that review's commit on its own
review branch; the head is the parent plus two commits — the production
namespace closure with its regressions, and the durable-record update. The
diff is in `changes.patch`, its inventory in `changed-files.txt` and
`commits.txt`, all regenerated at the sealed head.

## 3. What was wrong, and what was done

The review proved at `fetch` that a well-formed directory of this data root
was enough to be requested: a `text_prefix` of another namespace composed a
request, and a carried same-stem path under another namespace passed the
same-stem check and fetched a real Sources text sharing that id.
Whitespace-wrapped paths were trimmed into validity on the way.

`NAMESPACE-CLOSURE.md` states the contract, the two validators that now
enforce it, and the evidence — the valid-corpus preservation kept deliberately
apart from the adversarial matrix, and both driven at the request journal the
replay harness records. The journals themselves are
`logs/request-journals-head.log` and, for the defect demonstrated at the
parent, `logs/request-journals-parent.log`.

## 4. How to verify

Start with `checks.txt` — every command of the two batteries, its exact
invocation, exit, ledger timestamps and log, composed by `logs/checks.py`
from the ordering ledgers `logs/order-head.txt` and `logs/order-parent.txt`
that `logs/battery.sh` wrote as the batteries ran. Then:

1. `claims.json` / `DERIVED-CLAIMS.md` — every derived figure, one pass.
2. `logs/v8-tests-against-parent.log` — the head's test file against the
   parent's production files; the classes that distinguish the heads, by name.
3. `logs/request-journals-parent.log` against
   `logs/request-journals-head.log` — the defect's own fetch journal beside
   the closed one.
4. `MANIFEST.sha256`, then `logs/sanitize-and-seal.py --verify` — the member
   proof; `PRIVACY-AUDIT.md` describes the sanitization and its transcripts.
5. `EVIDENCE-INDEX.md` — every member, what it supports, what it does not.

`REVIEW_REQUEST.md` is questions only. `LIMITATIONS.md` states what this
package does not prove.
