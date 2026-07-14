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

The project is **Triptych: Catholic Studies in Faith, Worship, and Law**. Its repository slug is `triptych`. The local checkout name and a hosting service's repository name are external to tracked content; renaming them does not require or result from moving source files.

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

## Repository authoring skills

Repository-specific Codex workflows live in the tracked plugin at `plugins/triptych-authoring/`. Its local marketplace entry is `.agents/plugins/marketplace.json`; the marketplace is a repository integration surface, not a document source or publication tree. Keep the plugin manifest, marketplace entry, root README catalog, and plugin README coherent whenever skills are added, renamed, or removed. The manifest must declare `"skills": "./skills/"` so installed copies expose the workflows to new Codex tasks.

Each user-facing workflow is a skill directory at `plugins/triptych-authoring/skills/<name>/`. Its `SKILL.md` uses lowercase kebab-case `name` and a concise `description` that states both the outcome and triggering context; no command-only `argument-hint` or `$ARGUMENTS` interpolation belongs in skill frontmatter or prose. Keep these stable body sections: `What to provide`, `Preflight`, `Plan`, `Actions`, `Verification`, `Summary`, and `Next Steps`. Keep `agents/openai.yaml` synchronized with the skill and provide its display name, short description, and a starter prompt that explicitly mentions the skill. `plugins/triptych-authoring/references/conventions.md` is the single owner of the shared request, evidence, authorization, build, commit, and handoff contract; every skill reads it completely before applying its genre requirements.

`What to provide` is a reproducibility aid, not a parser or mandatory form. A skill must treat the user's entire request and thread context—structured fields, ordinary prose, links, pasted notes, guides, emphases, exclusions, limits, staging, and commit instructions—as controlling task context. It may infer facts safely from the repository and cited authorities, but asks when a missing choice would materially change the result. A creation skill authorizes its normal in-repository source and required publication artifacts; it does not by itself authorize a Git commit, history rewrite, external publication, communication with another person, or unrelated restructuring.

Route skills to documents by actual genre. They must begin with `AGENTS.md`, the universal editorial and repository guidance, every applicable profile, and the target's source and research records. A skill may automate the work sequence, but it cannot lower evidence, metadata, shared-source, build, visual-review, installation, catalog, or commit-message gates. Keep skill help and examples generic enough that edition-, calendar-, jurisdiction-, page-, or series-specific rules remain owned by the appropriate profile. Explicit installed-plugin mentions use `$triptych-authoring:<name>`; natural-language matching may invoke the same skill through its description.

## Adding or migrating a document

For a new document:

1. Select the provider, collection, genre profile, edition, locale, and jurisdiction.
2. Create its directory at the corresponding `src/` path with `main.tex` and required source records.
3. Confirm that recursive discovery finds the document; register only exceptional cross-document shared dependencies.
4. Build, validate, and install it to the exact mirrored `doc/` path.
5. Update the collection catalog and links in the same coherent change.

In the README's `Published Library`, every subsection that lists documents uses a Markdown table, including subsections with only one current publication. Give the plain document title, installed publication PDF, authoring source, and each distinct supporting or audit record separate named columns; do not bundle several links into the title or a catch-all records cell. A subsection may omit a record column that none of its rows uses. Mark an inapplicable cell with an em dash. Keep reader-facing collection-local identifiers in their own column where the governing profile exposes them; do not surface an internal-only ordering key merely to fill that column. Keep the concise scope, evidence state, and review status in a final prose column rather than mixing table rows with prose bullets.

When migrating an existing document, use history-preserving moves and update its imports, build target, dependencies, internal cross-references, README or catalog links, attributes, and installed PDF path together. Validate all consumers of any moved shared fragment. Do not leave a second editable copy at the old location. If a compatibility alias is genuinely needed, make it generated or explicitly transitional and document its removal condition.

Repository restructuring and content revision should remain distinguishable in review and history. Prefer a structure-only commit before substantive revisions when both are required, while ensuring each committed state has internally consistent paths and guidance.

## Version-control hygiene

Track `src/` and `doc/`; ignore `build/`. Preserve unrelated worktree changes and never treat an untracked source record as disposable merely because it can be regenerated. Stage only the files belonging to the coherent change being committed.

Every AI-assisted commit must have both a concise subject that states the result and a substantive commit body headed `AI summary:`. The body must record the principal content, source-record, guidance, build, and publication changes included in the commit, as applicable; the material verification performed and its outcome; and any consequential limitation or review still outstanding. Keep it concise enough to scan but complete enough to explain the committed state without relying on the chat transcript. Do not claim checks that were not run, include private reasoning or session details, or leave an AI-assisted commit with only a terse one-line subject.

Corrections, source substitutions, renewed verification, and newly resolved discrepancies are normal reviewed history. Update the relevant record and explain the reason in the commit rather than erasing the previous state. Avoid rewriting published history for ordinary renames or expanding project scope; a new commit records that evolution honestly unless a history rewrite is explicitly required and coordinated.
