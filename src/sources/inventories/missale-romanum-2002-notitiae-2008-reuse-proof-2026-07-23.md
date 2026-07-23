# 2002 Missale Romanum and 2008 Notitiae Reuse Review

Reviewed on 2026-07-23.

This record documents the second bounded canonicalization and reuse proof
inside `family.roman-missal.third-edition-latin-us-english`. It supplements the
family ledger and does not itself create a source identity, evidence state, or
publication binding. The proof covers the exact accessible 2002 Latin Missal
witness and the official 2008 *Notitiae* notice and variation list used by nine
proper guides and the liturgical-calendar reference. It does not represent the
variation list as the complete 2008 altar book.

## Identity boundaries

The source graph keeps four layers distinct:

- the *Missale Romanum* work and its 2002 third typical edition;
- the separately identified 2008 *reimpressio emendata*, for which this proof
  has edition metadata but no complete altar-book artifact;
- *Notitiae* volume 44, nos. 503--504, as the container that owns the exact
  official journal PDF; and
- the Italian reprint-status notice on printed p. 367 and the separately
  titled Latin *Variationes et additiones* with *Supplementum* on printed
  pp. 368--387 as two constituent works within that journal artifact.

The same constituent-work rule is applied inside the 2002 Missal witness.
The third-edition decree, Paul VI's *Mysterii Paschalis*, the *Normae
universales de anno liturgico et de calendario*, and the *Calendarium Romanum
generale* are not falsely owned as Missal passages merely because the Missal
contains them. Each has its own work and edition, a verified page-ranged
segment pointing across to the Missal artifact, and a complete checked
passage. Genuine Missal formularies and proper Vigil/Day headings remain
Missal-owned.

This separation makes *Mysterii Paschalis*, the Norms, and the General Calendar
reusable across later publications and delivery contexts. Other legacy
references to those works are not silently attached to this Latin 2002 witness;
their language, expression, locus, and actual use still require local review.

## Exact artifacts and rights

The 2002 delivery witness is an 828-page, 3,333,382-byte PDF obtained from a
non-ecclesiastical secondary host, SHA-256
`0b458944824d2ee92854b9664f83e553af0342e0b15a9dc14b00e846405523d7`.
Two acquisitions were byte-identical. Its title and decree identify the
Vatican third typical edition, but PDF inspection found zero embedded raster
images and one embedded font subset. The exact bytes are therefore a
digitally typeset secondary reproduction, not a page-image facsimile. A
54-page bounded review packet supplied the registered ranges and surrounding
context; every review sheet was inspected.

The *Notitiae* witness is the exact official 132-page, 1,280,566-byte PDF,
SHA-256
`74c8d1740284984d0f4d64b2223edf805dadfa55aec8a92f8cfba9ab901eca0f`.
Artifact pages 49--69, corresponding to printed pp. 367--387, were reviewed in
full. The issue has a source-local bibliographic discrepancy: its masthead
prints “Vol. 45 (2008),” while the official archive path and the following
year's official retrospective identify it as *Notitiae* 44 (2008). The
canonical edition follows the official archive and retrospective while
preserving the anomalous masthead in its notes.

Both modern artifacts are `restricted`. Public download did not establish
repository-redistribution permission, so Triptych retains exact identity,
hash, extent, provenance, review, and dependency metadata but no payload. No
whole-artifact corpus is declared: neither restricted PDF is a tracked
raw-line-searchable representation, and the proof does not claim inspection
outside its registered bounds.

## Passage normalization

Eighteen passages depend on the 2002 artifact:

- complete constituent passages for the third-edition decree,
  *Mysterii Paschalis*, the Universal Norms and precedence table, and the
  January--December General Roman Calendar;
- the seven Ordinary Time formularies for Weeks XI--XVII;
- the Trinity and Corpus Christi formularies; and
- proper Vigil/Day headings for Epiphany, Ascension, the Nativity of Saint John
  the Baptist, Saints Peter and Paul, and the Assumption.

Three passages depend on the *Notitiae* artifact:

- the complete Italian status notice, which says that the 2008 book is an
  emended reprint rather than a new typical edition and reports, but is not
  itself, decree Prot. N. 652/08/L;
- the complete General Calendar subsection of the variation list; and
- the complete *Tempus per annum* subsection, which lists changes only at
  Missal pp. 457 and 471.

The last passage supplies bounded no-listed-change evidence for the nine
formularies. It is not a negative search and does not prove that the 2002 and
2008 pages are otherwise identical. Direct 2008 altar-book page collation
therefore remains outstanding.

## Reviewed consumers

Ten publications consume this bounded source state:

1. the seven Year A proper guides for Ordinary Time Weeks XI--XVII;
2. the Most Holy Trinity and Most Holy Body and Blood of Christ proper guides;
   and
3. the third-edition liturgical-calendar reference.

Each proper guide binds the cataloged 2008 altar-book edition identity, its one
exact 2002 formulary, the 2008 edition-status notice, and the bounded *Tempus
per annum* variation subsection. The edition binding is intentionally
bibliographic and catalog-only because no exact complete 2008 altar-book
artifact was inspected. The calendar reference binds the same edition identity
and eleven passages: the four independently owned constituent works in the
2002 container, five genuine Missal proper-heading checks, the 2008 status
notice, and the General Calendar variation subsection.

Review corrected the legacy description of the 2002 witness from
“page-image facsimile” to an exact secondary-host digitally typeset PDF
reproduction. References to missing direct **2008** page images remain accurate
and were not removed. These are research-record corrections only; no rendered
TeX or installed PDF changed.

## Acceptance proof

The source graph validates with 38 artifacts, 4 corpora, 25 editions, 70
passages, 8 segments, 16 works, and 278 bindings. Reverse-use lookup returns:

- ten exact consumers for the cataloged 2008 altar-book edition identity;
- one exact consumer for each of the eighteen 2002-controlled passages;
- ten consumers for the 2008 edition-status notice;
- nine consumers for the *Tempus per annum* subsection; and
- one consumer for the General Calendar variation subsection.

Impact from the 2002 artifact reaches 22 dependent source records, 18 binding
uses, and 10 unique publications. Impact from the *Notitiae* artifact reaches
5 dependent source records, 20 binding uses, and the same 10 unique
publications. Impact from the metadata-only 2008 Missal edition independently
reaches 10 bibliographic binding uses and all 10 publications; this keeps its
edition identity discoverable without pretending that its pages were acquired
or verified.

Five run-local mirrors of the actual graph validated before mutation:

- changing valid 2002 artifact metadata produced exactly 18 stale binding
  fingerprints across all fourteen Missal passages and four constituent-work
  branches;
- changing valid *Notitiae* artifact metadata produced exactly 20 stale
  fingerprints: ten status-notice, nine *Tempus per annum*, and one General
  Calendar use;
- changing only valid *Tempus per annum* passage metadata produced exactly
  nine stale fingerprints; and
- changing only valid General Calendar variation-passage metadata produced
  exactly one stale fingerprint; and
- removing the metadata-only 2008 Missal edition produced exactly ten dangling
  binding diagnostics, one for every reviewed consumer.

The artifact mutations prove that a correction to shared container evidence
reaches every reviewed dependent use, including cross-work segments. The
passage mutations prove that independently normalized subsections do not
invalidate unrelated consumers. The 2008 edition bindings are deliberately
catalog-only and therefore have no verification fingerprint; the removal test
instead proves their referential dependency and exact reverse-use fan-out
without overstating uninspected altar-book evidence.

## Remaining family work

The broad family remains open. Later proofs should separately normalize a
complete exact 2008 altar-book artifact when lawful access and direct review
permit it, the Latin GIRM states, additional Missal formularies and
constituents as consumers require them, later universal variations, the 2011
United States altar book, and other territorial expressions. An official or
page-image 2002 witness may also be added as a distinct artifact; it must not
be conflated with the digitally typeset secondary reproduction proved here.
