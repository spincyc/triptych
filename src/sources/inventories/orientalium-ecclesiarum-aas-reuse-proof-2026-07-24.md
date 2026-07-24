# *Orientalium Ecclesiarum* and AAS 57 Reuse Review

Reviewed on 2026-07-24.

This record documents the bounded normalization of *Orientalium Ecclesiarum*
within `family.vatican-ii.acts` and its reuse of the volume 57 component of
`family.acta.aas-ass`. It makes complete official witnesses centrally
identifiable for later expansive examination, binds current publications only
at the loci they actually use, and proves cross-publication propagation by
mutating run-local copies of the real source graph. The canonical manifests
and publication-local bindings remain the machine-enforced records.

## Identity boundaries

The graph distinguishes the Decree, its expressions, its gazette container,
and a related but separate notice:

- *Orientalium Ecclesiarum* is one intellectual work, solemnly promulgated on
  21 November 1964 and comprising numbered articles 1--30;
- the dated English and Latin Vatican web states are separate editions and
  exact HTML artifacts;
- the Latin constituent printed in *Acta Apostolicae Sedis* 57 (1965) is a
  separate edition represented as one segment of the existing exact volume
  artifact;
- *Acta Apostolicae Sedis* volume 57 remains an official-gazette container
  containing many distinct acts, not another identity for the Decree; and
- the notice on printed p. 89 establishing the Decree's vacatio is a distinct
  act and work, not article 31 or part of the Decree's numbered body.

The notice makes the Decree effective two months after promulgation and gives
patriarchs a just-cause faculty to reduce or extend that interval. It has its
own edition, segment, and complete passage. No publication currently relies
on it, so it remains centrally available without a decorative consumer
binding.

## Exact artifacts, extent, and rights

Three exact Holy See artifacts control the normalized records:

| Artifact | Extent | SHA-256 |
| --- | ---: | --- |
| English *Orientalium Ecclesiarum* HTML response | 33,012 bytes | `c552394af0d4ea9c5eb52dc8005b5b0d84e2c133157edf673c87cd1cd6e5d923` |
| Latin *Orientalium Ecclesiarum* HTML response | 51,347 bytes | `63f68901d6346de7cb9a748b5b6bfb029168fac4fb943ea9d447573c4b2b6a1e` |
| Holy See AAS 57 OCR PDF | 1,094 pages; 4,983,675 bytes | `bd6d813da15fd67d4e227de8e9a12660359192c65d580cd785c8dcbddd8cd94f` |

The English and Latin HTML metadata misspell the Decree's incipit. The
English response's article 26 reverses its displayed footnote markers 31 and
32. The Latin delivery appends unrelated *Lumen gentium* material. Those
delivery defects and boundaries are recorded rather than silently
normalized, and the unrelated appended span is excluded from every
*Orientalium Ecclesiarum* passage.

In the exact *Acta* artifact, the Decree begins on printed p. 76. Its numbered
body occupies pp. 76--85; the promulgation and subscription material
continues through p. 89. The distinct vacatio notice follows on p. 89, and
*Unitatis redintegratio* begins on p. 90. The OCR is a locating aid rather
than an independently authoritative transcription.

The Vatican portal's legal notice did not establish repository redistribution
permission. The HTML and PDF artifacts are therefore `restricted`,
nonretained, and nonindexable. The repository stores exact hashes, byte or
page extent, provenance, boundaries, and dependency records, but not their
payloads.

## Expansive availability and bounded use

The complete dated English and Latin web states and complete Latin *Acta*
constituent are centrally identifiable for later work-wide examination. That
availability does not imply that every consumer inspected or relied on the
whole Decree.

The reusable English passage records cover articles 1--30, 2--6, 6, 12--14,
12--18, and 17. Exact article records govern the clerical-celibacy article and
the two sacramental publications. The broad 2--6 and 12--18 records preserve
only the sacramental treatise's bibliography ceilings. The complete English
and *Acta* body records remain available without a verified publication
consumer. The Latin web state is likewise cataloged as a complete witness
without manufacturing a publication-level claim of direct use.

## Source-of-source non-inheritance

The Decree's notes expose Scripture, prior councils, Fathers, liturgical books,
and earlier disciplinary sources as leads. A publication using a Decree
article does not thereby become a direct consumer of those cited works.
Likewise:

- article 6 does not replace independent evidence for the history or current
  law of married Eastern clergy;
- articles 12--14 do not replace CCEO 694--697 and 710 as the current
  common-law controls or the 1996 Eastern liturgical Instruction as the
  authoritative implementation and anti-Latinization control;
- article 17 does not prove that any particular Church currently implements a
  stable diaconate; and
- the distinct vacatio notice is not inherited merely because a publication
  cites the Decree.

This preserves first-class source discovery while preventing the graph from
claiming inspection or evidentiary dependence that did not occur.

## Reviewed consumers and exclusions

Seven binding rows across four publications now share the normalized
identities. Four rows across three publications are fingerprinted verified
uses:

- the clerical-celibacy article uses English articles 6 and 17;
- the sacramental treatise uses English articles 12--14; and
- the at-a-glance companion uses the same 12--14 passage for the unchanged
  initiation table it shares with the treatise.

Three rows preserve honest catalog ceilings. The sacramental treatise lists
articles 2--6 and 12--18 as broader bibliography ranges, while the council
article uses work-level title, genre, date, and subject metadata in its
sixteen-document inventory. Neither kind of row claims inspection of the
complete Decree.

The Nuptial Mass is excluded: thematic relevance to Eastern matrimonial
discipline is not a demonstrated source dependency. No consumer inherits the
distinct vacatio notice, the Latin web response, or the complete English or
Latin *Acta* bodies simply because those witnesses are now reusable.

## Reverse use and mutation proof

The unmodified graph validates. Sixteen isolated copies of the actual source
tree then received valid metadata-only mutations:

| Mutated node | Stale fingerprints | Publications | Unexpected diagnostics |
| --- | ---: | ---: | ---: |
| English *Orientalium Ecclesiarum* artifact | 4 | 3 | 0 |
| English articles 1--30 passage | 0 | 0 | 0 |
| English articles 2--6 passage | 0 | 0 | 0 |
| English article 6 passage | 1 | 1 | 0 |
| English articles 12--14 passage | 2 | 2 | 0 |
| English articles 12--18 passage | 0 | 0 | 0 |
| English article 17 passage | 1 | 1 | 0 |
| Latin web artifact | 0 | 0 | 0 |
| *Orientalium Ecclesiarum* work | 4 | 3 | 0 |
| Latin AAS articles 1--30 passage | 0 | 0 | 0 |
| Latin AAS constituent segment | 0 | 0 | 0 |
| Vacatio-notice work | 0 | 0 | 0 |
| Vacatio-notice web edition | 0 | 0 | 0 |
| Vacatio-notice AAS segment | 0 | 0 | 0 |
| Vacatio-notice AAS complete passage | 0 | 0 | 0 |
| Existing AAS 57 container artifact | 4 | 2 | 0 |

Passage mutations invalidate only their exact verified consumers. The English
artifact reaches four rows across the celibacy article and two sacramental
publications, while catalog-only rows do not stale. The work mutation reaches
all four verified rows across three publications. Mutating the complete
bodies, bibliography-only ranges, Latin web artifact, or unconsumed notice
reaches no publication, proving that expansive central availability does not
falsely become publication use.

The shared AAS 57 mutation reaches exactly four pre-existing rows across two
publications: the council article's three separate *Lumen gentium* apparatus
constituents and the Ninth Sunday guide's *Lumen gentium* witness. Those rows
were explicitly re-reviewed and repinned after the AAS artifact note changed.
This proves real container reuse and propagation without conflating any
constituent with the gazette or with another act.

## Textual corrections and acceptance results

The proof produced three reader-facing source calibrations:

- the clerical-celibacy article now attributes preservation of Eastern rite
  and way of life to article 6 while reserving explicit honor for married
  presbyters to *Presbyterorum ordinis* 16;
- its permanent-diaconate discussion now states article 17's exact desire and
  narrower legislative clause, without turning CCEO 760's universal capacity
  into evidence of local implementation; and
- the sacramental reference now distinguishes current CCEO common law,
  conciliar confirmation and restoration, and the 1996 Instruction's
  authoritative liturgical application.

Settled builds produced a 31-page clerical-celibacy article with SHA-256
`de073a0ab275159cfe4065105c432781b2d9bcb33c5394a22dfe103c3908561d`,
a 71-page sacramental treatise with SHA-256
`d97fdea5bad97eab4cb4e85e6fc7c267454b24652ef8cc941bceeb71009ede5a`,
and a 10-page at-a-glance companion with SHA-256
`a092436881584f3693d8d4a19f5a29ffd62fef59701ee5a56ed601d9f0f3052f`.
The final logs, structures, metadata, embedded-font and Unicode-map checks,
text extraction, and build/install identity gates passed. Review rasters were
generated through `scripts/pdf-review`, and every rendered page was visually
inspected. That review caught and corrected a pre-existing rights-only final
page in the treatise; the four distinct generation records and compact rights
colophon now share a readable terminal metadata page. No prior exact-byte
release clearance attaches to the changed PDFs.

The completed source graph contains 55 artifacts, 4 corpora, 60 editions, 153
passages, 24 segments, 31 works, and 499 bindings. The family ledger assigns
the Decree and notice identities to `family.vatican-ii.acts` while reusing the
already canonical AAS 57 artifact owned by `family.acta.aas-ass`. Remaining
conciliar acts and the separate complete sixteen-document search corpus stay
open for later proofs. These are internal source and production checks, not
external specialist or ecclesiastical approval.
