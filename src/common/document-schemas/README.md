# Publication schemas

`publication.toml` version 1 declares a publication's canonical source owner,
genre, outputs, semantic source associations and dependencies. Existing authored
TeX stays canonical plaintext. Existing typed dictionaries, calendars,
chronology, response banks and exercise/answer sources keep their own owners
and schemas. This contract does not interpret arbitrary TeX as a semantic tree
or rewrite scholarship into a different format.

The [registry](registry.toml) defines every current provider genre, its owning
profile, required records and review obligations. The executable parser and
adapters are in `scripts/_document_schema.py`; `tools/document-schema` exposes
them without building, installing, fetching witnesses or deploying anything.

```toml
schema_version = 1
id = "gpt/articles/faith/example"
kind = "article-faith"
profile = "guidance/articles.md"
source_format = "latex"
entrypoint = "main.tex"

[[outputs]]
id = "gpt/articles/faith/example"
role = "canonical"
entrypoint = "main.tex"
derivation = "authored"

[[structure]]
role = "body"
source = "main.tex"
outputs = ["canonical"]

[[structure]]
role = "scope"
source = "research/scope.md"

[[structure]]
role = "source-audit"
source = "research/source-audit.md"
```

Source paths are leaf-relative; `data` paths instead name repository-relative
files under `src/`. Exactly one of `source` and `data` is required. Deterministic
file globs may select a bounded set, such as the seven canonical sacramental
summaries; empty matches fail. A structure record may also declare a stable
`key`, `depends_on` keys and selected output roles. Keys cannot form a cycle.
Semantic role names are lowercase kebab case. A role associates actual source
content; it does not certify that a claim or interpretation is correct.

Only the documented fields are accepted. Additional top-level arrays
`content_inputs`, `evidence_inputs` and `render_inputs` declare exact canonical
files or file globs. `canonical_owner` preserves an existing same-provider
generation-inheritance pointer for a mechanical companion. `[contracts]`
preserves existing proper component schema, presentation, format, authority,
chronology presentation and appointed-text-completeness declarations. Those
values must agree with the actual `proper-components.toml`; removing an
applicable contract cannot evade its owning gate.

Output roles are `canonical`, `synthesis` and `homily`. Canonical IDs are
provider-qualified leaf paths; companion IDs add their corresponding suffix.
Schema-1 proper synthesis is a `projection`; schema-2 concise and homily prose
is `authored` within the canonical leaf. Inherited prayer, sacramental and card
companions remain mechanical projections with their exact existing source
owner. Each output has a distinct source-review identity. A future explicitly
declared Markdown owner may use `source_format = "markdown"` and a `.md`
entrypoint; this support grants no automatic conversion or approval of TeX.

## Checks

```sh
tools/document-schema check
tools/document-schema check --include-sources
tools/document-schema check --phase content --json
tools/document-schema show --provider gpt --document articles/faith/example
tools/document-schema identities --provider gpt --document articles/faith/example --json
tools/document-schema propose --provider gpt --document articles/faith/example
```

`source` checks independently discover every `main.tex` leaf and every declared
Markdown owner. They refuse missing or orphaned manifests, unknown fields,
invalid types/identities, omitted or reclassified outputs, unsafe paths,
symlink escapes, cross-provider authored inputs, missing literal TeX imports,
and declared/literal dependency cycles. Adapter discovery reports existing
owners without hiding missing or invalid manifests; default checks still fail
on those defects. `--allow-adapters` is a diagnostic option.

`content` additionally checks required roles against actual bounded canonical
records, nonempty content, applicable source cardinalities and existing
source-only genre validators. These include proper component/chronology
contracts, curriculum selections and answers, dictionary typed inventories,
server data, reference censuses and prose-family evidence structures.
Historical exemptions remain in their existing owning contracts. Current
research currency defects are reported, never repaired by inventing data or
silently regenerating accepted research.

`check --include-sources` also applies the separate neutral source-family
registry and its source-edition validators. Its report and errors are included
without treating a Bible, reading-plan volume or papal reader as an AI-authored
provider leaf. Owning neutral gates marked `not-run` remain separate; this
option neither builds PDFs nor hydrates witness payloads.

`render` adds the applicable existing artifact-phase gates when explicitly run.
`--run-gates` runs the listed owning validators; the default reports them as
`not-run`. A successful manifest/source check does not imply those validators
passed. No phase builds a PDF. Page placement, one-page summaries, trainer
alignment, duplex imposition, typography, rights and actual visual/source
review remain governed by their profiles. Free-text registry requirements are
editorial obligations, not claims that a machine has proved them.

## Identities and Python interface

`discover(root)` returns normalized dictionaries for every discovered owner,
including invalid declarations as `discovery_error` records. `load_manifest`
loads one declared owner. `adapter_manifest` and `dumps_manifest` propose a
lossless declaration of existing files without manufacturing missing records.
`validate(root, record, phase="source", run_gates=False)` reports errors and
separately names owning gates. `identities(root, record)` returns `content`,
`evidence`, `render` and per-output SHA-256 identities with exact input paths.

Content identity covers canonical authoring sources, semantic declarations and
declared/shared source inputs. Render identity adds presentation dependencies.
Evidence identity covers current publication research, declared controlling
owners and source-library metadata ancestry, including artifact hashes/rights
as declared in their canonical manifests. It never hydrates or reads external
witness payloads; exhaustive byte verification remains a separate source gate.
`evidence_metadata(root, paths, source_ids=())` exposes that same metadata-only
closure before a publication manifest exists.

Historical evaluation archives and operational acceptance/install receipts
are excluded from evidence identity so writing a review receipt cannot
invalidate its own seal. Actual scope, source bindings, rights, chronology and
source-audit changes remain visible. Explicit computed TeX imports are reported
as limitations, not guessed at or executed. The adapter conservatively includes
known family shared sources; existing genre validators own their actual
selection semantics. Source identities are neither PDF hashes nor approval
events.


The initial deeper content/currentness findings are recorded in
[`content-baseline.json`](content-baseline.json). They remain errors in the
content phase; source-manifest normalization grants no waiver or renewed
research/print approval. Source-schema publication and content-review
acceptance are deliberately reported separately.
