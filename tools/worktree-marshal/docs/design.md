# Worktree Marshal Design

## Product boundary

Worktree Marshal is a transactional supervisor for coding-agent work in Git
repositories. It allocates independent worktrees, records durable run state,
audits results, and performs explicitly authorized cleanup or integration.
Several Marshal processes may run concurrently; Marshal is not a prompt
scheduler, agent-message bus, model router, or task-DAG engine.

The first supported agent is Codex because the Triptych launcher already has a
tested, default-deny Codex argument and sandbox policy. Supporting another
agent requires an explicit adapter and sandbox capability; accepting an
arbitrary executable is not equivalent support.

## Intended package boundaries

The current package deliberately keeps lifecycle transition selection,
validation, persistence, and orchestration in one shared `engine.py`. `cli.py`
owns the installed grammar, `profiles.py` owns immutable durable profile
identities, `git.py` now owns only the cycle-free Git policy kernel, `model.py`
now owns the exact state vocabulary, pure classifier, and I/O-free
integration-transaction restoration transform, `state.py` now owns run
identity, state-location selection, repository-name normalization, and lexical
lock and manifest paths, `identity.py` now owns immutable runtime identity
records and launcher-entry authentication, `locks.py` now owns lock-descriptor
bookkeeping and validation algorithms, `process.py` now owns child waiting and
exit-status normalization, and `triptych_compat.py` binds the frozen adapter.
The rest of the engine will be separated behind these modules only after
parity tests protect each seam:

```text
worktree_marshal/
  cli.py                 command parsing and stable exit behavior
  model.py               state vocabulary and transaction restoration now
  state.py               run identity, state-base policy, and lexical paths; writes later
  locks.py               descriptor bookkeeping now; flock acquisition later
  git.py                 transforms and captured-config policy now; invocation later
  process.py             child signal forwarding and exit normalization
  identity.py            runtime records and launcher authentication now; other authentication later
  worktrees.py           allocation, audit, reopen, and cleanup
  integration.py         verification, rebase, landing, and rollback
  conflicts.py           resolver scope, continuation, and abort
  retirement.py          separately authorized destructive retirement
  adapters/base.py       agent contract and declared capabilities
  adapters/codex.py      Codex argv, environment, and sandbox policy
  sandboxes/base.py      enforcement contract independent of an adapter
  resources/             generated integration assets such as the Make fragment
```

Integration, conflict, and retirement workflows remain together until their
durable invariants have direct state-machine tests. File boundaries are not a
reason to weaken an atomic lifecycle operation.

## Trust model

A linked worktree is an isolation mechanism for cooperative development, not
an operating-system security boundary. Linked worktrees share Git
administration and object storage, and a same-user unconfined process can
potentially reach launcher state, other checkouts, credentials, and the
network. Post-run auditing detects and contains many mistakes and races but
cannot prove that hostile code never touched unrelated state.

An `AgentAdapter` owns accepted arguments and environment construction. A
separate `SandboxBackend` owns enforceable filesystem, process, and network
claims. Marshal must not infer sandbox assurance merely because an adapter
exists. Any future trusted-command adapter must be an explicit opt-in and must
state that it is unconfined.

## Extraction sequence

1. Freeze the schema-1 Triptych compatibility contract and extract the Make
   API without moving lifecycle behavior.
2. Relocate the existing launcher behind a thin `scripts/triptych-codex`
   compatibility entry point, preserving state paths, refs, environment names,
   diagnostics, and every retained run.
3. Add wheel and source-distribution parity tests, including installation of a
   wheel rebuilt from the source distribution.
4. Introduce the explicit `generic-v1` profile and generic branding while
   keeping the Codex adapter as the only supported confined agent and the
   Triptych domain available only by explicit compatibility selection.
5. Split pure identity, state, locking, Git, and process helpers; encode valid
   state transitions before separating integration and recovery logic.
6. Publish a `0.x` release only after installation outside the Triptych
   checkout passes the complete lifecycle suite.
7. Add another agent or stronger workspace backend only with its own threat
   model, enforcement tests, and explicit capability declaration.

Each step remains behavior-preserving unless it includes a documented state or
command migration. A new installation never implies permission to migrate,
integrate, clean, retire, push, or deploy a run.

The repository currently implements steps 1 through 4 as pre-release seams and
has begun step 5 with ten behavior-preserving boundaries. The pure Git policy
kernel now transforms an explicit environment mapping and Git argument
sequence in `git.py`; `engine.py` retains its optional environment-acquisition
wrapper and all executable discovery, subprocess creation and command
execution, lock acquisition, repository authentication, configuration
probing, ref transactions, and lifecycle orchestration.
The second cycle-free boundary places the exact durable state vocabulary, the
existing retirement-pending and managed-conflict families, and a pure
classifier in `model.py`. Manifest validation uses that predicate while
retaining its exact diagnostics and engine-global rebinding behavior. The
third boundary moves the ordered integration-transaction and manual-landing
field inventories plus their deterministic in-place clear/archive transform
into `model.py`. Engine wrappers retain their existing signatures, pass their
current field inventories explicitly, acquire the abort timestamp only after
the transform, and continue to own transition selection, validation, durable
writes, and recovery. The transform deliberately preserves the existing
direct-call behavior of restoring any string previous state; manifest loading
still validates durable states separately. A transition graph, typed run
records, checkpoint validation, and all recovery choices remain deferred.
The fourth boundary moves the immutable registered-lock descriptor and the
register, unregister, stale-entry pruning, identity-validation, and
sorted-selection algorithms into `locks.py`. Explicit resolvers let engine
wrappers obtain the current registry and record factory at the same operation
points as before, preserving even reentrant rebinding behavior. The
process-global registry, repository and per-run lock paths, `flock` acquisition
and release, subprocess `pass_fds`, and lifecycle lock ownership remain in
`engine.py`. The fifth boundary moves only the existing child wait loop,
temporary `SIGHUP` and `SIGTERM` forwarding, interrupt escalation, handler
restoration after successful setup, and negative-return-code normalization
into `process.py`. The engine wrapper supplies lazy resolvers at the original
signal-operation, handled-exception, timeout, and negative-status
absolute-value lookup points. Process creation, command execution, executable
discovery, arguments, environments, inherited descriptors, and post-exit
lifecycle decisions remain in `engine.py`. Direct tests also retain the legacy
partial-setup behavior: a failure while installing the second handler occurs
before the protected wait and does not roll back the first installation.
The sixth boundary extends `git.py` with deterministic parsing and rejection
of command-bearing values in the effective-configuration bytes captured by the
engine. The engine retains working-directory authentication, the exact Git
configuration probe, unsuccessful-probe diagnosis, executable pinning, and
subprocess execution. Lazy resolvers preserve the engine's existing
configuration-policy and error lookups at their original decision points.
The seventh boundary moves the exact run-ID grammar, dependency-injected
timestamp and random-suffix composition, and lexical repository-lock,
run-lock, and manifest path construction into `state.py`. Engine wrappers
retain their original signatures, profile-aware invalid-ID diagnostics, and
lazy clock and entropy lookup order. These constructors intentionally perform
no validation, resolution, authentication, directory creation, or filesystem
access. That boundary left state-base selection and every stateful operation
in `engine.py`.
The eighth boundary extends `state.py` with the existing profile-override,
`XDG_STATE_HOME`, and home-fallback selection policy plus ASCII
filtering for repository slugs. The state-base wrapper retains its signature,
resolves the active profile once, and supplies lazy environment, path, home,
and error dependencies. The repository-slug wrapper retains its signature and
captures the current substitution operation before reading the repository
name. Repository digest calculation, final state-root joining and resolution,
outside-worktree containment rejection, directory creation, authentication,
and all durable writes remain in `engine.py`.
The ninth boundary moves only the frozen `Repository`,
`LinkedWorktreeIdentity`, and `LauncherIdentity` records into `identity.py`.
The engine imports and re-exports those exact class objects, so existing
constructors and type comparisons keep their established surface. Their
canonical Python module and new pickle provenance are now `identity.py`; the
engine aliases keep old engine-qualified lookups resolvable, and Marshal does
not persist these records with pickle. That record-only checkpoint did not
perform validation or I/O.
The tenth boundary moves only the existing in-process launcher-entry
authentication operation into `identity.py`. Its exact-signature engine
wrapper supplies lazy resolvers for the current operating-system error and
launcher error types, regular-file predicate, executable access operation and
mode, and identity factory. This preserves lexical absolute-path rejection,
strict resolution followed by metadata capture, short-circuiting regular-file
and executable checks, late identity construction, the three exact
diagnostics, and the narrow rule that only resolution or metadata-read
operating-system errors are translated and chained. The operation
authenticates a read-only path snapshot; it deliberately does not strengthen
the existing stat/access race into descriptor-based authentication. Launcher
sequencing, the public error type, Git executable pinning and discovery,
repository and linked-worktree authentication, identity caches, all other
path and file authentication, lifecycle decisions, and every mutation remain
in `engine.py`.
Direct tests freeze all ten extracted boundaries, their
compatibility surfaces, artifact inclusion, field and operation order,
partial-failure behavior, and the dynamic restoration of every vocabulary
value currently accepted in
`integration_previous_state` before any graph is introduced. The Make API and
legacy contract are frozen; the shared engine is
co-located behind the thin `scripts/triptych-codex` bootstrap; wheel and source
artifacts are built, a wheel is rebuilt from the extracted source artifact,
and that wheel is installed and checked outside the source checkout without
source-tree import paths; and the generic console requires the versioned,
separately named `generic-v1` state profile. The installed artifact now also
passes a bounded
stateful checkpoint covering generic preservation, integration, and cleanup
through the packaged unprefixed Make targets; bidirectional Triptych schema-1
run, status, and clean interoperability through the packaged compatibility
adapter; cross-profile selected-run lookup isolation without manifest
mutation; and generic installed-console alias rejection. A second installed
checkpoint now covers the generic packaged Make conflict flow through
resolution, continuation, opaque final-diff review, and fresh exact-candidate
landing, plus exact Triptych source restoration when aborting after a staged
resolution. A third installed checkpoint covers two deliberately overlapping
generic runs with distinct locked namespaces and isolated committed results,
followed by serial packaged Make integration: one direct fast-forward and one
conflict-free rebase onto the captured advanced target. The latter lands a
linear candidate containing both results, records its exact integration
identities, and cleans the generic worker namespace. This does not establish
scheduling throughput, concurrent integration, target-race handling, or crash
recovery. A fourth installed checkpoint covers direct generic retirement of one
eligible clean rewritten quarantine. It verifies representative non-mutating
refusals, the exact discard, containment, initial-target, and cleanup-target
identities, unchanged target and control state, bounded removal of the worker
and its exact namespace as observed at completion, retention of the cleaned
manifest, durable completion checkpoints, and completed-state exact-command
idempotency across the manifest, refs, worktree registrations, and surviving
sentinels. The containment checkpoint proves reachability only, not
incorporation or semantic supersession.

The retirement checkpoint does not establish the full eligibility and refusal
matrix, target-race, tamper, active-worker, interrupted-checkpoint,
worktree-removal, ref-transaction, receipt-recovery, garbage-collection, or
concurrent-retirement behavior. Those cases and the broader recovery, security,
complete installed-lifecycle, and supported Python and Git CI matrices remain
release gates. These bounded checkpoints advance but do not satisfy step 6.

## Distribution and repository integration

The extracted project is a standard Python package named `worktree-marshal`,
requires Python 3.10 or newer on POSIX, has no runtime dependency beyond the
standard library and Git, and is licensed under MIT. Release artifacts should
be reproducible wheels and source distributions published from a dedicated
repository after signed tags and CI across supported Python and Git versions.

End users should install a pinned release with an isolated application
installer such as `pipx` or `uv tool`. A package command will write a versioned
Make fragment into a repository so Make does not execute Python merely to find
an installed resource at parse time. The fragment defaults to the plain
targets `codex`, `status`, `reopen`, `final-diff`, `integrate`, `resolve`,
`continue`, `abort`, and `clean-run`; projects may configure those names before
generation when they conflict. Generated configuration is fixed Makefile code,
not invocation-controlled shell input, and target names use a restricted
literal grammar. The native CLI remains canonical for automation and for any
run ID not obtained from the local launcher.
