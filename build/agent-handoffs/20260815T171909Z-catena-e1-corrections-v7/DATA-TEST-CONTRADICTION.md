# The `src/web/data/` contradiction, preserved

## What it is

`tools/tests/test_day_reader_integration.py` contains, in
`test_data_legacy_shell_css_and_visual_oracle_are_frozen`, a guard of the form

    changed_data = git("diff", "--name-only", BASE, "--",
                       "src/web/data", "src/sources/calendars").splitlines()
    self.assertEqual(changed_data, [])

with `BASE = "af6c0c8df"`. It asserts that **nothing** under `src/web/data/` has
changed since that commit, for any reason, by any owner, with any authorization.

A separate accepted review authorized exactly one change under that path — the
V4 Catena voice seam. Both records are durable and they contradict each other.
The guard therefore fails, and so does its sibling
`test_candidate_does_not_leak_fixture_or_discovery_records`, which runs the same
`git diff --name-only BASE`.

## What V7 did about it

Nothing, deliberately — as V6 did, and for the same reason.

- V7 changed **no** path under `src/web/data/`. The changed-file list is in
  `changed-files.txt` and `DERIVED-CLAIMS.md`, both derived from the sealed
  head; `git diff --stat <parent>..<head> -- src/web/data src/sources/calendars`
  is empty.
- The guard was **not** weakened, whitelisted for V7, expect-marked, skipped, or
  rebased onto a newer `BASE`.
- The prior authorized V4 seam was **not** backed out to make the guard pass.
- V7's adversarial data lives in `tools/tests/test_catena_wave_1.py` as fixture
  literals served by the replay harness's own stub network, and in nothing
  else. No generated file was altered to make a malformed test pass, which is
  the specific thing a lane in this position is most tempted to do.

## Why not

The contradiction is between two owners' records, and resolving it means
choosing which record is wrong. That is an adjudication, not an implementation
detail, and this lane owns neither record. Making the guard pass by any of the
means above would convert an open question into a silent answer.

## How to tell it is inherited

The same two tests fail identically at the parent and at this head. Both runs
ship — `logs/full-discovery-parent.log` and `logs/full-discovery-head.log` — and both
identities appear in the FAIL/ERROR name set that `logs/derive-claims.py`
compares between the two, reported under "Suites" in `DERIVED-CLAIMS.md`. The
comparison is of the identity SET, not of a count: the head runs more tests.
