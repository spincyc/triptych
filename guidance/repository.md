# Repository and Publication Contract

## Governing priorities

Apply these rules in order:

1. keep authoritative inputs and audit records under `src/`, reviewed publications under `doc/`, and reproducible intermediates under ignored `build/`;
2. preserve provider, collection, rite, edition, locale, jurisdiction, and document identity in the path and records;
3. give shared text one owner and declare every consumer dependency;
4. build deterministically, inspect every affected page, and install only the reviewed PDF; and
5. treat editing, committing, integrating, pushing, and deployment as separate authorized operations.

`guidance/editorial.md` governs universal content quality. The applicable genre profiles govern document-specific sources, records, structure, and gates. This file governs ownership, paths, builds, catalogs, release artifacts, and version control.

## Ownership and paths

- `src/` contains tracked authoring sources, focused evidence and research records, and reusable fragments.
- `doc/` contains tracked PDFs installed from reviewed builds.
- `build/` contains only ignored, reproducible intermediates, logs, caches, review rasters, and generated release artifacts.

Anything required to understand, verify, or reproduce a publication belongs under `src/`, never `build/`. `doc/` is not a build directory. Cleaning may remove `build/` but never `src/` or `doc/`.

Generated documents retain a provider branch. The present provider is `gpt`; do not flatten it from existing paths. Use this collection hierarchy:

```text
src/gpt/
  common/
  curriculums/
    <curriculum>/
      shared/
      research/
      <stage>/<numbered-module>/
  liturgy/roman-rite/
    1962/
      propers/{temporal,ritual}/
      ordinary/
      reference/
    postconciliar/<edition-locale>/
      propers/
        registry/                 edition-owned registry records
        <calendar-family>/
      ordinary/
      reference/
    comparative/
  theology/
    virtues/
    sacraments/
    sacraments-at-a-glance/
    mariology/{<document>,shared}/
    heresies/{<document>,shared}/
  devotions/novenas/{shared,<numbered-document>}/
  biographies/{shared,<subject>}/
  history/<series>/<numbered-document>/
  articles/{faith,canon-law}/
```

`<edition-locale>` must distinguish the governing books and territory; never use `current`, `novus-ordo`, or a bare language as its sole identity. Postconciliar proper guides also use the stable universal registry in `guidance/liturgy/postconciliar-propers-registry.md`; edition-specific collation, unresolved branches, and instantiated leaves belong under the edition's `propers/registry/` directory rather than in the reusable profile. A curriculum keeps course-wide teaching, practice, reference, and audit sources at its non-publishable owner root and gives each independently printable module or companion its own publishable leaf. Do not duplicate shared lessons or answer sources into module leaves.

Each publishable leaf contains `main.tex`, `generation-metadata.tex` or a profile-authorized inherited declaration, and the profile-required records. Shared directories are non-publishable and have no PDF mirror. Put shared material at the narrowest ancestor that genuinely owns it; keep global typesetting primitives under `src/gpt/common/` and rite-, edition-, collection-, or work-specific material within its subtree.

`build/gpt/` and `doc/gpt/` mirror a publishable leaf's path below `src/gpt/`; the PDF is named for the leaf. For example:

```text
src/gpt/articles/canon-law/example/main.tex
build/gpt/articles/canon-law/example.pdf
doc/gpt/articles/canon-law/example.pdf
```

Use lowercase kebab-case slugs. Stable identifiers are namespaced by their profiles and are not interchangeable across collections or editions. Numbered series use their profile's ordering rules; a number is not a claim of importance.

## Shared sources and records

One text has one authoritative owner. Import it into every consumer and declare build dependencies that rebuild all consumers after it changes. Do not create editable copies for convenience. Derived companions must identify their canonical owner and may inherit provenance only when their profile permits it.

Keep records with the owning leaf or a clearly owned shared source. They must identify the exact editions, witnesses, translations, jurisdictions, dates, source roles, checked loci, unresolved discrepancies, rights basis, and completed review required by the profile. Focused third-party extracts may be tracked when necessary and distributable; complete scans, bulk OCR, private caches, and machine-specific corpora do not belong in publication leaves.

Do not combine unlike formularies, editions, translations, jurisdictions, or unrelated works in one record merely because they share a theme. Never record credentials, private communications, host or user identity, machine paths, network data, launcher state, or session identifiers.

## Rights and project identity

`LICENSE` defines the outbound terms and `THIRD_PARTY.md` the repository-wide exclusions. Project-created content is CC BY 4.0; the software and reusable infrastructure identified there are MIT-licensed. Those grants do not relicense third-party or public-domain content.

Record a local rights statement wherever Scripture, official or liturgical text, a received prayer or hymn, a third-party translation or quotation, OCR, a font, or other external material could be mistaken for project-owned expression. Identify the known author, source, attribution, license, permission, public-domain basis, or legal exception. Age, official status, citation, retrieval, and public availability do not establish permission.

Every publication retains the common rights notice as a compact final-page colophon; it must not force a dedicated page. The colophon contains only the universal license boundary and pointers to `LICENSE` and `THIRD_PARTY.md`. A local notice may add necessary precision but may not weaken or duplicate that boundary. The Triptych name and visual identity do not convey endorsement, official status, or ecclesiastical approval to a derivative.

## Build and review contract

The normal lifecycle is:

```sh
make                  # bounded parallel build into build/
make pdf              # incremental PDF build
make review-pdfs      # artifacts for changed PDFs
make review-all-pdfs  # artifacts for every built PDF
make install          # copy reviewed PDFs into doc/
make clean            # remove reproducible intermediates only
```

Build recipes must:

- validate structured generation records before compilation and rendered metadata afterward;
- derive PDF modification time only from the tracked revision, omit build-clock creation dates and automatic trailer IDs, and reproduce identical bytes from unchanged inputs under the same toolchain;
- preserve mirrored paths without basename collisions and isolate concurrent targets;
- declare every render-affecting input and shared-consumer edge;
- stop on fatal failure and never install a partial result; and
- keep all intermediates out of `doc/`.

Compile each affected publication for enough passes to settle references and contents. Reject fatal errors, undefined references, overflow, and unresolved layout warnings.

Use only `make review-pdfs`, `make review-all-pdfs`, or `scripts/pdf-review` to prepare page rasters and bounded contact sheets. The helper owns concurrency and memory controls; do not replace it with raw parallel ImageMagick or equivalent whole-document commands. A cache hit or contact sheet is not review. Inspect every rendered page, opening full-size rasters where scale matters, then verify PDF structure, fonts, metadata, extracted text, and byte identity between reviewed build and installed mirror.

Research records that cannot affect rendered bytes need not force recompilation. Adding a publication may use deterministic controlled discovery; exceptional shared dependencies must be explicit.

## Isolated Codex workers

Mutating Codex sessions follow the isolation and authority contract in `AGENTS.md`. Start them through `make codex` or `scripts/triptych-codex`; a session already in its assigned linked worktree must not invoke the launcher again or administer worktrees.

Workers may edit, build, inspect, and commit only when authorized. They never switch branches, merge, rebase, amend, push, use the shared stash, change shared Git configuration or remotes, administer worktrees, or leave background processes running. Runtime paths, run IDs, locks, manifests, prompts, logs, and private launcher state are never tracked.

The launcher exports the same exact run-owned directory as `TMPDIR`, `TMP`, and `TEMP`. Every off-worktree transient produced by a worker or resolver—downloads, OCR and text extracts, generated helper scripts, screenshots, review rasters, and ad hoc caches—must be created below that directory rather than in an arbitrary shared `/tmp` path. Stable shared IPC locks are the narrow exception. Reproducible repository intermediates belong in the ignored `build/` tree while a worker is retained; material that must survive completed integration must be incorporated into the authorized tracked paths. No process may keep using the run-owned temporary tree after its worker or resolver exits; the inherited lifecycle lock and prohibition on background processes establish cleanup exclusivity. Ordinary managed cleanup authenticates and removes only the exact temporary path recorded for that run before deleting its private lifecycle refs; failure leaves a retryable retained state, and a cleaned run must have no such path. The separately authorized rewritten-quarantine retirement retains its stricter receipt transaction and removes the same authenticated temporary path only during finalization.

From the primary checkout, inspect and manage ordinary retained runs with:

```sh
make status                 # list runs that still need attention
make status <run-id>        # inspect one exact record, including a cleaned run
make reopen <run-id>        # start a fresh Codex process in a retained worker
make clean-run <run-id>     # request launcher-verified safe cleanup
```

The cleanup command never force-discards a result, and `make clean` remains the build-artifact cleanup target. The Make reopen wrapper accepts only the exact run ID; use the direct `--triptych-reopen` launcher form when supported Codex arguments are needed. Status may reconcile a stale lifecycle record while reporting it.

Integration is launcher-owned and separately authorized. The opaque lifecycle is:

```sh
make final-diff <run-id>
make integrate <run-id>
make resolve <run-id>    # only after a recorded conflict
make continue <run-id>
make abort <run-id>
```

Except for the no-argument status overview, Make lifecycle commands are convenience wrappers for exact launcher-produced run IDs. Use direct launcher forms for untrusted or externally supplied input because GNU Make interprets options and assignments before target validation. A resolver may edit and stage only the recorded conflict; it may not commit or administer the rebase. Only the launcher continues, aborts, lands, and cleans the retained run. Review the complete object-to-object final diff and every affected consumer before authorizing landing. Reconcile PDF conflicts from authoritative sources and rebuild; never choose one binary side. The launcher never pushes or deploys.

### Exceptional rewritten-quarantine retirement

Retirement is a destructive exception for a quarantined run that an operator has explicitly determined is superseded after its worker history was rewritten. It requires separate authorization to discard the exact head and is available only from the primary checkout through the direct launcher form:

```sh
scripts/triptych-codex --triptych-retire RUN_ID --discard-head FULL_OID --target-contains FULL_OID
```

There is deliberately no Make wrapper. Both object arguments must be full, exact commit IDs. `--discard-head` must identify the freshly audited, clean head of the inactive worker on its recorded branch, and that head must still descend from the recorded base while no longer descending from the last terminal `final_head`; `recorded_clean_final_head` is not a substitute for that terminal audit. The recorded target must exist and contain `--target-contains`. That object is only an operator-selected reachability checkpoint: reachability does not establish that the target semantically incorporates, supersedes, or is equivalent to the discarded work. Retirement verifies the target but never moves it, and it does not relax ordinary cleanup or integration eligibility.

Before removing the authenticated worker checkout, the launcher resolves and verifies the retirement arguments, terminal and observed heads, base ancestry, selected containment checkpoint, and exact initial target once, then durably records that eligibility proof and anchors the discarded head under a private per-run ref. Retries do not repeat that initial history proof. Before every still-avoidable worktree removal, the launcher freshly resolves the recorded target and requires it to contain the selected checkpoint. While the only valid pre-transaction tuple remains branch and anchor at the discarded head with the receipt absent, it checks containment again, durably updates `retirement_cleanup_target_head` to that exact current target, and atomically verifies that ref while creating the receipt and exact-deleting the branch and anchor. The only valid post-transaction tuple is branch and anchor absent with the receipt at the discarded head. Every other tuple fails closed.

Only after observing the exact post-transaction tuple does the launcher durably record the transaction. It then deletes the receipt with an exact-old-object check, observes its absence, durably records that removal, and finalizes cleaned metadata. A target race leaves the pre-transaction refs intact; an exact retry may checkpoint a newer target descendant that still contains the selected checkpoint. Loss of containment fails closed without deleting those refs and succeeds only after containment is restored. Once the receipt transaction has committed, recovery uses only durable fields and strict phase refs without resolving the initial, discard, final, base, selected-checkpoint, or target objects, so garbage collection may already have pruned them. Conflicting lifecycle state, a partial deletion, an active worker, a changed checkout, or a tampered tuple also fails closed. Repeating the command with the exact checkpointed argument text is idempotent; changed arguments are rejected. A completed retirement uses the ordinary cleaned state, so the overview omits it; its durable record remains addressable by exact run ID with `make status <run-id>`. The compact status output does not print the full retirement audit, which remains in the durable manifest. `make clean-run <run-id>` may resume a retirement only after the direct command has checkpointed it and must continue to reject an untouched quarantine.

## Adding or moving a publication

For a new work:

1. select provider, collection, profile, edition, locale, jurisdiction, and stable identity;
2. create the publishable leaf and all required records;
3. register exceptional shared dependencies;
4. build, validate, review, and install the exact mirrored PDF; and
5. add it to its one owning `library/` page.

For a move, preserve history and update imports, dependencies, internal links, catalog entries, attributes, build paths, and installed mirrors together. Validate every consumer of moved shared material. Leave no second editable copy. Prefer a separate structural commit before substantive revision when the requested order permits it.

## Public navigation and catalog

`README.md` is a terse reader landing page, not a catalog or maintainer guide. It begins with `Don't Panic!`, explains AI and authority limits in ordinary language, links the library sections with the 1962 and postconciliar liturgy pages first and Prayer next, states the reuse boundary, and explains the name.

`LIBRARY.md` is the section index. Each installed publication has exactly one
owning catalog under `library/`. The section landing pages are:

- `library/traditional-latin-mass.md`
- `library/novus-ordo-liturgy.md`
- `library/prayer.md`
- `library/curriculums.md`
- `library/faith.md`
- `library/biographies.md`
- `library/heresies.md`
- `library/historical-accounts.md`
- `library/mariology.md`
- `library/law-and-church-discipline.md`

When one course or repeatable collection would dominate its section landing,
give it one narrowly scoped child catalog such as
`library/ecclesiastical-latin.md`. Link that child from the section landing and
link it back to the section landing. The child, not its parent, owns the
publication entries; do not repeat their PDF links on the landing page. Keep
all `library/` pages at the same filesystem level so source and generated links
remain predictable.

Do not cross-list. Keep derived companions in their canonical work's entry. Link the title directly to the installed PDF, then give a short scope/status statement and separately named reader-facing records required by the profile. Do not link TeX authoring files. Distinguish generation provenance, source audit, independent review, production state, and release status; retain profile identifiers only when they aid readers.

Keep section landing pages terse and prefer compact tables. Expose only the columns a reader needs to choose a work: normally its linked title and a short scope/status statement, with a date, stable ID, or companion column only when it materially aids navigation. Put repository-facing audit links in a final `Supporting records` column. Sort by a profile's stable series order or by occurrence or governing event date where one applies; otherwise use a predictable alphabetical subject or title order, keeping a canonical work and its derived companions together.

On the 1962 page list the Ordinary first, assembly and calendar references second, and proper guides in their compact series table. Keep each curriculum's modules and assessment or reference companions together on its owning catalog page, grouped in prerequisite order. Keep novenas and their short forms together on the Prayer page. Every postconciliar entry names its exact books, edition, language, territory, and date; comparative or discursive works remain with their substantive study category.

`CONTRIBUTING.md` keeps an ordinary-language no-Git path, an isolated agent workflow, and an experimental-branch path. Feedback triggers verification rather than becoming authority. Submissions retain ownership, accept the applicable outbound license, and identify third-party material and its distribution basis.

## Exact-snapshot release

Repository visibility and reader-site deployment are separate decisions. A public repository exposes tracked content and reachable history; a reader site is a generated, history-free artifact under ignored `build/`. Neither follows automatically from a successful build or commit.

`release/public-alpha.json` must exhaustively account for every discovered source and installed PDF:

- `hold` excludes the work from public and private-preview artifacts;
- `review` permits it only in a clearly marked, no-index private preview; and
- `release` requires a current rights record, effective authorization, cleared distribution gates, and the exact approved PDF SHA-256.

`release` means exact-snapshot distribution approval only. It never implies editorial maturity, complete collation, specialist review, an imprimatur, a nihil obstat, or ecclesiastical approval. A changed PDF is a new snapshot and loses its old approval until a new exact binding is recorded.

The authorization inventory also binds every reader-facing Markdown file, template, stylesheet, copied license text, generator, and dependency lock capable of changing the artifact. The public generator may copy only authorized HTML, styles, licenses, PDFs, and narrowly scoped host-control or verification files. It must not copy authoring sources, research records, intermediates, repository metadata, history, or private-preview output.

Preparation, build, verification, push, and deployment are distinct. A preparation command may print current candidate hashes but grants no approval and changes nothing. Verification must independently prove the complete artifact file set, approved repository hashes, dependency lock, local links and fragments, checksums, excluded identifiers, and absence of machine-private paths.

Conditional authorization records its effective instant, timezone, duration, exclusive cutoff when temporary, scope, and machine-recognized conditions. A temporary or request-time-restricted release requires enforceable controls for every page and direct PDF request, cache and rollback protection, monitoring, withdrawal, and purge; a static artifact cannot revoke itself. GitHub Pages is acceptable only for a perpetual authorization that needs no request-time expiration or discovery headers. Publish only a verified artifact through the authorized host workflow, never the repository root or private preview.

## Version control and authority

Preserve unrelated changes and stage only a coherent requested result. Editing, building, installing, committing, integrating, updating a local target, pushing a named ref, and deploying are distinct authorities. A worker's permission for one does not imply another.

Before any push to a public ref, review the exact outgoing range and confirm that every newly reachable source, record, PDF, and historical object is authorized. A push to `main` may trigger Pages after the source is already public; a failed workflow does not retract it. Keep uncleared experiments and private-review material off public refs.

Every AI-assisted commit has a concise result-oriented subject and a body headed `AI summary:` recording the material content, records, guidance, build/publication changes, verification performed, and consequential limitations. Do not claim unperformed checks or include private reasoning or machine-local state.

Use new commits for ordinary corrections, source substitutions, renewed verification, and reorganizations. Do not amend, filter, force-update, or otherwise rewrite published history unless the user expressly requests and coordinates that consequence.
