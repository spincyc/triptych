# Repository and Publication Contract

## Governing priorities

Apply these rules in order:

1. keep authoritative plaintext, typed data, manifests, and audit records under `src/`, and track no derived copy of a document's text anywhere;
2. preserve provider, collection, rite, edition, locale, jurisdiction, and document identity in the path and records;
3. give shared text one owner, keep reusable external sources provider-neutral, and declare every consumer dependency;
4. validate source structure and evidence independently of optional print rendering; and
5. treat editing, committing, integrating, pushing, and deployment as separate authorized operations.

`guidance/editorial.md` governs universal content quality. The applicable genre profiles govern document-specific sources, records, structure, and gates. This file governs ownership, paths, builds, catalogs, release artifacts, and version control.

## Ownership and paths

- `src/` contains tracked authoring sources, semantic publication manifests,
  evidence and research records, reusable fragments, and provider-neutral
  typed source data.
- `src/index/` is the narrow derived-metadata exception: shared, reproducible
  addresses, identities, hashes and the small discovery records readers need.
  It contains no copy of corpus prose or rendered reading bodies and is never
  edited as an authority. Canonical TSV, TOML, YAML and TeX retain ownership.
  [Web data](web-data.md#tracked-discovery-and-ordinary-indexed-reading) owns
  freshness, maintenance and the boundary between indexed reading and full
  publication checks.
- Web readers are generated from those sources when the site is built
  (the `web-editions` browser product); no reader text is tracked.
  `guidance/web-editions.md` owns them.
- `build/` contains ignored, reproducible site and build intermediates. In a
  workspace, task-created logs, review output, caches, and experiments go under
  the owning `.scratch/` directory.
- Generated browser reading payloads are outside Git.
  `release/browser-products.json` binds per-family canonical inputs and exact
  expected outputs; `tools/browser-products`
  verifies warm caches and rebuilds exact misses offline. Workspace caches use
  `TRIPTYCH_BROWSER_DATA_ROOT=.scratch/browser-data`; direct producers write to
  an unsealed sibling working tree. `guidance/web-data.md` owns this contract.
- PDF files are downstream print outputs, generated on demand from canonical
  sections and current shared styles. Browser native TeX supplies the public
  action; `tools/print-document` builds one selected local edition. No PDF
  corpus is tracked, maintained externally, or required by normal checks,
  catalog generation, or site deployment.

Anything needed to understand or reproduce a publication belongs in tracked
source or a declared exact-artifact delivery record. The current authoring
format remains lossless TeX plaintext where that is what a publication uses;
existing typed inventories and canonical shared fragments keep their owners.
Adding semantic manifests does not authorize flattening them into Markdown,
dropping content, or creating another editable rendition.

`guidance/document-schemas.md` owns the per-leaf `publication.toml` contract:
explicit kind, profile, semantic roles, dependencies, and ordered editions.
Source review identifies the exact source/evidence graph. Print receipts
identify a renderer/template and a particular inspected render. A successful
source check is not visual approval, and a historical PDF review is not an
approval of changed sources or a different print template.

Normal releases are source and web releases. They validate canonical inputs,
rights, source bindings, manifests, and admitted reader surfaces without
building PDFs, hydrating the evidence archive, invoking Poppler, or demanding
equality with old PDF bytes. When a print edition is requested, apply the
owning profile's print gates to that edition. Strict page counts, paired pages,
duplex geometry, and physically meaningful layouts remain exact unless the
maintainer explicitly changes the profile.

The maintainer's 2026-11-03 clarification rejects a separately maintained PDF
collection as well as PDFs in Git. Canonical sections, manifests, source-owned
apparatus and shared styles are the inputs; selection and assembly precede
typesetting, and a PDF is produced only for a requested edition. A style or
structure change updates those inputs without requiring a corpus PDF rebuild
before deployment. This supersedes the intervening prepared-download proposal.
The current public implementation runs native WebAssembly TeX in the browser
against exact source bundles, original packages and fonts.

An ephemeral output or disposable browser cache is permitted. Reuse must bind
the selected current source graph, shared styles and exact typesetter; changed
inputs invalidate the affected result. Neither a cache nor an archived printing
can become the authoritative source or silently satisfy a request for changed
inputs. Normal publication assembles and verifies the source/runtime transport
without producing PDF outputs. The browser's actual current-edition generation
and its performance require separate evidence.

Exact binary evidence has a separate preservation and delivery layer governed
by `guidance/sources.md`. Its source identity, acquired hashes, rights, passage
pins, and frozen review fingerprints remain authoritative. The physical
delivery sidecar at `src/sources/artifact-delivery.json` maps those identities
to hash-verified external packs and an optional `.scratch/` cache. No ordinary
site build fetches those packs. An archive URL is advertised only after the
particular upload and downloaded bytes have been verified.

Old PDF URLs may lead to an identified reader or print page that explains the
available edition. Such a page is HTML, not a PDF response or a claim that a
historical file is hosted there. Offer a historical binary download only when
its exact archive delivery is verified. Preserve old hashes and review facts
as historical evidence rather than replacing them with current output hashes.

This policy supersedes the former installed-PDF exceptions for reading plans
and papal readers, the deploy-time full-corpus typeset, and release gates that
depended on installed PDF bytes. Removing current-tree binaries does not remove
old Git objects or make an existing clone smaller. History rewriting, remote
cleanup, repository replacement, and publishing an external archive each need
their own authorization; this source migration grants none of them.

External source records remain under `src/sources/`, not a generated provider
branch. Generated indexes and reports are reproducible outputs, not source
identity records. The thin discovery metadata permitted under `src/index/`
does not change that distinction.

Frozen papal installation/review input snapshots use the separate delivery
index `release/papal-documents/input-delivery.json`. Exact original bytes are
preserved externally; compact, mechanically attested input records retain
complete headers and selected rows at unchanged original indices. Routine
metadata checks use those records without opening or fetching raw snapshots.
`guidance/papal-documents.md` owns the extraction and explicit full-audit
contract. Historical evidence is preserved; generated browser caches remain
disposable and are never substituted for that evidence.

Generated documents retain a provider branch. The present providers are `gpt` (documents authored by OpenAI ChatGPT/Codex) and `claude` (documents authored by Anthropic Claude); do not flatten a provider from existing paths. Each provider branch uses this collection hierarchy:

```text
src/common/                       provider-neutral typesetting primitives
src/<provider>/
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
    angelology/
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

Each publishable leaf contains `publication.toml`, its declared authoring entrypoints (currently `main.tex`), `generation-metadata.tex` or a profile-authorized inherited declaration, `web-edition.toml` declaring reader eligibility, and the profile-required records. Shared directories are non-publishable and have no independent output. Put shared material at the narrowest ancestor that genuinely owns it; keep provider-neutral global typesetting primitives under `src/common/` — both providers import the shared preamble, which the build resolves as `\input{common/preamble}` through `TEXINPUTS` — and rite-, edition-, collection-, or work-specific material within its subtree. Hoist a file to `src/common/` only when it is pure typesetting or format and providers genuinely share it. Content-bearing shared material — lesson content, prayer texts, verified liturgical texts, response references — remains inside its provider branch; a provider's documents must not ride on another provider's authored substance.

A proper-guide profile may authorize one canonical leaf to produce multiple PDFs
through a provider-neutral `proper-components.toml` manifest. The bare leaf ID
is the canonical research edition. The mechanical `-synthesis` output is a
derived companion, not a second editable leaf: it has no `main.tex`, source
records, generation record, web declaration of its own, or independently
authored prose, and its web reader is converted from its synthesis entrypoint
under the leaf's declaration (`guidance/web-editions.md`). It is compiled
through the leaf's `synthesis.tex`, inherits canonical provenance, and may
include only components whose manifest mode is `synthesis`. Both output roles
are derived from that manifest ([document schemas](document-schemas.md#derived-fields)) and cataloged in the
canonical row. Their print renderings have independent inspection receipts
when produced; their shared source owner remains the leaf.

For schema 2, [the three-document profile](liturgy/propers-three-documents.md)
supersedes the preceding schema-1 membership and prose-free companion rule.
One leaf owns three independently reviewed entrypoints: the research study,
the concise `-synthesis` study, and the `-homily` companion. Their authored
prose remains in the canonical leaf, with one research trail and generation
record; neither companion is another editable publication leaf. Each has its
own edition role, optional print identity and its own web reader, converted from
its own entrypoint (`guidance/web-editions.md`). The manifest and include graph
establish the build dependencies of all three outputs.

A web reader's route, `web/<provider>/<output>.html`, mirrors the output's
leaf path below `src/<provider>/`; it is built, not tracked. Print output goes to
an explicitly selected ignored destination; a basename is never a publication
identity. For example:

```text
src/gpt/articles/canon-law/example/publication.toml
src/gpt/articles/canon-law/example/main.tex
web/gpt/articles/canon-law/example.html   (site route, built from main.tex)
.scratch/print/example.pdf
```

The stable identity `publication:gpt/articles/canon-law/example` selects the
source owner; a declared edition role selects one output. The same rule
applies to each provider. Historical mirrored `pdf/` paths may remain in
receipts and compatibility routing, but are not current input paths.

A document leaf ID such as `articles/faith/ontological-vertigo` may exist under more than one provider. Each provider edition is an independent work on the same scope: it keeps its own research records, its own sections, and its own generation metadata, and reuses no text across providers. Publication identity is provider-qualified — the provider plus the leaf ID.

Use lowercase kebab-case slugs. Stable identifiers are namespaced by their profiles and are not interchangeable across collections or editions. A number is not a claim of importance.

**Anything with an inherent order sorts in that order in a directory listing.**
A path component carrying an ordered thing is prefixed with what orders it,
zero-padded to a stated width — canon position for a book of scripture, date for
an edition, a witness or an act. A listing is the first index anyone reads, and
one arriving alphabetically when its subject is chronological or canonical makes
a reader reconstruct the order in their head every time.

`guidance/sources.md` settles that rule and its two limits — a path is not an
identity, and the prefix is *derived* from the record rather than typed beside
it. Its applications live with their subtrees and are not restated here:
`guidance/web-data.md` for canon position and chapter padding, derived in
`scripts/_canon.py`; `guidance/act-histories.md` §13 for act and witness dates.
A profile fixes the series order within a collection; it does not decide whether
an ordered thing sorts.

## Shared sources and records

One text has one authoritative owner. Import it into every consumer and declare build dependencies that rebuild all consumers after it changes. Do not create editable copies for convenience. Derived companions must identify their canonical owner and may inherit provenance only when their profile permits it.

For componentized proper guides, the manifest is the ordered dependency graph.
Every component and its component-scoped reference file belongs to the
canonical leaf. A component included in an output may not depend on a
component omitted from that output. Stable element keys and synthesis-relation
keys are publication data and must not be derived from headings or display
order.

Keep records with the owning leaf or a clearly owned shared source. They must identify the exact editions, witnesses, translations, jurisdictions, dates, source roles, checked loci, unresolved discrepancies, rights basis, and completed review required by the profile. Focused third-party extracts may be tracked when necessary and distributable; complete scans, bulk OCR, private caches, and machine-specific corpora do not belong in publication leaves.

Repository-wide external-source reuse follows `guidance/sources.md`. Its work,
edition, artifact, segment, passage, corpus, and binding records remain
distinct from shared authored publication fragments. A segment may identify a
constituent under its truthful edition while pointing to exact container bytes
owned by another work; it does not transfer or duplicate those bytes. Lawful
textual source artifacts may remain tracked under `src/sources/`;
exact binary preservation uses the declared delivery layer. Restricted bytes
and machine-private caches may not enter Git or public output. A
publication-local binding records why and how that publication used a central
source. Central identity never supplies a consumer's interpretation
automatically.

Do not combine unlike formularies, editions, translations, jurisdictions, or unrelated works in one record merely because they share a theme. Never record credentials, private communications, host or user identity, machine paths, network data, or session identifiers.

## Rights and project identity

`LICENSE` defines the outbound terms and `THIRD_PARTY.md` the repository-wide exclusions. Project-created content is CC BY 4.0; the software and reusable infrastructure identified there are MIT-licensed. Those grants do not relicense third-party or public-domain content.

Record a local rights statement wherever Scripture, official or liturgical text, a received prayer or hymn, a third-party translation or quotation, OCR, a font, or other external material could be mistaken for project-owned expression. Identify the known author, source, attribution, license, permission, public-domain basis, or legal exception. Age, official status, citation, retrieval, and public availability do not establish permission.

Every publication retains the common rights notice as a compact final-page colophon; it must not force a dedicated page. The colophon contains only the universal license boundary and pointers to `LICENSE` and `THIRD_PARTY.md`. A local notice may add necessary precision but may not weaken or duplicate that boundary. The Triptych name and visual identity do not convey endorsement, official status, or ecclesiastical approval to a derivative.

## Tool registry

`tmt.json` indexes the repository's tools. Every registry id is an executable
script at exactly `tools/<id>`, which `tmt` requires and `tmt check` enforces;
an id may not be aliased to another basename. Run a tool directly, or through
the `tools/tpt <id> [args]` launcher, which adds `--list`, `--info <id>`,
`--path <id>`, and `--check`; the first two take `--json`. The launcher's own
controls are dash-prefixed and tool ids are not, so a new entry can never
shadow one.

Everything else under `tools/` is either a subdirectory, which `tmt` ignores,
or a `.md`/`.test` companion. Shared library code and tool data live in
`scripts/`; a bare file in `tools/` without a registry entry fails the gate.
Python tests live in `tools/tests/`; `tests/tools/<id>.test` holds each tool's
shell smoke test, and every registered id must have one. `tmt check` counts the
registry and not the smoke tests, so the rule is enforced by
`tools/tests/test_tool_registry.py`; every registered id has one as of
2026-08-02, `act-history` having been the last without. A rule stated as
enforced and checked by nothing is the apparatus committing the defect it
exists to catch.

Register a new tool with `tmt new <id>`. `make check` runs `tmt check`, which
must stay green; it is skipped, not failed, where `tmt` is not installed.

Every verb's help ends in two real invocations, and they are held to real runs:
`make check` runs `make check-examples`, which replays each one and compares it
to the transcript stored beside it, line for line, so a transcript changes by
`make recapture-examples` and never by hand. An invocation that must not be
replayed — one that reaches a model or the network, or writes tracked release
state — is named with its reason in `scripts/replay_examples.py`, as is every
transcript already known to be stale; all of them are printed on each run.

The help page shows the invocations and the note, and **not** the transcript.
The two jobs a capture does are separate: the reader wants the command to copy,
and the replay wants the bytes. Printing both put a page of output under every
verb. The transcripts are still captured, still stored in each tool's
`EXAMPLES` table, and still replayed — the replay is now their only reader,
which is what keeps them honest.

## What a tool may print

The stream at the far end of a tool decides what it can carry, and the question
is a property of the run rather than of any tool, so it is answered once in
`scripts/_tooling.py` and passed to every renderer as an argument. Three tiers:

- **plain** — ASCII only: `V.`/`R.` for ℣/℟, `--` for an em dash, no colour. It
  is reached by `--plain` (or `--style plain`) **whatever is detected**, because
  detection is a guess and an operator who says plain means plain; and by
  detection where the stream's encoding cannot carry the glyphs, or where a
  terminal advertises no capability at all (`TERM` empty or `dumb`).
- **unicode** — the glyphs, decided by the stream's own encoding and not by
  `TERM`: a UTF-8 pipe into a file carries ℣ with no terminal at either end.
- **rich** — headings, rules, weight and colour, where the stream is a tty and
  the terminal names itself. Colour honours `NO_COLOR` and is never the only
  carrier of meaning: every distinction it draws is also drawn in words or in a
  rule, so a monochrome reader loses decoration and no fact.

`--json` and `--format yaml` bypass the layer entirely and are byte-identical
across tiers: they are contracts other programs read, and must not move with
the terminal they happen to be printed at. Detection is tested by table in
`tools/tests/test_terminal_tiers.py`, from any machine and with no pty.

## Build and review contract

The normal lifecycle validates sources and builds the reader site:

```sh
export TRIPTYCH_BROWSER_DATA_ROOT=.scratch/browser-data  # workspace cache
make                       # source-only public site
tools/document-schema check
make check
make public-site
```

The Pages build job runs `make pages-site`: the same deployment source gates
and site build as `make check-deployment-sources` and `make public-site`, but
with the gates beside the single-process site build instead of before it. A
failing gate fails that step, so `public-alpha verify`, cache retention and the
upload never follow it; the site it may have assembled never leaves the runner.
Locally, `make public-site` keeps the stricter order.

`make` and `make all` select the source-only site path. `make pdf` remains an
explicit developer opt-in for a corpus PDF build; it is not a normal check or
deployment prerequisite. Prefer the selected-document print command for an
individual edition. Pages deploys only after its `print-compile` job
(`make check-native-print-compile`, owned by `docs/printing.md`) has compiled
every admitted edition from its served source bundle against the browser
runtime's file closure; that job is a verification gate whose PDFs are
discarded, not the superseded deploy-time corpus typeset, a prepared-PDF
collection or a print review.

`docs/printing.md` gives the single-document print commands. A print request
selects one stable document identity, one declared edition, and an output
path. It must not silently rebuild the corpus or install into tracked paths.

Build recipes declare every render-affecting input and shared-consumer edge,
isolate concurrent targets, stop on fatal failure, and never expose partial
output. Every build that typesets a publication edition supplies its
revision stamp, derived from Git history by `scripts/_edition_revision.py`
under the rule in `guidance/editorial.md` (§ Revision timestamp), as the
generated `<job>.revision.tex` the shared preamble reads; a build with no stamp
fails rather than printing none. Such a build therefore needs a full, unshallow
checkout. Omit build-clock PDF dates and automatic trailer IDs; the only
build-time date is the marked stamp of a build from uncommitted sources.
Repeating unchanged inputs and history under a pinned toolchain should
reproduce a render, but ordinary source releases do not compare rebuilt PDFs
with historical publication bytes.

The shared provider preamble owns its guarded `\pdfcompresslevel=1` setting.
It trades some output size for faster lossless stream compression without
altering source wording or page layout. Keep the setting in that authoritative
style, so its source identity invalidates affected browser results naturally;
do not introduce an untracked compiler override or regenerate a PDF corpus to
adopt it. Other print families retain their own styles. The bounded comparison
and review limits are linked from [printing](../docs/printing.md).

Source-bearing changes run the universal and profile content/evidence gates,
`tools/document-schema check`, and `make check-sources`. The latter validates
the source graph, publication bindings, legacy inventory, and reviewed family
ledger; honestly pending family review remains permitted. The separate
`make check-source-family-screening` target is a completion audit. Neither
source-schema validation nor source release confers print-layout approval.

Normal deployment uses the complete browser-product descriptor for source and
act-history projection freshness. Its strict cold producers, exact input/output
closure and held publication snapshot replace the separate warm receipt gates.
The older receipt checks remain explicit standalone audits and part of
`make check-research-sources`, without becoming publication authorities. This
consolidation retains the other rights, source, schema and currentness gates.

When producing a reviewed print edition, compile enough passes to settle
contents and references. Reject fatal errors, undefined references, overflow,
and unresolved layout warnings. Check PDF structure, embedded fonts,
metadata, extracted text, clipping, density, and the rights colophon. Follow
every exact pagination, paired-page, card, illustration, and physical-use gate
in the owning profile; flowing browser print does not satisfy those gates.

Use `tools/pdf-review` for page rasters and bounded contact sheets. It owns
concurrency and memory controls; do not substitute raw parallel ImageMagick or
equivalent whole-document jobs. Give each invocation its own replaceable
`.scratch/` directory and keep logs and receipts outside it. A cache hit or
contact sheet is not inspection. Record the reviewed output hash, renderer
and template identity, inputs, and actual page extent inspected when a review
is required. Never infer a full-page PASS from a schema or build result.

Audit print and artwork size after composition settles. Investigate a PDF
above 1 MiB or 75 KiB per page and a publishing raster above 1 MiB, above two
megapixels without a placement need, above 450 effective dpi, or RGB in a
monochrome work. These are review triggers, not quotas. Preserve an artwork
normalization's dimensions, mode, hashes, comparison and full-size inspection
in its owning record, and review affected print consumers.

Exact acquired evidence is a preservation input. Do not recompress, re-encode,
or optimize it to reduce storage; a new derivative is a distinct artifact.
`guidance/sources.md` owns physical relocation without changed bytes or source
fingerprints. An evidence-only correction need not render unchanged text,
but its affected consumers must remain discoverable and reviewed for source
impact.

## External-review handoffs

When a task or governing record requires external visual, product, source,
architectural, or acceptance review, prepare the unique ignored review package
and sibling ZIP governed by
[external-review handoffs](external-review-handoffs.md). The package transfers
evidence; the owning tracked record retains any durable review disposition.

## Direct Codex sessions

The ordinary Codex workflow runs directly in the current checkout. A direct
session may edit, build, inspect, create coherent commits, and push validated
checkpoints regularly to `origin/main` within the standing authority in
`AGENTS.md`. Before a push, inspect the exact outgoing range, confirm that
every newly reachable object is intended for public disclosure, and complete
the checks required by the affected guidance. Pushing `origin/main` starts the
GitHub Pages workflow and therefore authorizes that automatic deployment
attempt. It does not authorize another deployment, a force-push, or history
rewriting.

An assigned workspace branch and explicit task limits govern that session;
the ordinary `main` workflow does not authorize switching its branch or
publishing a different ref.

## Adding or moving a publication

For a new work:

1. select provider, collection, profile, edition, locale, jurisdiction, and stable identity;
2. create the publishable leaf and all required records, opting into the
   genre's [document type](document-schemas.md#document-types) where one
   exists rather than hand-writing its entrypoints;
3. register exceptional shared dependencies;
4. validate its manifest, source records, and eligible reader edition; and
5. add it to its one owning `library/` page.

For a move, preserve history and update manifests, imports, dependencies, internal links, catalog entries, attributes, and generated routes together. Validate every consumer of moved shared material. Leave no second editable copy. Prefer a separate structural commit before substantive revision when the requested order permits it.

## Public navigation and catalog

`README.md` is a terse reader landing page and the section index — not a
per-publication catalog and not a maintainer guide. It links the seven durable
library portals, the browser entry points, and the `docs/` accounts of how the
work was built. `ABOUT.md` is the consumer overview: it begins with
`Don't Panic!` and explains AI and authority limits, the reuse boundary, and the
name in ordinary language.

Each publication has exactly one
owning catalog under `library/`. A related-resource link on another row of
that same catalog uses an explicit
`<!-- triptych-publication-reference: [provider:]output-id -->` for each
repeated HTML destination. A reference must name a declared output owned by
this catalog and visibly linked on that row; it never supplies a missing owner
or declares another publication. Ordinary duplicate-owner, provider and hold
checks still apply, and the markers are removed from rendered pages.

The root landing tables expose exactly seven
reader portals, in this order and with these muted liturgical-color identities:
white `Faith`, gold `Scripture`, red `Liturgy`, green `History`, violet
`Formation`, rose `Mary`, and black `Law`. Gold is an interface category for
Scripture rather than a claim that gold is a separate universally prescribed
Roman liturgical color.

`library/faith.md`, `library/scripture.md`, `library/liturgy.md`,
`library/history.md`, `library/formation.md`, `library/mariology.md`, and
`library/law-and-church-discipline.md` are the portal landings. Detailed
catalogs such as the two Roman Rite pages, Prayer, Curricula, Biographies,
Heresies, and Historical Accounts remain their children. A portal may route to
an existing child subsection when a subject spans categories, but publication
links remain on exactly one owning catalog.

The root tables do not promote a subsection already contained by a portal, a
child catalog, or an individual publication to a peer row. A direct
child-catalog or publication spotlight is an explicit maintainer exception
and belongs outside the section table under a clear featured-work label; it is
not a precedent for cross-listing.

When one course or repeatable collection would dominate its section landing,
give it one narrowly scoped child catalog such as
`library/ecclesiastical-latin.md`. Link that child from the section landing and
link it back to the section landing. The child, not its parent, owns the
publication entries; do not repeat their edition links on the landing page. Keep
all `library/` pages at the same filesystem level so source and generated links
remain predictable.

A single unusually long or prominently requested work may likewise receive one
narrowly scoped child landing when readers materially benefit from direct
format links, a safety or reliance boundary, and section-level web navigation.
That child owns the publication entry and stable publication marker. Its
section landing links to the child without repeating its edition links.
`README.md` may feature the child outside its section tables when the
maintainer has expressly requested landing-page visibility. Keep a review
edition's status and material completion shortfall conspicuous on the child
page; navigation must never imply that an interim edition fulfills the
promised final scope.

A leaf ID keeps exactly one owning catalog page no matter how many provider
editions exist. Outside profile-authorized provider-specific subsections, its
provider editions occupy one row even when their titles differ. In that case,
use a neutral shared-work label in the first cell and preserve each exact title
in its provider cell's publication link. Ordinary catalogs use named `ChatGPT`
and `Claude` columns.
The complete Sunday-propers calendars also keep named provider columns.
The postconciliar calendar adds a `Cycle` column: distinguish `A`, `B`, and
`C` rows wherever their available editions differ; cycles with identical
availability may share one row. The maintainer requested this separation on
2026-09-28 so each provider's documents can be compared directly. A hidden
stable-publication marker retains ownership for held work whose reader cell
is plain text; it never replaces a released artifact's visible link.
Title cells remain unlinked bold text.

A componentized proper guide remains one catalog identity. Its provider cell
links the available reader edition and declared print editions in source order.
Schema 2 distinguishes research, synthesis, and homily; neither companion gets
another work row or another source owner. Label a rights-limited or authorized
reference-only research edition accurately. A companion without an HTML
conversion may link a page explaining print options, with its available format stated
plainly. Do not label that page as a PDF download.

A named `ChatGPT` or `Claude` column contains only that provider's editions.
Format labels need not repeat the provider. In mixed-provider legacy tables,
every edition link names its provider. Show `Planned` where a provider has no
admitted edition; keep the stable-publication marker for held work without
advertising it as released.

A curriculum landing follows the provider-column rule at course level. Each
provider link opens its course section in the child catalog, which lists
modules and companions in reader order. Each work retains one owning row.

Do not cross-list or expose source ZIPs as the reading experience. Reader
links open the existing reader or an honest page explaining print options. Do not
link TeX, research records, audits, manifests, provenance, production state,
or release bookkeeping from reader landing pages. Those records remain
auditable in source. Keep an edition, territory, as-of date, stable ID, or
availability notice only when it helps readers choose or use the work.

Keep section landing pages terse and prefer compact tables. Normally expose
only a bold title, its provider links, and a short statement of subject, use,
or audience. Add a
date, stable ID, or companion column only when it materially aids navigation.
Sort by a profile's stable series order or by occurrence or governing event
date where one applies; otherwise use a deliberate reader sequence, keeping a
canonical work and its derived companions together.

On the 1962 page list the Ordinary first, assembly and calendar references second, and proper guides in their compact series table. Keep each curriculum's modules and assessment or reference companions together on its owning catalog page, grouped in prerequisite order. Keep novenas and their short forms together on the Prayer page. Every postconciliar entry names its exact books, edition, language, territory, and date; comparative or discursive works remain with their substantive study category.

`CONTRIBUTING.md` keeps an ordinary-language no-Git path, an isolated agent workflow, and an experimental-branch path. Feedback triggers verification rather than becoming authority. Submissions retain ownership, accept the applicable outbound license, and identify third-party material and its distribution basis.

## Exact-snapshot release

Repository visibility and reader-site deployment are separate decisions. A public repository exposes tracked content and reachable history; a reader site is a generated, history-free artifact under ignored `build/`. Neither follows automatically from a successful build or commit.

The public-alpha inventory must account for every discovered publication leaf
and declared output role. Accounting is provider-qualified: one provider's
release state never covers another provider or an undeclared companion:

- `hold` excludes the work from public artifacts and ordinary review previews;
- `alpha` includes an admitted edition when its source, rights, safety,
  reproducibility, mechanical-validity, and basic-visual-usability checks pass;
  and
- `published` records deployment of a verified alpha artifact.

The editorial status `review` includes an admitted edition in the public alpha
when the alpha concerns pass. It is internal release control and does not
control reader-facing labeling or ordinary discoverability.

Alpha and published are distribution states, not editorial promotions. Neither
asserts completeness, finality, official status, an imprimatur, a nihil obstat,
or approval by an external authority. These internal states are not rendered
in a PDF, web edition, catalog, title-page footer, running footer, or public-site
banner. The owning document instead states its actual scope, completion limits,
completed review facts, and any work-wide reliance boundary once in its
terminal scope-and-qualifications appendix, without explaining the release
workflow. Immediate safety warnings, claim-local legal qualifications, and
legally necessary notices remain where readers need them.

Each migrated publication owns
`release/publications/<provider>/<leaf-id>.json`; the path below the provider
mirrors the leaf ID. That independently writable record contains its catalog,
alpha or hold state, and standing authorization reference. Current source
identities,
provider and status counts, and the aggregate publication manifest are
generated during artifact construction and are not tracked publication inputs.
During migration, a local record overrides its matching legacy row in
`release/public-alpha.json`; an unmigrated publication continues to use its
legacy row. Ordinary publication work never rewrites a shared rights-table
snapshot inventory.

The maintainer's standing public-alpha decision of 27 July 2026 authorizes
every current and later document snapshot to enter `alpha` without a new
document-by-document approval request, provided that the six alpha concerns
pass and the source/evidence and generated reader identities are reproducible.
This standing decision authorizes ordinary research, source validation,
reader builds,
and coherent commit steps needed to prepare current public links.
For a direct session on `main`, it also authorizes regular validated pushes to
`origin/main` after review of the exact outgoing range and its public
disclosure. Such a push starts the GitHub Pages workflow and authorizes that
automatic deployment attempt. Launcher-managed workers remain non-pushing and
must use their retained-run integration boundary. No part of this authority
may be recorded as external approval or final editorial judgment.

An explicit user deliverable—such as promised scope, minimum extent, named
sections, formats, or publication surfaces—must be recorded in the owning
research scope before work is represented as complete. If the admitted edition
does not yet meet that deliverable, it may remain discoverable as `alpha` if it
states its actual present scope in the terminal scope-and-qualifications
appendix and in its owning record, and never substitutes successful build,
review, installation, or distribution for fulfillment of the promised
deliverable.

The authorization inventory also binds every reader-facing Markdown file, template, stylesheet, copied license text, generator, and dependency lock capable of changing the artifact. The public generator may copy only authorized reader HTML, browser data, styles, licenses, and narrowly scoped host-control or verification files. It does not build or copy PDFs or binary evidence packs. It must not copy authoring sources, research records, intermediates, repository metadata, history, or private-preview output, except for the explicitly bounded native print source bundles below.

The maintainer's 2026-11-03 native-print request authorizes one narrow static
transport: the current admitted edition's exact native TeX render inputs,
identified and hash-bound under the native source-bundle protocol. These
bundles preserve canonical source bytes and original virtual paths; they
exclude research, repository metadata, held/withdrawn outputs and unrelated
source-library material. Verified native engine, package and font assets may
be published alongside them under their own delivery and license manifests.
This exception permits actual TeX generation in a browser worker on GitHub
Pages; it does not authorize copying source directories or generating a PDF
corpus during deployment. The public action uses client-side native TeX;
alternative execution methods remain separate design work and do not authorize
a persistent prepared-PDF collection or a deploy-time corpus rebuild.

Preparation, build, verification, push, and deployment are distinct. A preparation command may print current candidate hashes but grants no approval and changes nothing. Verification must independently prove the complete artifact file set, approved repository hashes, dependency lock, local links and fragments, checksums, excluded identifiers, and absence of machine-private paths.

Conditional authorization records its effective instant, timezone, duration, exclusive cutoff when temporary, scope, and machine-recognized conditions. A temporary or request-time-restricted release requires enforceable controls for every authorized page and direct request, cache and rollback protection, monitoring, withdrawal, and purge; a static artifact cannot revoke itself. GitHub Pages is acceptable only for a perpetual authorization that needs no request-time expiration or discovery headers. Publish only a verified artifact through the authorized host workflow, never the repository root or private preview.

## Version control and authority

**Storage migration does not authorize history cleanup.** Removing current-tree
binaries leaves reachable historical objects intact. Do not infer that a fresh
ordinary clone is small until the retained history and fetch policy have been
measured. A history rewrite or remote-ref cleanup requires explicit authority.

**Do not repack this repository with Git's defaults.** The pack was built by an
aggressive repack and is held together by long delta chains; a plain
`git repack -adf` recomputes them at the default window and depth and makes the
pack *larger* — measured on 2026-09-05 at 399.78 MiB before and 413.49 MiB
after, a 3.4% loss. Nothing in the repository records this, because pack
settings live in `.git/config` and are not tracked, so the trap is invisible
until it is sprung. Use `git gc --aggressive`, or pass `--window=250
--depth=250`, and leave a repository alone that does not need one.

The reason is structural rather than incidental: 72% of the pack is PNG, JPG
and PDF, which zlib already compressed and which deltify only against earlier
revisions of the same file. Tuning cannot recover it either — the best of eight
measured configurations beat the current pack by 1.96 MiB, and marking those
extensions `-delta` in `.gitattributes`, which looks like a free saving, costs
**35 MiB** because 64 PNGs and 117 PDFs do get useful delta bases. The `binary`
attributes already recorded there are correct and do not imply `-delta`.

Preserve unrelated changes and stage only a coherent requested result.
Editing, building, installing, committing, updating another local target,
pushing another ref, and deploying outside the
automatic Pages workflow remain distinct authorities. Direct sessions follow
the authority in `AGENTS.md`. An assigned workspace
branch and explicit task limits take precedence over its ordinary `main`
workflow; do not switch or rename a workspace branch.

Before any push to a public ref, review the exact outgoing range and confirm
that every newly reachable source, record, PDF, and historical object is
authorized. Run the checks required by every affected profile and publication
surface before pushing. A push to `origin/main` triggers Pages after the
source is already public; a failed workflow does not retract it and must be
diagnosed and corrected in a later coherent checkpoint. Keep uncleared
experiments and `hold` material off public refs.

### Branches

Origin carries `main` and three other kinds of ref, and nothing else. A name
says who is doing what, so it can be predicted before the branch exists and
found after it is gone.

| Ref | Holds | Lifetime |
| --- | --- | --- |
| `main` | integrated work; a push deploys | permanent |
| `feature/<agent>/<area>/<topic>` | one line of work by one agent | until merged into `main` or archived |
| `evidence/<topic>` | review evidence that exists nowhere else; never merged | permanent |
| tag `archive/<former-branch>` | tip of a superseded or abandoned line whose commits exist nowhere else | permanent |

- `<agent>` is the tool doing the work — `claude`, `codex`, `droid` — or
  `maintainer`. `<area>` is the part of the project: `propers`, `catena`,
  `browser`, `bible`, `missal`, `sources`, `theology`, `pictographic`,
  `metaphysics`, `tpt`, `repo`; add one only when none fits. `<topic>` is one
  or more lowercase kebab-case components, such as `tlm/54` or `homily`.
- `wt <agent> triptych/<agent>/<area>/<topic>` creates the workspace, its
  clones, and this branch. Name the workspace, not the branch.
- Leaves only. Git cannot hold `feature/claude/propers/tlm` beside
  `feature/claude/propers/tlm/54`, so no name is a prefix of another. When one
  topic needs several branches — an implementation and its independent review,
  or two replays — make each a leaf under the topic (`…/<topic>/impl`,
  `…/<topic>/review`), never a numbered sibling such as `-v2` … `-v16`.
- A correction round is new commits on the same branch. A review names the
  exact commit it reviewed; that SHA, not a version suffix, identifies the
  snapshot.
- Once merged into `main`, delete the branch on origin. A line superseded or
  abandoned with commits nowhere else becomes tag `archive/<branch>` before
  its branch is deleted; one with nothing unique is simply deleted.
- Clones made before the 2026-09-05 rewrite carry the old history. Never push
  from one; clone again.

On 2026-09-24 origin was brought to this shape. Of 104 branches, 17 stayed
(`main`, the fifteen `evidence/*` branches, and one active propers branch);
three unfinished lines moved to `feature/claude/pictographic/low-mass`,
`feature/droid/metaphysics/reading-metaphysics`, and
`feature/droid/browser/catena-omnia-b0-b1`; 29 superseded lines became
`archive/*` tags; and 55 branches already merged or contained elsewhere were
deleted.

**Several agents share one working copy, and therefore one git index.** `git add`
stages into that shared index, and a bare `git commit` commits all of it —
including whatever a sibling staged a second earlier. Always name the paths:

```sh
git commit -m "..." -- <path> [<path> ...]   # or: git commit --only <paths>
```

Check `git status --short` before and `git show HEAD --stat` after. Rebind the
release record the same way, `make refresh-release-bindings ONLY="<paths>"`,
never `ADOPT=1` while others are working.

On 2026-08-01 a one-file guidance edit committed with a bare `git commit`
carried another lane's staged deletions — 62 files, 49,029 lines of the
catena's browser structure — into a push, publishing a deletion before its
replacement existed; Catena Omnia returned 404 on the live site until the
replacement landed. Two other lanes had work swept into each other's commits
the same day, and one such commit is pushed and no longer safely fixable.

**The stash is shared too, and it is worse than the index.** `git stash pop`
takes `stash@{0}` — whichever entry is on top when it runs, not the one you
pushed. Between a sibling's push and your pop the top entry changes, so a
scoped `git stash push -- <path>` does not make the matching pop scoped. On
2026-08-01 a pop applied a stash taken at `4a9769b8`, months of tree-shape
behind HEAD, leaving conflict markers in 14 paths including `scripts/_catena.py`,
which broke every catena gate and the coverage tool with a `SyntaxError` while
two lanes were mid-flight in the same files. Prefer `git worktree`, or copy the
file aside and copy it back; if you must stash, pop by exact ref and message.

Recovering a bad pop: a conflicted pop does NOT drop the entry, so the stash is
still the copy of record — check `git stash list` before anything else. Take
the working-tree side, `git checkout --ours -- <path>`, because for a stash pop
that is the tree as it stood, uncommitted sibling work included; the stash side
is what you are declining to apply. `git add` each path to clear the unmerged
state, then `git reset -- <path>` so the resolution does not sit staged in the
shared index waiting to be swept. Verify what you repaired actually parses.

Every AI-assisted commit has a concise result-oriented subject and a terse body headed `AI summary:` — one or two sentences naming the material change and the verification performed. Do not claim unperformed checks or include private reasoning, narration, or machine-local state. The same terseness governs code comments: state only what the code cannot say itself.

Use new commits for ordinary corrections, source substitutions, renewed verification, and reorganizations. Do not amend, filter, force-update, or otherwise rewrite published history unless the user expressly requests and coordinates that consequence.
