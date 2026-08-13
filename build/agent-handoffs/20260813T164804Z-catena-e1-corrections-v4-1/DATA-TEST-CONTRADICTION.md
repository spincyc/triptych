# The `src/web/data/` test contradiction — unresolved, for the reviewer

## Status in V4.1: preserved exactly, not touched, not worked around

This lane changed **nothing** under `src/web/data/`. The contradiction below is
inherited from V4 and is reproduced here unchanged, because the directions for
this lane and the guidance both put it outside a micro-correction's authority.

## The contradiction

`tools/tests/test_day_reader_integration.py`, class `DayReaderIntegrationTests`,
`test_candidate_does_not_leak_fixture_or_discovery_records` asserts that a
candidate branch changes **nothing** under `src/web/data/`:

```python
changed = git("diff", "--name-only", BASE).splitlines()
forbidden = [
    path for path in changed
    if path.startswith("src/web/data/")
    or "fixtures/liturgy-reader-state" in path
    or path.endswith("sitemap.xml")
]
self.assertEqual(forbidden, [])
```

with `BASE = "af6c0c8df"`. The filter is **repo-wide** — it is not scoped to
liturgy — so any Catena data write trips it.

The V3 independent review **explicitly authorised exactly one** such change: the
exact Catena voice-key projection. V4 implemented it, writing
`src/web/data/structure/catena/index.json` (the counted `voices` array) and
`src/web/data/structure/catena/27-is/008.json`.

Both cannot hold. A test that forbids every `src/web/data/` change and a review
that authorises one particular `src/web/data/` change are in direct conflict.

## What this lane did NOT do

Per the standing constraint, and stated so a reviewer can check it:

- the test was **not weakened**;
- the test was **not deleted**;
- the test was **not rewritten to whitelist** V4 or V4.1;
- the authorised data projection was **not backed out** to satisfy it;
- the failure was **not silently marked expected** anywhere.

## The evidence

The test fails at the V4.1 base `e40720d5d` and at the V4.1 head
`f93757854` **identically** — same test, same status, same four forbidden
paths. V4.1 adds nothing to the list:

| | forbidden paths |
| --- | --- |
| base `e40720d5d` | `src/web/data/structure/catena/27-is/008.json`, `src/web/data/structure/catena/index.json`, `src/web/data/structure/propers/roman-1962.json`, `src/web/data/structure/propers/roman-pre-1955.json` |
| head `f93757854` | the same four, unchanged |

Two of the four (`propers/*`) predate V4 entirely and belong to a separate
propers/commons lane; the guard's `BASE` was never re-based after that work. Two
are V4's authorised seam. **None is V4.1's.**

The sibling assertions in `test_propers_reader_integration.py` and
`test_day_missal_integration.py` move for the same reason and are likewise
untouched here.

## The question this leaves the reviewer

This is an **independent-review judgment**, and it is put here rather than
decided:

1. Does the day-reader guard need an exemption for the seam the V3 review
   authorised, or should its `BASE` simply be re-based by its owning lane?
2. Or should the authorised voice-key projection have been carried some other
   way that never writes `src/web/data/`?

Either answer belongs to the day-reader/liturgy owner and to the reviewer, not
to a refusal-copy micro-correction.
