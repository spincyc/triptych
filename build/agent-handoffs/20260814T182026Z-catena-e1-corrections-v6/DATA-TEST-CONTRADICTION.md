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

## What V6 did about it

Nothing, deliberately.

- V6 changed **no** path under `src/web/data/`. Verified:

      git diff --name-only 19982ab433dd25704ed60b1ac6ddb678bc3a98f9..HEAD
      → src/web/browser/catena/catena-model.js
        src/web/browser/catena/catena.js
        tools/tests/test_catena_wave_1.py
        PROJECT-WORK.md
        guidance/corpus-browser-roadmap.md
        promised-deliverables.toml

- The guard was **not** weakened, whitelisted for V6, expect-marked, skipped, or
  rebased onto a newer `BASE`.
- The prior authorized V4 seam was **not** backed out to make the guard pass.

## Why not

The contradiction is between two owners' records, and resolving it means
choosing which record is wrong. That is an adjudication, not an implementation
detail, and this lane owns neither record. Making the guard pass by any of the
means above would convert an open question into a silent answer.

## How to tell it is inherited

The same two tests fail identically at the parent
`19982ab433dd25704ed60b1ac6ddb678bc3a98f9` and at this head. Both runs ship:
`logs/all-tests-parent.log` and `logs/all-tests-head.log`, and both identities
appear in the 27-entry name set that is identical at both ends
(`logs/names-parent.txt`, `logs/names-head.txt`).
