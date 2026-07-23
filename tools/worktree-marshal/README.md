# Worktree Marshal

Transactional Git worktrees for coding agents.

## Extraction status

This directory now contains the operational Triptych compatibility engine as
well as the future distribution name, Python import namespace, license, and
compatibility baseline. The repository-local
[`scripts/triptych-codex`](../../scripts/triptych-codex) command is a thin,
in-process bootstrap for the co-located package engine.

The package is not publishable yet and deliberately has no installed generic
command-line entry point. Its current engine still owns Triptych's schema-1
state namespace, refs, environment variables, flags, diagnostics, and Codex
policy. Do not upload this version to a package index or treat importing it as
authorization to operate on a repository or retained run.

It does contain the first extracted integration surface: the importable
[`worktree-marshal.mk`](src/worktree_marshal/resources/worktree-marshal.mk)
fragment. Its default Make targets are deliberately unprefixed:

```text
codex  status  reopen  final-diff  integrate
resolve  continue  abort  clean-run
```

Lifecycle targets take `RUN=<run-id>`; `status` also works without `RUN` for
an overview. Target names, the executable, and fixed command arguments are
configured in the including Makefile before importing the fragment; invocation
and environment overrides are rejected. Target names use the literal grammar
`[A-Za-z0-9][A-Za-z0-9_.-]*`. Triptych currently binds the fragment to its
compatibility launcher and temporarily accepts its former
`make <target> <run-id>` spelling as well. Generic consumers get only the
`RUN=` form unless they deliberately enable positional compatibility. A later
package command will install or update a pinned copy in a consumer repository;
consumers should not locate package resources dynamically during every Make
parse.

The extraction will continue by adding artifact-level parity for the packaged
compatibility engine, then introducing a generic CLI only with an explicit
profile and state namespace. The frozen legacy contract and current security
boundary are recorded in
[`docs/compatibility-contract.md`](docs/compatibility-contract.md); the target
architecture and release sequence are in [`docs/design.md`](docs/design.md).

## Development check

From this directory, run the package tests with:

```sh
python3 -m unittest discover -s tests -v
```

The repository's `make check-agent-isolation` target additionally runs the
complete Triptych lifecycle suite through the thin compatibility bootstrap.

The initial package uses only the Python standard library at runtime and
requires Python 3.10 or newer. Its source is licensed under the MIT License.
