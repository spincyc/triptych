# External-review handoffs

## Status and scope

This document governs the review package a Codex task creates when it requires
judgment outside the active task for visual, product, source, architectural, or
acceptance review. It standardizes the transfer of evidence; it does not grant
authority to contact a reviewer, publish an artifact, accept a milestone, or
change the underlying work.

The handoff is an ignored review output under `build/`. Durable product,
source, acceptance, and implementation decisions remain in their tracked
owners. Creating a package is not evidence that an external reviewer approved
it. When approval or a blocking finding affects the repository, record that
disposition in the owning roadmap, research record, or other tracked authority.

## Trigger

Use this protocol whenever a task, roadmap, profile, acceptance gate, or user
requires external review of any of these:

- visual or responsive behavior;
- product behavior or information architecture;
- source selection, provenance, rights, or historical claims;
- software or data architecture; or
- acceptance of a milestone, release candidate, or promised outcome.

An ordinary internal self-review does not trigger the protocol unless its task
or governing guidance calls for external judgment. The requirement to prepare a
handoff does not itself authorize sending it or taking an external action.

## Identity and location

Take one UTC timestamp when the package is ready to be assembled:

```text
YYYYMMDDTHHMMSSZ
```

Combine it with a short lowercase kebab-case task slug:

```text
build/agent-handoffs/<UTC_TIMESTAMP>-<short-task-slug>/
build/agent-handoffs/<UTC_TIMESTAMP>-<short-task-slug>.zip
```

For example:

```text
build/agent-handoffs/20260803T150000Z-liturgy-browser-vision/
build/agent-handoffs/20260803T150000Z-liturgy-browser-vision.zip
```

The timestamp makes the name compact, sortable, and unambiguous. The slug
identifies the reviewed task rather than a person, agent, or session.

Before creating anything, check both paths. **Never reuse, merge into, replace,
or overwrite an existing handoff directory or archive.** If either path exists,
take a new current UTC timestamp and create a new pair. Do not “refresh” an old
package in place; a corrected or superseding handoff is a new package that names
the earlier one in `HANDOFF.md`.

## Required core files

Every handoff contains these four files.

### `HANDOFF.md`

This is the factual entry point. It contains:

1. task and intended outcome;
2. current branch, or `detached HEAD` when applicable;
3. current commit SHA and the task's base commit when known;
4. whether the reviewed state includes uncommitted changes;
5. focused files changed;
6. preview URLs or exact startup commands, including required route state;
7. implementation summary;
8. known limitations;
9. unresolved decisions; and
10. artifact inventory, including why any conditional artifact class was
    omitted.

Use repository-relative paths inside the package. Do not include credentials,
private hosts, user names, machine identifiers, session identifiers, or other
machine-private values. A local startup command uses repository-relative paths
and documented prerequisites. A public preview URL may include nonsecret route
state needed to reproduce the review.

### `REVIEW_REQUEST.md`

This file contains only questions that need external judgment. Divide them into
`Blockers` and `Optional feedback`. Each blocker says which acceptance decision
cannot be made without its answer and points to the relevant artifact or state.
Optional questions are concrete and independently answerable. Use `None` when a
section has no questions.

Do not repeat the implementation summary, paste a generic review checklist, or
ask whether the work “looks good.” The reviewer must be able to tell exactly
what judgment is requested and which answers prevent acceptance.

### `changes.patch`

This is the focused relevant diff. Prefer a diff from the task's recorded base
commit to the reviewed commit, limited to the task's paths and with renames
detected. If the reviewed state is intentionally uncommitted, include the
focused worktree and index diff against the recorded base and say so in
`HANDOFF.md`.

Do not include unrelated changes merely because they share a checkout. When no
repository diff exists, keep the file and explain the zero-diff review scope at
its top rather than substituting an unrelated patch.

### `checks.txt`

For each relevant check, record:

- the exact command;
- its numeric exit status;
- a concise result; and
- any material qualification.

Record skipped checks in a separate `Skipped` section with the reason. Do not
write `passed` for a command that was not run, hide a failing exit status inside
a prose summary, or paste unbounded logs here. A relevant failure log belongs
under `logs/` and is referenced from the concise entry.

## Conditional artifacts

### `screenshots/`

Include screenshots when the review concerns browser-visible behavior,
rendered publications, visual acceptance, responsive behavior, print, or a
task or roadmap that requires them.

- Name every image by route or surface, state, and viewport, for example
  `day--read-default--393x852.png`.
- Include the desktop and mobile states required by the applicable task,
  profile, or roadmap.
- When visual behavior changed, include comparable `before--...` and
  `after--...` images unless the before state cannot lawfully or technically be
  reproduced; record that limit in `HANDOFF.md`.
- Capture real supported states. Do not alter production data merely to
  manufacture a screenshot.
- Record full-page, focused-region, print, forced-color, or other variants in
  the filename when they are not ordinary viewport captures.

Screenshots support judgment; they do not replace DOM, accessibility,
interaction, source, or semantic checks.

### `logs/`

Include only logs relevant to the requested review: browser console,
accessibility, performance, or focused failure output. Give each log a specific
name such as `day--read-default--393x852--console.txt`. Exclude routine verbose
build output, caches, credentials, private URLs, and machine identifiers.

### `sources.md`

Include this file when the task involved research, standards, provenance,
rights, source selection, historical claims, or source-grounded architecture.
It names the sources actually used, their role, the checked locus or URL, the
date when mutability matters, and the reasoning the reviewer must evaluate.
Keep verified sources, repository evidence, inference, and unresolved leads
distinct. Do not copy protected source material merely to make the package
self-contained.

If a conditional class does not apply, omit its directory or file and state the
reason in the `HANDOFF.md` artifact inventory. Do not create empty screenshot or
log directories to imply review evidence exists.

## Assembly and verification

Assemble a handoff only after the reviewed state, focused diff, checks, and
conditional artifacts are known. Use this order:

1. resolve the exact branch, current commit, task base, changed paths, preview
   state, and requested external judgments;
2. allocate a new timestamped directory after proving neither target exists;
3. write the core files and applicable conditional artifacts;
4. audit the artifact inventory, private-data boundary, and focused patch;
5. from `build/agent-handoffs/`, create the sibling ZIP so the archive contains
   the complete timestamped directory as its top-level entry and stores no
   absolute paths;
6. list or test the ZIP and confirm every inventory entry is present; and
7. leave both outputs under ignored `build/` unless the task explicitly
   requires them to be tracked.

The ZIP is a transport copy of the directory, not a second hand-authored
record. Create it only after the directory is complete. Never update an
existing ZIP in place.

## Acceptance and final reporting

When external review is an acceptance gate, keep the milestone open until the
reviewer has answered every blocking question and the owning tracked record
states the disposition. Optional feedback may remain open if the owning gate
allows it. Neither a successful archive command nor a screenshot set marks work
accepted.

The task's final response prints all four of these facts explicitly:

- absolute handoff directory path;
- whether the directory was successfully created;
- absolute ZIP path; and
- whether the ZIP was successfully created and verified.

Handoff artifacts under `build/` are review outputs and are not committed
unless the task expressly requires that exception. Confirm their absence from
the staged and outgoing ranges before committing or pushing.
