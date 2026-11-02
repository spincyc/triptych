# Papal document source editions

This profile governs the provider-neutral catalog and mechanical reading
editions of papal acts. Apply the universal editorial standard, repository
contract, and reusable source contract first. The factual rights position is
owned by
[`papal-documents-rights-v1.toml`](../src/sources/inventories/papal-documents-rights-v1.toml).

## Identity and scope

The catalog identifies papal encyclicals, bulls, briefs, apostolic
constitutions, apostolic exhortations, apostolic letters, and letters issued
*motu proprio*. Retain the source's genre, pope, act date, incipit, language,
and edition. A bull describes an instrument's form and need not be a mutually
exclusive subject classification. Do not infer doctrinal or juridical weight
from the catalog's type field.

The acquisition boundary is explicit: the named formal-document indexes of
the Vatican's pontiff collections, beginning with Benedict XIV, together with
identified earlier witnesses. Addresses, audiences, homilies, messages, and
curial acts have separate scopes when acquired. An index is a discovery
boundary; it is not proof that every act of a pontificate survives there.
Record failed indexes, missing languages, unavailable bodies, and archival
volumes awaiting segmentation as gaps. Neither a successful crawl nor the
Bullarium's possession warrants the label “all historical papal documents.”

Use work/edition/artifact identities from the source library. One work may
have several language editions and delivery artifacts; language links are
not separate works. Recurrent incipits require the pope and date for
disambiguation. A modern web delivery is not the original publication date.

A web-index row can identify a composite delivery, a constituent, a related
curial regulation, or a mislinked body. Preserve the index's assertion and
record the reviewed source identity separately. A curial instrument issued on
papal mandate names its actual responsible issuer; papal context does not
turn it into an independently authored papal act. Joining an archival witness
to an existing work requires positive identity evidence beyond a shared title.

A formal audience rescript may record a papal administrative grant in the
third person. Preserve its actual recorded-grant genre, audience/grant formula
and recording official or office, with the papal context distinguished from
personal authorship. First-person wording is not an admission requirement.
A curial report merely mentioning papal approval still needs a distinct source
identity. The Holy See's [1992 rescript](https://www.vatican.va/roman_curia/secretariat_state/archivio/documents/rc_seg-st_19921126_rescriptum-battesimo_lt.html)
illustrates the distinction; each historical record needs its own evidence.

## Acquisition and rights

Retrieve complete source responses mechanically; source wording never passes
through a model. Hash the complete parent response before transformation.
Register a retained plain-text derivative separately from its exact parent,
declaring the removed wrapper and the normalized characters or whitespace.
Mark extraction completeness independently of the completeness of discovery.

Identify an archival OCR PDF as such. The Vatican's `-ocr.pdf` files can be
text reconstructions rather than facsimile scans, so inspecting their rendered
pages does not by itself establish the glyphs or pagination of the original
printing. Record separate facsimile evidence when an image-level claim needs it.

Apply the rights record per artifact and edition. The original Latin of a
historically published act can qualify on its identified historical
publication basis. An act date on or before 1930 is only a candidate filter:
it does not establish the publication date or provenance of the retained
wording. An identified human translation printed by 1930 can qualify on its
own expired-term basis; identify its translator or historical edition and
publication facts independently of the act. Record a shared basis once at
the controlling edition or container and reference it from its constituent
artifacts without duplicating or weakening the evidence. Later translations,
introductions, editorial notes, creative revisions, images, and website markup
require their own basis. Preserve
historical internal notes only when their membership in the historical
edition is established. Record an unresolved note as a review item instead of
assuming it belongs to the historical edition.

An annual journal's nominal year does not settle every fascicle's publication
date. When a volume straddles the rights cutoff, admit only bounded units with
their own documented historical publication basis. Preserve contrary release
evidence and withdrawn selections. A dated signature alone does not clear a
later publication, and a later binding or index does not automatically date
earlier independently published issues.

Keep protected or unresolved bodies out of tracked inputs and public
outputs. Their catalog entries retain factual identity, source links,
language availability, and the specific reason no local text is offered.
Do not substitute an AI translation. Acquisition, rights clearance, textual
checking, source admission, print inspection, and deployment remain separate facts.

## Historical constituent reconstruction

Keep archive/container discovery, candidate segmentation, reviewed admission
and render selection distinct. A complete volume is not one papal act. The
container owns its acquired OCR or facsimile; constituent segments own exact
bounds within that artifact. Preserve source-order and column-order evidence,
including discontiguous historical notes. A machine heading or date detector
proposes candidates and never establishes completeness by itself. An unparsed
date can remain unknown without excluding an otherwise identified witness.

An admitted complete printed witness retains its substantive text, closing,
subscriptions and its own historical notes as that edition prints them.
Separately identified editorial titles, date captions or other non-substantive
publishing furniture may be excluded with exact source bounds and an explicit
extent qualification. Such a reader represents the complete papal body, not
every item of printed apparatus. This exception does not permit dropping an
address, protocol, actual dating clause, subscription or substantive note, or
accepting interleaved body words merely because their ownership is known.
Conventional chancery abbreviations may remain literal when disclosed; do not
expand them from memory or promise an unfolded autograph. An explicit omission
of a proem, substantive body, annex or subscriptions receives its own finding.
An identified historical fragment uses a separate manifest and visible fragment
title with its missing-content notice. Inseparable neighboring acts or mixed
column order remain unresolved. Do not designate an arbitrary clean OCR
subrange of a complete printing as a historical fragment to bypass an
extraction failure.

A protocol or incipit followed by a reference to an omitted body is a catalog
lead, not a substantive fragment reader. Retain its source and relation as
metadata without creating a PDF that implies recovered act wording.

Record a correction in a separately identified derivative with exact input
hashes, retained source evidence, affected loci and a replayable transformation.
Character-encoding repair does not establish word-level collation. Preserve
the prior artifact and reviewed consumer pins; superseding an incomplete
selection requires an explicit disposition before its reader can be exposed.

Reusable replay helpers are tracked software: pin their repository path and
exact SHA-256 in transformation evidence and reuse that implementation. Do not
copy a current helper into every source container solely to create an artifact
ID. When a retained recipe needs older implementation bytes, retain them or
identify an immutable repository revision and an exact replay command. Record
the implementation's actual license separately from historical source wording;
an archive copied from `scripts/` preserves its MIT grant under `LICENSE`.

Where an OCR text stream fuses a printing's marginal summaries into body
lines, a whole-volume coordinate reading-order derivative may restore source
order. It is such a separately identified derivative. Every native WORD appears
exactly once with its value unchanged, and only order, role and inter-WORD
whitespace change. Pages whose geometry is uncertain are held and keep their
raw OCR bytes. Readers keep marginal summaries as separate TAB-led blocks, each
emitted at its anchor beside the section it annotates and never fused into a
body line; this is how the continuation series already retains its own
historical marginal summaries literally. The printing's page-foot footnotes
are likewise kept as separate blocks at the page break. A footnote set as its
own block is acceptable; a footnote run into a body, synopsis or protocol
paragraph blocks the reader. A single OCR WORD that joins marginal
and body glyphs is an inseparable mixture. Any unit containing one stays held
for a character-geometry pass and is not admitted with a disclosure. Only a
unit whose prior reviewed extent maps cleanly and contiguously through WORD
identity is registered, as a new reading selection of the same work that
preserves its withdrawn predecessor. A reading selection found defective is
replaced by a later derivative's selection that explicitly supersedes it;
the earlier derivative, selection and document remain as historical records.
A fragment's extent statement from the earlier raw-OCR review identifies its
raw OCR line numbers as such. Each volume must first pass an evidence
gate of at least twelve native page images, at least half of them held out
from the proposal's tuning, with the running-head rows of every page listed
for a quick scan. Source admission records the exact corrected text and its
evidence. If a repaired print edition is issued, every page receives the required visual
review under its own rendering receipt.

## Mechanical reading edition

These are source editions, attributed to the named pope and source edition.
They are not GPT or Claude authored studies. Keep their source identities and
retained payloads under `src/sources/`; never create duplicate provider leaves
to satisfy a publication catalog. Original exposition about an act belongs
in the appropriate provider's publication and cites this source edition.

Each reader edition identifies its actual text language. Its optional print
edition uses two columns that continue in normal reading order. A historical
witness that includes an act or annex in another language preserves that source
order and identifies
the multilingual extent explicitly; a Latin collection title does not make
every constituent Latin. Do not split, translate or relabel substantive source
text merely to fit a single-language template. Two columns do not imply a
Latin/English parallel edition. Display the text language, responsible issuer, title/incipit,
and known act date unambiguously. Omit an unresolved date from the title line
without describing the source as undated. Preserve source paragraph numbers,
section order, signatures,
dating clauses, and historical footnotes/endnotes. Unnumbered paragraphs must
not receive invented canonical numbers. Keep source notes addressable and
distinguish them from project apparatus. Do not abridge, modernize, silently
correct, or combine language editions.

Begin with the source text after compact identification. Place source
edition, transcription limitations, citation, and rights details in terminal
apparatus. State whether the text is a web transcription, OCR, or
image-collated text; mechanical extraction is not collation. The common
rights boundary remains a compact final-page colophon. The retained source
wording is excluded from Triptych's project-content license.

Generation records identify the canonical input artifact and hash, generator
and version, transformation options, and tracked source revision timestamp.
A print receipt separately records the renderer/template and exact output
hash. Record unknown facts as unknown. Identify mechanical typesetting
and project-created apparatus without assigning papal wording to an AI
provider. Source-library evidence states retain their existing meanings;
rendering a source does not promote it to `verified`.

### Classic reading typography

The current reader design uses Latin Modern Roman at 10.5pt with 13pt leading,
indented paragraphs without extra paragraph gaps, a restrained roman title,
and a short rule above the smaller terminal apparatus. English and Latin are
justified with their own Babel hyphenation patterns. Other identified languages
retain ragged-right composition rather than inheriting English patterns.
Babel shorthands are disabled so literal source quotation marks and adjoining
characters cannot become language-specific markup in either body or title.
Short all-capital source paragraphs use flush-left composition to avoid
stretched heading words, without becoming newly invented semantic headings.
Historical notes remain in their source order; typography does not infer new
note anchors, rewrite OCR word divisions, or move notes into invented footnotes.

XeLaTeX needs the Latin Modern OpenType fonts and Babel's English and Latin
support. A TeX Live installation requires `babel-english`, `babel-latin` and
`hyphen-latin`; rebuild its XeLaTeX format after enabling the Latin patterns.
Arch packages supply the additional Latin support through `texlive-langother`.
Missing Latin patterns stop compilation rather than silently substituting
English patterns. Junicode and FreeSerif remain character-specific fallbacks.

Generator version 2 records this design and its transformation options. Its
text-fidelity check permits an added visible hyphen only at a physical line or
page ending between source letters. Every original source hyphen must still
match; the check does not remove all hyphens from either text. Whitespace,
soft-hyphen and Unicode compatibility normalization retain their previous
declared meanings. Old frozen receipts remain exact records of their original
generator and
reviewed PDF. A typography change requires a new print receipt and inspection
when that print edition is issued; it does not rewrite historical source
review or make PDF equality a normal source-release gate.

## Review and use in larger projects

Before a source reader is admitted, confirm that its exact selected artifact
has an affirmative basis for the actual release surface, account for every
body block, number, signature and note, and inspect its beginning and ending
boundaries. Mechanical extraction is not source collation. Compare the
reader against the exact selected source, allowing only declared
transformations. A source/schema PASS is not a claim of visual print review.

When issuing a reviewed print edition, additionally compare source and
extracted PDF text, compile sufficient passes, inspect logs, structure,
fonts, metadata, and column reading order, then inspect every page with the
repository PDF-review tool. Record the exact output hash, renderer/template,
input selection and actual review extent. A successful build or contact sheet
is not inspection. Print output stays outside Git and normal deployment.

A sparse final page can retain a genuine historical subscription, registration
line or source note. Record that qualification without treating it as a layout
failure solely for its sparseness. A terminal page containing only project
source/rights notices or unrelated running-head furniture does not establish
source-bearing final-page coverage.

Presentation projects reuse the canonical source-library IDs and their own
`research/source-bindings.toml`, pinning exact witnesses and loci. A slide,
study, timeline, or bibliography may link an identified source or source
reader, but must keep its own interpretation and source-sufficiency
judgment. A catalog topic or proposed relation is a finding aid, not an
independent textual authority. Modern or untranslated items remain useful
metadata references without promising a local text or historical PDF.

## Source readers and historical print receipts

Canonical source text, reading selections, their rights basis, and the
mechanical recipes are the durable deliverable. `release/papal-documents.json`
preserves the historical installed-reader identities and inspection evidence;
its frozen input snapshots use the separate exact delivery contract below.
No historical PDF hash or review extent may be manufactured, refreshed to a new
render, or treated as source verification. These records are not additional
historical witnesses. Retain them without machine paths or runtime identifiers.

### Frozen input snapshots and compact records

`release/papal-documents/input-delivery.json` describes the exact historical
JSON and JSONL snapshots formerly under `release/papal-documents/inputs/`.
`tools/snapshot-store` preserves their whole-file hashes, sizes, archive/member
identities and delivery routes separately from source-library artifacts. It
covers unreferenced snapshots as well as current release inputs. Those bytes
are preserved evidence, not a disposable browser cache; physical relocation
does not alter the raw release JSON, source pins or historical review facts.

Routine checks use `release/papal-documents/input-records.json` and its shards
under `release/papal-documents/input-records/`. The mechanical extraction binds
the exact release identity and original whole-file hashes/sizes, retains complete
headers and complete required rows at their unchanged original row indices,
and records the original document counts. A selected row never becomes a
renumbered or padded replacement `documents` array. The extraction is marked
`editorial_approval = false`; it attests exact historical records, not new
research, source verification, permission, or page inspection.

`python3 scripts/_papal_input_receipt.py check` checks the current plan and the
release's semantic, revision, PASS, page-report and reuse relationships against
those attested records. It neither opens raw snapshots/PDFs nor fetches them.
`record` independently verifies exact originals before writing the index and
shards; a detached row plus a whole-file hash alone is not extraction proof.

Full original-byte verification is explicit:

```sh
tools/snapshot-store check --archives --archive-dir .scratch/papal-input-packs
tools/snapshot-store hydrate --all --archive-dir .scratch/papal-input-packs
python3 scripts/_papal_input_receipt.py audit
```

The audit verifies every declared original byte stream and compares extracted
headers/rows with their controlling originals. Missing originals may be obtained
from registered delivery routes only through explicit `audit --fetch` or
`snapshot-store hydrate --fetch`. A normal build or metadata check does not require that
archive. Before deleting a snapshot, verify exact complete pack coverage and
the extraction contract. Advertise an archive route only after delivery is
verified. No original-byte audit renews the historical editorial or visual PASS.

### Explicit input staging for reviewed print maintenance

A new optional reviewed print installation follows this order:

1. Run `typeset-papal prepare-install` and inspect its scratch proposal.
   The proposal must bind the current source plan, exact rendered bytes and
   complete page-review evidence.
2. Run `tools/typeset-papal stage-inputs --prepared
   .scratch/papal-install/prepared.json`. Staging regenerates and compares the
   proposal, repeating the source, PDF-fidelity and review checks. It writes
   only the proposal's exact hash-addressed JSON/JSONL input snapshots under
   ignored `release/papal-documents/inputs/`. Installed PDFs, the release
   record, reports, delivery declarations and extraction records stay unchanged.
   Existing matching snapshots are preserved; collisions, symlinks or changed
   inputs are refused, and a staging failure rolls back its new snapshots.
3. Inventory and pack those inputs while retaining every previously declared
   historical snapshot, including unreferenced ones. Previously externalized
   originals must be available in the verified local cache for repacking;
   restore them explicitly when needed. Verify the complete offline pack,
   publish it through the separately authorized archive workflow, and verify
   each published archive against its recorded hash and size at its registered
   delivery URL. Update `input-delivery.json` before installation. Packing and
   staging do not upload anything.
4. Run `typeset-papal install --prepared` with the inspected proposal.
   Installation revalidates the proposal and refuses undeclared input references
   before changing installed bytes. It does not accept an unregistered raw
   snapshot as delivery evidence.
5. Run `python3 scripts/_papal_input_receipt.py record`, then `audit` and
   `check`, and the explicit `typeset-papal check-install --plan` byte check.
   Refresh the governed browser products and release bindings, then run the
   owning publication gates before publishing a source checkpoint.

Routine metadata checks intentionally fail between declaration, installation
and extraction updates. Keep publication closed until the new extraction binds
the exact new release and the final gates pass. Staging, archive declaration
and newly rendered bytes confer no source admission, visual PASS or publication
approval. Old snapshots and review facts remain preserved throughout.

### Current reader delivery

The source-first publication policy supersedes the former tracked
`pdf/papal-documents/` exception. Historical PDF bytes use the exact-artifact
delivery layer in `guidance/sources.md`; a download is offered only after its
archive delivery is verified. Current source readers are exposed through the
existing papal reader surface, and optional print output is generated explicitly
with `tools/print-document`, as described in `docs/printing.md`. Neither the
site build nor an ordinary source check typesets the collection or fetches its
binary evidence.

Apply source supersessions and withdrawals before choosing a current reader.
Pending, failed and rejected selections retain explicit delivery states and
no reader link that implies admission. A historical PDF URL may lead to an
honest HTML reader or page explaining print options; it must not pretend to serve
the old PDF. Preserve source identity and language when deriving routes, with
`unknown-date` for an unresolved date. A changed current selection cannot
leave a withdrawn source advertised as current. A source checkpoint does not
itself deploy a website or publish an archive.
