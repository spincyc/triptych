# Papal document collection

This collection identifies papal acts by pope, date, kind, and source edition.
The catalog is a discovery index. Canonical works, editions, artifacts, and
passages belong to the [source library](../README.md), under the
[reusable-source contract](../../../guidance/sources.md).

| Record | Purpose |
| --- | --- |
| `catalog.json` | Discovered acts, linked languages, stable IDs, source indexes, index hashes, and declared coverage gaps. |
| `archives.json` | Bullarium, ASS and AAS container identities and the download routes actually listed by their catalogs. |
| `overrides.json` | Reviewed aliases, source-boundary observations and date resolutions, with their evidence. |
| `source-links.json` | Catalog identities mapped to canonical source works, editions and artifacts; composite and constituent rows remain explicit. |
| `publication-approvals.json` | Exact original-language or historical-translation text hashes and historical publication evidence admitting retained Latin text. |
| `typeset-manifest.json` | Exact admitted source artifacts and their rights basis for the two-column reader. |
| `encyclicals-source-corrections-manifest.json` | Nine independently page-reviewed source repairs; immutable parent witnesses, replay recipes and exact prior-reader supersessions remain retained. |
| `encyclicals-classic-manifest.json` | 221 independently page-reviewed classic selections; together with nine source repairs, 230 of the original 327 versions have installed classic readers. Exact prior-reader supersessions remain retained. |
| `encyclicals-classic-renderer-review.md` | Independent renderer regression and adversarial fidelity findings; every replacement PDF retains its own every-page review. |
| `vatican-corrections-manifest.json` | Explicit replacement source or reader selections and recorded supersessions of earlier Vatican outputs. |
| `historical-english-manifest.json` | Thirty-one bounded source entries from the 1903 Benziger collection, including an explicitly abridged excerpt. |
| `historical-english-supplement-manifest.json` | Additional identified historical English editions, with their own source, rights and transcription limits. |
| `historical-english-supplement-fragment-manifest.json` | Separately identified abridged historical English witnesses and their missing-content notices. |
| `historical-english-journal-manifest.json` | Additional individually reviewed English journal witnesses, preserving each row's rendering revision. |
| `historical-english-journal-fragment-manifest.json` | Separately identified damaged or abridged English journal witnesses. |
| `historical-english-book-manifest.json` | Additional complete historical book witnesses, retaining each rendering revision. |
| `historical-english-completion-manifest.json` | Twenty-three independently source-admitted and page-reviewed historical human English additions, including the six earlier witnesses. Damaged Coyne Ubi remains excluded; imprint, OCR and source-order qualifications remain explicit. |
| `historical-english-source-intake-02.json`, `historical-english-source-intake-03.json` | Independent bounded source-admission judgments for the six additions; separate from PDF-layout acceptance and source-library verification states. |
| `historical-english-source-intake-02-scope.json`, `historical-english-source-intake-03-scope.json` | Exact three-act scope inputs identifying source rows and evidence pins for those two source-admission judgments. |
| `historical-english-source-intake-01.json`, `historical-english-source-intake-04.json` through `-08.json`, and their `-scope.json` inputs | Exact additional source-admission report/scope envelopes for the seventeen added witnesses; metadata ownership creates no verified passage or PDF-layout authority. |
| `historical-english-source-intake-supplement.json` | Exact selected source rows, qualified-imprint/native-order successors, and publication-derivative provenance. Current report consumers pin the normalized publication hashes; original raw evidence hashes remain explicitly historical. |
| `historical-english-book-fragment-manifest.json` | Separately identified damaged or abridged historical book witnesses. |
| `historical-english-corrections-manifest.json` | Source-identical English metadata/layout repairs, with exact supersessions when a prior PDF exists. |
| `quanta-syllabus-manifest.json` | Separately bounded *Quanta cura* and *Syllabus* constituents of one composite delivery. |
| `bullarium-catalog.json` | Individual printed units in the selected historical volumes, exact extents, review dispositions and unresolved extraction problems. |
| `bullarium-manifest.json` | Admitted complete printed-act witnesses from the selected *Bullarium* deliveries. |
| `bullarium-fragment-manifest.json` | Identified historical fragments with explicit missing-content findings, separate from complete witnesses. |
| `bullarium-rescue-manifest.json` | Additional complete printed witnesses from a later reviewed reconstruction pass. |
| `bullarium-rescue-fragment-manifest.json` | Additional identified historical fragments from that pass. |
| `bullarium-corrections-manifest.json` | Replacement selections with explicit supersessions of earlier selections, including missing source notes and corrected reader apparatus. |
| `acta-catalog.json` | Individual *ASS* and *AAS* witnesses, journal containers, act boundaries and stated coverage gaps. |
| `acta-manifest.json` | Selected admitted historical journal witnesses, one per work and language. |
| `acta-title-corrections.json` | Source-pinned display-title review ledger, preserving original metadata and exact evidence. |
| `acta-title-corrections-manifest.json` | Explicit replacement reader selections and exact prior-PDF supersessions. |
| `acta-layout-corrections-manifest.json` | Separately identified layout repairs for initial failed renders. |
| `acta-visual-corrections-manifest.json` | Cumulative source-pinned metadata/layout repairs arising from page review, with exact supersessions. |
| `historical-series-corrections-manifest.json` | Cumulative source-boundary and reader repairs for the continuation and pontificate-specific historical series, with exact supersessions. |
| `bullarium-geometry-manifest.json` | Individually reviewed complete witnesses recovered through exact source-coordinate mappings. |
| `bullarium-geometry-fragment-manifest.json` | Identified historical fragments recovered through the same checked mappings. |
| `bullarium-active-withdrawals.json` | Empty reader selection with exact active-source withdrawals, affected units and confirmed source-order holds. |
| `bullarium-continuatio-config.json` | Identified *Bullarium* continuation volumes and their acquisition configuration. |
| `bullarium-continuatio-catalog.json` | Reconstructed continuation witnesses, source extents, review dispositions and coverage gaps. |
| `bullarium-continuatio-manifest.json` | Admitted complete printed witnesses from the continuation. |
| `bullarium-continuatio-fragment-manifest.json` | Identified historical fragments from the continuation. |
| `benedict-xiv-bullarium-config.json` | Identified Benedict XIV *Bullarium* volumes and their acquisition configuration. |
| `benedict-xiv-bullarium-catalog.json` | Reconstructed Benedict XIV collection witnesses and stated coverage. |
| `benedict-xiv-bullarium-manifest.json` | Admitted complete printed witnesses from that collection. |
| `benedict-xiv-bullarium-fragment-manifest.json` | Identified historical fragments from that collection. |
| `gregory-xvi-acta-config.json` | Identified Gregory XVI Acta volumes and their acquisition configuration. |
| `gregory-xvi-acta-catalog.json` | Reconstructed Gregory XVI collection witnesses and stated coverage. |
| `gregory-xvi-acta-manifest.json` | Admitted complete printed witnesses from that collection. |
| `gregory-xvi-acta-fragment-manifest.json` | Identified historical fragments from that collection. |
| `pius-ix-acta-config.json` | Identified Pius IX Acta volumes and their acquisition configuration. |
| `pius-ix-acta-catalog.json` | Reconstructed Pius IX collection witnesses and stated coverage. |
| `pius-ix-acta-manifest.json` | Admitted complete printed witnesses from that collection. |
| `pius-ix-acta-fragment-manifest.json` | Identified historical fragments from that collection. |
| `vatican-visual-review.json` | Hash-bound page-review dispositions for a frozen Vatican reader receipt. |
| `bullarium-visual-review.json` | Hash-bound page-review dispositions for a frozen *Bullarium* reader receipt. |
| `english-visual-review.json` | Hash-bound page-review dispositions for a frozen English reader receipt. |
| `acta-visual-review.json` | Hash-bound page-review dispositions for a frozen Acta reader receipt. |
| `historical-series-visual-review.json` | Hash-bound page-review dispositions across the separately identified historical series. |
| `english-encoding-raster-comparison.json` | Exact page-raster equality and changed-page evidence connecting the original and encoding-repaired English PDFs. |

The catalog follows the Vatican's curated HTML collections from Benedict XIV
onward. Modern discovery follows encyclicals, bulls, briefs, apostolic
constitutions, exhortations, apostolic letters, and motu proprio. The earlier
mixed lists also contain letters and addresses. Ordinary modern
correspondence can be added explicitly. Completeness of these indexes is a
bounded result. The separate *Bullarium* and Acta inventories reconstruct
individual constituents from their identified historical containers; their
unresolved entries remain visible. Later journal bodies without an affirmative
distribution basis are represented by metadata.

```sh
tools/papal-documents check --json
tools/papal-documents list --type encyclical
tools/papal-documents show --document ID --json
tools/papal-documents export --format biblatex --out .scratch/papal-documents/papal.bib
tools/bullarium status --json
tools/papal-acta list --series ASS --summary --json
```

`ID` is a catalog identity printed by `list`. Text is acquired as a complete
byte stream, hashed, and mechanically extracted; this process does not confer
passage verification. Exact HTML and normalized text are distinct artifacts.
Only text with an affirmative recorded distribution basis enters a retained
source artifact or reader. A modern translation's rights are considered
separately from the act it translates.

These are project-created inventories, not additional source-manifest record
types. Their exact named JSON envelopes and immediate Markdown records are
recognized by the source-tree validator; external source wording belongs only
in manifested artifacts. The catalog, acquisition and typesetting tools own
their semantic checks. Unlisted JSON, nested files and loose payloads are
rejected.

The table names the exact permitted inventory files, including later workflow
phases; a filename here does not assert that its snapshot has been created or
reviewed. Each series configuration uses `triptych-papal-series-config/v1`
with `series_id`, `title`, `revision` and `volumes`. Its catalog uses
`triptych-papal-series-catalog/v1` with `series_id`, `revision`, `volumes`,
`documents` and `coverage`. Complete and fragment render manifests retain the
shared typesetting schema below. Acquisition, candidate reconstruction,
boundary admission, compilation and page review remain separate measured
phases; their artifacts and declared coverage establish the state reached.

The shared visual audits use `triptych-papal-visual-review/v1`, with
`frozen_receipt_sha256` and `documents`. They identify reviewed bytes and page
dispositions rather than a whole-series completion status. The English
encoding comparison uses `triptych-english-page-raster-comparison/v1`, with
`source_receipt_sha256`, `documents`, `total_documents` and `total_pages`.
Exact raster equality can carry an existing visual finding to unchanged pages;
changed pages require their own inspection. Neither proves transcription
accuracy against historical print.

The render manifests use `triptych-papal-typeset/v1`, with `revision` and
`documents`. A row's explicit `revision` overrides the top-level fallback;
the generated receipt records its effective `render_revision`. Correction
manifests record exact `supersessions` when source selections or existing PDFs
are replaced; source-identical metadata or layout repairs preserve their exact
source pins. The Acta title ledger separately uses
`triptych-papal-acta-title-corrections/v1`, with `revision`, `base_manifest` and
`rows`.
Initial *Bullarium* complete and fragment snapshots remain frozen. Later rescue
and correction snapshots preserve prior source bytes and identities. A final
selection must apply the recorded supersessions and exclude superseded PDFs,
including earlier selections missing their own historical notes. Concatenating
all batches does not produce a valid current selection. Each receipt and
hash-specific review remains evidence for the bytes it actually identifies.

`make papal-plan` writes `PAPAL_OUT/current-manifest.json` from
`PAPAL_BASE_MANIFESTS` and ordered `PAPAL_CORRECTION_MANIFESTS`, preserving input
manifest and row hashes and explicit exclusion history. `make papal-pdfs`
renders only that active selection under `PAPAL_OUT/current/`, then writes
the combined index under `PAPAL_OUT/collection/`; obsolete source batches are
not rebuilt. `PAPAL_REVIEW_MANIFESTS` supplies exact page-review evidence.
`make papal-collection` reads existing current outputs without compiling.
Explicit multi-batch `typeset-papal collect` remains available for already
frozen receipts and their exact source manifests, supersessions and reviews.
A complete passing review may transfer to a new receipt only for the exact
same PDF bytes and fully pinned page evidence; the collection retains the
original receipt identity. It does not infer review from a filename or source
match.

The historical English files remain uncollated transcriptions with substantial
inherited OCR word errors and heading-date discrepancies. A separate derivative
repairs 205 source-corroborated encoding spans in 11 selections; the exact
originals, audit and replay recipe remain available. The other 20 selections
keep their prior controllers. A successful source-to-PDF comparison proves
faithful typesetting of its controlling transcription, not correctness against
every word of the 1903 printed pages. The Philippine entry omits legal clauses
in the historical translation itself. Consult its source notice and the
item-specific review before quoting. Exact Wikisource responses and the repair
audit retain their own CC BY-SA 4.0 notices; the historical English wording has
its separately recorded United States public-domain basis.

The [English expansion record](english-expansion-coverage.md) owns the
supplemental book and journal source identities, boundary findings and stated
gaps. Complete, abridged and damaged witnesses remain separate selections.
Each manifest retains its own render revision and source-quality limits;
source admission alone supplies no PDF or page-review completion claim.

Historical admission identifies complete printed witnesses, not expanded
autographs. Literal conventional abbreviations retain their source form and
notice. Substantive historical omissions identify fragments; unresolved mixed
columns or neighboring-act boundaries prevent admission. Each selected segment
points to the exact artifact owned by its truthful collection or journal.
Generating a PDF neither changes that ownership nor verifies its OCR wording.

The constituent's actual language controls its record and reader. A Latin
collection can contain an Italian act, an Italian annex or another historical
language mixture. Preserve that extent and source order explicitly rather than
relabeling every constituent Latin or omitting substantive material to fit a
single-language assumption. Separate supplemental English printings retain
their own translator/edition identity, publication basis, abridgment findings
and OCR limitations.
Collected civil or curial instruments retain their actual issuer and relation
to papal authority; a collection's title does not establish papal authorship of
every constituent.

The Vatican's archive files ending in `-ocr.pdf` may reconstruct text rather
than reproduce original page images. Checks against those files establish
bounded archival OCR evidence; they are not facsimile image collation.

[Using the collection in papers and presentations](../../../docs/papal-documents.md)
explains CSV, BibLaTeX, Beamer source cards, source-body includes, PDF
appendices, and publication-local source bindings. Those exports reuse source
identity; the consuming publication owns its own interpretation and the
evidence for its claims. Beamer cards identify reviewed compound constituents
and visibly label constituent or mislinked index records, preserving the
distinction between the source body and its original discovery label.

The shared historical native-spacing helper with SHA-256
`8163acf4cc10c54c974690bc8f87f21f302b52ccde2d2124eacaa5e83d9249ea`
is retained in the source library as a hash-verified recovery from the archived
`b67` implementation. No original file copy was located. Its artifact record
states the recovery and preserves the MIT grant from `scripts/`; existing
recipe and cold-review pins remain unchanged. This restores replay support
for already retained evidence and makes no new reader-admission claim.
