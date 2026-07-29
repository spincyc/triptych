# Books and supports: priestly review packet

Historical status on 2026-07-27: **ready for bounded priestly/ceremonial
review; not publication approval**

Prepared: 2026-07-27

Current status (2026-07-29): this packet is retained as a record of questions
that informed later source and artwork work. It is not a current review
request, alpha admission path, release gate, or promise of external review.
Any concrete source, rights, safety, reproducibility, mechanical, or visual
defect recorded below remains actionable on its own terms.

## Review boundary

This packet asks a priest experienced with the 1962 Roman books, or a
competent master of ceremonies working under one, to review the dictionary's
first books-and-supports family. It does not ask the reviewer to approve the
whole dictionary, settle material history from memory, or treat present local
practice as a universal rubric.

The current family contains:

- altar Missal;
- Missal stand;
- Missal cushion;
- Missal markers;
- freestanding lectern;
- Epistle book; and
- Gospel book.

Official chant books, the complete *Rituale Romanum*, *Pontificale Romanum*,
and *Caeremoniale Episcoporum* book families, processional books, bindings,
tabs, removable covers, and historical forms remain incomplete. A positive
review of this packet must not be represented as completeness review for
those omitted families.

## Evidence supplied to the reviewer

The claim-level research is in
`books-and-book-supports-source-pass.md`. The directly inspected controlling
witness is the 1962 Vatican typical Missal facsimile registered as
`artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf`.

The propositions offered for ceremonial review are:

1. General Rubric 527, printed p. XXXVI / artifact PDF p. 34, contrasts a
   *cussinus* and *legile* as alternatives beneath the altar Missal.
2. *Ritus servandus* I.1 and I.4, printed p. LIV / artifact PDF p. 56,
   establish preparation of the Missal's *signacula* and the Low-Mass Missal
   opened on its cushion at the Epistle side.
3. *Ritus servandus* VI.1, printed p. LVII / artifact PDF p. 59, establishes
   the Low-Mass Missal's movement and Gospel-side orientation.
4. *Ritus servandus* VI.4--5, printed pp. LVII--LVIII / artifact PDF
   pp. 59--60, establish distinct *liber Epistolarum* and *liber
   Evangeliorum* identities and the ordinary held-book Gospel mode at Solemn
   Mass.
5. Palm Sunday n. 8, Good Friday nn. 7, 9, and 10, and Easter Vigil
   nn. 13/13a establish ceremony-specific lecterns and distinguish bare
   lecterns from the Easter-Vigil lectern covered with a white cloth.

The 1948 *Caeremoniale Episcoporum* findings in the source pass are supplied
only as an edition-identified near-horizon comparison. The reviewer should
not promote them to an unqualified 1962 norm unless the operative-edition and
amendment audit is independently closed.

## Canonical records for review

| Object ID | Record | Current state | Review focus |
| --- | --- | --- | --- |
| `obj-altar-missal` | `shared/objects/altar-missal.toml` | identified | identity, presence, movement, handling boundary |
| `obj-missal-stand` | `shared/objects/missal-stand.toml` | identified | stand/cushion distinction; server movement |
| `obj-missal-cushion` | `shared/objects/missal-cushion.toml` | identified | alternative support; server movement |
| `obj-book-marker` | `shared/objects/book-marker.toml` | identified | *signacula* function; preparation boundary |
| `obj-lectern` | `shared/objects/lectern.toml` | identified | Holy Week bare/covered states; distinction from altar stand |
| `obj-epistle-book` | `shared/objects/epistle-book.toml` | identified | separate identity and subdeacon's use |
| `obj-gospel-book` | `shared/objects/gospel-book.toml` | identified | altar relationship and held-book Gospel mode |

No record is `source-audited`, `art-reviewed`, or `publication-ready`.
Reviewer comments should be recorded by object and claim ID. A correction to
one claim must not silently approve the others.

## Artwork and provenance supplied

The complete exact prompts, technical identities, received and normalized
hashes, lack of reference inputs, planned consumers, and review states are in
the canonical `artwork-manifest.toml`.

| Artwork ID | File | What it may demonstrate | What it may not demonstrate |
| --- | --- | --- | --- |
| `art-altar-missal-on-stand` | `shared/artwork/pencil/books/RPD-FIG-books-0001-in-use-missal-on-stand.png` | readable relationship among one open Missal, support, and markers | prescribed binding, dimensions, stand construction, ornament, or marker count |
| `art-altar-missal-on-stand-v2` | `shared/artwork/pencil/books/RPD-FIG-books-0001-in-use-missal-on-stand-v2.png` | the same checked relationship with a transparent, feathered publication boundary | any new morphology or source claim beyond the unchanged predecessor |
| `art-missal-stand-isolated-v2` | `shared/artwork/pencil/books/RPD-FIG-books-0005-iso-missal-stand-v2.png` | isolated recognition of the empty low support and distinction from the cushion and freestanding lectern | prescribed folding construction, wood, hinge arrangement, proportions, dimensions, or surface treatment |
| `art-missal-cushion-isolated` | `shared/artwork/pencil/books/RPD-FIG-books-0002-iso-missal-cushion.png` | visual distinction between a soft support and a rigid stand | prescribed wedge, fabric, fringe, color, stuffing, or size |
| `art-lectern-isolated` | `shared/artwork/pencil/books/RPD-FIG-books-0003-iso-lectern.png` | distinction between a freestanding support and the low altar stand | universal pedestal construction or the bare/covered ceremonial state by itself |
| `art-book-marker-ribbons-detail` | `shared/artwork/pencil/books/RPD-FIG-books-0004-detail-marker-ribbons.png` | one familiar physical realization of book markers | that *signacula* must be ribbons, that six are required, or that alternating tones encode liturgical colors |

All four are project-generated through the built-in image-generation
interface without a reference image. The exposed interface supplied no exact
model identifier or runtime version. Each selected output was copied into the
repository, stripped, converted to 8-bit grayscale, hashed, and personally
inspected by the generating agent for object count, contact, silhouette,
crop, obvious impossible construction, and absence of baked-in text, arrows,
numbers, borders, watermarks, or color. No content correction was made.

This was an internal visual/technical check, not priestly, independent,
material-culture, print, consumer, rights, or release approval. The figures
remain at `generated`; the canonical object links remain
`identity-checked`.

The 2026-07-28 duplication pass adds a versioned, strictly isolated Missal
stand drawing with a transparent publication boundary. It is the canonical
recognition view for `obj-missal-stand`. The combined drawing remains the
contextual formation for `obj-altar-missal`, `obj-missal-stand`, and
`obj-book-marker`, including its bespoke altar-server use. Its versioned
boundary successor changes only the perimeter alpha; the original file and
record remain as generation and review provenance. Neither boundary successor
adds evidence for construction or material.

## Morphology qualifications to retain

The 1962 loci establish ritual identities, alternatives, functions, and
spatial relationships. They do not establish:

- the Missal's dimensions, binding material, boards, clasps, corner pieces,
  cover ornament, or page-edge treatment;
- that physical markers are attached ribbons, their number, width, colors,
  or attachment;
- one universal folding, carved, wooden, metal, silver, or fixed form of
  altar stand;
- the cushion's slope, stuffing, fabric, fringe, color, or dimensions;
- one universal portable-lectern silhouette, pedestal, material, height, or
  ornament; or
- a universal binding design that visually distinguishes the Epistle and
  Gospel books.

The generated figures are therefore representative recognition candidates.
They cannot be promoted to publication artwork merely because they look
traditional or resemble one parish's objects. Material morphology requires a
dated, provenanced witness; local-form testimony may identify needed variants
and errors but does not by itself prove universality.

## Questions for the priestly reviewer

Please answer from the ceremony actually reviewed and identify the church,
community, or source tradition in non-machine-local terms. Mark an answer
`local` unless it is supported by an exact governing or competent ceremonial
locus.

1. In the reviewed 1962 Low-Mass practice, is the Missal normally moved
   together with its support, or is the book removed from the support for any
   ordinary move? Does this differ between cushion and rigid stand?
2. Does the generated stand's height, angle, lower retaining structure, and
   footprint resemble a form actually used on the altar, or does it read as a
   floor or choir support? Which feature should be corrected?
3. Is a folding wooden altar stand a familiar substantive form in the
   reviewed setting? Are metal, silver, fixed-angle, folding, or adjustable
   forms common enough there to merit distinct figures rather than a note?
4. Does the generated Missal cushion read as an altar-book cushion, or as a
   modern wedge/pillow? What locally encountered silhouette, thickness,
   edging, fringe, or tassel treatment would make identification reliable?
5. When a cushion is used locally, is it moved with the Missal? Who ordinarily
   prepares and moves it at Low, sung, Solemn, and pontifical functions?
6. Are the markers in the reviewed Missal attached ribbons, loose markers,
   tabs, or a combination? How many are ordinarily present? Which of those
   facts are merely binding design or preparation practice?
7. Does alternating grayscale on the generated ribbons risk falsely implying
   a prescribed color code? Should every ribbon be rendered in the same tone
   for the universal plate?
8. Do local servers ever prepare or rearrange the Missal markers, or should
   the server edition say only “recognize; do not rearrange without
   direction”? Identify any role distinction.
9. Does the freestanding lectern figure resemble an article actually used for
   the 1962 Holy Week readings? Which materially different local forms should
   be shown: portable wood, portable metal, covered stand, pulpit, or
   architectural ambo?
10. For Palm Sunday and Good Friday, does “bare lectern” require a stronger
    visual contrast than simply omitting a cloth? Are there objects a novice
    might wrongly add?
11. For the Easter Vigil, how is the white cloth fitted or draped on the
    lectern in the reviewed use? Is the cloth a local loose covering, a
    purpose-made cover, or another documented form?
12. At ordinary Solemn Mass in the reviewed practice, is the Gospel book held
    by the subdeacon as the 1962 *Ritus* describes? Are there local or
    pontifical lectern branches that must be explicitly separated?
13. Are the Epistle and Gospel books locally separate volumes, a combined
    volume, or extracted from another authorized book? Which answer is
    universal, authorized variant, or local economy?
14. Can a server reliably distinguish local Epistle and Gospel books by
    physical form alone? If not, should the plate use identical representative
    silhouettes and let TeX labels and in-use context carry the distinction?
15. Are removable silk covers encountered for the Missal, Epistle book, or
    Gospel book? In which pontifical or other exact context, and should those
    be separate figures rather than generic cover variants?
16. Which handling warning would materially help a young server: book
    balance, support grip, ribbon protection, avoidance of page damage,
    procession posture, or a different locally observed failure?

## Requested review decision

For each object and figure, record one of:

- **accurate within stated qualification**;
- **accurate only for the named local form**;
- **requires the listed correction**;
- **insufficient evidence to judge morphology**; or
- **reject**.

Also record:

- reviewer name and competence/role;
- review date;
- rite, books, ceremony, and local-use boundary reviewed;
- exact source loci used beyond the packet;
- object and artwork IDs reviewed;
- corrections and unresolved questions; and
- whether the event was ceremonial, morphology, handling/safety, print, or
  another review class.

Do not use “approved” without naming its class. Priestly ceremonial review
does not replace material-culture, rights, production, exact-snapshot
distribution, or ecclesiastical approval.

## Gate after review

A favorable review may advance only the propositions and figures actually
checked. Before consumer use, the project must still:

1. bind a dated material-culture witness for each accepted representative
   morphology or explicitly label it as a local example;
2. correct or replace any generated figure whose construction is misleading;
3. add the missing official book families and close edition/terminology
   audits;
4. perform independent factual, actual-size monochrome print, page/plate,
   consumer, rights, and release reviews; and
5. update canonical records and the artwork manifest with the exact review
   event rather than changing state by inference.
