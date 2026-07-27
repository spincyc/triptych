# Promised deliverables

`promised-deliverables.toml` is the repository's fail-closed record of work
that a reader or maintainer was told would be completed. It records the
requested outcome separately from publication, review, release, and
discoverability state.

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
`scripts/check-promised-deliverables --require-complete <id>` passes.
