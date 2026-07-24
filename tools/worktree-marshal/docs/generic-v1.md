# Generic v1 Profile Contract

## Selection and command grammar

`generic-v1` is Worktree Marshal's first native lifecycle profile. Every
stateful invocation begins with the exact, case-sensitive tokens
`worktree-marshal --profile generic-v1`. Profiles are not selected from the
environment, repository configuration, filesystem contents, or a retained run
ID. Only top-level `--help` and `--version` operate without a profile, and they
do not discover Git or create state.

The commands are:

```text
run --agent codex [-- CODEX_ARGUMENTS...]
status [RUN_ID]
reopen RUN_ID [-- CODEX_ARGUMENTS...]
final-diff RUN_ID
integrate RUN_ID
resolve RUN_ID
continue RUN_ID
abort RUN_ID
clean RUN_ID
retire RUN_ID --discard-head FULL_OID --target-contains FULL_OID
```

Codex arguments after `run` or `reopen` require the literal `--` delimiter.
`retire` is a destructive, direct-only exception and deliberately has no Make
wrapper. Run IDs and object IDs remain opaque inputs to the lifecycle engine.

## Durable identity

The profile owns these exact identifiers:

- profile ID `generic-v1`, manifest format `worktree-marshal-run`, manifest
  schema integer `1`, and agent ID `codex`;
- diagnostic name `worktree-marshal`;
- worker branch prefix `worktree-marshal/generic-v1/isolated/`;
- private ref prefix `refs/worktree-marshal/generic-v1/runs/`;
- linked-worktree lock reason prefix `worktree-marshal generic-v1 `; and
- environment variables `WORKTREE_MARSHAL_ROLE`,
  `WORKTREE_MARSHAL_RUN_ID`, `WORKTREE_MARSHAL_PROFILE_ID`,
  `WORKTREE_MARSHAL_AGENT_ID`, `WORKTREE_MARSHAL_REAL_CODEX`, and
  `WORKTREE_MARSHAL_STATE_DIR`.

Without an override, state begins at
`$XDG_STATE_HOME/worktree-marshal/profiles/generic-v1` when
`XDG_STATE_HOME` is set to an absolute path. When it is unset, state begins at
`$HOME/.local/state/worktree-marshal/profiles/generic-v1`; a set relative
`XDG_STATE_HOME` is rejected. An absolute
`WORKTREE_MARSHAL_STATE_DIR` names the Worktree Marshal state base, below
which the profile still appends `profiles/generic-v1`. Each repository then
uses the same normalized-name and common-Git-directory digest scheme as the
compatibility engine.

Each repository state root contains a `profile.json` marker. The marker is
authenticated before its repository lock, run manifests, worktrees, or
temporary paths are used. A generic run manifest includes the exact
`format_id`, `profile_id`, and `agent` values above in addition to the shared
lifecycle fields.

## Codex executable selection

A nonempty `WORKTREE_MARSHAL_REAL_CODEX` value is the sole executable
candidate and must be an absolute path. When it is absent or empty, Marshal
scans the inherited executable path in order for the literal name `codex`,
treating an empty entry as the current directory. It skips candidates whose
metadata cannot be read, that are not regular executable files, that fail the
executable access check, or whose followed device and inode match the
authenticated launcher snapshot. It returns the selected spelling using
`candidate.absolute()`, not a canonical resolution.

The exact failures are
`WORKTREE_MARSHAL_REAL_CODEX must be an absolute path`,
`WORKTREE_MARSHAL_REAL_CODEX does not name a usable non-launcher executable`,
and `cannot find the real Codex executable; set WORKTREE_MARSHAL_REAL_CODEX`
for, respectively, a relative override, an unusable override, and unsuccessful
inherited-path search.

This is point-in-time selection of a usable non-launcher candidate. It does not
authenticate provenance, signature, version, or actual Codex behavior;
distinguish a copy or wrapper; pin a file descriptor or device/inode identity;
close the stat/access/use replacement window; or establish sandbox assurance.
Metadata lookup follows symbolic links, and the selected link or file may
later be replaced. Executable selection does not alter the profile's durable
identity, discover or migrate retained runs, or grant lifecycle authority.
The engine continues to bind the profile and own Codex arguments, child and
resolver environments, sandbox-enforcement arguments, process creation, and
post-exit lifecycle policy.

## Isolation and compatibility

The generic profile and Triptych schema 1 are separate coordination domains.
They may contain identical-looking run IDs without referring to the same run.
Generic operations inspect only generic state and refs and never fall back to,
migrate, or mutate Triptych state. The explicit `triptych` profile is the only
installed-command route to the compatibility adapter. There is no migration
command in v1.

All built-in managed-worktree markers, lock prefixes, and branch prefixes are
recognized when refusing nested agent allocation, regardless of which profile
the nested command selected. Selection changes durable identity, not the
underlying safety model: `generic-v1` supports only the hardened Codex adapter
and does not accept an arbitrary executable.

## Make integration

The packaged fragment defaults to `--profile generic-v1` and the unprefixed
targets `codex`, `status`, `reopen`, `final-diff`, `integrate`, `resolve`,
`continue`, `abort`, and `clean-run`. Lifecycle targets take a validated
command-line `RUN=<run-id>`; the status overview needs no run ID. A repository
may pin trusted fixed global arguments while importing the fragment, but Make
invocations and the environment may not override them.
