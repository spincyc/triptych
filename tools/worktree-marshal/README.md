# Worktree Marshal

Transactional Git worktrees for coding agents.

## Extraction status

This directory contains the shared lifecycle engine, its first extracted
cycle-free Git policy, durable-state vocabulary, and integration-transaction
restoration seams, its lock-descriptor bookkeeping boundary, its first generic
profile, its child-process supervision boundary, its run-identity and lexical
state-path boundary, its state-location and repository-name boundary, the
frozen Triptych compatibility adapter, the Python distribution, and the Make
integration fragment. The repository-local
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
console, including symbolic- and hard-link aliases. It also passes a managed
conflict checkpoint: the generic packaged Make flow retains a conflict, stages
a resolver result, continues to a review-pending candidate, renders an opaque
read-only final diff, and lands that exact candidate only on a fresh integrate;
the installed Triptych adapter discards a staged resolution and restores the
exact audited source on abort. A further installed checkpoint starts two
deliberately overlapping generic run invocations from one unchanged control
base and verifies distinct run IDs, branches, locked worktrees, active run
locks, temporary roots, and isolated committed results without entering the
Triptych state domain. Serial integration through the packaged Make targets
then lands the first result by fast-forward and rebases the second result onto
that advanced target. The rebased landing records the exact source, target,
candidate, and integrated heads and produces linear no-merge history containing
both results; both integrations clean their worker namespaces. These bounded
overlap and non-racing integration checks do not establish scheduler
throughput, concurrent integration, target-race handling, or recovery
guarantees.

A fourth installed checkpoint creates one eligible clean rewritten generic
quarantine through the installed run and reopen commands. It verifies that no
Make retirement target exists, ordinary cleanup cannot acquire destructive
authority, and representative wrong full object IDs leave the quarantine
unchanged. The exact direct-only retirement command records the selected
discard and target-containment identities while leaving the target and control
checkout unchanged. Its manifest records the completed worktree-removal,
ref-transaction, and receipt-removal checkpoints; afterward the worker
worktree, run temporary directory, worker branch, and exact per-run retirement
refs are absent, while the cleaned manifest, adjacent state, and an unrelated
ref remain. An immediate repeat with the identical command and object IDs
leaves that manifest, the target and control snapshot, the ref set, worktree
registrations, and surviving sentinels unchanged; changed valid object IDs are
refused. The selected target checkpoint establishes reachability only, not
incorporation, semantic equivalence, or supersession of the discarded history.

This is one stable-target retirement happy path, representative pre-checkpoint
refusals, and completed-state exact-command idempotency. It does not cover the
full eligibility and refusal matrix, target races or lost containment,
active-worker, path, manifest, or ref tampering, interrupted checkpoints,
worktree-removal or ref-transaction failures, receipt recovery, garbage
collection, or concurrent retirement. Those retirement cases, broader crash
and race recovery, broader security coverage, the complete installed lifecycle
matrix, and the supported Python and Git CI matrix remain release gates; the
first eight step-5 seams are protected by direct source tests and artifact
provenance, and the installed abort checkpoint covers archived transaction
restoration. Each remaining helper boundary still requires its own direct
parity coverage.

Step 5 has begun narrowly: [`git.py`](src/worktree_marshal/git.py) owns only
the deterministic environment and argument transforms, their fixed policy
constants, and validation of effective-configuration bytes captured by the
engine. The engine still authenticates the repository, executes the exact
configuration probe, and diagnoses probe failure. Direct tests freeze those
seams, their source-copy behavior, and their wheel and source-distribution
presence.

[`model.py`](src/worktree_marshal/model.py) now owns the exact durable state
vocabulary, its two existing pending-state families, and the pure predicate
used by manifest validation. It also owns the ordered integration-transaction
field inventories and the deterministic in-place transform used to clear or
archive a transaction and restore its recorded prior state. The existing
engine wrappers still choose when to apply that transform, acquire the archive
timestamp afterward, and own validation, persistence, and recovery. Typed run
records and transition-graph enforcement remain deferred. Executable
discovery, subprocess creation and command execution, repository
authentication, effective-configuration probing, ref transactions, and
lifecycle orchestration also remain together in `engine.py`.

[`state.py`](src/worktree_marshal/state.py) owns only the exact run-ID grammar,
dependency-injected timestamp and random-suffix composition, and lexical
repository-lock, run-lock, and manifest path construction. It now also owns
the dependency-injected precedence policy that selects a profile override,
`XDG_STATE_HOME`, or the home-directory fallback, plus ASCII repository-name
filtering for repository slugs. Engine wrappers retain their existing signatures,
profile-aware invalid-ID and relative-path diagnostics, and lazy environment,
path, home, error, clock, and entropy lookups. State-base selection acquires
the current profile once, and repository normalization captures the current
substitution operation before reading the repository name. These helpers do
not resolve, authenticate, create, or otherwise touch a selected path.
Repository digesting, final state-root construction and containment rejection,
private-directory setup, the profile marker, manifest persistence and
validation, temporary-path authentication, lock acquisition, and all lifecycle
decisions remain in `engine.py`.

[`locks.py`](src/worktree_marshal/locks.py) owns only the immutable registered
descriptor record and the algorithms that register, unregister, authenticate,
prune, and sort descriptors inherited by child processes through explicit
registry and record-factory resolvers. The engine retains the process-global
registry, Repository-bound path wrappers, `flock` acquisition and release,
subprocess propagation, and every lifecycle locking decision in `engine.py`.

[`process.py`](src/worktree_marshal/process.py) owns only the existing child
wait loop, temporary `SIGHUP` and `SIGTERM` forwarding, interrupt escalation,
handler restoration after successful setup, and negative-return-code
normalization. The engine wrapper supplies lazy resolvers for signal operations,
handled exception classes, timeout matching, and negative-status absolute-value
calculation, preserving its existing global rebinding behavior. The engine
still creates every process, chooses its arguments, environment, working
directory, and inherited descriptors, and owns all post-exit lifecycle
decisions. The frozen legacy contract and current security boundary are
recorded in
[`docs/compatibility-contract.md`](docs/compatibility-contract.md); the target
architecture and release sequence are in [`docs/design.md`](docs/design.md).

## Development check

From this directory, run the package tests with:

```sh
python3 -m unittest discover -s tests -t . -v
```

This package suite includes artifact-content checks and the bounded
installed-artifact lifecycle checkpoints described above; it does not yet run
the complete legacy lifecycle matrix against the installed console.

The repository's `make check-agent-isolation` target additionally runs the
complete Triptych lifecycle suite through the thin compatibility bootstrap.

The initial package uses only the Python standard library at runtime and
requires Python 3.10 or newer. Its source is licensed under the MIT License.
