# Repository and Build Layout

## Ownership model

The repository has three top-level content trees with distinct roles:

- `src/` contains tracked authoring sources, focused source records, research audits, and reusable fragments.
- `doc/` contains tracked publishable documents installed from reviewed builds.
- `build/` contains only transient, reproducible artifacts and is ignored by Git.

An input required to understand, verify, or reproduce a document belongs under `src/`, never under `build/`. A PDF becomes a tracked publication only after installation under `doc/`. Cleaning the project removes `build/` without deleting `src/` or `doc/`.

Generated documents retain a provider branch. The present provider is `gpt`, so source and publication paths begin with `src/gpt/` and `doc/gpt/`. A future provider may use a parallel branch; do not flatten provider identity out of existing paths.

## Target collection hierarchy

Use this hierarchy for the expanding library:

```text
src/gpt/
  common/
  liturgy/
    roman-rite/
      1962/
        propers/
          temporal/
          ritual/
        ordinary/
        reference/
      postconciliar/
        <edition-locale>/
          propers/
            <calendar-family>/
          ordinary/
      comparative/
  theology/
    sacraments/
    sacraments-at-a-glance/
    mariology/
      <document>/
      shared/                    optional non-publishable fragments
    heresies/
      <document>/
      shared/                    optional non-publishable research fragments
  devotions/
    novenas/
      shared/                    non-publishable common prayers and formatting
      <numbered-document>/
  biographies/
    shared/                    optional non-publishable common fragments
    <subject>/
  history/
    <series>/
      <numbered-document>/
  articles/
    faith/
    canon-law/
```

`<edition-locale>` must identify the governing edition and language or territory precisely enough to prevent unlike liturgical texts from sharing a directory. Do not use `novus-ordo`, `current`, or a bare language name as the sole identifier. Record additional calendar, lectionary, translation, and jurisdiction details in the document's source record when the directory component cannot express them safely.

The hierarchy distinguishes content families; it does not prescribe a single internal template. Each publishable source document has a directory containing `main.tex` and the supporting files required by its profile. Shared inputs belong at the narrowest common ancestor that genuinely owns them. Keep global typesetting primitives under `src/gpt/common/`; keep rite-, edition-, collection-, and work-specific fragments within their respective subtrees.

Mariological reference works use publishable leaves beneath `theology/mariology/`. Any `theology/mariology/shared/` directory is non-publishable, owns only genuinely shared source material, and has no PDF mirror; all consuming documents must be rebuilt after it changes.

Historical heresy references use publishable leaves beneath `theology/heresies/` and follow `guidance/theology/heresies.md`. Any `theology/heresies/shared/` directory is non-publishable, has no PDF mirror, and may own only material genuinely shared across that collection. A comprehensive survey must keep its controlling census with the document rather than treating a title or inherited polemical list as a self-proving universal register.

Edition-specific manuals for resolving the 1962 calendar and assembling admitted formularies use publishable leaves beneath `liturgy/roman-rite/1962/reference/`. They follow the 1962 assembly profile rather than inheriting the weekly proper-guide or Ordinary-exposition architecture.

Novenas use numbered publishable leaves beneath `devotions/novenas/` and follow `guidance/devotions/novenas.md`. The `devotions/novenas/shared/` directory is non-publishable and owns only genuinely common prayer text or formatting; every novena consumer must be rebuilt after it changes.

A mechanically derived novena prayer book uses the sibling leaf `<numbered-document>-daily-prayer/`. It imports prayer fragments from the canonical full-guide leaf, declares inherited provenance, and requires explicit cross-document build dependencies; it must not become a second textual owner.

Historical and hagiographic biographies use unnumbered publishable leaves beneath
`biographies/` and follow `guidance/biographies.md`.  Each person owns an
independent leaf, source audit, chronology, and tradition audit; a shared feast
or mission does not make two persons one document.

Repeatable historical monographs use numbered publishable leaves beneath `history/<series>/` and follow `guidance/history/historical-accounts.md`. The series owns its short catalog prefix and stable two-digit ordering; the number is not a claim about importance or historical sequence.

## Mirrored publications and transient builds

`doc/gpt/` mirrors the path of each publishable source document beneath `src/gpt/`, replacing the document directory's `main.tex` with a PDF named for that directory. `build/gpt/` uses the same relative publication path for transient output.

For example:

```text
src/gpt/liturgy/roman-rite/1962/propers/temporal/15-trinity-sunday/main.tex
build/gpt/liturgy/roman-rite/1962/propers/temporal/15-trinity-sunday.pdf
doc/gpt/liturgy/roman-rite/1962/propers/temporal/15-trinity-sunday.pdf

src/gpt/articles/canon-law/validity-and-liceity/main.tex
build/gpt/articles/canon-law/validity-and-liceity.pdf
doc/gpt/articles/canon-law/validity-and-liceity.pdf
```

Non-publishable shared directories such as `common/`, fragment libraries, and research-only directories have no required PDF mirror. Do not place LaTeX auxiliary files, logs, downloaded corpora, caches, or scratch material under `doc/`.

## Naming and identity

Use lowercase kebab-case for directory and document slugs. Keep rite and edition names explicit in their ancestor paths rather than repeating them inconsistently in every basename. Within a collection, catalog identifiers must be stable, namespaced, and defined by its profile; a temporal-cycle number from one edition must not become a global project identifier.

The project is **Triptych: AI Driven Studies in Catholic Faith, Worship, and Law**. Its repository slug is `triptych`. The local checkout name and a hosting service's repository name are external to tracked content; renaming them does not require or result from moving source files.

## Licensing and project identity

`LICENSE` is the authoritative map from repository material to its outbound terms. Project-created content uses CC BY 4.0; software and the specifically listed reusable typesetting infrastructure use MIT. Apply those grants only to copyright and similar rights held by contributors and available for them to license. A mixed source file remains project content unless `LICENSE` identifies its separable infrastructure as MIT-licensed.

`THIRD_PARTY.md` records the repository-wide exclusions. Keep a more specific rights statement beside the source when a work contains Scripture, liturgical or official text, a received prayer or hymn, a third-party translation or quotation, OCR, a font, or other external material whose status could be mistaken. Record its known author, source, attribution, license, permission, public-domain basis, or applicable legal exception. Do not infer ownership or permission from age, official status, citation, retrieval, or public availability.

A source or PDF containing excluded material is a composite work. Describe the CC BY grant as applying to project-created exposition, translations, annotations, selection, arrangement, and design, as applicable; never describe every passage or embedded component as project-owned. Public-domain wording remains public domain and is not made exclusively licensed by its inclusion here.

Every rendered publication carries the standard compact rights notice supplied by `src/gpt/common/preamble.tex`. A profile or document may add a more specific local notice when its incorporated material requires one, but it must not remove or weaken the common license boundary.

The licenses grant no trademark or project-identity rights. A derivative may identify Triptych accurately for attribution, but it must not use the name, subtitle, or visual identity to imply that it is an official or endorsed Triptych publication or that it has ecclesiastical approval.

## Document records

Every document keeps its source and audit records with the document or in a clearly owned shared source directory. The applicable profile decides which records are required. Examples include:

- a structured `generation-metadata.tex` record imported exactly once by the document, or an explicit inherited-provenance declaration where a profile permits it;
- exact retrieved text retained without silent cleanup;
- an edition-identified verified text and provenance record;
- a research scope recording source roles and material limits;
- shared canonical fragments imported by several documents;
- a record of edition, locale, jurisdiction, effective date, and amendments.

Do not combine different formularies, editions, translations, jurisdictions, or unrelated articles in one source record merely because they share a theme. Do not duplicate a canonical shared fragment into several documents; import it so corrections have one authoritative home.

Focused third-party extracts may be tracked when they are necessary evidence and redistribution is permitted. Complete scans, bulk OCR, private caches, and machine-specific corpora are not repository source records.

## Build contract

The normal lifecycle is:

```sh
make          # compile into build/
make install  # copy reviewed PDFs into doc/
make clean    # remove transient build artifacts only
```

Build recipes must:

- validate every document's structured generation record before compilation and verify its rendered values after compilation;
- support nested source paths without flattening or basename collisions;
- create the matching parent directory under `build/` or `doc/`;
- compile with stable, slash-free job names while preserving the mirrored output path;
- expose shared-fragment dependencies so a relevant edit rebuilds every consumer;
- keep parallel targets isolated;
- stop on fatal compilation errors and avoid installing a failed or partial output;
- never use `doc/` as a scratch or intermediate directory.

Build manifests may enumerate publishable documents explicitly or discover them under controlled roots. Whichever method is used, adding a document must be deterministic, reviewable, and compatible with profile-specific shared dependencies.

## Isolated Codex sessions

`scripts/triptych-codex` is the ordinary CLI entry point for a Codex session that may modify the repository. It allocates the linked worktree before Codex starts and then launches the real CLI with that worktree as both its process directory and Codex workspace. `make codex` provides the interactive no-argument form; the launcher also accepts the agent-oriented `exec` and `review` surfaces with an explicit allowlist of options. Unsupported options and Codex administration, server, remote-control, update, arbitrary-sandbox, and saved-session subcommands fail before allocation. This is launcher infrastructure, not an editorial agent and not a source of content, commit, integration, push, or publication authority.

The primary checkout must be clean, on a named branch, and free of an unfinished merge, rebase, cherry-pick, revert, or bisect before a new worker is allocated. The launcher never stashes, resets, commits, copies, or silently omits a dirty primary state. Each run records one exact base commit, receives a unique `codex/isolated/<run-id>` branch and locked linked worktree, and preserves the caller's repository-relative starting directory. A session already in a linked worktree is not nested inside another one.

Runtime worktrees, locks, manifests, temporary files, and opaque run identifiers live beneath the user's private state directory, outside the tracked repository. They must not be copied into `src/`, `doc/`, `build/`, Git notes, commit messages, research records, or publication metadata. The launcher records no prompt, transcript, credential, complete argument vector, or environment snapshot. A private absolute `TRIPTYCH_CODEX_STATE_DIR` override exists for testing and controlled installations; it is runtime configuration and must not be tracked.

Every launcher-created worker is confined to its worktree: the launcher supplies no additional writable directory, rejects caller-selected working roots, host-side output paths, rules bypasses, and danger-full-access modes, clears Git redirection variables, prevents nested multi-agent writers, and uses a private per-run temporary directory. Workers must not switch branches, merge, rebase, amend, push, use the repository-wide stash, change shared Git configuration or remotes, or run worktree or maintenance administration. Git worktrees isolate files and indexes but share objects, refs, configuration, remotes, and stash state, so these prohibitions remain necessary.

Allocation and launcher-owned Git administration are serialized by one repository lock; a per-run lock prevents concurrent reopen, integration, or cleanup of the same worker and remains held by the Codex child if its launcher supervisor dies. The repository lock is released while Codex works, so separately allocated workers may run concurrently. A launcher-managed worker rejects recursive launcher use so a second Codex process cannot enter the same worktree through the supported path. Workers must not leave preview servers, watchers, or other background processes running when their Codex session ends. Worktrees remain Git-locked against pruning throughout their active and retained lifetimes. Manual `git worktree prune`, forced removal, branch deletion, or state-directory deletion is prohibited while any run is active or retained.

The launcher cleans a newly allocated run automatically on its first exit only when Codex exits successfully, the expected task branch and lock remain intact, `HEAD` still equals the recorded base, and the worktree has no staged, unstaged, or non-ignored untracked change. A reopened run is re-audited and preserved even if it has become unchanged; cleanup then remains explicit. Ignored reproducible artifacts may be discarded with an otherwise unchanged worker. The launcher preserves every tracked or non-ignored change, every committed result, nonzero or interrupted run, changed branch, audit inconsistency, and cleanup failure. Preservation is success: it prevents a worker or crash from destroying another result. Use `scripts/triptych-codex --triptych-status`, `--triptych-reopen <run-id>`, `--triptych-integrate <run-id>`, and `--triptych-clean <run-id>` for opaque lifecycle operations without handling worktree paths. Reopening starts a fresh Codex process in the retained worktree rather than resuming its saved conversation. Safe cleanup refuses uncommitted work, a worker whose `HEAD` changed after its last terminal audit, and any commit not already reachable from the recorded target branch; there is no force-discard operation.

The launcher never commits a preserved result and never integrates one merely because Codex exits. After review and separate authorization, `make integrate <run-id>` provides the one-step landing path from the primary checkout; `scripts/triptych-codex --triptych-integrate <run-id>` is its direct equivalent. Using either form requires authority both to integrate the result and to update its recorded local target, including local `main` when `main` was the dispatch branch. It requires that clean named target, an inactive and intact locked worker on its expected branch, a clean worker index and worktree whose `HEAD` exactly matches the last terminal launcher audit, and histories that still descend from the recorded base. A retained rebase conflict is managed with `make resolve`, `make continue`, and `make abort` followed by the same run ID; their direct equivalents are `--triptych-resolve`, `--triptych-continue`, and `--triptych-abort`.

Integration prefers the flattest history. A result already reachable from the target is confirmed and cleaned. A result that already descends from the target is fast-forwarded without rewriting it. When the target and worker have both advanced from the recorded base, the launcher requires the worker-only range to be linear, rebases its audited commits onto the captured current target, permits Git to omit commits whose changes are already present at that tip or become empty, and then performs an `--ff-only` merge with Git’s no-overwrite-ignore guard. An unexpected worker-side merge is refused because flattening it could discard content introduced by the merge commit. The launcher never rebases existing target history and never falls back to a merge commit. The original audited worker head and the actual rebased landing head remain distinct in the private lifecycle record. Authorization to execute this integration includes only that launcher-owned rewrite of the inactive, reviewed, and still-unlanded worker branch; it does not authorize a worker session to rewrite history or authorize amendment, rebase, or force-update of the target or any published history.

If rebasing conflicts, the launcher leaves the rebase active and retains the run for source-aware reconciliation. Resolve opens Codex in that worker with a fixed prompt limited to editing the conflicts and staging the resolution; it may not commit, continue, abort, or perform other lifecycle work. Continue runs `git rebase --continue` with `GIT_EDITOR=:` and either retains the next conflict or completes the existing fast-forward, audit, and cleanup path. Abort runs `git rebase --abort`, then verifies and, when safely necessary, restores the exact original audited source state while leaving the target unchanged. If the launcher is interrupted while a rebase is pending, any active rebase, unknown commit, or dirty state remains retained for these controlled operations or manual inspection. If a rebase succeeds but the subsequent fast-forward fails before the target moves, it restores the original worker and retains the run. It performs that hard rollback only from a known clean rebased state; failure to prove a safe restoration is retained without cleanup for inspection. Once the target advances, later verification or cleanup failure never rolls it back; the command records the actual landing, reports the incomplete lifecycle state, and permits a safe cleanup retry. If later history rewriting removes that recorded landing from the target, integration refuses to reapply it silently; the target must first be restored or reconciled. Before cleanup it rechecks the target’s branch, cleanliness, exact or descendant reachability, and the rebased worker’s branch, head, and cleanliness. A dirty or mismatched checkout, an uncommitted worker or one whose audited state subsequently changed, an unavailable recorded base, or a history that no longer descends from that base is refused without integration. The launcher itself never invokes `git push` or deployment. It disables hooks for its internal worker rebase so they cannot alter the generated candidate. Target-side merge hooks still run; the post-merge audit can prevent cleanup when they alter checked-out state but cannot undo their external side effects.

Before landing a result, review the complete final diff, confirm that its paths match the task's authorized scope, inspect every affected document and consumer, and run the applicable gates. Integrate results serially; each later run is rebased onto the results already landed when the changes combine cleanly. Text conflicts require source-aware reconciliation; shared-fragment changes require every consumer to be rebuilt; PDF conflicts are never resolved by choosing one binary side but by reconciling the authoritative sources and rebuilding. Preserve both inputs when reconciliation is incomplete.

## Adding or migrating a document

For a new document:

1. Select the provider, collection, genre profile, edition, locale, and jurisdiction.
2. Create its directory at the corresponding `src/` path with `main.tex` and required source records.
3. Confirm that recursive discovery finds the document; register only exceptional cross-document shared dependencies.
4. Build, validate, and install it to the exact mirrored `doc/` path.
5. Update the publication's one owning section page under `library/`; update `LIBRARY.md` only when the section index itself changes.

When migrating an existing document, use history-preserving moves and update its imports, build target, dependencies, internal cross-references, README or catalog links, attributes, and installed PDF path together. Validate all consumers of any moved shared fragment. Do not leave a second editable copy at the old location. If a compatibility alias is genuinely needed, make it generated or explicitly transitional and document its removal condition.

Repository restructuring and content revision should remain distinguishable in review and history. Prefer a structure-only commit before substantive revisions when both are required, while ensuring each committed state has internally consistent paths and guidance.

## Public navigation and catalog

`README.md` is a deliberately terse landing page for clergy, religious, and lay readers. Its subtitle identifies the studies as AI driven, while its first heading remains the standalone `Don't Panic!`. The opening moves from AI and authority limits to skeptical reading, ordinary-language feedback, and reassurance that no technical background is needed. It then links Traditional Latin Mass (1962 Roman Rite), Novus Ordo (Postconciliar Roman Rite), Prayer, Faith, Biographies, Heresies, Historical Accounts, Mariology, and Law in one compact library table; keeps the two clearly distinguished liturgy pages first and Prayer next without directing readers where to begin; states the reuse boundary; and ends by explaining the name. Do not put publication catalogs, raw status matrices, repository history, build commands, or maintainer-oriented layout detail back onto the landing page.

`LIBRARY.md` is the public catalog index. Publication listings live on the mutually exclusive section pages `library/traditional-latin-mass.md`, `library/novus-ordo-liturgy.md`, `library/prayer.md`, `library/faith.md`, `library/biographies.md`, `library/heresies.md`, `library/historical-accounts.md`, `library/mariology.md`, and `library/law-and-church-discipline.md`. Every installed publication has exactly one catalog entry across those pages; do not repeat a title or PDF as a cross-listing. A mechanically derived companion belongs in the same entry or row as its canonical work and counts as part of that one catalog home. A page with no dedicated publication says so plainly instead of borrowing cross-disciplinary works from another section.

Restrict `Traditional Latin Mass: 1962 Roman Rite` to the 1962 Ordinary, assembly references, and proper guides: list the Ordinary first, `Assembling the Mass` second, and the proper guides in a compact table. Keep devotional prayer on the separate `Prayer` page; list the novenas there in a compact table with each short form in the same row as its full guide. The reader-facing `Novus Ordo: Postconciliar Roman Rite` title honors common usage while distinguishing the collection from the 1962 books, but every publication placed there must identify the exact postconciliar books, edition, language, territory, and date it studies. Place comparative or other discursive works under their substantive study category rather than duplicating or misclassifying them merely because they discuss liturgy. Lead each primary entry with its plain title linked directly to the installed PDF. Follow with a short scope and status statement, then separately named links to every distinct reader-facing supporting or audit record required by the governing profile. Do not link TeX authoring files from Markdown; they remain discoverable through the repository structure when needed for technical work. A shared scope or status that truly applies to every item in a compact series may appear once before its table or list; do not repeat it on every entry. Focused raw retrieval extracts and structured generation records remain reachable through the supporting records and need not be linked from the catalog unless a profile expressly requires them. Prefer readable lists for heterogeneous works and compact tables for the profile-defined numbered series.

Keep generation provenance, source evaluation, independent review, and production status distinct in catalog language. Preserve mutable as-of dates and profile-local evidence codes where they materially qualify a publication, but explain them in ordinary language or link their definitions. Keep reader-facing collection identifiers where they aid navigation; do not expose an internal ordering key merely to fill a catalog field.

`CONTRIBUTING.md` is the public contribution guide. It must keep a no-Git path for short, ordinary-language feedback, a clone-and-run path for contributors using an AI agent, and an experimental-branch path for testing materially different base guidance. It must make clear that feedback initiates verification rather than becoming authority, that alternative branches remain distinct from the reviewed library, and that an intentional submission is offered under the applicable outbound license without transferring ownership. Require contributors to identify third-party material and the authority under which it may be distributed.

## Public release artifacts

Repository visibility and reader-site publication are separate release decisions. Keep the development repository private unless a recorded authorization expressly covers its tracked sources, research records, installed PDFs, licensing and infrastructure files, and reachable history. The current Triptych authorization permits public GitHub visibility for that full recorded scope. Whether the repository is private or public, build the reader-facing edition as a generated, history-free artifact under ignored `build/`, copying only the material authorized by an exhaustive release manifest.

`release/public-alpha.json` governs the first public edition and must account for every discovered `src/gpt/**/main.tex` document and mirrored `doc/gpt/**/*.pdf`. Its statuses are fail-closed:

- `hold` excludes a work from both public builds and private review previews;
- `review` permits a work only in the clearly marked, no-index private preview; and
- `release` requires a work-specific rights record, or an exhaustive shared record that identifies the work, an effective authorization and its duration, no unresolved release gate, and the exact SHA-256 of the approved installed PDF.

`release` is an exact-snapshot distribution decision, not an editorial-maturity,
source-audit, specialist-review, or ecclesiastical-approval label.  An express
snapshot authorization may clear the project's rights and distribution gates
for the exact recorded PDF even when disclosed profile-final or source-audit
work remains outstanding.  The authorization must bind the final PDF hash,
identify the accepted limitations, and leave each publication's source and
review disclosures intact; it must never imply that an unperformed collation,
source check, specialist review, imprimatur, or other ecclesiastical approval
occurred.  A rebuilt or otherwise changed PDF is a new snapshot and requires a
new exact approval before it can retain `release` status.

The public site generator renders the canonical reader-facing Markdown rather than maintaining a second editable catalog, but filters publication entries by the manifest. It may copy rendered HTML, site styling, license notices, approved PDFs, and narrowly scoped generated host-control files required to enforce release conditions. It must not copy authoring Markdown, TeX, research or retrieval records, build intermediates, repository metadata, or prior Git history unless a later release policy explicitly reviews and authorizes a category. A private preview may additionally contain `review` PDFs, but it must be marked `noindex, nofollow`, remain local or access-controlled, and never be deployed as the public site.

Before publishing, verify the generated artifact independently against the manifest: its complete file set must be exact; every artifact PDF must match its repository-approved hash rather than merely a generated artifact manifest; every reader-facing source, rendered page, and copied static file must match the approved repository input; the artifact manifest must have no missing or extra fields; local links and fragments must resolve; excluded publication identifiers and machine-private paths must be absent; and recorded checksums must match. Publish only the verified public artifact through the configured host or deployment workflow. A public repository may expose its tracked development material when separately authorized, but GitHub Pages must never deploy the repository root, a development branch's raw tree, or the private-preview output.

A conditional release must encode its duration, effective instant, timezone, scope, machine-recognized conditions, and either a null cutoff for perpetual authorization or an exclusive cutoff for temporary authorization. Public checks, builds, and verification fail before the effective instant, and temporary releases also fail at and after the cutoff of their half-open authorization interval. A release that requires discovery controls emits no-index HTML metadata and host response-header instructions for every page and PDF. A public-repository authorization may instead permit ordinary platform and search indexing while retaining a narrower no-active-promotion condition. Record that distinction explicitly; public visibility and search directives must not be inferred from the word “unadvertised” alone.

A generated static artifact cannot revoke or delete itself. Any temporary public release therefore requires a host control that runs before every asset request, including direct PDF requests, and returns `410 Gone` at the cutoff. It also requires cache control, prevention of rollback to an unguarded deployment, independent monitoring, and a manual project-withdrawal and cache-purge fallback. Verify these controls against the live host before sharing its URL. Do not deploy a temporary release to a host that ignores the generated control runtime merely because the local generator will reject a later rebuild.

## Version-control hygiene

Track `src/` and `doc/`; ignore `build/`. Preserve unrelated worktree changes and never treat an untracked source record as disposable merely because it can be regenerated. Stage only the files belonging to the coherent change being committed.

Editing, building, installing reviewed PDFs, committing, integrating, updating local `main`, pushing a non-main ref, pushing `main`, and deploying are distinct operations requiring distinct authority. A request for an earlier operation does not authorize a later one. Naming a task “complete,” “finished,” or “ready” does not broaden that authority.

On a public repository, every pushed ref immediately exposes its tracked tree and reachable history, including a task or integration branch that GitHub Pages does not deploy. A push to `main` additionally triggers `.github/workflows/pages.yml`; release checks run only after the ref has already become public, and a failed workflow does not retract the pushed source or history. Before pushing, review the complete outgoing commit range and verify that new protected content, changed PDFs, and future publications have the authority and rights review required for the named remote and ref. Keep uncleared experiments and private-review material off public refs. A manual `workflow_dispatch` is deployment authority, not a routine verification step.

Every AI-assisted commit must have both a concise subject that states the result and a substantive commit body headed `AI summary:`. The body must record the principal content, source-record, guidance, build, and publication changes included in the commit, as applicable; the material verification performed and its outcome; and any consequential limitation or review still outstanding. Keep it concise enough to scan but complete enough to explain the committed state without relying on the chat transcript. Do not claim checks that were not run, include private reasoning or session details, or leave an AI-assisted commit with only a terse one-line subject.

Corrections, source substitutions, renewed verification, and newly resolved discrepancies are normal reviewed history. Update the relevant record and explain the reason in the commit rather than erasing the previous state. Avoid rewriting published history for ordinary renames or expanding project scope; a new commit records that evolution honestly unless a history rewrite is explicitly required and coordinated.
