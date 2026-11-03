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

| Field | Contract |
| --- | --- |
| `schema_version` | Version of this manifest contract; currently `1`. |
| `id` | Provider-qualified leaf identity, for example `gpt/articles/faith/example`; it matches the owning directory. |
| `kind`, `profile` | The registered genre and its owning profile. A title or similar-looking layout does not determine genre. |
| `source_format`, `entrypoint` | Explicit canonical format and leaf-relative entrypoint. Existing `latex` and `structured` sources keep their complete import/data graphs; `markdown` is supported only when it is actually authoritative. |
| `[[outputs]]` | Ordered output identities, roles, entrypoints and `derivation`. Exactly one `canonical` output uses the canonical entrypoint; declared companions use `synthesis` or `homily`. |
| `[[structure]]` | Semantic role with exactly one leaf-relative `source` or repository-relative `data` path under `src/`. Optional `key`, `outputs`, and `depends_on` declare stable nodes, output membership and an acyclic dependency graph. |
| `canonical_owner` | Another same-provider publication that owns a mechanical companion's content, when applicable. It does not transfer research ownership or manufacture another authored work. |
| `[contracts]` | Existing component schema, presentation, format, authority, chronology, and appointed-text-completeness contracts. Values must agree with the owning `proper-components.toml`. |
| `content_inputs`, `evidence_inputs`, `render_inputs` | Additional repository-relative dependencies when controlled discovery is insufficient. Evidence inputs name metadata, never binary witness payloads. |

`derivation = "authored"` identifies authored output; `"projection"` identifies
a mechanical selection or companion. Schema-1 proper synthesis is a projection;
schema-2 synthesis and homily retain their separately authored presentations.
They remain outputs of the same research owner. Do not label a projection as
independent authorship or invent prose to satisfy a common template.

Roles identify meaning and ownership; they need not become visible headings.
One canonical fragment may fulfill several roles without copied text. A
declared required role must point to its actual nonempty record or content,
not an unrelated file renamed to pass a check. A role declaration does not
prove that its content meets the profile.

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

The complete-edition web Print action assembles the selected canonical sections
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

## Browser-print projections

The canonical kind and manifest also select a source-owned browser-print
adapter. They do not replace the native print recipe. General prose and proper
studies, curricula, server guides and cards, pictorial dictionaries, Bibles, and
provider-neutral source volumes retain their own selection and apparatus rules.
The browser controller accepts a finite HTML tag, class, and attribute vocabulary
for each print type, implemented in
[`web-print.js`](../src/web/browser/shared/web-print.js); source-style normalization
is bounded by [`_web_print_common.py`](../scripts/_web_print_common.py). An
unknown executed source construct or untyped formatting requires an adapter
repair, never silent omission or a smaller output.

Independent coverage enumerates the selected canonical source units before
conversion and checks their content, identity, occurrence, and order against
the complete print output. Each adapter retains these additional obligations:

| Print family | Canonical content checked before final sealing |
| --- | --- |
| General publications and propers | Complete semantic ledger, including title qualifiers, headings, source text, notes, references and rights. |
| Curricula | Selected canonical lesson/companion DSL, answers and apparatus, plus the independently derived writing-space and strut geometry. |
| Server guides and cards | Complete selected macro/argument/definition occurrence schedule and unmarked context; final assembly retains every audited fragment, face, label, note, diagram and rights notice. |
| Pictorial dictionaries | Selected object fields, claims, qualifications, audience notes, references, artwork/captions and native cover/plate/terminal context. |
| Bibles | Native verses, labels and order, plus canonical introduction, division/book/chapter headings, source bounds, transformations, rights, links and language. |
| Papal sources and reading plans | Canonical body/reading units and the complete title, extent, period context, source/rights apparatus, attribution links and language envelope. |

An identity count or a list of successful fragment conversions cannot prove
that the final document retained their content. Expectations come from the
canonical source before rendering; the final assembled output must satisfy
them before its text and HTML hashes are sealed. Two identical cold builds
establish reproducibility and do not substitute for that completeness proof.

Parts carry bounded transport, text and structure
hashes, semantic counts, ordered unit inventories, and exact asset identities.
Measuring converted output alone cannot establish this source proof. The retained
HTML-print controller can recheck that projection and its styles; it does not
provide the native TeX generation action. An absent appendix, card face, note,
image, or source unit fails at its owning boundary. These are executable
completeness checks, not source verification, editorial approval, or
certification of physical pagination or duplex alignment.

[Web data](web-data.md#complete-browser-print-products) owns cold preparation and
hot assembly. [Web editions](web-editions.md#browser-printing) owns the reviewed
reader's complete-print action; [printing](../docs/printing.md) explains the
browser and optional native choices.
