# Triptych Compatibility Contract

## Purpose and authority

This document freezes the observable compatibility baseline for extracting
`scripts/triptych-codex` into Worktree Marshal. It describes the legacy
launcher at schema version 1; it does not make this scaffold operational.

Until an extraction change deliberately replaces a behavior and supplies a
migration, the existing launcher and its black-box tests remain authoritative.
Existing retained runs must continue to be managed by code that understands
their exact legacy identity. A generic command must not silently adopt,
rename, rewrite, or clean legacy state.

## Legacy identity

The compatibility mode owns these exact identifiers:

- executable and diagnostic name: `scripts/triptych-codex` and
  `triptych-codex`;
- manifest schema: integer `1`;
- run ID grammar: eight UTC date digits, `t`, six time digits, `z-`, and
  twelve lowercase hexadecimal digits;
- worker branch prefix: `codex/isolated/`;
- private ref prefix: `refs/triptych-codex/runs/`;
- environment variables: `TRIPTYCH_CODEX_ROLE`, `TRIPTYCH_CODEX_REAL`,
  `TRIPTYCH_CODEX_STATE_DIR`, and `TRIPTYCH_CODEX_RUN_ID`; and
- linked-worktree lock reason prefix: `triptych-codex `.

The state-base override in `TRIPTYCH_CODEX_STATE_DIR` must be absolute. Without
it, the base is `$XDG_STATE_HOME/triptych-codex` when `XDG_STATE_HOME` is an
absolute path, otherwise `$HOME/.local/state/triptych-codex`. Beneath that
base, each repository owns a directory formed from a normalized checkout name
and the first twelve hexadecimal digits of the SHA-256 digest of its common
Git-directory path.

Each repository directory contains `repository.lock`, `runs/`, `worktrees/`,
and `tmp/`. One run owns matching `<run-id>` entries in the latter three
locations: a JSON manifest and lock under `runs/`, a linked worktree under
`worktrees/`, and its only run-scoped temporary directory under `tmp/`.

## Manifest and durable-state behavior

The allocation record begins with these fields:

- `schema_version`, `run_id`, `state`, `created_at`, and `updated_at`;
- `base_sha`, `target_ref`, and `branch`;
- `control_root`, `common_git_dir`, and `relative_cwd`; and
- `worktree` and `tmpdir`.

Lifecycle operations add audit, integration, conflict, rollback, cleanup, and
retirement checkpoints. Schema 1 accepts these lifecycle states:

```text
allocating
allocation-failed
ready
running
preserved
failed-preserved
interrupted
quarantined
retirement-pending
retirement-ref-cleanup-pending
cleaned
cleaned-branch-retained
integration-conflict
integration-continue-pending
integration-review-pending
integration-manual-landing-pending
integration-abort-pending
integration-abort-recovery-failed
integration-rebase-pending
integration-rebase-recovery-failed
integration-rebase-rollback-pending
integration-rebase-rollback-failed
integration-merge-pending
integration-merge-failed
integration-verification-pending
integration-verification-failed
integrated-pending-cleanup
integration-cleanup-pending
integration-cleanup-failed
cleaned-ref-retained
```

Manifests are private UTF-8 JSON files written with sorted keys, two-space
indentation, a trailing newline, atomic replacement, file synchronization, and
parent-directory synchronization. The state root and its `runs`, `worktrees`,
and `tmp` containers are mode `0700`; manifest and lock files are mode `0600`.
Loading validates the schema, run identity, repository identity, state, paths,
refs, branches, and recorded object IDs and fails closed on an inconsistency.

A future manifest schema must be versioned explicitly. Migration must be
tested against retained schema-1 runs and must never make an older executable
silently misinterpret newer state. Merely installing or invoking Worktree
Marshal is not authorization to migrate or delete state.

## Legacy command surface

With no Triptych lifecycle option, the launcher creates a unique locked
worktree from a stable, clean primary checkout and starts Codex there. The
direct lifecycle surface is:

```text
--triptych-status [RUN_ID]
--triptych-reopen RUN_ID [-- CODEX_ARGUMENTS...]
--triptych-resolve RUN_ID
--triptych-continue RUN_ID
--triptych-abort RUN_ID
--triptych-final-diff RUN_ID
--triptych-integrate RUN_ID
--triptych-clean RUN_ID
--triptych-retire RUN_ID --discard-head FULL_OID --target-contains FULL_OID
--triptych-help
```

All commands currently discover and validate a non-bare Git working tree,
including help. Operator errors return status 2. An invoked Codex process has
its exit status normalized and propagated. Reopen starts a new Codex process;
it does not resume a prior conversation.

The Triptych Make interface exposes `codex`, `status`, `reopen`, `clean-run`,
`integrate`, `resolve`, `continue`, `abort`, and `final-diff`. Except for the
status overview, its original interface accepted the opaque run ID as a second
Make goal, such as `make integrate <run-id>`. The extracted fragment documents
`make integrate RUN=<run-id>` as the preferred form. Triptych enables the
fragment's positional compatibility mode so both forms remain usable during
the migration; generic consumers do not enable that mode by default. The
direct launcher is the required interface for untrusted or external values.
Retirement deliberately has no Make target.

## Lifecycle invariants

- Allocation requires a stable, clean primary checkout and refuses nested
  allocation from a managed linked worktree.
- Each worker has a unique locked branch and linked worktree. Repository and
  run locks serialize their respective lifecycle transitions.
- Workers and resolvers receive the same exact run-owned path as `TMPDIR`,
  `TMP`, and `TEMP`; managed cleanup authenticates and removes that directory.
- An unchanged first successful run may be cleaned automatically. Changed,
  committed, failed, interrupted, inconsistent, or still-active work is
  retained or quarantined rather than discarded.
- Cleanup fails closed unless it proves the managed worktree, branch, head,
  index, temporary directory, and relevant private refs are in the expected
  state. A run is not marked cleaned while its temporary path remains.
- Integration requires separate authorization and a clean, audited worker.
  It confirms already-contained work, lands a linear result with an
  expected-old ref transaction, or performs the launcher-owned rebase of the
  audited linear worker commits. It never creates a merge commit.
- A genuine rebase conflict stays in the managed worker. The resolver may edit
  and stage only recorded conflict scope; only the launcher may continue or
  abort the rebase.
- Successful manual continuation stops at a clean review-pending candidate.
  `final-diff` compares exact objects without exposing the private worktree.
  Landing that candidate requires fresh authorization and an unchanged
  captured target.
- Hooks, signing, credential prompts, pagers, and editors are disabled for
  launcher-owned Git operations as applicable. The launcher does not push or
  deploy.
- Retirement is a separately authorized destructive exception. It uses exact
  object arguments, durable checkpoints, an anchored discard head, a
  containment check, and an atomic branch/anchor/receipt transaction. It does
  not move the target or establish semantic equivalence.

## Codex adapter boundary

The legacy implementation supports Codex only. It resolves a real Codex
executable, accepts only the interactive, `exec`, and `review` agent surfaces
and allowlisted options, and treats free-form prompts as data. It forces the
child working directory, disables Codex multi-agent mode, clears additional
writable roots and sandbox permissions, and defaults to Codex
`workspace-write` sandboxing. A caller may narrow that to `read-only` but may
not request a broader sandbox through the launcher.

These rules belong to a Codex adapter in the extracted design. A generic core
must not claim the same containment for another agent unless an adapter
provides and tests equivalent enforcement.

## Threat boundary and platform assumptions

The launcher hardens its own Git operations: it pins a resolved Git
executable, removes Git configuration and tracing environment channels,
disables replace objects, hooks, signing, editors, pagers, and terminal
credential prompts, validates relevant effective Git configuration, and uses
exact ref and object checks for destructive transitions.

That is not a complete operating-system sandbox. The child inherits much of
the host environment after Git-specific sanitization. The launcher does not
independently remove arbitrary credentials, block the network, constrain every
executable, or prevent an unconfined child from invoking Git or remote tools.
Its workspace containment relies on the Codex sandbox settings it enforces.
Consequently, an arbitrary-command or unconfined-agent adapter must not be
presented under the legacy assurance boundary.

The implementation also relies on POSIX facilities including `fcntl` locks,
inherited file descriptors, directory descriptors, no-follow opens, signals,
and POSIX rename and unlink semantics. Native Windows is outside the frozen
platform contract; WSL or a future separately tested backend is required.

The launcher protects managed lifecycle state against accidental changes,
races, path replacement, and many Git configuration attacks. It does not
protect against a hostile account that can rewrite the launcher's code, its
state files, the repository's Git object database, or the resolved Git or
Codex executables while they are in use.

## Extraction acceptance baseline

The legacy suite contains 184 focused tests in
`scripts/tests/test_triptych_codex.py`. Before any compatibility wrapper
delegates to packaged code, the package test matrix must cover the same
observable lifecycle, failure, concurrency, recovery, Make forwarding, and
security behavior against disposable repositories. Triptych-specific output
and identities remain compatibility assertions rather than generic defaults.
