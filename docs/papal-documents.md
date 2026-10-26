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

## Find a document

Run these commands from the repository root:

```sh
tools/papal-documents check --json
tools/papal-documents list --type encyclical --pope leo-xiii
tools/papal-documents list --type bull
tools/papal-documents list --language la
```

`make papal-catalog` writes the Vatican JSON, CSV and BibLaTeX exports, plus
separate archive, *Bullarium* and Acta JSON snapshots, under
`.scratch/papal-pdfs/`. `make papal-pdfs` compiles the admitted reader manifests.
Each batch has an `index.html` with PDF and TeX links and a receipt identifying
the exact inputs and successful outputs. `PAPAL_OUT` changes the output root
and `PAPAL_JOBS` bounds compilation concurrency. `make check-papal` runs catalog,
input-hash, rights and focused tool checks. These commands generate local source
editions; installation and deployment have their own review requirements.

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
hash, and compiled PDF identity:

```sh
tools/typeset-papal check --manifest src/sources/papal-documents/typeset-manifest.json --json
tools/typeset-papal render --manifest src/sources/papal-documents/typeset-manifest.json --out .scratch/papal-project/readers --compile --jobs 4 --json
```

Choose a manifest by its source edition:

| Manifest in `src/sources/papal-documents/` | Reader input |
| --- | --- |
| `typeset-manifest.json` | Admitted historical Latin transcriptions from the Vatican collections. |
| `historical-english-manifest.json` | Bounded English entries from the 1903 Benziger collection. |
| `historical-english-supplement-manifest.json` | Independently identified additional historical English editions. |
| `quanta-syllabus-manifest.json` | Separate *Quanta cura* and *Syllabus* constituents of one composite Latin delivery. |
| `bullarium-manifest.json` | Admitted complete printed-act witnesses from the selected *Bullarium* volumes. |
| `bullarium-fragment-manifest.json` | Explicitly identified historical fragments, each with its missing-content notice. |
| `bullarium-rescue-manifest.json` | Additional complete printed witnesses recovered by a later reviewed reconstruction pass. |
| `bullarium-rescue-fragment-manifest.json` | Additional identified historical fragments from that reviewed pass. |
| `bullarium-corrections-manifest.json` | Replacement selections and explicit supersessions for earlier incomplete notes or corrected reader apparatus. |
| `acta-manifest.json` | Selected admitted historical *ASS* and *AAS* act witnesses. |

A manifest can be empty while identification or boundary review is unfinished.
Its count describes selected source editions, not the number of all papal acts.
Different historical witnesses of the same act remain distinct source editions.
Additional historical series use their own complete and fragment manifests;
the [collection's ownership table](../src/sources/papal-documents/README.md)
names each configuration, catalog, render manifest and visual audit exactly.
Some named files belong to later workflow phases. Their presence and coverage
records, rather than their reserved names, establish which work has finished.

The render manifests use `triptych-papal-typeset/v1`, with an explicit
`revision` and `documents` array. The correction manifest also carries a
`supersessions` array. The initial *Bullarium* complete and fragment snapshots
remain frozen; rescue snapshots add reviewed witnesses, and correction
snapshots replace specific earlier selections without rewriting their source
bytes or identities. For a final handout or publication, apply the recorded
supersessions and exclude the named old PDFs. Concatenating every batch would
retain withdrawn selections alongside their replacements. Separate batch
receipts preserve the review history; they do not by themselves choose the
current combined set.

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
