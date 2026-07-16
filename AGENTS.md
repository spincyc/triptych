# Repository Instructions

## Project

This repository contains **Triptych: AI Driven Studies in Catholic Faith, Worship, and Law** (`triptych`), a source-first collection of liturgical, theological, and canonical study documents.

Read these files before changing document content, structure, or build behavior:

1. `README.md` for the public consumer overview, `LIBRARY.md` for the catalog index, and the section pages under `library/` for publication listings and supporting records.
2. `CONTRIBUTING.md` for the public contribution paths and ordinary-language agent workflow.
3. `LICENSE` and `THIRD_PARTY.md` for the applicable license boundary and excluded source material.
4. `guidance/editorial.md` for the universal evidence, attribution, metadata, review, and publication standard.
5. `guidance/repository.md` for source ownership, target paths, mirrored publications, and build rules.
6. The one or more profiles that govern the requested document.

The user's request takes priority when it deliberately changes a project convention. Record the new convention in the correct universal or profile guidance rather than leaving the implementation and guidance inconsistent.

## Profile routing

Select profiles by the document's actual genre and sources, not by superficial similarity:

- 1962 Roman Rite temporal, ritual, votive, or other proper guides: `guidance/liturgy/roman-1962-propers.md`
- edition-specific references for assembling the Ordinary and propers under the 1962 calendar and rubrics: `guidance/liturgy/roman-1962-assembly.md`
- postconciliar Roman Rite proper guides: `guidance/liturgy/postconciliar-propers.md`
- expositions of the Ordinary or Order of Mass in either form: `guidance/liturgy/ordinary-expositions.md`
- the sacramental treatise, at-a-glance companion, or their shared fragments: `guidance/theology/sacramental-reference.md`
- the Rosary, Marian-apparition judgment studies, or other repeatable Mariological reference works: `guidance/theology/mariology.md`
- historical and hagiographic lives in the biographies collection: `guidance/biographies.md`
- novenas and other works in the numbered novena collection: `guidance/devotions/novenas.md`
- discursive articles on faith, theology, or canon law: `guidance/articles.md`

A document may require more than one profile only when it truly combines genres. For example, a canonical article about a liturgical question follows the articles profile for its argument and the relevant liturgical profile for edition-specific textual claims. State which profile governs each part rather than merging their templates.

The sacramental treatise and its at-a-glance companion are established theological reference works with shared canonical fragments. Follow the universal guidance, their sacramental-reference profile, and their local research scope; do not impose a Mass-propers or discursive-article template on them.

If no profile fits a requested repeatable series, add or revise a profile before multiplying documents. Keep universal guidance genre-neutral. Put rite-, edition-, locale-, calendar-, jurisdiction-, page-, and section-specific rules in the appropriate profile, not in this file or the universal editorial standard.

## Isolated agent sessions

Mutating Codex CLI sessions must run in the isolated linked worktree assigned by `scripts/triptych-codex`. The primary checkout is a control and integration checkout, not an autonomous worker workspace. A session already running in a linked worktree remains there and must not invoke the launcher again or create, remove, lock, unlock, prune, or enter another worktree.

If a mutating Codex session starts in the primary checkout without isolation, fail closed: do not edit, build, commit, or try to emulate relocation with a shell `cd`. Read-only inspection may continue. Start a replacement session with `make codex` or `scripts/triptych-codex`; the launcher allocates the worktree before Codex starts. A linked worktree created by another trusted manager is already isolated and must not be nested.

Isolation does not grant authority. Authorization to edit content, change structure, install PDFs, create commits, integrate results, update local `main`, push any ref, or trigger deployment remains separate; do not infer a later action from an earlier one. Workers never push, switch branches, merge, rebase, amend, use the shared stash, change Git configuration or remotes, administer worktrees, or leave background processes running after the session. After explicit integration authorization, the primary-checkout launcher may perform only the documented rebase of an inactive, audited, and unlanded worker through `make integrate` or its direct launcher equivalent; this does not permit a worker session to rebase or authorize rewriting the target or published history. Unless the task expressly authorizes a commit, leave the result uncommitted for review.

An integration conflict remains an active launcher-owned rebase. From the primary checkout, `make resolve <run-id>` opens the retained worker with a fixed prompt that permits only conflict edits and staging; `make continue <run-id>` advances the rebase and either retains the next conflict or completes the existing fast-forward and cleanup path; `make abort <run-id>` aborts the rebase and verifies or restores the original audited source state. Do not run the underlying rebase operations manually.

Never record worktree paths, run identifiers, prompts, logs, process data, or other machine-local launcher state in tracked files or publication metadata.

## Work sequence

Before editing:

1. Inspect the worktree and preserve unrelated user changes.
2. Identify the document's provider, collection, genre, rite, edition, language or locale, jurisdiction, and as-of date where applicable.
3. Read the applicable profile completely and inspect the document's source and research records.
4. Confirm whether the request authorizes content changes, structural moves, installed PDF changes, commits, integration, updating local `main`, pushing a named ref, deployment, or history rewriting; do not infer broader authority from a narrower request.

During research and drafting:

- verify claims from primary, official, edition-identified sources wherever available;
- treat OCR, searchable transcriptions, aggregations, and secondary citations as leads until checked as the profile requires;
- keep verified source text, checked quotation or paraphrase, source-grounded synthesis, original editorial or AI proposal, and unverified leads distinct;
- preserve material disagreement, uncertainty, jurisdiction, and currentness rather than silently harmonizing sources;
- update the repository-owned source and research records required by the profile;
- cite only sources actually used and do not invent a search, verification event, quotation, attribution, doctrine, law, or historical fact;
- keep third-party quotations focused, record their known rights status, and comply with copyright and redistribution limits;
- never put credentials, tokens, hostnames, usernames, machine-specific paths, network addresses, hardware identifiers, or session identifiers into tracked sources or metadata.

When legal rules, current discipline, translations, software, or other mutable facts matter, verify their present state. Canon-law work must name the governing body of law, jurisdiction, promulgating authority, effective or as-of date, and material amendments or authentic interpretations. It remains a study aid, not legal advice.

## Repository and build discipline

Preserve the provider hierarchy under `src/gpt/`. New and migrated documents follow the collection schema in `guidance/repository.md`; their installed PDFs and transient artifacts mirror the same relative path under `doc/gpt/` and `build/gpt/`.

- Tracked inputs and audit records belong under `src/`.
- Reviewed, publishable PDFs belong under `doc/`.
- LaTeX intermediates, logs, caches, and other reproducible artifacts belong only under ignored `build/`.
- Shared theological or typesetting text has one authoritative source and is imported by its consumers; do not create drifting copies.
- Never use `doc/` as a build directory or treat `build/` as an authoritative input.

Use `rg` or `rg --files` first for repository search. Use history-preserving moves for tracked paths, and update imports, build dependencies, catalogs, links, attributes, and installed mirrors coherently. Existing relative TeX imports and shared-fragment consumers must be checked before moving a source directory.

Build each affected document for enough passes to settle references and contents. Inspect logs for fatal errors, undefined references, overflow, and layout warnings; visually inspect every page; then install only the reviewed PDF. When a shared source changes, build and inspect every affected consumer. Run the profile's quality gates in addition to the universal gates in `guidance/editorial.md`.

## Commits and history

Keep structural refactors separate from substantive document revisions when the requested order permits it. Stage only the coherent files requested, verify the staged diff, and use a concise commit subject plus the `AI summary:` body required by `guidance/repository.md`. Source records and the installed PDF belong in the same content-revision commit when the profile requires both.

Do not amend, rebase, filter, force-update a ref, or otherwise rewrite history unless the user explicitly requests history rewriting and its consequences have been assessed. Authorization to execute `make integrate` or its direct launcher equivalent covers only the documented launcher-owned rewrite of an unlanded worker; it never covers rewriting the target or published history. A project rename normally belongs in a new commit; local checkout and hosted-repository names are external operations.
