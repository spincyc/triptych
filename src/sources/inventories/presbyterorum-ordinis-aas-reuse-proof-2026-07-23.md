# *Presbyterorum ordinis* and AAS 58 Reuse Review

Reviewed on 2026-07-23; rendered correction reviewed on 2026-07-24.

This record documents the bounded normalization of *Presbyterorum ordinis*
within `family.vatican-ii.acts` and its reuse of the volume 58 component of
`family.acta.aas-ass`. It makes complete official witnesses centrally
identifiable for later expansive examination, binds current publications only
at the loci they actually use, and proves cross-publication propagation by
mutating run-local copies of the real source graph. The canonical manifests
and publication-local bindings remain the machine-enforced records.

## Identity boundaries

The graph distinguishes the decree from its expressions and container:

- *Presbyterorum ordinis* is one intellectual work, solemnly promulgated on 7
  December 1965 and comprising numbered articles 1--22;
- the dated English and Latin Vatican web states are separate editions and
  exact HTML artifacts;
- the Latin constituent printed in *Acta Apostolicae Sedis* 58 (1966) is a
  separate edition represented as one segment of the existing exact volume
  artifact; and
- *Acta Apostolicae Sedis* volume 58 remains an official-gazette container
  containing many distinct acts, not another identity for the Decree.

The English web response contains the complete numbered body and consolidated
notes, but no promulgation formula or subscription material and no named
translator. Its HTML metadata incorrectly gives `eventDate="1967-12-07"`;
the visible heading, Latin response, and *Acta* all give 7 December 1965, so
the malformed delivery metadata does not control the work date.

The Latin web response contains the complete numbered body, consolidated
notes, a duplicated delivery of the promulgation formula and date, and a
partial subscription block ending with Cardinal Callori di Vignale. The
*Acta* instead prints the formula, papal subscription, and a reference to the
common subscriptions on pp. 941--946. Those pages are not silently absorbed
into the Decree's constituent segment.

## Exact artifacts, extent, and rights

Three exact Holy See artifacts control the normalized records:

| Artifact | Extent | SHA-256 |
| --- | ---: | --- |
| English *Presbyterorum ordinis* HTML response | 95,582 bytes | `7d5a46cee1731fbce6fd5325817b83d47fe8d193259f224827681e88ffeb3448` |
| Latin *Presbyterorum ordinis* HTML response | 137,996 bytes | `cd0e9d19be746bf4971e9711580f3df930f45a4b988ee79392e9744d6b7e52f0` |
| Holy See AAS 58 OCR PDF | 1,279 pages; 5,944,403 bytes | `69c27224cde7f27547e18c544f5b99064793ada9509ebc902b20fa548e15bac8` |

The Vatican archive aliases recorded in the artifact manifests returned
byte-identical responses where available and tested. The complete *Acta*
constituent begins with the heading and article 1 on printed p. 991. Article
22 ends on p. 1024 before the promulgation formula; the following page begins
*Gaudium et spes*. The preceding page ends *Ad gentes*. Article 13 spans pp.
1011--1013, with the relevant clause and source note on pp. 1011--1012. These
boundaries were checked against the exact artifact. Its OCR remains a locating
aid rather than an independently authoritative transcription.

The Vatican portal's legal notice did not establish repository redistribution
permission. All three artifact identities are therefore `restricted` and
nonretained: the repository stores exact hashes, byte or page extent,
provenance, boundaries, and dependency records, but not the payloads.

## Expansive availability and bounded use

The complete dated English and Latin web states and complete Latin *Acta*
constituent are centrally identifiable for later work-wide examination. That
availability does not imply that every consumer inspected or relied on the
whole Decree.

The reusable English passage records cover articles 1--22, 2, 2--6, 5, and
16. Exact article records govern the two Ordinary expositions and the
celibacy article; the broad 2--6 record preserves only the sacramental
treatise's bibliography ceiling. The Latin web and *Acta* article-13 records
govern one reception claim. The complete English and *Acta* body records
remain available without a verified publication consumer.

Witness differences remain first-class. The Latin web apparatus numbers the
Ninth Sunday attribution as note 105; the *Acta* chapter apparatus numbers the
equivalent note 14. The article reads `opus nostrae redemptionis continuo
exercetur`, reusing the Secret's clause with an inserted adverb rather than
repeating it verbatim.

## Source-of-source non-inheritance

The graph records discovery boundaries without manufacturing direct use:

- English article 2 note 13 cites Augustine, *De civitate Dei* 10.6, and note
  9 cites the Roman Pontifical and earlier ordination sources. A publication
  using article 2 does not thereby become a direct consumer of those works.
- Article 5's Thomas citations likewise do not create *Summa* bindings for
  the Ordinary expositions.
- Article 13's Missal attribution does not replace direct liturgical
  collation. The Ninth Sunday guide independently binds the exact 1962 Missal
  for its textual claims and binds *Presbyterorum ordinis* only as later
  reception.
- Article 16's historical and Eastern-discipline references do not replace
  the celibacy article's independent current CIC and CCEO controls.

This answers the central reuse question structurally: a first-class source may
expose its own references as leads, but downstream publications inherit
neither inspection nor evidentiary dependence without their own bindings.

## Reviewed consumers and exclusions

Nine binding rows across six publications now share the normalized
identities. Seven rows across four publications are fingerprinted verified
uses:

- the 1962 Ordinary exposition uses English articles 2 and 5 as complementary
  doctrinal controls;
- the postconciliar Order of Mass exposition uses the same two articles, with
  the current Missal and territorial law controlled separately;
- the clerical-celibacy article uses English article 16; and
- the Ninth Sunday guide uses both the Latin web and *Acta* article 13 as
  distinct reception witnesses.

Two rows preserve honest catalog ceilings. The sacramental treatise lists
articles 2--6 only in its bibliography, and the council article uses
work-level title, genre, date, and subject metadata in its sixteen-document
inventory. Neither row claims publication-level inspection. In particular,
normalizing this Decree does not prove the council article's still-open claim
about the absence of two proper names from all sixteen documents.

The FSSP article is excluded: it reports that an FSSP constitutional excerpt
cites *Presbyterorum ordinis*, so its direct witness is the constitutional
excerpt and the Decree is only a source of that source. The sacramental
at-a-glance companion and the Nuptial Mass likewise do not inherit the
treatise's bibliography through their narrower shared-fragment imports.

The audit also identified nonblocking reader-reference improvements for later
content revisions. Both Ordinary bibliographies and the sacramental
bibliography could give the Decree's date, link, language, and distinct role
more explicitly. Those presentation issues do not change the evidence
dependencies recorded here.

## Reverse use and mutation proof

The unmodified graph validates. Thirteen isolated copies of the actual source
tree then received valid metadata-only mutations:

| Mutated node | Stale fingerprints | Publications | Unexpected diagnostics |
| --- | ---: | ---: | ---: |
| English *Presbyterorum ordinis* artifact | 5 | 3 | 0 |
| English articles 1--22 passage | 0 | 0 | 0 |
| English article 2 passage | 2 | 2 | 0 |
| English articles 2--6 passage | 0 | 0 | 0 |
| English article 5 passage | 2 | 2 | 0 |
| English article 16 passage | 1 | 1 | 0 |
| Latin web artifact | 1 | 1 | 0 |
| Latin web article 13 passage | 1 | 1 | 0 |
| *Presbyterorum ordinis* work | 7 | 4 | 0 |
| Latin AAS articles 1--22 passage | 0 | 0 | 0 |
| Latin AAS article 13 passage | 1 | 1 | 0 |
| Latin AAS constituent segment | 1 | 1 | 0 |
| Existing AAS 58 container artifact | 2 | 2 | 0 |

Passage mutations invalidate only their exact verified consumers. The English
artifact reaches five rows across the celibacy article and two Ordinary
expositions, while the two catalog-only English rows do not stale. The work
mutation reaches all seven verified rows across four publications. Mutating
the complete English or *Acta* body, or the bibliography-only 2--6 passage,
reaches no publication, proving that expansive central availability does not
falsely become publication use.

The shared AAS 58 mutation reaches exactly two publications: La Salette's
separate p. 445 Index notification and the Ninth Sunday's article-13 witness.
This proves real container reuse and propagation without conflating either
constituent with the gazette or with one another.

## Textual correction and acceptance results

The proof caught a rendered textual overstatement before commit. The Ninth
Sunday guide had called article 13 a repetition of the Secret's clause while
omitting `continuo`. The publication and research scope now give the exact
conciliar wording and classify the relation as documented reuse. A settled
two-pass build produced a 10-page PDF with SHA-256
`e912d945ea1cdd3e6c50b9de3b626ab01f38563c1aaa1976a77df9404723da5e`.
The log, structure, metadata, embedded-font, Unicode-map, text-extraction, and
install-identity checks passed. Bounded review rasters were generated through
`scripts/pdf-review`, and every rendered page was inspected at full size.
No prior exact-byte release clearance attaches to the changed PDF.

The completed source graph contains 53 artifacts, 4 corpora, 55 editions, 145
passages, 22 segments, 29 works, and 492 bindings. The family ledger assigns
all new identities to `family.vatican-ii.acts` while reusing the already
canonical AAS 58 artifact owned by `family.acta.aas-ass`. Remaining conciliar
acts and the separate complete sixteen-document search corpus stay open for
later proofs. These are internal source and production checks, not external
specialist or ecclesiastical approval.
