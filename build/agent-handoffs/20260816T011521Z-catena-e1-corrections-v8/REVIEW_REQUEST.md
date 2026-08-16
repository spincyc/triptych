# Review request — Catena E1 V8

**The exact head, the parent, the review answered and every count in this
package are in `DERIVED-CLAIMS.md` and `claims.json`, computed at seal time
by `logs/derive-claims.py`.** No identity or figure is typed into this file,
and `logs/head-consistency.py` refuses a package whose prose names a commit
those claims do not entitle it to name.

This file is questions only. The review that dispatched this lane asked for a
fresh independent review of the exact head, **scoped first to the namespace
closure**; the questions below are in that order.

---

## The closure itself

### 1. Is the boundary drawn at the right place?

`textTrail` accepts `structure/catena/text/` and any directory below it;
`textLeaf` accepts any grammar-valid JSON file inside the namespace, with the
pre-existing same-stem-as-own-id requirement still on top for the carried
form. The corpus today uses exactly the namespace root and single-segment
stems. Should the contract have been drawn tighter — exactly the root
directory, exactly one segment — or is refusing to tighten beyond the stated
namespace the right reading of the correction brief?

### 2. Is the prefix rule right for a prefix the corpus never writes?

A `text_prefix` outside the namespace now zeroes the prefix, and a fragment
under it falls back to its carried path, which must itself be inside the
namespace and same-stem. So a wrong-namespace prefix beside a valid owned
carried path yields the carried request. Is that composition acceptable, or
should a wrong-namespace prefix poison the whole file's text layer?

### 3. Is the sink evidence sufficient?

The journals pin the replay harness's stubbed `fetch`, which is the same seam
the V7 review used to prove the defect. No real-Chromium probe of this route
is included, for the reason `LIMITATIONS.md` §3 states. Is that the right
economy for this micro-lane, or should the fresh review require one?

## The lane's boundaries

### 4. Is the record update proportionate?

The durable records gain one lane section, one roadmap section and row, one
ownership-row move, and one ledger deliverable; the review's own record is
referenced by SHA and deliberately not merged into implementation history. Is
anything missing that the next lane will need, or anything present that
overstates this lane?

### 5. Are the open blockers stated at the right altitude?

`UNRESOLVED-BLOCKERS.md` lists every V7 finding this lane left open, in the
review's own numbering, each deliberately untouched. The review remains the
authoritative statement of each; the list here is a pointer, not a
restatement. Is that the right division, or should the package carry the full
text of each finding?

## Standing questions this lane re-asks rather than answers

### 6. The uncapped combined payload

The model grew by the closure's own bytes and carries no ceiling; the two
files' combined gzipped payload is measured at both ends in
`logs/gzip-sizes-head.log` and `logs/gzip-sizes-parent.log` and disclosed in
the durable records. The V5, V6 and V7 reviews each asked the owner whether
the model should be capped and none was answered. The question stands a
fourth time; this lane could not answer it for itself.
