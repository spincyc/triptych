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

Read `guidance/sources.md` before adding, migrating, storing, or reusing a
repository-wide external source, corpus, edition, artifact, passage record, or
publication binding.

The user's request takes priority when it deliberately changes a project convention. Record the new convention in the correct universal or profile guidance rather than leaving the implementation and guidance inconsistent.

## Profile routing

Select profiles by the document's actual genre and sources, not by superficial similarity:

- 1962 Roman Rite temporal, ritual, votive, or other proper guides: `guidance/liturgy/roman-1962-propers.md`
- edition-specific references for assembling the Ordinary and propers under the 1962 calendar and rubrics: `guidance/liturgy/roman-1962-assembly.md`
- 1962 Roman Rite altar-server response, pronunciation, memorization, and ceremonial training guides for Low Mass, Missa Cantata, and Solemn Mass: `guidance/liturgy/roman-1962-server-training.md`
- self-paced Ecclesiastical Latin curricula centered on the 1962 Missal, including modular teaching packets, reference, practice, assessments, and keys: `guidance/curriculums/ecclesiastical-latin.md`
- edition-specific histories and complete normative inventories of Roman calendars: `guidance/liturgy/roman-calendar-references.md`, plus the profile for the identified edition where its rules are used
- postconciliar Roman Rite proper guides: `guidance/liturgy/postconciliar-propers.md`, with permanent IDs, keys, slugs, counts, and occurrence grammar in `guidance/liturgy/postconciliar-propers-registry.md` and edition dispositions under the selected `<edition-locale>/propers/registry/`
- expositions of the Ordinary or Order of Mass in either form: `guidance/liturgy/ordinary-expositions.md`
- the sacramental treatise, at-a-glance companion, or their shared fragments: `guidance/theology/sacramental-reference.md`
- the comprehensive reference on theological, cardinal, intellectual, and annexed virtues: `guidance/theology/virtues.md`
- the Rosary, Marian-apparition judgment studies, or other repeatable Mariological reference works: `guidance/theology/mariology.md`
- historical and hagiographic lives in the biographies collection: `guidance/biographies.md`
- comprehensive historical reference works on heresies, censured propositions, and ecclesial responses: `guidance/theology/heresies.md`
- novenas and other works in the numbered novena collection: `guidance/devotions/novenas.md`
- repeatable source-first histories of texts, institutions, events, or reception: `guidance/history/historical-accounts.md`
- discursive articles on faith, theology, or canon law: `guidance/articles.md`

A document may require more than one profile only when it truly combines genres. For example, a canonical article about a liturgical question follows the articles profile for its argument and the relevant liturgical profile for edition-specific textual claims. State which profile governs each part rather than merging their templates.

The sacramental treatise and its at-a-glance companion are established theological reference works with shared canonical fragments. Follow the universal guidance, their sacramental-reference profile, and their local research scope; do not impose a Mass-propers or discursive-article template on them.

If no profile fits a requested repeatable series, add or revise a profile before multiplying documents. Keep universal guidance genre-neutral. Put rite-, edition-, locale-, calendar-, jurisdiction-, page-, and section-specific rules in the appropriate profile, not in this file or the universal editorial standard.

## Isolated agent sessions

Mutating Codex CLI sessions must run in the isolated linked worktree assigned by `scripts/triptych-codex`. The primary checkout is a control and integration checkout, not an autonomous worker workspace. A session already running in a linked worktree remains there and must not invoke the launcher again or create, remove, lock, unlock, prune, or enter another worktree.

If a mutating Codex session starts in the primary checkout without isolation, fail closed: do not edit, build, commit, or try to emulate relocation with a shell `cd`. Read-only inspection may continue. Start a replacement session with `make codex` or `scripts/triptych-codex`; the launcher allocates the worktree before Codex starts. A linked worktree created by another trusted manager is already isolated and must not be nested.

Isolation does not grant authority. Authorization to edit content, change structure, install PDFs, create commits, integrate results, update local `main`, push any ref, or trigger deployment remains separate; do not infer a later action from an earlier one. Workers never push, switch branches, merge, rebase, amend, use the shared stash, change Git configuration or remotes, administer worktrees, or leave background processes running after the session. A resolver opened by `make resolve RUN=<run-id>` or `--triptych-resolve` is narrower still: it starts at the managed worktree root under a fixed launcher-supplied safety prompt and may inspect, edit, and stage a launcher-recorded active conflict, but it must not commit, amend, reset, switch, merge, run any form of `git rebase`, or administer worktrees. Forwarded resolver prompts or options are not accepted. The resolver and ordinary workers never continue, skip, or abort the rebase; only the opaque launcher commands `make continue RUN=<run-id>` and `make abort RUN=<run-id>` (or their direct equivalents) own those operations. After explicit integration authorization, the primary-checkout launcher may perform only the documented rebase of an inactive, audited, and unlanded worker through `make integrate RUN=<run-id>` or its direct launcher equivalent; this does not permit a worker session to rebase or authorize rewriting the target or published history. Unless the task expressly authorizes a commit, leave the result uncommitted for review.

From the primary checkout, `make status` lists retained runs that still need attention; `make status RUN=<run-id>` inspects one exact record, including a cleaned record. Use `make reopen RUN=<run-id>` to start a fresh Codex process in an ordinary retained worker and `make clean-run RUN=<run-id>` to request launcher-verified safe cleanup. The latter never force-discards a result, and `make clean` remains reserved for reproducible build artifacts.

The no-argument status overview is the only Make lifecycle form without a run ID. Every Make lifecycle target that accepts a run ID takes it as `RUN=<run-id>` and is a convenience wrapper only for an exact ID emitted by the launcher. The former `make <target> <run-id>` spelling remains accepted only as a local compatibility transition; new instructions and automation use `RUN=`. GNU Make processes options and command-line variable assignments before the Makefile can validate them, so do not forward arbitrary or external values to these wrappers. Use the corresponding direct launcher form, such as `scripts/triptych-codex --triptych-resolve <run-id>`, for such input; its lifecycle parser requires one syntactically valid run ID without GNU Make's option or assignment reinterpretation. The Make reopen wrapper forwards no Codex arguments; use `scripts/triptych-codex --triptych-reopen <run-id> -- <arguments...>` when supported agent options are required.

Ordinary conflict-free integration remains one step. Before a launcher-owned rebase can move the worker branch, the launcher anchors its exact audited source under a private per-run ref and keeps that anchor through conflict and review. When the rebase reaches a genuine conflict, the launcher retains the active rebase and records a managed conflict instead of replaying Git's generic continuation advice. After a resolver stages the reconciliation, launcher-owned continuation runs with hooks, signing, and editors disabled and may repeat the resolve/continue cycle for later conflicts. Resolver and continuation read the target ref directly and do not require or change a clean, matching primary checkout. Correctable resolver over-staging remains inside the managed conflict boundary; after proving the managed rebase and source identity, explicit abort may discard that staging while restoring the exact audited source. An unprovable managed rebase or source identity enters recovery failure. Successful continuation stops at a clean review-pending candidate and does not update the target. Review its object-to-object patch with `make final-diff RUN=<run-id>` before a later, fresh `make integrate RUN=<run-id>` authorization. Landing disables all hooks and may update only the recorded target from its exact expected old commit to the exact candidate; primary index and file synchronization never resets a raced unrelated ref. If that target advances, retain the manually resolved candidate and source anchor without reset, rebase, merge, cleanup, or silent discard. A manually resolved `integration-verification-failed` candidate may be explicitly aborted only when no rebase is active, the worker is clean at the exact recorded candidate, the private source anchor still names the exact recorded source, and neither `integrated_head` nor any landing checkpoint exists. Cleanup checkpoints before unlocking the worktree and atomically verifies the target while deleting the worker branch and source anchor; a provable interrupted checkpoint remains retryable by opaque run ID. Explicit abort instead restores and verifies the exact audited source without depending on or touching the live target ref.

An integration conflict remains an active launcher-owned rebase. From the primary checkout, `make resolve RUN=<run-id>` opens the retained worker with a fixed prompt that permits only conflict edits and staging; `make continue RUN=<run-id>` advances the rebase and either retains the next conflict or completes the existing fast-forward and cleanup path; `make abort RUN=<run-id>` aborts the rebase and verifies or restores the original audited source state. Do not run the underlying rebase operations manually.

One destructive exception exists for an explicitly superseded rewritten quarantine whose clean current history no longer descends from its last terminal audit. It requires separate, explicit authorization to discard the exact worker head and is available from the primary checkout only as `scripts/triptych-codex --triptych-retire RUN_ID --discard-head FULL_OID --target-contains FULL_OID`; it deliberately has no Make wrapper. `--discard-head` identifies the exact clean worker and branch head to destroy. `--target-contains` is only an operator-selected reachability checkpoint that the recorded target must contain; it does not establish semantic equivalence, incorporation, or supersession of the discarded history. The launcher verifies but never moves the target, durably checkpoints the initial eligibility proof once, and anchors the discarded head. Before removing a retained worktree, and again while the branch and anchor remain exact with no receipt, it freshly requires the current target to contain the selected checkpoint and durably records that exact current target for the atomic ref transaction. The transaction verifies that exact ref, creates the per-run receipt at the discarded head, and exact-deletes the worker branch and retirement anchor. A target race retains those pre-transaction refs so an exact retry can checkpoint a newer containing descendant; lost containment refuses deletion until a containing descendant is restored. Only after observing and recording the transaction does the launcher exact-delete the receipt and record its absence. Recovery after that transaction uses only durable fields and strict phase refs, so completed objects may be pruned. Changed state, an unexpected ref tuple, or partial cleanup fails closed. Repeating the exact command is idempotent; changed object arguments fail. `make clean-run RUN=<run-id>` may resume an already checkpointed retirement but must reject an untouched quarantine; this exception never weakens ordinary safe cleanup or integration.

Never record worktree paths, run identifiers, prompts, logs, process data, or other machine-local launcher state in tracked files or publication metadata. The launcher gives each worker and resolver one exact run-owned path through `TMPDIR`, `TMP`, and `TEMP`. Put every off-worktree transient created for the run—including downloads, OCR and text extracts, generated helper scripts, screenshots, review rasters, and ad hoc caches—below that path; do not create arbitrary siblings directly under `/tmp`. Stable shared IPC locks are the narrow exception. Reproducible repository intermediates belong in the ignored `build/` tree while the worker is retained; material that must survive completed integration must be incorporated into the authorized tracked paths. No process may keep reading or writing the run-owned temporary tree after its worker or resolver exits; the lifecycle lock and prohibition on background processes are the cleanup exclusivity boundary. Successful managed cleanup removes only the exact manifest-recorded temporary directory and does not mark the run cleaned while that path remains or cannot be authenticated.

An initial rebase stopped before its first replay commit may be aborted only after the launcher proves its merge-backend administration, captured target HEAD, anchored source branch, first audited replay, independently reproduced index tree, and clean worktree boundary. Changed administration, index, worktree, or untracked state fails closed.

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

Preserve the provider hierarchy under `src/<provider>/`; the present providers are `gpt` and `claude`. New and migrated documents follow the collection schema in `guidance/repository.md`; their installed PDFs and transient artifacts mirror the same relative path under `doc/<provider>/` and `build/<provider>/`.

- Tracked inputs and audit records belong under `src/`.
- Provider-neutral reusable external-source records and lawful retained
  artifacts belong under `src/sources/` and follow `guidance/sources.md`.
- Reviewed, publishable PDFs belong under `doc/`.
- LaTeX intermediates, logs, caches, and other reproducible artifacts belong only under ignored `build/`.
- Shared theological or typesetting text has one authoritative source and is imported by its consumers; do not create drifting copies.
- Never use `doc/` as a build directory or treat `build/` as an authoritative input.

Use `rg` or `rg --files` first for repository search. Use history-preserving moves for tracked paths, and update imports, build dependencies, catalogs, links, attributes, and installed mirrors coherently. Existing relative TeX imports and shared-fragment consumers must be checked before moving a source directory.

Build each affected document for enough passes to settle references and contents. Inspect logs for fatal errors, undefined references, overflow, and layout warnings. Generate review rasters and contact sheets through `make review-pdfs` or `scripts/pdf-review`; never fan out raw `montage`, `magick`, or equivalent whole-document contact-sheet commands. Visually inspect every rendered page, then install only the reviewed PDF. When a shared source changes, build and inspect every affected consumer. Run the profile's quality gates in addition to the universal gates in `guidance/editorial.md`.

## Commits and history

Keep structural refactors separate from substantive document revisions when the requested order permits it. Stage only the coherent files requested, verify the staged diff, and use a concise commit subject plus the `AI summary:` body required by `guidance/repository.md`. Source records and the installed PDF belong in the same content-revision commit when the profile requires both.

Do not amend, rebase, filter, force-update a ref, or otherwise rewrite history unless the user explicitly requests history rewriting and its consequences have been assessed. Authorization to execute `make integrate` or its direct launcher equivalent covers only the documented launcher-owned rewrite of an unlanded worker; it never covers rewriting the target or published history. A project rename normally belongs in a new commit; local checkout and hosted-repository names are external operations.
