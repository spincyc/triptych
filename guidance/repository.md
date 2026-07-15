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
  devotions/
    novenas/
      shared/                    non-publishable common prayers and formatting
      <numbered-document>/
  articles/
    faith/
    canon-law/
```

`<edition-locale>` must identify the governing edition and language or territory precisely enough to prevent unlike liturgical texts from sharing a directory. Do not use `novus-ordo`, `current`, or a bare language name as the sole identifier. Record additional calendar, lectionary, translation, and jurisdiction details in the document's source record when the directory component cannot express them safely.

The hierarchy distinguishes content families; it does not prescribe a single internal template. Each publishable source document has a directory containing `main.tex` and the supporting files required by its profile. Shared inputs belong at the narrowest common ancestor that genuinely owns them. Keep global typesetting primitives under `src/gpt/common/`; keep rite-, edition-, collection-, and work-specific fragments within their respective subtrees.

Mariological reference works use publishable leaves beneath `theology/mariology/`. Any `theology/mariology/shared/` directory is non-publishable, owns only genuinely shared source material, and has no PDF mirror; all consuming documents must be rebuilt after it changes.

Edition-specific manuals for resolving the 1962 calendar and assembling admitted formularies use publishable leaves beneath `liturgy/roman-rite/1962/reference/`. They follow the 1962 assembly profile rather than inheriting the weekly proper-guide or Ordinary-exposition architecture.

Novenas use numbered publishable leaves beneath `devotions/novenas/` and follow `guidance/devotions/novenas.md`. The `devotions/novenas/shared/` directory is non-publishable and owns only genuinely common prayer text or formatting; every novena consumer must be rebuilt after it changes.

A mechanically derived novena prayer book uses the sibling leaf `<numbered-document>-daily-prayer/`. It imports prayer fragments from the canonical full-guide leaf, declares inherited provenance, and requires explicit cross-document build dependencies; it must not become a second textual owner.

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

`README.md` is a deliberately terse landing page for clergy, religious, and lay readers. Its subtitle identifies the studies as AI driven, while its first heading remains the standalone `Don't Panic!`. The opening moves from AI and authority limits to skeptical reading, ordinary-language feedback, and reassurance that no technical background is needed. It then links Traditional Latin Mass (1962 Roman Rite), Novus Ordo (Postconciliar Roman Rite), Prayer, Faith, Mariology, and Law in one compact library table; keeps the two clearly distinguished liturgy pages first and Prayer next without directing readers where to begin; states the reuse boundary; and ends by explaining the name. Do not put publication catalogs, raw status matrices, repository history, build commands, or maintainer-oriented layout detail back onto the landing page.

`LIBRARY.md` is the public catalog index. Publication listings live on the mutually exclusive section pages `library/traditional-latin-mass.md`, `library/novus-ordo-liturgy.md`, `library/prayer.md`, `library/faith.md`, `library/mariology.md`, and `library/law-and-church-discipline.md`. Every installed publication has exactly one catalog entry across those pages; do not repeat a title or PDF as a cross-listing. A mechanically derived companion belongs in the same entry or row as its canonical work and counts as part of that one catalog home. A page with no dedicated publication says so plainly instead of borrowing cross-disciplinary works from another section.

Restrict `Traditional Latin Mass: 1962 Roman Rite` to the 1962 Ordinary, assembly references, and proper guides: list the Ordinary first, `Assembling the Mass` second, and the proper guides in a compact table. Keep devotional prayer on the separate `Prayer` page; list the novenas there in a compact table with each short form in the same row as its full guide. The reader-facing `Novus Ordo: Postconciliar Roman Rite` title honors common usage while distinguishing the collection from the 1962 books, but every publication placed there must identify the exact postconciliar books, edition, language, territory, and date it studies. Place comparative or other discursive works under their substantive study category rather than duplicating or misclassifying them merely because they discuss liturgy. Lead each primary entry with its plain title linked directly to the installed PDF. Follow with a short scope and status statement, then separately named links to every distinct reader-facing supporting or audit record required by the governing profile. Do not link TeX authoring files from Markdown; they remain discoverable through the repository structure when needed for technical work. A shared scope or status that truly applies to every item in a compact series may appear once before its table or list; do not repeat it on every entry. Focused raw retrieval extracts and structured generation records remain reachable through the supporting records and need not be linked from the catalog unless a profile expressly requires them. Prefer readable lists for heterogeneous works and compact tables for the two series named above.

Keep generation provenance, source evaluation, independent review, and production status distinct in catalog language. Preserve mutable as-of dates and profile-local evidence codes where they materially qualify a publication, but explain them in ordinary language or link their definitions. Keep reader-facing collection identifiers where they aid navigation; do not expose an internal ordering key merely to fill a catalog field.

`CONTRIBUTING.md` is the public contribution guide. It must keep a no-Git path for short, ordinary-language feedback, a clone-and-run path for contributors using an AI agent, and an experimental-branch path for testing materially different base guidance. It must make clear that feedback initiates verification rather than becoming authority, that alternative branches remain distinct from the reviewed library, and that an intentional submission is offered under the applicable outbound license without transferring ownership. Require contributors to identify third-party material and the authority under which it may be distributed.

## Public release artifacts

The full development repository, its history, and installed PDFs may remain private even when a selected reader-facing edition is released publicly. Do not make the development repository public merely to host that edition. Build a public edition as a generated, history-free artifact under ignored `build/`, copying only the material authorized by an exhaustive release manifest.

`release/public-alpha.json` governs the first public edition and must account for every discovered `src/gpt/**/main.tex` document and mirrored `doc/gpt/**/*.pdf`. Its statuses are fail-closed:

- `hold` excludes a work from both public builds and private review previews;
- `review` permits a work only in the clearly marked, no-index private preview; and
- `release` requires a work-specific rights record, or an exhaustive shared record that identifies the work, an effective authorization and its duration, no unresolved release gate, and the exact SHA-256 of the approved installed PDF.

The public site generator renders the canonical reader-facing Markdown rather than maintaining a second editable catalog, but filters publication entries by the manifest. It may copy rendered HTML, site styling, license notices, approved PDFs, and narrowly scoped generated host-control files required to enforce release conditions. It must not copy authoring Markdown, TeX, research or retrieval records, build intermediates, repository metadata, or prior Git history unless a later release policy explicitly reviews and authorizes a category. A private preview may additionally contain `review` PDFs, but it must be marked `noindex, nofollow`, remain local or access-controlled, and never be deployed as the public site.

Before publishing, verify the generated artifact independently against the manifest: its complete file set must be exact; every artifact PDF must match its repository-approved hash rather than merely a generated artifact manifest; every reader-facing source, rendered page, and copied static file must match the approved repository input; the artifact manifest must have no missing or extra fields; local links and fragments must resolve; excluded publication identifiers and machine-private paths must be absent; and recorded checksums must match. Publish only the verified public artifact to a fresh repository or host artifact. Never deploy from the development repository root, a development branch, or the private-preview output.

A conditional release must encode its duration, effective instant, timezone, scope, machine-recognized conditions, and either a null cutoff for perpetual authorization or an exclusive cutoff for temporary authorization. Public checks, builds, and verification fail before the effective instant, and temporary releases also fail at and after the cutoff of their half-open authorization interval. An unadvertised release emits no-index HTML metadata and host response-header instructions for every page and PDF; it has no sitemap, feed, announcement, public release attachment, or promotional metadata. These controls discourage discovery but do not make a public URL private.

A generated static artifact cannot revoke or delete itself. Any temporary public release therefore requires a host control that runs before every asset request, including direct PDF requests, and returns `410 Gone` at the cutoff. It also requires cache control, prevention of rollback to an unguarded deployment, independent monitoring, and a manual project-withdrawal and cache-purge fallback. Verify these controls against the live host before sharing its URL. Do not deploy a temporary release to a host that ignores the generated control runtime merely because the local generator will reject a later rebuild.

## Version-control hygiene

Track `src/` and `doc/`; ignore `build/`. Preserve unrelated worktree changes and never treat an untracked source record as disposable merely because it can be regenerated. Stage only the files belonging to the coherent change being committed.

Every AI-assisted commit must have both a concise subject that states the result and a substantive commit body headed `AI summary:`. The body must record the principal content, source-record, guidance, build, and publication changes included in the commit, as applicable; the material verification performed and its outcome; and any consequential limitation or review still outstanding. Keep it concise enough to scan but complete enough to explain the committed state without relying on the chat transcript. Do not claim checks that were not run, include private reasoning or session details, or leave an AI-assisted commit with only a terse one-line subject.

Corrections, source substitutions, renewed verification, and newly resolved discrepancies are normal reviewed history. Update the relevant record and explain the reason in the commit rather than erasing the previous state. Avoid rewriting published history for ordinary renames or expanding project scope; a new commit records that evolution honestly unless a history rewrite is explicitly required and coordinated.
