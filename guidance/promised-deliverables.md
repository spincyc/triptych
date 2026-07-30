# Promised deliverables

`PROJECT-WORK.md` and `promised-deliverables.toml` are the repository's
provider-neutral, fail-closed operational memory. They survive a particular
provider, agent, process, machine, or conversation context. `PROJECT-WORK.md`
is the human-readable status, discrepancy, and reconciliation record; the TOML
ledger is the mechanically checked promise and acceptance-criterion record.
Neither belongs under a provider branch.

Read both files before beginning or resuming project work, after any context
compaction or handoff, before reporting status or completion, and before each
commit. Reconcile them after every material scope decision and completed work
unit. A later process must recover the requested outcome, exact current state,
work already performed, evidence paths, open requirements, blockers, and
superseded decisions from tracked files without relying on chat history.

Record a substantive conversation outcome before material implementation.
Give it a stable ID; state what was requested, what has and has not been done,
where its evidence lives, and what proves completion. Never record prompts,
private reasoning, provider runtime details, usernames, machine paths, session
identifiers, or ephemeral process state. If earlier conversation cannot be
recovered exactly, record the known requirement and the uncertainty rather
than silently narrowing it.

Each `[[deliverables]]` entry has a stable `id`, a tracked `owner`, a concise
`promise`, and a workflow `state`: `planned`, `in_progress`, `blocked`,
`candidate`, or `complete`. Each nested requirement has a stable `id`, an
objective criterion, and a status: `open`, `blocked`, `pass`, or `waived`.
Waivers require both `waiver_reason` and `waiver_authority`.

A `pass` requirement must name at least one tracked evidence path. It may also
declare one mechanical check:

- `path_exists`: every evidence path exists;
- `contains`: `path` contains the literal `needle`;
- `pdf_min_pages`: `path` is a PDF with at least `minimum` physical pages.

The validator rejects duplicate identifiers, missing owners or evidence,
unsupported states and checks, and any `complete` deliverable with an open,
blocked, or unproved requirement. A `candidate` is not complete. A released
artifact is not complete merely because its bytes and release binding agree.
Review status controls reader-facing labeling; it must not be used to remove a
tracked deliverable from ordinary discovery.

Add a requirement before beginning material work when a request changes scope.
Do not weaken or delete an unmet requirement. Supersede it with a new
requirement or record an explicit user-authorized waiver. Completion claims in
commit messages, catalogs, release notes, or handoffs are permitted only when
`tools/tpt check-promised-deliverables --require-complete <id>` passes.

Keep coherent commits small enough that completed work is durably checkpointed
without waiting for an unrelated workstream. A clean direct Codex session on
`main` has standing authority to make ordinary coherent commits for authorized
work and regularly push validated checkpoints to `origin/main` after each
independently reviewable unit. Before each push, run the checks required by the
affected guidance, inspect the exact outgoing range, and confirm that every
newly reachable object is intended for public disclosure. An `origin/main`
push authorizes the automatic GitHub Pages deployment attempt that it triggers;
verify the workflow and affected production routes before representing the
snapshot as live. This standing authority does not permit force-pushing,
amending or otherwise rewriting published history, changing remotes,
integrating a retained worker, or triggering another deployment mechanism. A
commit, push, installed artifact, catalog link, or deployed page remains
evidence of that state only; none substitutes for an unmet acceptance
criterion.

Each ledger ID must have exactly one
`<!-- promised-deliverable: ID -->` marker in `PROJECT-WORK.md`. The register
also records audit findings that are not yet sufficiently specified as user
promises. Promote such a finding into the TOML ledger as soon as its promised
outcome and completion criteria are known.
