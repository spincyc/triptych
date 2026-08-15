# Catena E1 — V7 typed-projection correction handoff

## 1. Task and intended outcome

Answer the fresh independent review of V6 — **CHANGES REQUIRED** — with the
smallest bounded correction of its proven blocking classes, behind an explicit
typed projection; correct the oracles that had blessed each defect; issue one
immutable exact-head handoff whose claims are derived rather than typed; and
stop for a fresh independent review.

The intended outcome is a reviewable head, not an accepted one. **This lane
records no acceptance of its own work and does not review it.**

This package supersedes nothing and mutates nothing. It names, and does not
touch, `build/agent-handoffs/20260814T182026Z-catena-e1-corrections-v6`.

## 2. Identity

**Every SHA, count, size and identity claim in this package is in
`DERIVED-CLAIMS.md` and `claims.json`, computed at seal time by
`logs/derive-claims.py`.** None is typed into a document. `logs/head-consistency.py`
refuses a package whose prose names a commit those claims do not entitle it to
name, calls the head a parent, or names a package path the package does not
contain.

That is the direct answer to the V6 review's finding that `REVIEW_REQUEST.md`
opened by naming a head the package was not sealed for, and to the four other
count claims it found wrong.

Branch: `impl/catena-wave-1-e1-corrections-v7`, started at the exact reviewed
V6 head.

## 3. Uncommitted changes in the reviewed state

None; `claims.json` records the working tree as clean at the head, checked
rather than asserted.

Every head-side measurement was taken in a **clean, separate checkout**, one
command at a time, never in parallel and never in the background, with an
ordering ledger recording each command's start, end and exit
(`logs/order-head.txt`). The parent battery ran the same way in its own
checkout (`logs/order-parent.txt`). V6 disclosed that its first head-side round
let `make -k check` and the browser gate run concurrently with full discovery
in one checkout, and discarded it; this lane never produced such a round.

## 4. Files changed

The list, the per-commit attribution and the diffstat are derived —
`changed-files.txt`, `commits.txt`, `changes.patch`, and the tables in
`DERIVED-CLAIMS.md`.

Production changes are confined to `src/web/browser/catena/catena.js`,
`src/web/browser/catena/catena-model.js` and `scripts/_catena.py`, with tests
in `tools/tests/test_catena.py` and `tools/tests/test_catena_wave_1.py`.

**Byte-identical and untouched:** `src/web/browser/catena/catena.css`,
`src/web/browser/catena/index.html`, every path under `src/web/data/`, every
release record, the common gate, the shared shell, protected Liturgy, and all
PDFs.

## 5. Exact startup commands

```
make public-site
python3 -m http.server --directory build/public-alpha/site
python3 -m unittest discover -s tools/tests -p 'test_catena*.py' -v
```

The route is `/catena/#book=Gen&chapter=1&bible=douay-rheims`. All paths are
repository-relative and every command runs from the repository root.

## 6. What was wrong, and what was done

`TYPED-PROJECTION.md` is the full account, and is this package's successor to
the boundary document V5 and V6 shipped. In brief:

1. **`chapterFragments` shallow-copied.** Every own property of the shared
   source record and then of the fragment went into one object, and the two
   dangerous fields were cleared afterwards — `text_path` only when a valid
   composed form existed. Where the id or the file's prefix could not be read,
   the record's own `text_path` survived and `openFragment` handed it to the
   real request sink. V7 **projects**: a record of known, validated fields and
   nothing else, with `text_path` composed rather than carried.

2. **Hollow members made rows, tallies and claims.** A fragment that can name
   neither an identity, an author nor a work is not a thin fragment. An
   absence source is validated before it takes a work's row. A refusal needs
   the whole typed record the projection writes — the closed kind and the
   chapter **matched against the chapter being read**.

3. **A contradiction spoke after declining.** V6 blanked the finding and then
   printed one side's `reason`, chosen by ranking the two on length. V7 emits
   no prose where no single finding can be read.

4. **`partial` was coerced in the generator.** `str(row.get("partial") or "")`
   turned a mapping into `"{'a': 1}"`. Both prose fields are refused at build
   time when they are not text, and a `partial` detached from
   `partial-public-domain` is refused with them.

5. **Unreadable roots manufactured domain claims.** Holdings, canon, voices,
   the edition manifest, the paragraph layer, the verses container and the
   chapter spine itself each now distinguish *we read it and found nothing*
   from *we could not establish what is there*.

6. **The oracles had blessed each defect.** Ten `CORRECTED ORACLE (V7)` blocks,
   each with its reason recorded rather than deleted. `CORRECTED-ORACLES.md`.

7. **The late-work guard omitted the final status sink.** It compared the
   announcement JOURNAL, which a stale write cannot shorten. It now compares
   the live region's current contents and every other projection the page
   writes on a settled route, and asserts the release really happened.

## 7. This lane attacked its own change three times

The first pass confirmed **five** defects in it: one introduced by the
correction, four the correction had not reached, all the same
manufactured-negative class it set out to close.

The second pass found that class **again, one level under three of those
fixes**, and that is the finding worth carrying forward. The chapter payload
had been given a third answer and its contents had not; `null` had been made
the mark of an unreadable document in one place and left as the mark of a 404
in three others; an optional layer's failure still took down the bootstrap;
and two address spellings passed the grammar and then rendered something the
reader had not asked for, rewriting the address to say they had.

The third pass found **eleven** more, three of them introduced by the second
round's own fixes, and by then the pattern is the finding. Each round had
closed a CONTAINER and left its MEMBERS; or replaced one data-comparable
sentinel and left three; or caught one optional fetch and left the one beside
it. A payload could still forge the page's own 404 and its own failed request,
and the second was printed to a reader inside the page's own failure sentence.

Each pass is a separate commit whose message says what it found. Nineteen
defects were found and fixed this way, and `CORRECTED-ORACLES.md` records
every oracle that had to move with them.

**Two confirmed findings are recorded as NOT fixed** — `REVIEW_REQUEST.md` §1,
and `UNRESOLVED-BLOCKERS.md` §7, which is composed inside the shared shell and
is not this route's to write.

That every pass found something is evidence that attacking one's own work
finds things. It is not evidence that it finds everything — each fix revealed
the next level, and a fourth level is not ruled out — and this package does
not offer three passes as a substitute for the independent review that is
owed. `LIMITATIONS.md` §10 states that plainly rather than implying the bottom
was reached.

## 8. Known limitations

`LIMITATIONS.md`, twelve numbered, opening with the V6 evidence faults rather
than with the correction. Not duplicated here.

## 9. Unresolved decisions

`REVIEW_REQUEST.md` — six blockers and three optional, questions only.
`UNRESOLVED-BLOCKERS.md` records the open items this lane did not touch, each
with its owner, none repaired here.

## 10. Artifact inventory

| Path | What it is |
| --- | --- |
| `HANDOFF.md` | this file |
| `claims.json` | **every machine-derived claim, and the source for every figure in this package** |
| `DERIVED-CLAIMS.md` | the same values rendered for a reader, written in the same pass |
| `TYPED-PROJECTION.md` | what crosses the boundary and what does not, and why |
| `CORRECTED-ORACLES.md` | every oracle this correction changed, with the reason each is recorded under |
| `LIMITATIONS.md` | what this package does not prove |
| `REVIEW_REQUEST.md` | questions only |
| `UNRESOLVED-BLOCKERS.md` | open items, each with its owner, none repaired here |
| `DATA-TEST-CONTRADICTION.md` | the `src/web/data/` guard contradiction, preserved |
| `PRIVACY-AUDIT.md` | the sanitization method, its captured transcripts, and the sealer's own two defects |
| `EVIDENCE-INDEX.md` | every artifact, the claim it supports, and what it does not prove |
| `checks.txt`, `logs/checks.py` | every command, its invocation, its exit, its log and the commit it ran at — composed from the batteries' own ledgers, not typed |
| `commits.txt`, `changed-files.txt`, `changes.patch` | git-derived, bare |
| `logs/derive-claims.py` | writes `claims.json` and `DERIVED-CLAIMS.md` from one pass |
| `logs/head-consistency.py` | refuses a package whose prose disagrees with those claims |
| `logs/sanitize-and-seal.py`, `logs/test-sanitize-and-seal.py`, `logs/sealer-tests.log` | the sealer, corrected, its tests and their run |
| `logs/seal-check.log`, `logs/seal.log` | the sealing transcripts, captured rather than quoted |
| `logs/v7-tests-against-parent.log` | the V7 test file replayed against the PARENT's production files |
| `logs/focused-catena-head.log`, `logs/focused-catena-parent.log` | the focused Catena suite at each end |
| `logs/full-discovery-head.log`, `logs/full-discovery-parent.log` | full discovery at each end |
| `logs/make-check-head.log`, `logs/make-check-parent.log` | `make -k check` at each end |
| `logs/promised-head.log`, `logs/promised-parent.log`, `logs/catena-check-head.log`, `logs/catena-check-parent.log`, `logs/release-bindings-head.log`, `logs/release-bindings-parent.log`, `logs/gzip-sizes-head.log`, `logs/gzip-sizes-parent.log`, `logs/public-site-head.log`, `logs/public-site-parent.log`, `logs/browser-static-head.log` | ledger, catena check, release bindings, budgets, site build, and the browser scripts no test loads — one log per command |
| `logs/browser-gate-head.json`, `logs/browser-gate-parent.json`, `logs/browser-gate-head.log`, `logs/browser-gate-parent.log` | the two browser-gate reports and their invocations |
| `logs/order-head.txt`, `logs/order-parent.txt` | the ordering ledger for each battery |

**Deliberately omitted, with reasons:**

- **A sources record** — no research, provenance, rights or source-history work was
  done; this is a defensive-boundary correction over existing records.
- **Screenshots** — the CSS and the markup are byte-identical and the change is
  semantic. `LIMITATIONS.md` §2, and the count is derived as zero rather than
  described as none.
- **Print and forced-colors captures** — no CSS changed. V4.1's accepted matrix
  is neither superseded nor re-issued.
- **PDF artifacts** — no PDF was touched.
- **Re-signed release bindings** — stale at both ends and correctly fail-closed;
  `refresh-release-bindings` and `approve-release` were not run.
- **Any repair of the inherited red targets** — none was worked around,
  whitelisted, weakened or expect-marked.
- **No empty directory was created to imply evidence that does not exist.**
