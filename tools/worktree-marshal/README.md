# Worktree Marshal

Transactional Git worktrees for coding agents.

## Extraction status

This directory contains the shared lifecycle engine, its first generic
profile, the frozen Triptych compatibility adapter, the Python distribution,
and the Make integration fragment. The repository-local
[`scripts/triptych-codex`](../../scripts/triptych-codex) command is a thin,
in-process bootstrap for the co-located package engine.

Built artifacts now install a `worktree-marshal` command. This remains a
pre-release extraction at version `0.0.0`; do not upload it to a package index
yet or treat installation as authorization to operate on a repository or
retained run. Stateful invocations select one immutable lifecycle domain
explicitly:

```text
worktree-marshal --profile generic-v1 run --agent codex
worktree-marshal --profile generic-v1 status [RUN_ID]
worktree-marshal --profile generic-v1 reopen RUN_ID [-- CODEX_ARGUMENTS...]
worktree-marshal --profile generic-v1 final-diff RUN_ID
worktree-marshal --profile generic-v1 integrate RUN_ID
worktree-marshal --profile generic-v1 resolve RUN_ID
worktree-marshal --profile generic-v1 continue RUN_ID
worktree-marshal --profile generic-v1 abort RUN_ID
worktree-marshal --profile generic-v1 clean RUN_ID
worktree-marshal --profile generic-v1 retire RUN_ID --discard-head FULL_OID --target-contains FULL_OID
```

Only `--help` and `--version` work without a profile. The explicit
`--profile triptych` spelling reaches the legacy state domain through the
compatibility adapter; the generic profile never discovers, adopts, migrates,
or falls back to Triptych runs. The exact generic identities are frozen in
[`docs/generic-v1.md`](docs/generic-v1.md).

The importable integration fragment is
[`worktree-marshal.mk`](src/worktree_marshal/resources/worktree-marshal.mk)
and its default Make targets are deliberately unprefixed:

```text
codex  status  reopen  final-diff  integrate
resolve  continue  abort  clean-run
```

Lifecycle targets take `RUN=<run-id>`; `status` also works without `RUN` for
an overview. Target names, the executable, and fixed command arguments are
configured in the including Makefile before importing the fragment; invocation
and environment overrides are rejected. Target names use the literal grammar
`[A-Za-z0-9][A-Za-z0-9_.-]*`. Triptych currently binds the fragment to its
compatibility launcher, clears the fragment's default
`--profile generic-v1` arguments, and temporarily accepts its former
`make <target> <run-id>` spelling as well. Generic consumers get only the
`RUN=` form unless they deliberately enable positional compatibility. A later
package command will install or update a pinned copy in a consumer repository;
consumers should not locate package resources dynamically during every Make
parse.

The package tests now install a wheel rebuilt from the source distribution in
an environment outside this checkout, with source-tree import paths removed.
That installed artifact passes a bounded lifecycle checkpoint covering generic
run preservation, integration, and cleanup through the packaged unprefixed
Make targets; bidirectional Triptych schema-1 run, status, and clean
interoperability through the packaged compatibility adapter; cross-profile
selected-run lookup isolation without manifest mutation; and rejection when
the generic profile's configured Codex executable aliases the installed
console, including symbolic- and hard-link aliases. This checkpoint is not the
complete installed lifecycle or release matrix. The next installed-artifact
checkpoint covers managed conflict resolution, continuation, abort, and
final-diff. Retirement, concurrency, crash recovery, and broader security
coverage remain release gates; the step-5 helper split remains protected by
the source and installed parity suites. The frozen legacy contract and current
security boundary are recorded in
[`docs/compatibility-contract.md`](docs/compatibility-contract.md); the target
architecture and release sequence are in [`docs/design.md`](docs/design.md).

## Development check

From this directory, run the package tests with:

```sh
python3 -m unittest discover -s tests -v
```

This package suite includes artifact-content checks and the bounded
installed-artifact lifecycle checkpoint described above; it does not yet run
the complete legacy lifecycle matrix against the installed console.

The repository's `make check-agent-isolation` target additionally runs the
complete Triptych lifecycle suite through the thin compatibility bootstrap.

The initial package uses only the Python standard library at runtime and
requires Python 3.10 or newer. Its source is licensed under the MIT License.
