# Catena E1 — V6 typed-membership correction handoff

## 1. Task and intended outcome

Answer the fresh independent review of V5 —
`fa5b2f601565508acee2b1b236b0c69138af07a3`, **CHANGES REQUIRED** at exact
candidate `19982ab433dd25704ed60b1ac6ddb678bc3a98f9` — with the smallest
bounded correction of its proven blocking classes, behind one typed record
boundary; replace the runtime oracles the review proved lossy with assertions
on the sinks the page actually writes; issue one truthfully labelled immutable
exact-head handoff; and stop for a fresh independent review.

The intended outcome is a reviewable head, not an accepted one. **This lane
records no acceptance of its own work, and does not review it.**

This package supersedes nothing. It names, and does not mutate,
`build/agent-handoffs/20260814T123524Z-catena-e1-corrections-v5` — evidence
commit `fe71d03e51bc3a89f01b9262cd3a4d9077bb0cef`, package digest
`18500400ce617365ef8322e41f011f44dc5a0a88dc39fbbcb5deb1abd78b75ea`, re-verified
byte-exact from that commit by this lane before anything here was written
(`checks.txt` W).

The review answered is a **sibling** of this line: its merge base with this
head is the reviewed parent itself, and it is not an ancestor of the head
(`checks.txt` X). It is deliberately not merged in.

## 2. Branch

`impl/catena-wave-1-e1-corrections-v6`, started at the exact reviewed V5 head.

## 3. Commits

| | |
| --- | --- |
| review addressed | `fa5b2f601565508acee2b1b236b0c69138af07a3` |
| parent (V5 head) | `19982ab433dd25704ed60b1ac6ddb678bc3a98f9` |
| implementation (1 of 5) | `2c1f87e5d6b1c07e9da6392693315c1049aa94b0` |
| implementation (2 of 5) | `e041411f67c725b78deac41f15b4411e8c46101a` |
| records (3 of 5) | `ee1048c903300e21ccb942b6b268f941dfe126e0` |
| correction (4 of 5) | `83cb63b61e366fac07b298fee77f63d1658086f7` |
| records (5 of 5) | `4639b139f2179b1fca7f9cb1e4ba3ac19c9bbc46` |
| HEAD (final) | `4639b139f2179b1fca7f9cb1e4ba3ac19c9bbc46` |

**Five** commits, and **two of the five touch production.**

| Commit | Touches | Production? |
| --- | --- | --- |
| `2c1f87e5d` | `src/web/browser/catena/catena-model.js`, `src/web/browser/catena/catena.js`, `tools/tests/test_catena_wave_1.py` | **yes** |
| `e041411f6` | `tools/tests/test_catena_wave_1.py` | no |
| `ee1048c90` | PROJECT-WORK.md, `guidance/corpus-browser-roadmap.md`, promised-deliverables.toml | no |
| `83cb63b61` | `src/web/browser/catena/catena-model.js`, `tools/tests/test_catena_wave_1.py`, PROJECT-WORK.md, `guidance/corpus-browser-roadmap.md` | **yes** |
| `4639b139f` | PROJECT-WORK.md, `guidance/corpus-browser-roadmap.md` | no |

**The last two commits are this lane correcting itself, and both are recorded
as such rather than folded into the ones before them.** The fourth changes one
line of production — a raw NUL byte written as a separator in the model's
`absenceRows` sort key, replaced by its escape, so the file and the shipped
patch are text to `grep`, `diff` and a pager again — stamps the one V6 fixture
root that was missing the adversarial banner, and corrects two counts the
durable records overstated in this lane's favour. The fifth touches no code at
all: it repairs an arithmetic error in the class decomposition (an earlier
record said 19 + 5 + 1, which is 25, where the measurement is 19 + 4 + 1) and
restates the relocation cost as measured after the NUL fix. Because a published
commit message cannot be amended, that record says in place that the
`ee1048c90` message quotes the pre-fix figures. No behaviour moves in either:
the string value of the separator is the same as a raw byte or an escape, and
the focused suite is 423 green at the head.

## 4. Uncommitted changes in the reviewed state

None. `git status --porcelain` is empty at `4639b139f` (`checks.txt` T).

**Every head-side measurement in this package was taken at `4639b139f`, on that
clean tree, in one sequential process** — `logs/measure-all.sh`, which ships.
Earlier head-side rounds were discarded rather than merged: in the first,
background waiters let `make -k check` and the browser gate run concurrently
with full discovery in the same checkout, and concurrent jobs writing under
`build/` measure neither; the later ones predated the fourth and fifth commits.
`checks.txt` says this in its header, because a reader is owed the reason there
is exactly one run of each command.

## 5. Focused files changed

| File | Change |
| --- | --- |
| `src/web/browser/catena/catena-model.js` | the membership half of the typed boundary: `ident`, `bookToken`, `trail` and the identity-gated `sources[key]` join; the member constructors `canonBook`, `bibleRecord`/`bibles`, `leadRow`/`leadRows`, `blockedRow`/`blockedRows`, `refusalNote`; `absenceRows` re-read as a set with an `offer` derived beside the finding that licenses it; the canonical verse key in `chapterLines`; `languageChip` and `sayLanguage`; `TESTAMENTS` and `testamentName`. The fourth commit writes the `absenceRows` sort-key separator as `'\u0000'` rather than as a raw byte |
| `src/web/browser/catena/catena.js` | calls them; `lang` omitted rather than defaulted at both sinks; the testament line from `book.testamentName`; lead, blocked and refusal rows taken from the model's members; `index = bag(index)` at the root; the canon checked before the address is judged; `startFailed` made a transaction |
| `tools/tests/test_catena_wave_1.py` | ten oracles corrected in place with their reasons, in nine annotated blocks across five pre-existing classes; eleven new harness projections; 23 new test classes; all ten V6 fixture roots stamped `_adversarial`; `MODEL_SHA256` pinned to the head's model, `adb61eb7…` |
| PROJECT-WORK.md, `guidance/corpus-browser-roadmap.md`, promised-deliverables.toml | durable records |

**Byte-identical and untouched:** `src/web/browser/catena/catena.css`,
`src/web/browser/catena/index.html`, every path under `src/web/data/`, every
release record, the common gate, the shared shell, protected Liturgy, and all
PDFs. Verified by an empty `git diff --stat` over those paths (`checks.txt` R).

## 6. Exact startup commands

```
make public-site
python3 -m http.server --directory build/public-alpha/site
python3 -m unittest discover -s tools/tests -p 'test_catena*.py' -v
```

The route is `/catena/#book=Gen&chapter=1&bible=douay-rheims`. All paths are
repository-relative and every command runs from the repository root.

## 7. Implementation summary

`TYPED-PRESENTATION-BOUNDARY.md` is the full account. In brief: V5 validated a
**shape** where the contract needed a **membership**, and the correction is
made once, in `src/web/browser/catena/catena-model.js`, which carries no byte
ceiling.

1. **Collection members are validated per collection before anything is
   counted, rendered, refused or called absent.** `leadRow`, `blockedRow`,
   `refusalNote` and `records` each state what one member of their collection
   IS. A record that states none of it is not a thin member; it is not a
   member, and it enters no row, no count and no derived claim, while its valid
   siblings are untouched.
2. **Root and identity joins are typed.** `bibleRecord`/`bibles` normalize the
   edition manifest before the control sees it; `ident`, `bookToken` and
   `trail` state the grammars the corpus actually writes; the `sources[key]`
   join in `chapterFragments` resolves only for a string key the record owns,
   so a one-member list no longer takes a real edition's rights and language.
3. **An unsupported claim is omitted, never guessed.** No `lang` is written
   from a language nobody can read — `|| 'en'` is gone from both sinks — and
   `testamentName` is `''` where the canon states no testament.
4. **Findings are read as a set.** One recognized finding is the record
   speaking; two different ones are a record contradicting itself, and the page
   declines rather than choosing the harsher claim. `partial` is licensed only
   by `partial-public-domain`.
5. **A verse has one canonical identity**, `^[1-9][0-9]*$`, so an edition
   carrying `"1"` and `"01"` renders verse 1 once instead of twice.
6. **Unsafe textual identities are unroutable.** A fragment id, edition id,
   book path or text prefix that is not an identity this corpus issued reaches
   no fetch, no route and no link, and refusing it costs its siblings nothing.
7. **A null or unreadable bootstrap is terminal.** `index = bag(index)` at the
   root, and `startFailed` invalidates pending render work, clears the tally
   and completes focus. **The canon is now checked before the address is
   judged** — judged against an empty canon the page had answered "book=Gen is
   not a book of this canon", a claim about the canon drawn from a parse
   failure. **The review did not name this defect**; it was found writing the
   regressions the review required, and `REVIEW_REQUEST.md` asks whether
   correcting it belongs inside a bounded correction.
8. **The lossy oracles are replaced.** Ten test methods that expected the
   defects are corrected in place with their reasons recorded rather than
   deleted, in nine annotated `CORRECTED ORACLE (V6)` blocks across five
   pre-existing classes; the harness gains `verseNumbers`, `verseTexts`,
   `lengths`, `bibleLabels`, `bibleValues`, `referenceBookText`,
   `absenceAuthors`, `absenceWorks`, `refusalCount`, `failureText` and
   `released`, none of which the parent's harness projected.
   `CORRECTED-ORACLES.md` is the per-oracle record.

## 8. Known limitations

`LIMITATIONS.md`, twelve numbered, and it opens with the four evidence faults
the V5 review found rather than with the correction. Not duplicated here.

## 9. Unresolved decisions

`REVIEW_REQUEST.md`, six blockers, one unnamed-defect question and three
optional. Not duplicated here. `UNRESOLVED-BLOCKERS.md` records the seven open
items this lane did not touch, each with its owner.

## 10. Artifact inventory

| Path | What it is |
| --- | --- |
| `HANDOFF.md` | this file |
| `checks.txt` | every command, its exact invocation, its numeric exit, its log and the commit it ran at |
| `EVIDENCE-INDEX.md` | every artifact, the claim it supports, and what it does not prove |
| `BASELINE-COMPARISON.md` | parent against head, suite by suite, with the exclusions stated |
| `TYPED-PRESENTATION-BOUNDARY.md` | what each grammar and predicate admits and refuses, and why |
| `CORRECTED-ORACLES.md` | every oracle this correction changed, with the reason each is recorded under |
| `LIMITATIONS.md` | what this package does not prove, opening with the V5 evidence faults |
| `REVIEW_REQUEST.md` | questions only — six blockers, one unnamed defect, three optional |
| `UNRESOLVED-BLOCKERS.md` | seven open items, each with its owner, none repaired here |
| `DATA-TEST-CONTRADICTION.md` | the `src/web/data/` guard contradiction, preserved untouched |
| `PRIVACY-AUDIT.md` | the sanitization method, its result, and the sealer's own audited gaps |
| `PROBE-DIFFERENCE.md`, `SCREENSHOT-METHOD.md` | the capture lane's records |
| `commits.txt` | the ancestry — all five commits — and the file list of each |
| `changed-files.txt` | `git diff --name-status` and `--stat` against the parent, bare |
| `changes.patch` | the exact parent→head diff, regenerated at the sealed head; 228,083 bytes, NUL-free, reproduces `git diff` at `4639b139f` |
| `logs/measure-all.sh` | the one sequential process every head-side measurement was taken by |
| `logs/misc.sh` | the short read-only checks it runs last, including the budget code |
| `logs/focused-catena-head.log`, `logs/focused-catena-parent.log` | the focused Catena suite at each end, verbose |
| `logs/all-tests-head.log`, `logs/all-tests-parent.log` | full discovery at each end |
| `logs/names-head.txt`, `logs/names-parent.txt` | the sorted FAIL/ERROR identity sets the comparison is made over |
| `logs/names.sh` | the extraction script both were derived by |
| `logs/v6-tests-against-parent.log` | the V6 test file replayed against the parent, unfiltered, harness death included |
| `logs/v6-tests-against-parent-filtered.log` | the same with three scenarios dropped, so the rest can report per class |
| `logs/parent-run-filter.patch` | the filter that made the second run possible, as a literal diff |
| `logs/gate-head.json`, `logs/gate-parent.json` | the two whole browser-gate reports |
| `logs/gate-head.log`, `logs/gate-parent.log` | their invocations, exits and counts |
| `logs/gate-comparison.log` | `compare-gate.py` over the two reports |
| `logs/compare-gate.py` | the comparison tool, excluding four volatile fields |
| `logs/make-k-check-head.log`, `logs/make-k-check-parent.log` | `make -k check` at each end |
| `logs/misc-checks-head.log`, `logs/misc-checks-parent.log` | ledger, catena check, release bindings, budgets, the relocation, byte-identity and `file`, at each end |
| `logs/public-site-head.log`, `logs/public-site-parent.log` | the two builds the gates ran against |
| `logs/sanitize-and-seal.py` | the package sealer, lane-local |
| `logs/test-sanitize-and-seal.py`, `logs/sealer-tests.log` | 45 tests over the sealer's own behaviours, and that run |
| `logs/v5-package-verify.log` | the V5 package digest, claimed against measured against the recorded sidecar |
| `logs/probe-catena.mjs`, `logs/probe-head.json`, `logs/probe-parent.json`, `logs/probe-head.stdout.txt`, `logs/probe-parent.stdout.txt` | the capture lane's instrument and its two runs |
| `logs/pair-audit.py`, `logs/pair-audit.json`, `logs/pair-audit.txt` | the capture lane's pair audit and its output |
| `logs/fixtures-source.json` | the fixtures the capture lane extracted from `tools/tests/test_catena_wave_1.py` |
| `screenshots/` | the capture lane's images and indexes |

**This file describes none of the capture lane's members** —
`PROBE-DIFFERENCE.md`, `SCREENSHOT-METHOD.md`, the `probe-*`, `pair-audit-*`
and `fixtures-source.json` artifacts, and everything under `screenshots/`. They
are listed so the inventory is complete, and their records are their own.
Nothing in this file, and no entry in `checks.txt`, should be read as vouching
for what any of them shows. `MANIFEST.sha256` is written by the sealer and does
not exist until the package is sealed.

**Deliberately omitted, with reasons:**

- **`sources.md`** — no research, provenance, rights or source-history work was
  done; this is a defensive-boundary correction over existing records.
- **Print and forced-colors captures** — `src/web/browser/catena/catena.css` is
  byte-identical to the parent and nothing here bears on those media. V4.1's
  accepted 53-image matrix is neither superseded nor re-issued.
- **PDF artifacts** — no PDF was touched.
- **Re-signed release bindings** — four are stale at both ends and correctly
  fail closed; `refresh-release-bindings` and `approve-release` were not run.
- **Any repair of the four inherited red targets** — none was worked around,
  whitelisted, weakened or expect-marked.
- **No empty directory was created to imply evidence that does not exist.**
