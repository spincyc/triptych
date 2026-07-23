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

The current package deliberately keeps lifecycle transitions in one shared
`engine.py`. `cli.py` owns the installed grammar, `profiles.py` owns immutable
durable identities, and `triptych_compat.py` binds the frozen adapter. The
engine will be separated behind these modules only after parity tests protect
each seam:

```text
worktree_marshal/
  cli.py                 command parsing and stable exit behavior
  model.py               typed run records and state transitions
  state.py               private paths and durable manifest writes
  locks.py               repository and per-run locking
  git.py                 hardened Git invocation and ref transactions
  identity.py            repository, checkout, and path authentication
  worktrees.py           allocation, audit, reopen, and cleanup
  integration.py         verification, rebase, landing, and rollback
  conflicts.py           resolver scope, continuation, and abort
  retirement.py          separately authorized destructive retirement
  adapters/base.py       agent contract and declared capabilities
  adapters/codex.py      Codex argv, environment, and sandbox policy
  sandboxes/base.py      enforcement contract independent of an adapter
  resources/             generated integration assets such as the Make fragment
```

Integration, conflict, and retirement transitions remain together until their
durable invariants have direct state-machine tests. File boundaries are not a
reason to weaken an atomic transition.

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

The repository currently implements steps 1 through 4 as pre-release seams:
the Make API and legacy contract are frozen; the shared engine is co-located
behind the thin `scripts/triptych-codex` bootstrap; wheel and source artifacts
are built, a wheel is rebuilt from the extracted source artifact, and that
wheel is installed and checked outside the source checkout without source-tree
import paths; and the generic console requires the versioned, separately named
`generic-v1` state profile. The installed artifact now also passes a bounded
stateful checkpoint covering generic preservation, integration, and cleanup
through the packaged unprefixed Make targets; bidirectional Triptych schema-1
run, status, and clean interoperability through the packaged compatibility
adapter; cross-profile selected-run lookup isolation without manifest
mutation; and generic installed-console alias rejection. The next
installed-artifact checkpoint covers managed conflict resolution,
continuation, abort, and final-diff. Retirement, concurrency, crash recovery,
and broader security coverage remain release gates. This bounded checkpoint
advances but does not satisfy step 6: a release still waits on the complete
installed lifecycle matrix and the broader CI gate.

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
