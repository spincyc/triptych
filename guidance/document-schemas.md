# Publication schemas

This contract makes a publication's source ownership and structure explicit.
It supplements `guidance/editorial.md`, `guidance/repository.md`, and the
owning genre profile. The executable registry is
[`src/common/document-schemas/registry.toml`](../src/common/document-schemas/registry.toml),
validated by `tools/document-schema`. The registry owns kind names, path
routing, required source roles, and existing gate dispatch; this guide does
not replace the profiles' substantive judgment.

## Canonical sources

Each publishable leaf under `src/gpt/` or `src/claude/` owns one
`publication.toml`. It declares what already has one authoritative owner:
plaintext, shared fragments, typed inventories, and their output entrypoints.
Current TeX remains a lossless authoring source. A manifest is not permission
to flatten a curriculum, liturgical component graph, dictionary inventory, or
table into a generic Markdown document. A future format migration requires
explicit content-equivalence work and the owning profile's review.

Every discovered `main.tex` remains in the publication universe even when its
manifest is missing or invalid. Missing declarations fail validation rather
than silently hiding a work. Shared research and format owners are not new
publication leaves. Provider-neutral external evidence stays in the source
library; another provider's authored substance cannot become a dependency.

## Manifest fields

A manifest states only what is the leaf's own. Everything its path, its
registered kind or its other records already state is derived by the loader
(`scripts/_document_schema.py`) and is not written; a manifest that spells a
derived value out must agree with it, or it is refused. Since 2026-11-04 the
maintainer's rule is one canonical source for every fact: no record repeats
another.

| Field | Contract |
| --- | --- |
| `[document]` | The leaf's [document type](#document-types): the `type`, the leaf's metadata fields, per-edition region lists and option choices. Its edition entrypoints are generated, and its regions are the leaf's one ordered section list. |
| `[[structure]]` | A record the loader cannot derive: a semantic role with exactly one leaf-relative `source` or repository-relative `data` path under `src/`, such as `research/source-bindings.toml` or a curriculum's shared data. Optional `key`, `outputs`, and `depends_on` declare stable nodes, output membership and an acyclic dependency graph. Sections are never listed here. |
| `content_inputs`, `evidence_inputs`, `render_inputs` | Additional repository-relative dependencies when controlled discovery is insufficient. Evidence inputs name metadata, never binary witness payloads. |

### Derived fields

| Field | Derived from |
| --- | --- |
| `schema_version` | This contract: `1`. |
| `id` | The owning directory, provider-qualified (`gpt/articles/faith/example`). |
| `kind` | The registry pattern matching the path; a title or similar-looking layout does not determine genre. |
| `profile` | The kind's registered owning profile. |
| `source_format`, `entrypoint` | The kind: `structured` for a pictorial dictionary, otherwise `latex`; `main.tex`. Only an authoritative `markdown` source states its own. |
| `[[outputs]]` | The canonical output, plus `synthesis` (and `homily` for component schema 2) when the leaf carries `proper-components.toml`; `derivation` is `projection` for an inherited companion and schema-1 synthesis. |
| `[contracts]` | The component schema and contract versions of the leaf's `proper-components.toml`. |
| `canonical_owner` | The inherited generation declaration of `generation-metadata.tex`: another same-provider publication that owns a mechanical companion's content. It does not transfer research ownership. |
| `[[structure]]` records | The body at the entrypoint, `generation-metadata.tex` and `web-edition.toml` when present, and each required role of the kind (and of component schema 2) at its registered path when that record exists. A missing required record still fails as a missing role. |
| Section roles | The leaf's `[document]` regions (below). |

A proper's `proper-components.toml` is read the same way, by
`_proper_components.load_manifest`: `record_type`, `document` (the leaf's
path), `calendar` (`roman-1962` or `postconciliar`, from that path), the
`entrypoint`, `synthesis_entrypoint` and `homily_entrypoint` file names and the
whole `[outputs]` table (the edition ids and their PDF labels, which follow from
`appointed_text_completeness`) are derived, and an explicit value must agree.
The manifest keeps what is the leaf's own: its schema, its element keys, its
components, relations, lanes and presentation roles, its appointed-text
completeness, and its contract pins (`format_contract`, `presentation_contract`,
`authority_contract`, `chronology_presentation`). A pin stays written even where
every current leaf names the same version, because a published leaf keeps its
version when a later one becomes current: a default would re-pin it silently.

A release record, `release/publications/<provider>/<output>.json`, is completed
the same way by `_document_schema.release_record`: its `schema_version`, its
`id` (its path) and its `catalog` (the owning kind's registered `catalog` in the
registry) are derived. Its `status` and `authorization` are release decisions
and always written; a kind with leaves in several catalogs registers none, and
its records state their own ([the record format](../release/publications/README.md)).

`derivation = "authored"` identifies authored output; `"projection"` identifies
a mechanical selection or companion. Schema-1 proper synthesis is a projection;
schema-2 synthesis and homily retain their separately authored presentations.
They remain outputs of the same research owner. Do not label a projection as
independent authorship or invent prose to satisfy a common template.

Roles identify meaning and ownership; they need not become visible headings.
One canonical fragment may fulfill several roles without copied text. A
declared required role must point to its actual nonempty record or content,
not an unrelated file renamed to pass a check. A role declaration does not
prove that its content meets the profile. A role never names a generated
entrypoint: its text lives in the section files the regions place.

## Genre routing

The registry provides the 37 kinds and their exact required-role lists. These
families preserve the material differences between genres:

| Registered kinds | Structure retained by the owning profile |
| --- | --- |
| `article-faith`, `article-canon-law`, `article-scripture` | Free argumentative order; exact sources and terminal scope. Legal work retains jurisdiction and as-of facts; Scripture work retains its bounded passage and reception evidence. |
| `biography` | Chronological life, chronology audit, witness dates, and separately identified later tradition. |
| `history-parish`, `history-translation`, `history-account` | Source-grounded historical sequence and evidence map; pastor succession for parish histories and periodized edition/language history for translations. |
| `novena`, `novena-companion` | Nine distinct received day prayers and their audit; the companion imports exact canonical prayers mechanically. |
| `proper-1962`, `proper-postconciliar` | Appointed sources, actual component-schema version, exact edition/territory/cycle/branches, interpretations and component membership. |
| `mass-ordinary`, `mass-comparison` | Ordered sequence inventory with speech, action, mode and conditional status; comparisons keep each edition's own trail. |
| `assembly-reference`, `calendar-reference` | Rubric decisions and worked cases, or complete normative calendar inventory with exact governing editions. |
| `curriculum-guide`, `curriculum-reference`, `curriculum-memory` | Course dependencies, reference selection, memory recurrence, shared vocabulary and answer ownership. |
| `curriculum-packet`, `curriculum-poetry`, `curriculum-assessment` | Stable lessons, passage/worksheet selections and coupled answers; qualitative readiness and profile-specific teaching order. |
| `server-low-mass`, `server-trainer`, `server-sung`, `server-cards` | Actor/cue/action sequence, shared responses, child/trainer correspondence, team routes, and exact selected duplex faces. |
| `pictorial-dictionary` | Canonical typed objects, claims, variants, artwork and plate selections; audience editions are curated projections. |
| `sacraments`, `sacraments-summary` | Shared sacrament matrix, lexicon, summaries and initiation table, with the profile's distinct treatise/companion order. |
| `virtues`, `angelology`, `heresies` | Subject-specific census, terminology and authority/source inventories rather than a generic monograph outline. |
| `marian-rosary`, `marian-prayer`, `marian-dogma`, `marian-apparition`, `marian-monograph`, `marian-authority` | Exact prayer witnesses, four-dogma scope, competent apparition acts, or the particular monograph/authority structure. |

Provider-neutral Bibles, reading-plan volumes and papal source readers retain
their existing typed canonical schemas and source identities. They are listed
by `tools/print-document` without fabricated GPT/Claude leaves or duplicate
publication manifests.

## Document types

A *document type* writes a kind of edition's skeleton once -- preamble,
PDF metadata, title block, the order of the leaf's own sections, the
deterministic pages placed between them, and the closing provenance block --
so that no leaf hand-codes it and a change to it reaches every leaf of the
type. A type is a directory `src/common/document-types/<type>/`, its name
carrying its version (`proper-study-v1`), holding a `type.toml` and one TeX
template per edition, named `<edition>.template.tex` (a template named
`main.tex` would itself be discovered as a publication). Types are found by directory: adding one edits no list.
`tools/tpt document-types types` lists them with each edition's fields,
regions, section roles, options and slots.

**A leaf opts in** with a `[document]` table in its `publication.toml` naming
the `type`. The table supplies only what is the leaf's own:

- *fields*, the metadata the type declares (PDF title and subject, title-block
  lines, running head). A string at the `[document]` level serves every edition
  that declares that field; `[document.<edition>]` overrides it.
- *regions*, per edition: the ordered list of the leaf's own section files
  (leaf-relative, without `.tex`), and any raw TeX between them that the leaf's
  layout needs (`'\Needspace{12\baselineskip}'`), copied as written. The
  regions are the leaf's **one section list**: no other record lists its
  sections again. A section's semantic roles are stated where it is placed. A
  type may give a region's plain path entries a default role
  (`section_roles = { body = "argument" }`); an entry with other roles, or
  several, is a table, `{ source = 'sections/90-scope', roles = ['scope-appendix'] }`.
  A proper places each of its components by key, `{ component = 'opening' }`:
  the component's path, kind, modes, dependencies and references are its
  `proper-components.toml` record, and a region may not restate that path.
  The schema loader derives each section's structure role from the regions;
  the proper component checker reads each component from its manifest.
- *options*: a choice among the type's fragments `<type>/<option>/<value>.tex`,
  such as a closing block; the type names the default.

Doc-local macros stay in the leaf's `format.tex`, which a template inputs when
it exists. An output whose entrypoint file exists must have its edition table;
a companion that is declared but not yet written may gain one later.

**Entrypoints are generated.** `tools/tpt document-types refresh --leaf
<provider>/<document>` instantiates the type's templates with the declaration
and writes each declared edition's entrypoint (`main.tex`, `synthesis.tex`,
`homily.tex`) as ordinary literal TeX headed "Do not edit". Change the
declaration or the template, never the entrypoint. The entrypoint is literal on
purpose: Make's dependency graph and recorder check, print bundles,
`web-edition`, the schema closure and every content gate follow literal
`\input` paths, so they serve every type without type-specific code.

**Deterministic pages fill slots.** A template line `%@ slot
<projection>/<output>` places a generated page. A projection is one module in
`scripts/document_projections/`, found by file name, that returns every file it
owns for one leaf: its pages under the leaf's `generated/`, and any record it
regenerates. `refresh` runs each projection a leaf's templates slot, then writes
the entrypoints; `refresh --check`, run by `make
check-generated-documents-current`, refuses any generated file that differs from
its regeneration and any authored copy of a generated page. The template
directives and the projection contract are stated in
`scripts/_document_types.py` and `scripts/document_projections/__init__.py`.
The first projection, `scriptural-date-location`, is the proper studies'
Scriptural Date and Location page; its content contract is
[Scripture chronology §14.1](scripture-chronology.md#141-the-propers-wired).

- **To add a type,** create its directory: `type.toml` (`schema = 1`,
  `record_type = "document-type"`, `id` equal to the directory name, a
  `description`, the admitted publication `kinds`, and per edition its output
  `role`, `template`, `entrypoint`, `fields`/`optional_fields`,
  `regions`/`optional_regions`, `options` with defaults and any
  `section_roles`) and its templates.
  A changed skeleton that would move published pages is a new versioned
  directory, so leaves keep their bytes until they are migrated.
- **To move a leaf onto a type,** record its editions first with
  `scripts/render_compare.py snapshot`, write the declaration (moving any body
  held in the entrypoint into section files byte for byte), run `refresh`,
  snapshot again and `compare`. Every difference outside a page the migration
  intends to change is either repaired or reported with its cause.
- **To add a deterministic page to every leaf of a type,** write its projection
  module, add one slot line to the template, and run `tools/tpt document-types
  refresh --all`. No leaf is edited by hand.

## Validation and review

```sh
tools/document-schema check
tools/document-schema check --phase content --document gpt/theology/angelology
tools/document-schema identities --document gpt/theology/angelology
```

| Phase | What it can establish |
| --- | --- |
| `source` | Manifest identity, ownership, known fields, existing paths, output roles, source closure and dependency consistency. |
| `content` | Source checks plus registered required roles and implemented genre content checks. |
| `render` | A request for the existing render-oriented gates; it never builds a PDF or confers visual approval. |

`--run-gates` explicitly runs the existing owning validators. Without it the
report identifies those gates as not run. `--allow-adapters` is diagnostic
only; an inferred proposal never satisfies the requirement for a tracked
manifest. `propose` helps prepare a declaration for review, not approve it.

Content, evidence, and render identities are separate hashes. Content covers
the declared source and its owned textual graph. Evidence covers audit and
binding metadata, whose exact source hashes remain pinned; it does not verify
unhydrated witness bytes. Render identity additionally covers the discovered
format and build inputs. Output identities bind a selected output to those
inputs; none is a PDF hash or an editorial PASS.

The owning `web-edition.toml` contributes its reader decisions to these
identities, excluding only the operational `inspected`, `inspected_by` and
`inspection` receipts at the root and in its recognized synthesis/homily
inspection tables. Recording an inspection must not invalidate that same
review. Eligibility, declaration `reviewed` date, constructs, contents,
withdrawal and all other values remain bound; the full declaration still
passes its validator. Converted reader bytes remain independently sealed.

Keep source/evidence review, print-template review, and actual render
inspection distinct. An existing full-page receipt remains a fact about its
exact old output. A current schema PASS cannot extend it to changed sources,
another renderer, or pages nobody inspected. Ordinary source/web release
verifies canonical inputs and their delivery without generating PDF outputs
or comparing them with historical printings. Issuing a reviewed native print
edition follows
[`docs/printing.md`](../docs/printing.md) and every exact pagination, paired-page,
card, image, and physical-use rule in the owning profile.

## Native print sources

The complete-edition **Generate PDF** action assembles the selected canonical sections
with current shared styles and runs the native TeX recipe in a browser
WebAssembly worker, retaining its original engine, source graph, templates and
fonts. The schema does not authorize flattening TeX into HTML for that PDF.
Source-only preparation may generate deterministic native TeX for structured
families without compiling or storing a PDF during publication. PDF output
remains downstream of this assembly; changing a style or section does not
require rebuilding a PDF corpus before deployment.

A browser source bundle is a bounded transport of one admitted output's
render inputs, with exact file hashes, entrypoint, virtual paths, engine and
source identity. It must preserve imports and source-owned apparatus and
exclude research records and unadmitted selections. Engine, package and font
delivery is separately hash-bound. The public admission set controls every
bundle; the larger local native recipe catalogue is not public authorization.
Changing shared print templates invalidates affected generated-PDF cache
identities without rebuilding the PDF corpus. A disposable browser cache must
match the current source, style and typesetter inputs; it is never a maintained
publication collection. [Repository guidance](repository.md) owns this boundary.

The additive `render_sha256` binds document, output and edition identity,
engine and format, entrypoint, working directory, environment and options,
and the sorted virtual file paths with each file's SHA-256 and size. It excludes
transport packaging and `source_revision`, which remains provenance. Moving
identical source bytes into a shared transport object does not change the
render; changing an included style does. The browser validates the current
bundle before cache reuse and combines this render identity with the runtime
identity and compiler implementation version. Older bundles without the field
retain their exact transport-bound cache identity.

Illustrated outputs carry only the raster artwork their edition typesets,
never a sibling or a filename mention. The sanctuary dictionary's selection
follows its generator's records, plates and per-object artwork; the server
guides' follows the diagram macros active under each guide's edition switches;
other outputs admit literal graphics arguments in active TeX.
[`_native_print_artwork.py`](../scripts/_native_print_artwork.py) and
[`_native_print_bundles.py`](../scripts/_native_print_bundles.py) own these
rules. [Web data](web-data.md#native-print-pages-and-source-bundles) owns the
print pages; [web editions](web-editions.md#browser-printing) owns the web
reader's Print action, and [printing](../docs/printing.md) explains the
browser and local native choices.
