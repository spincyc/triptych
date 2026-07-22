# Worktree Marshal

Transactional Git worktrees for coding agents.

## Extraction status

This directory is an extraction-stage package scaffold. It establishes the
future distribution name, Python import namespace, license, and compatibility
baseline while the operational implementation remains in
[`scripts/triptych-codex`](../../scripts/triptych-codex).

The package is not publishable yet. It has no command-line entry point and does
not create, supervise, integrate, or clean worktrees. Do not upload this
version to a package index or substitute it for Triptych's launcher.

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

The extraction will proceed by moving behavior behind tested package
boundaries while preserving existing Triptych runs. The frozen legacy
contract and current security boundary are recorded in
[`docs/compatibility-contract.md`](docs/compatibility-contract.md); the target
architecture and release sequence are in [`docs/design.md`](docs/design.md).

## Development check

From this directory, run the scaffold tests with:

```sh
python3 -m unittest discover -s tests -v
```

The initial package uses only the Python standard library at runtime and
requires Python 3.10 or newer. Its source is licensed under the MIT License.
