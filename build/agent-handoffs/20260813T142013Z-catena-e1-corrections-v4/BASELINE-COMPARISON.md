# Base versus head — measured, and stated only as far as it was measured

The V3 review found the word **identical** used where the compared output was
not identical. This file does not use it except where the comparison it
describes actually held, and it states each difference rather than summarising
them away.

- **Base**: `f2c9bc49dd29499734193b264ba9da21304b27f1` — the exact head the
  independent review examined. Measured in a **separate clean clone**, so both
  sides are real measurements.
- **Head**: the V4 head named in `HANDOFF.md`.
- Both sides: `python3 -m unittest discover -s tools/tests`, non-verbose, same
  machine, same interpreter, run concurrently.

## Totals

| | base `f2c9bc49` | head V4 |
| --- | --- | --- |
| tests run | 1,600 | **1,617** |
| failures | 15 | **14** |
| errors | 13 | 13 |
| skipped | 11 | 11 |
| exit | 1 | 1 |
| wall clock | 490.553 s | 491.717 s |

The 17 additional tests at head are this lane's regressions, listed in
`EVIDENCE-INDEX.md`.

## Failure identity

Compared as the set of `FAIL:`/`ERROR:` names.

| | count |
| --- | --- |
| names at base | 28 |
| names at head | 27 |
| **new at head** | **none** |
| present at base, absent at head | 1 |
| shared | 27 |

**There is no newly attributable V4 failure identity.**

### The one base-only name

```
FAIL: test_shell_smoke_tests_pass (test_tool_registry.ToolSmokeTests.test_shell_smoke_tests_pass) (test='pdf-review.test')
      AssertionError: 1 != 0 : expected an --output outside build/ to be refused
```

This is **not** claimed as a V4 fix. It is a clone-path artifact: the base was
measured in a fresh clone in a scratch directory, and this smoke test is
sensitive to where the checkout sits. The same commit measured in place does
not produce it, which is why the base here shows 15 failures where the V3
package recorded 14 for the same commit. Disclosed, not counted.

## Assertion detail

Identity alone is not enough — the V3 review asked for **full identity plus
detail**, because a shared name can hide a changed assertion. Two shared
failures differ in detail. Both are stated exactly.

### 1. Attributable to V4 — the forbidden-path list grows by two

`test_candidate_does_not_leak_fixture_or_discovery_records`
(`test_day_reader_integration`) does `git diff --name-only af6c0c8df` and
asserts that nothing under `src/web/data/` changed. **It fails at base and it
fails at head**, but the list is longer at head:

| | list |
| --- | --- |
| base | `src/web/data/structure/propers/roman-1962.json`, `src/web/data/structure/propers/roman-pre-1955.json` |
| head | the same two, **plus `src/web/data/structure/catena/27-is/008.json` and `src/web/data/structure/catena/index.json`** |

The two added entries are V4's, and they are the authorised generator/data
seam: the regenerated catena index carrying the exact `voices` array, and the
Isaiah 8 chapter file discussed below. **This is attributable drift in a
pre-existing failure, not a new failure**, and it is a direct consequence of
the seam the V3 review explicitly authorised. It is raised as a reviewer
question in `REVIEW_REQUEST.md`, because a test that forbids every
`src/web/data/` change and a review that authorises one particular
`src/web/data/` change cannot both be satisfied, and that conflict is not this
lane's to resolve.

The sibling assertion in `test_propers_reader_integration` moves the same way
for the same reason.

### 2. Environment-sensitive — an absolute path in a message

```
AssertionError: 2 != 0 : index-bible: <path>/src/sources/bibles/douay-rheims/index.yaml is stale
```

Same test, same status, same count; the path differs because the two runs sit
in different directories. Environment-sensitive, attributable to nothing.

### The deliverable-count assertion did NOT move

The V3 review recorded this assertion changing from `28 != 23` to `29 != 23`
because V3 added a promised-deliverable record. **V4 adds no deliverable
record, and the assertion reads `29 != 23` on both sides.** It is unchanged,
and is reported as unchanged rather than left for a reviewer to infer.

## Classification of every failing name at head

| class | count | notes |
| --- | --- | --- |
| introduced by V4 | **0** | no new failure identity |
| inherited | 25 | stand identically at base and head |
| attributable detail drift | 2 | the forbidden-path lists above; same identity and status |
| environment-sensitive | 1 | the absolute path in the `index-bible` message |
| separately owned | — | see `UNRESOLVED-BLOCKERS.md`; release, registry and example debt are inside the inherited count |
| unresolved | 0 | nothing observed here is left unexplained |

## A note on Isaiah 8

Regenerating the catena structure also writes
`src/web/data/structure/catena/27-is/008.json` and adds `8` to Isaiah's
`present` list. **This is pre-existing drift, discovered by V4 and not caused
by it**, and that was verified rather than assumed: running the *unmodified*
generator from `f2c9bc49` produces the same file and the same `present` entry.
The committed data was stale against its own generator.

It is kept rather than reverted, because shipping data that contradicts the
generator that writes it would be the worse of the two states, and because
suppressing it would mean hand-editing generator output. It is disclosed here,
in the commit message, and in the reviewer questions.
