# The `src/web/data/` contradiction — status at V5: unchanged, untouched

## What V5 did about it

Nothing, deliberately, and that is the requested disposition.

`git diff --name-only f93757854b54c19e50bdcb97ca0fed9b48d22bb7..HEAD` lists
exactly the files in `changed-files.txt`. **Not one is under `src/web/data/`.**
The parent-to-head data diff is empty, as it was for V4.1.

This lane did not:

- weaken, relax or rewrite `test_candidate_does_not_leak_fixture_or_discovery_records`;
- delete it, skip it, or mark it expected-failure;
- add a whitelist, an allowlist entry or a baseline bump;
- revert the V4 exact voice-key projection to satisfy it;
- add any new `src/web/data/` change of its own.

The default expectation stated for V5 — **no new `src/web/data/` changes** —
is met without exception. No blocking finding required a Catena-owned
generated fixture, because every V5 fixture is injected at read time by the
test harness or by the probe's own server, never written to the tracked
corpus.

## Why it still fails

Unchanged from the V4.1 review's own classification: **"C — a separate
owner/test mismatch, with an authorized Catena exception."**

The failing paths are:

| Path | Provenance |
| --- | --- |
| `src/web/data/structure/catena/index.json` | the exact voice-key projection review `9b1c23680` explicitly authorised, produced through the owning `scripts/_catena.py structure` writer |
| `src/web/data/structure/catena/27-is/008.json` | the same authorised seam |
| two `src/web/data/structure/propers/...` paths | predate V4 entirely |

The guard is a historical broad tripwire (`af6c0c8`) belonging to the
protected Liturgy / Day-reader owner. The V4.1 review recorded that **that
owner must separately re-review the integrated generated data and reform or
advance the tripwire with an exact baseline and explicit acceptance status**,
and that no candidate whitelist, silent baseline bump, test weakening or data
revert is authorized.

That instruction is unchanged by V5 and is not this lane's to execute.

## How a reviewer can verify the claim cheaply

```
git diff --name-only f93757854b54c19e50bdcb97ca0fed9b48d22bb7..<V5 head>
git diff --stat   f93757854b54c19e50bdcb97ca0fed9b48d22bb7..<V5 head> -- src/web/data/
git diff          f93757854b54c19e50bdcb97ca0fed9b48d22bb7..<V5 head> -- tools/tests/test_day_reader_integration.py
```

The second and third produce no output. `changes.patch` in this package is the
whole diff and can be read directly.
