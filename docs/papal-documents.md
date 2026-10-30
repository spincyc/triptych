# Papal documents: finding an act and reusing its source

The papal catalog groups encyclicals, bulls, briefs, apostolic constitutions,
apostolic exhortations, apostolic letters, and motu proprio by pope, date,
document kind, and available language. Each entry points to the issuing
authority's text. A repeated incipit remains a separate document when its
pope, date, or source identity differs.

The [collection](../src/sources/papal-documents/README.md) owns the catalog and
source workflow. The [source library](../src/sources/README.md) owns exact
editions, artifact hashes, rights, and evidence states. Generated two-column
readers use the retained source artifacts; the project does not author a new
translation to fill a language gap.

The [encyclicals browser](../src/web/browser/encyclicals/index.html) distinguishes
historical source PDFs held here from existing English translations on external
sites. **Complete English** selects acts with at least one explicitly complete
English text in either location. **English PDF, any extent** selects local human
translations; **English online, any extent** selects external links; **English
gaps** retains acts for which no complete English text is recorded. A fragment,
damaged text or unreviewed extent does not fill a complete-English gap. Counts
for local and external availability can overlap for the same act.

`src/sources/papal-documents/encyclicals-index.json` owns those links under its
v2 `english_routes` field. Each route records its URL, source label, English
language, extent, official or third-party status, check date, discovery source
and verification note. A checked external route does not establish a right to
retain its wording or generate a local PDF. Local `readers` still require exact
membership in the reviewed source release, independently of external links.

## Find a document

Run these commands from the repository root:

```sh
tools/papal-documents check --json
tools/papal-documents list --type encyclical --pope leo-xiii
tools/papal-documents list --type bull
tools/papal-documents list --language la
```

`make papal-catalog` writes the Vatican JSON, CSV and BibLaTeX exports, plus
separate archive, *Bullarium*, Acta and available historical-series JSON
snapshots, under `.scratch/papal-pdfs/`. `make papal-plan` resolves the admitted
base and correction selections into `PAPAL_OUT/current-manifest.json`, applying
recorded replacements and withdrawals before rendering. `make papal-pdfs`
validates that plan, renders only its current selections under
`PAPAL_OUT/current/`, then collects them under `PAPAL_OUT/collection/`. It does
not rebuild obsolete base or correction batches.

Open `collection/index.html` for the combined PDF and TeX links, source details
and page-review status; `collection/collection.json` retains the machine-readable
inventory. The index links existing outputs, so keep `current/` with
`collection/` when moving this local tree. The render receipt and frozen input
manifest remain under `current/`. `PAPAL_OUT` changes the output root and
`PAPAL_JOBS` bounds compilation concurrency. `make check-papal` runs catalog,
input-hash, rights and focused tool checks. These commands generate local source
editions; installation and deployment have their own review requirements.

`PAPAL_BASE_MANIFESTS` supplies named additive source selections;
`PAPAL_CORRECTION_MANIFESTS` supplies the ordered corrections to apply.
`PAPAL_REVIEW_MANIFESTS` supplies hash-bound page-review evidence to the
collection. Override these only with the exact manifests intended for that
selection. `make papal-collection` refreshes the plan and index from existing
current outputs without starting a render; a changed plan requires matching
rendered bytes and receipt before collection can succeed.

## Retain reviewed PDFs outside the build directory

`typeset-papal prepare-install` checks existing frozen receipt/manifest pairs
against a newly resolved default source plan. It selects only exact current
PDFs with passing source fidelity and hash-bound layout inspection of every
page. Pending, missing, failed and rejected readers remain delivery states;
they do not receive installed PDF links. A layout PASS retains the source's
OCR and historical qualifications.

The pair inventory is a JSON object with schema
`triptych-papal-render-batch-pairs/v1` and a `batches` array. Each entry names
`name`, repository-relative `receipt` and `manifest` paths, and their exact
`receipt_sha256` and `manifest_sha256` digests. Use the immutable
`frozen-manifest.json` retained by that render, or its exact earlier frozen
snapshot. The inventory locates evidence; it cannot override current source
withdrawals or missing review evidence.

```sh
make papal-install-plan PAPAL_INSTALL_BATCH_PAIRS=.scratch/papal-pdfs/batch-pairs.json
# Inspect .scratch/papal-pdfs/prepared-install.json before copying the release.
make papal-install
make check-papal-install
```

`PAPAL_INSTALL_PREPARED` changes the prepared JSON path. Installation consumes
that existing proposal and repeats the checks; it refuses a changed proposal
or source inventory. Preparation and checking resolve the repository's default
source inputs, including newly admitted correction and withdrawal files.
They do not accept a source subset as a release of the whole collection.

Installed readers live in `pdf/papal-documents/` with date, identity and
language in their names. `release/papal-documents.json` binds their exact
bytes and records the remaining delivery states. Frozen source selections,
receipts, review records and full-page reports are retained by content hash
under `release/papal-documents/`, so deleting `.scratch` does not erase the
release's evidence. Standalone TeX and body fragments remain reproducible
build outputs. The release record's `documents[].pdf` paths can supply
appendices or a presentation's source-reader list without introducing an
AI-provider publication.

Checking reconciles the installed set with the current source plan and
verifies its files and retained evidence. New selections are reported as
uninstalled; a withdrawn or changed installed selection fails the check.
Installation removes an obsolete owned path only when its bytes still match
the previous release. Unexpected or unowned files are preserved for review.

`list --language` selects documents with a linked edition in that language.
`show --document ID` prints the full catalog record, including its language
URLs and source indexes. Obtain the stable `ID` from `list`; an incipit alone
does not identify an act.

The check reports the catalog's measured extent, failed index requests,
unresolved dates, filename-derived dates awaiting confirmation, and rows
without a linked text. An index label and a machine-normalized date are
finding aids; the controlling text and its publication witness settle a
claim about an act.

## Bring the catalog into a larger project

The same catalog can supply a spreadsheet, a bibliography, and source cards
for a presentation:

```sh
tools/papal-documents export --format csv --out .scratch/papal-project/catalog.csv
tools/papal-documents export --format biblatex --out .scratch/papal-project/papal.bib
tools/papal-documents export --type encyclical --pope leo-xiii --format beamer --language en --out .scratch/papal-project/source-cards.tex
```

CSV and BibLaTeX contain one record for each linked language edition. A work
whose text link is missing remains a work-only record with an empty language
and URL; the CSV `record_kind` distinguishes it. JSON exports retain every
work, the linked editions, and the complete index-coverage report even when
the selected works are filtered.

Citation keys derive from stable document identity and language. A correction
to a title, date, or delivery URL keeps the key; two documents named *Quanta
cura* and two translations of the same act have distinct keys. The CSV
`citation_key` column matches the generated `.bib` entries and the comments
in the Beamer source. Existing BibLaTeX projects can load the generated file
with `\addbibresource{papal.bib}` and use that key in `\autocite[LOCUS]{KEY}`.
BibLaTeX and its bibliography processor are separate optional dependencies.

Beamer exports contain the document title, responsible issuer, date, kind, and
an official source link. A curial regulation issued on papal mandate retains
its actual issuer and papal context. A compound delivery's card names the
reviewed constituents rather than presenting a misleading original index title
as one verified act. Constituent and index-mislink notes remain visible on
their cards. `--language` is the preferred edition for this export; the card
names the language actually available. These source cards carry metadata
alone and can accompany a presentation even when its source text has no
recorded redistribution basis. Compile a selected deck with XeLaTeX:

```sh
xelatex -interaction=nonstopmode -halt-on-error -output-directory=.scratch/papal-project .scratch/papal-project/source-cards.tex
xelatex -interaction=nonstopmode -halt-on-error -output-directory=.scratch/papal-project .scratch/papal-project/source-cards.tex
```

For an authored talk, retain the useful cards, add the argument in that
project's own sources, and cite the relevant paragraphs. A source link or a
bibliography entry does not mean a passage has been checked.

## Include a source reader as an appendix

`papal-sources plan --json` reports which catalog entries have a candidate
original Latin text for acquisition. `papal-sources acquire` retrieves whole
source responses into its named `.scratch` staging directory. A separate
publication-approval record controls which extracted texts may be retained;
acquisition alone grants no distribution status. Registration connects the
catalog to canonical source-library identities and reuses existing work
records where that identity has been established.

`typeset-papal` generates a separate two-column reader for each admitted
manifest entry, identifying its actual text language. A historical Latin
collection can contain an Italian act or a substantive Italian annex. Such a
constituent retains the source's language and order, with the multilingual
extent identified in its record and reader. Two columns do not imply a
Latin/English parallel translation. The tool also emits a `.body.tex` fragment beside
the standalone `.tex`. Its output receipt gives the exact filenames, source
hash, and compiled PDF identity.

Rendering requires Python 3.11 or later and XeLaTeX, with Latin Modern Roman,
Junicode and FreeSerif available to the font loader. English and Latin readers
use Babel's language-specific hyphenation; Latin requires TeX Live's
`hyphen-latin` patterns and `babel-latin` support. PDF checks use Poppler's `pdfinfo`,
`pdffonts` and `pdftotext`. The generated TeX retains its font declarations;
keep the standalone file and any support files beside its body fragment.

```sh
tools/typeset-papal check --manifest src/sources/papal-documents/typeset-manifest.json --json
tools/typeset-papal render --manifest src/sources/papal-documents/typeset-manifest.json --out .scratch/papal-project/readers --compile --jobs 4 --json
```

Choose a manifest by its source edition:

| Manifest in `src/sources/papal-documents/` | Reader input |
| --- | --- |
| `typeset-manifest.json` | Admitted historical Latin transcriptions from the Vatican collections. |
| `vatican-corrections-manifest.json` | Explicit source or reader corrections to the Vatican selection. |
| `historical-english-manifest.json` | Bounded English entries from the 1903 Benziger collection. |
| `historical-english-supplement-manifest.json` | Independently identified additional historical English editions. |
| `historical-english-supplement-fragment-manifest.json` | Identified abridged or damaged supplemental English witnesses. |
| `historical-english-journal-manifest.json` | Additional complete historical English journal witnesses. |
| `historical-english-journal-fragment-manifest.json` | Identified damaged or abridged journal witnesses. |
| `historical-english-book-manifest.json` | Additional complete historical English book witnesses. |
| `historical-english-book-fragment-manifest.json` | Identified damaged or abridged book witnesses. |
| `historical-english-corrections-manifest.json` | Explicit metadata or layout corrections to earlier English selections. |
| `quanta-syllabus-manifest.json` | Separate *Quanta cura* and *Syllabus* constituents of one composite Latin delivery. |
| `bullarium-manifest.json` | Admitted complete printed-act witnesses from the selected *Bullarium* volumes. |
| `bullarium-fragment-manifest.json` | Explicitly identified historical fragments, each with its missing-content notice. |
| `bullarium-rescue-manifest.json` | Additional complete printed witnesses recovered by a later reviewed reconstruction pass. |
| `bullarium-rescue-fragment-manifest.json` | Additional identified historical fragments from that reviewed pass. |
| `bullarium-corrections-manifest.json` | Replacement selections and explicit supersessions for earlier incomplete notes or corrected reader apparatus. |
| `bullarium-geometry-manifest.json` | Reviewed complete witnesses recovered through exact source-coordinate mappings. |
| `bullarium-geometry-fragment-manifest.json` | Identified historical fragments recovered through those mappings. |
| `acta-manifest.json` | Selected admitted historical *ASS* and *AAS* act witnesses. |
| `acta-title-corrections-manifest.json` | Reviewed display-title replacements with exact prior-PDF supersessions. |
| `acta-layout-corrections-manifest.json` | Layout repairs for initial failed Acta renders. |
| `acta-visual-corrections-manifest.json` | Source-pinned metadata or layout replacements arising from page review. |
| `historical-series-corrections-manifest.json` | Cumulative source-boundary and reader corrections for the continuation and pontificate-specific series. |

A manifest can be empty while identification or boundary review is unfinished.
Its count describes selected source editions, not the number of all papal acts.
Different historical witnesses of the same act remain distinct source editions.
Additional historical series use their own complete and fragment manifests;
the [collection's ownership table](../src/sources/papal-documents/README.md)
names each configuration, catalog, render manifest and visual audit exactly.
Some named files belong to later workflow phases. Their presence and coverage
records, rather than their reserved names, establish which work has finished.

The render manifests use `triptych-papal-typeset/v1`, with an explicit
`revision` and `documents` array. A document row may pin its own `revision`;
otherwise the top-level revision controls that row. The source plan preserves
this effective revision in every selected row, and the render receipt records
it as `documents[].render_revision`. Adding an unrelated selection therefore
need not alter the revision printed in an unchanged reader.

The plan's `selection_plan` retains the component manifest paths and hashes,
original row positions and hashes, and the reasons and source pins for excluded
predecessors. Same-source metadata or layout corrections remain distinct from
changes of source identity or extent, which require explicit supersessions.
The initial *Bullarium* complete and fragment snapshots
remain frozen; rescue snapshots add reviewed witnesses, and correction
snapshots replace specific earlier selections without rewriting their source
bytes or identities. The active plan applies recorded supersessions and excludes
the named predecessors. Concatenating every historical batch would retain
withdrawn selections alongside their replacements.

Already frozen multi-batch outputs can still be indexed with
`typeset-papal collect`: repeat `--batch NAME RECEIPT FROZEN_MANIFEST` for the
exact existing batches, `--supersessions PATH` for applicable corrections and
`--review PATH` for page-review audits. This reads and checks existing files;
it neither renders nor installs PDFs. Use `collect --help` for the full syntax.
A complete `PASS` review can follow the exact same PDF bytes into a new batch
receipt when document identity, language, PDF hash, page count and retained
full-page review evidence agree. The collection records both original and
current receipt hashes. A filename, matching source text or successful build
alone cannot transfer review; changed pages need inspection or a declared
exact-raster reuse proof.

A paper can input the generated body fragment in an appendix. Use XeLaTeX,
load `hyperref`, and retain the Unicode font declarations from the paired
standalone source, including its literal-punctuation font setting
`Ligatures=TeXOff`. Greek, combining marks and occasional Cyrillic source
characters need the same font coverage; the fragment alone does not install
those fonts. Give the source its title, responsible issuer, date, language, and reuse notice
from the manifest, and retain the artifact identified in the receipt. The
fragment records its artifact and hash in TeX comments; the consuming paper
supplies the visible attribution. Select the column layout in the consuming
document; the fragment supplies text without changing that layout. To attach
a reviewed reader unchanged,
load `pdfpages` in a paper and use
`\includepdf[pages=-]{PATH-TO-REVIEWED-READER.pdf}`. A slide presentation can
link that PDF as its handout while its slides use the catalog's citations.
Review the composed result before installing it as a publication.

## Connect a claim to the source library

The typeset manifest identifies its controlling `artifact_id`. Use that
identity for a publication-local `research/source-bindings.toml`; a catalog
ID or a generated PDF filename is a navigation address rather than an exact
textual witness. Source-library commands provide the review pin and the
existing consumers:

```sh
tools/source-library fingerprint SOURCE_ID
tools/source-library uses SOURCE_ID
tools/source-library impact SOURCE_ID
tools/source-reader show --edition EDITION_ID
```

Replace `SOURCE_ID` and `EDITION_ID` with the registered identities. Record
the exact loci, the role the passage has in the argument, the evidence state
actually reached, and the computed fingerprint. The binding contract and
its checked examples are in [the source schema](../src/sources/schema/README.md).
`source-reader` applies its artifact's distribution rights when projecting
text. Its presence in the catalog never overrides those rights. The browser's
source projection reports registered holdings; a segment used for a local PDF
need not yet have an independently readable passage in the browser.

## Reconstruct acts from historical volumes

The archive inventory identifies containers and download routes. Two separate
document inventories identify constituents within them:

```sh
tools/bullarium status --json
tools/bullarium check --json
tools/papal-acta list --series ASS --summary --json
tools/papal-acta list --series AAS --summary --json
tools/papal-acta check --json
```

`bullarium-catalog.json` records printed units, exact source-line ranges,
review dispositions and unresolved extraction problems. `acta-catalog.json`
records journal-volume witnesses, identified acts, source extents and gaps.
These inventories are separate from the Vatican web-index catalog. Their
counts must be read with their own declared scope and revision.

The *Bullarium* continuation, Benedict XIV's *Bullarium*, Gregory XVI's Acta
and Pius IX's Acta have separate series configurations and catalogs. Each
configuration identifies the actual volume deliveries; the corresponding
catalog reports candidate units, reviewed extents and coverage. A volume
acquisition, a reviewed constituent and a rendered reader are different
results. Shared visual audits bind page findings to a frozen render receipt;
their document rows do not certify every act in a series.
Series volumes can also contain civil instruments or acts by other issuers.
The constituent review identifies the actual issuer before admitting a unit
as a papal act; a pontiff's name on the collection is insufficient.

`bullarium acquire` preserves complete offered OCR and page-map inputs;
`reconstruct` proposes boundaries, and `admit` consumes an explicit reviewed
boundary recipe. `papal-acta acquire` obtains whole listed journal deliveries;
`index` merges reviewed recipes, `register` creates historical artifacts and
constituent segments, and `manifest` selects one admitted witness per work and
language. Reconstruction and registration require their documented inputs
and an explicit revision; inspect each verb's `--help` before refreshing a
snapshot. A heading detector's candidate is not automatically an admitted act.

The retained text belongs to its historical collection or journal. An act's
segment points to exact bounded lines of that container without duplicating
its bytes under the act. Reusing an existing act identity requires an identified
match; a shared incipit alone does not establish it. Composite web deliveries,
such as *Quanta cura* with the *Syllabus*, likewise retain one truthful
container and separate constituent bounds.

A complete printed witness preserves the substantive act, its ending and its
own historical notes, as printed in that edition. Conventional chancery
abbreviations can remain literal with a notice. An explicit omission of a
proem, substantive clauses, annex or subscriptions receives a specific
missing-content finding. An identified historical fragment is listed and
rendered as a fragment; an inseparable mixture of columns or neighboring acts
remains unresolved. A clean OCR subrange of an otherwise complete printing
does not become a historical fragment merely because extraction is difficult.
An unparsed act date remains unknown in metadata and is omitted from the
reader's date line; this does not imply that the source lacks a date.

For bounded original-page evidence, `papal-sources witness` works from a whole
cached PDF already registered under its truthful source edition:

```sh
tools/papal-sources witness --recipe .scratch/papal-project/page-recipe.json --cached-pdf .scratch/papal-project/whole-source.pdf --scratch .scratch/papal-project/page-evidence --json
```

The recipe pins the registered parent identity, complete SHA-256 and byte size,
same edition, increasing one-based pages, explicit rights basis and retained
extent. The command checks these before staging native pages. Its
`native-bilevel-images` backend additionally requires exact image selectors,
dimensions, resolution and pixel hashes. It fetches nothing and infers no
rights clearance. Inspect the staged receipt and output; repeating with
`--register` adds three immutable artifacts for the selected PDF, recipe and
receipt. It creates no passage records or `verified` evidence promotion. See
`witness --help` for the exact required recipe fields.

### Reading-order derivatives for fused marginal summaries

When the archive.org text stream fuses a volume's marginal summaries into body
lines, rebuild the whole volume from its native DjVu WORD coordinates instead
of repairing readers one by one. The input map locates the cached whole XML
(`triptych-bullarium-geometry-input-map/v1`). Proposal, replay and mapping
write only below `.scratch/` or `build/`:

```sh
tools/bullarium geometry propose --volume 4 --input-map .scratch/reading-order/input-map-volume-04.json --out .scratch/reading-order/v04
tools/bullarium geometry --recipe .scratch/reading-order/v04/recipe.json --input-map .scratch/reading-order/input-map-volume-04.json --out .scratch/reading-order/v04/replay
tools/bullarium geometry --recipe .scratch/reading-order/v04/recipe.json --input-map .scratch/reading-order/input-map-volume-04.json --out .scratch/reading-order/v04/replay --check
tools/bullarium geometry map-units --recipe .scratch/reading-order/v04/recipe.json --replay .scratch/reading-order/v04/replay --out .scratch/reading-order/v04/unit-mapping.json
```

`propose` writes an explicit v2 recipe, `running-heads.tsv`, which lists
every page's running-head row for a quick scan, and `note-suspects.tsv`. That
second file lists small-type rows below a rule's space at a column foot that
open on a short token but were not split as notes. The recipe records each page
as reordered, held (with its reason) or empty, and each reordered page's rows
of native WORD ordinals. Rows carry a role: running head, body column,
marginal summary (a TAB-led block at the section it annotates), page-foot note
(a separate block at the page break), gutter OCR or footer. A note starts at
a reference mark in small type, or at a mark or small type corroborated by
editorial wording ("(R. T.)", "Ex Regest.", "Cherub.", "Mainardus" and similar).
OCR-garbled marks such as `i`, `t`, `{`, `I)` or `1.` count only with that
support. It also records page measurements and any inseparable mixed
WORDs. Its thresholds are fractions of the measured column
width and line pitch. The replay expands the rows into the explicit v1 recipe
and proves that every WORD appears exactly once, unchanged. `map-units` places
every catalog unit in the derivative through WORD identity and assigns one
category: `clean`, `review:margin-ownership-at-boundary`,
`hold:inseparable-WORD`, `hold:body-not-contiguous`,
`review:possible-unsplit-note` (the unit contains a listed note suspect) or
another hold. Only
`clean` units can be registered. A unit's own page-foot notes printed after
the next unit begins form an extra range of its selection. Name the units
explicitly in a selection file,
`{"schema": "triptych-bullarium-reading-order-selection/v1", "units": [...]}`:

```sh
tools/bullarium geometry register --recipe .scratch/reading-order/v04/recipe.json --replay .scratch/reading-order/v04/replay --mapping .scratch/reading-order/v04/unit-mapping.json --units .scratch/reading-order/v04/selection.json --revision 2026-10-28T00:00:00Z --input-map .scratch/reading-order/input-map-volume-04.json
```

`register` writes four artifacts under the volume edition: the derivative,
the gzip recipe, the page map and the replay receipt. It declares them in the
volume container and then admits each selected unit through `bullarium admit`
as `<unit>.reading-order`, a new reading selection of the same work, into
`bullarium-geometry-manifest.json`. Every write is append-only. Raw artifacts,
prior segments and the withdrawal inventory are not touched.

To replace defective reading selections, register a corrected derivative with
`--supersede --reason "..."`. Each unit's newest reading selection is
superseded by `<unit>.reading-order-vN`, a new edition and segment of the same
work on the new derivative. Its document row and the supersession row go to
`bullarium-reading-order-corrections-manifest.json`, which the source plan
reads as a correction manifest. Earlier derivatives, selections and documents
are kept unchanged.

Admission is not installation: a volume must first pass its native-image evidence gate, and
every page of every repaired PDF is reviewed before install.

## Coverage

The discovery boundary is the Vatican's curated papal HTML collections from
Benedict XIV onward, using the English, Italian and Latin interfaces and every
language linked from each row. Ordinary correspondence is a separately
selected expansion, requested by `discover --include-letters`. Addresses
found in mixed historical lists keep their recorded kind.

The [Official Acts gateway](https://www.vatican.va/archive/atti-ufficiali-santa-sede/index_en.htm)
also provides *Acta Sanctae Sedis* and *Acta Apostolicae Sedis*. The historical
reconstruction covers the selected 25 *Bullarium* deliveries, the 41 *ASS*
volumes and the identified *AAS* archive series. Later *AAS* bodies remain
metadata-only where redistribution has no affirmative basis. The individual
inventories report which boundaries have been resolved and which remain open.
Downloading a volume does not establish that its constituent acts have been
cataloged or transcribed.

The catalog's gaps remain visible. Completing a curated index, acquiring a
source, generating a PDF, and checking its wording are separate results.
The rights record for an exact edition also remains separate from the age
of the underlying act. In particular, the
[Vatican terms](https://www.vatican.va/content/vatican/en/legal-notes.html)
distinguish personal access from redistribution; modern translations need
their own recorded distribution basis. Project licenses cover the project's
own contributions as described in [Third-Party Material](../THIRD_PARTY.md).

The retained 1903 English collection supplies 31 bounded source entries,
including two letters within one chapter and an explicitly abridged Philippine
excerpt. A separately retained derivative repairs 205 source-corroborated
character-encoding spans in 11 selections, with a replayable audit and the
original transcription preserved. Inherited OCR word errors and documented
heading-date discrepancies remain. These local PDFs are source transcriptions;
machine text comparison and visual layout review do not establish fidelity to
every printed word. Source-library search and presentation imports must retain
these edition-specific limits.

Additional English acquisition has its own supplement manifest. It identifies
historical human translations by their actual printing, including nineteenth-
century act collections and early twentieth-century collections or issues.
Modern reprints, later advertisements and an undated catalog entry do not
establish the age of the retained wording. Abridged chapters remain explicitly
bounded or unresolved, and literal OCR remains distinct from separately
recorded mechanical repairs. The supplement's source and review records state
the phase reached for each edition; it inherits no whole-text collation claim
from the 1903 collection.

The [English expansion record](../src/sources/papal-documents/english-expansion-coverage.md)
identifies the separate book and journal printings, complete and damaged
constituents, and bounded exclusions. Its source admissions, render receipts
and page reviews remain separate results.
