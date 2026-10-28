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
checking, PDF review, installation, and deployment remain separate facts.

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
selection requires an explicit disposition before its PDF can be installed.

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
for a quick scan. Every page of every repaired PDF is still visually reviewed
before installation.

## Mechanical reading edition

These are source editions, attributed to the named pope and source edition.
They are not GPT or Claude authored studies. Keep their source identities and
retained payloads under `src/sources/`; never create duplicate provider leaves
to satisfy a publication catalog. Original exposition about an act belongs
in the appropriate provider's publication and cites this source edition.

Each rendered edition identifies its actual text language, set in two columns
that continue in normal reading order. A historical witness that includes an
act or annex in another language preserves that source order and identifies
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
and version, transformation options, tracked render revision timestamp, and
output hash. Record unknown facts as unknown. Identify mechanical typesetting
and project-created apparatus without assigning papal wording to an AI
provider. Source-library evidence states retain their existing meanings;
rendering a source does not promote it to `verified`.

## Review and use in larger projects

Before a PDF enters an installed/public destination:

1. Confirm that its exact input artifact has an affirmative distribution
   basis and that excluded modern apparatus cannot enter the output.
2. Compare extracted source and PDF text mechanically, allowing only declared
   typesetting changes; account for every body block, number, signature, and
   note. Inspect beginning and ending boundaries against the source.
3. Compile sufficient passes, resolve references, inspect logs, and check PDF
   structure, embedded fonts, metadata, and column reading order.
4. Generate review rasters through the repository's PDF-review tool and
   inspect every page. Record the exact reviewed PDF hash and review extent;
   a successful build or contact-sheet generation is not visual review.
5. Install only those reviewed bytes and expose a link only when the
   installed artifact and the release surface exist.

A sparse final page can retain a genuine historical subscription, registration
line or source note. Record that qualification without treating it as a layout
failure solely for its sparseness. A terminal page containing only project
source/rights notices or unrelated running-head furniture does not establish
source-bearing final-page coverage.

Presentation projects reuse the canonical source-library IDs and their own
`research/source-bindings.toml`, pinning exact witnesses and loci. A slide,
study, timeline, or bibliography may link an identified source or reviewed
reading PDF, but must keep its own interpretation and source-sufficiency
judgment. A catalog topic or proposed relation is a finding aid, not an
independent textual authority. Modern or untranslated items remain useful
metadata references without promising a locally available PDF.

## Installed source readers

The 2026-10-25 request for individual papal reading PDFs requires a durable
deliverable as well as reproducible build tools. Reviewed current readers
therefore have a narrow tracked destination at `pdf/papal-documents/`, outside
the AI-provider publication trees. This exception does not change the normal
deployment-build policy for other PDFs. Generated standalone TeX and body
fragments remain reproducible intermediates, derived from the canonical source
artifacts and retained rendering selections.

`release/papal-documents.json` owns the installed set. It records the exact
source identities, selections and rendering revisions, PDF paths, hashes,
sizes and page counts, and full-page PASS evidence. Retain the frozen input
manifests and receipts needed to interpret those pins under
`release/papal-documents/inputs/`, deduplicated by their content hashes. These
are release records, not additional historical witnesses or verified passages.
Do not retain machine-specific paths or runtime identifiers in them.

Installation selects only current, affirmatively distributable readers that
pass source fidelity and hash-bound inspection of every page. Apply all source
supersessions and withdrawals first. Pending, failed and rejected readers
remain explicit delivery states without installed PDF links. Installation
copies the reviewed bytes; it does not rerender, rewrite their provenance or
promote a source's evidence state. File names derive their date prefix from
the selected record, using `unknown-date` when unresolved, and preserve a
collision-checked source identity and language.

Validate the complete owned path set and every installed hash against the
release record. An obsolete alias may be removed only when the previous release
owns it and its bytes still match that release; preserve an unexpected file
for investigation. Preserve prior releases in Git history. A changed current
selection cannot leave a withdrawn PDF advertised as current. Installation and
a feature-branch checkpoint do not themselves deploy a website.
