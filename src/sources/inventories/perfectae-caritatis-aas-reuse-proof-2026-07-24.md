# *Perfectae Caritatis* and AAS 58 Reuse Review

Reviewed on 2026-07-24.

This record documents the bounded normalization of *Perfectae caritatis*
within `family.vatican-ii.acts` and its reuse of the volume 58 component of
`family.acta.aas-ass`. It makes complete official witnesses centrally
identifiable for later expansive examination, binds the present publication
only at the loci it actually uses, and proves propagation by mutating
run-local copies of the real source graph. The canonical manifests and
publication-local bindings remain the machine-enforced records.

## Identity boundaries

The graph distinguishes the Decree, its expressions, and its
official-gazette container:

- *Perfectae caritatis* is one intellectual work, solemnly promulgated on
  28 October 1965 and comprising numbered articles 1--25;
- the dated English and Latin Vatican web states are separate editions and
  exact HTML artifacts;
- the Latin constituent printed in *Acta Apostolicae Sedis* 58 (1966) is a
  separate edition represented as one segment of the existing exact volume
  artifact; and
- *Acta Apostolicae Sedis* volume 58 remains an official-gazette container
  containing many distinct acts, not another identity for the Decree.

The English delivery contains the complete numbered body and its sole source
note. Its visible heading identifies Paul VI and the date of proclamation,
but the response omits the promulgation formula, date and subscription line,
conciliar subscriptions, and notarial attestations.

The Latin web delivery continues after the numbered body with the promulgation
formula, date, Paul VI subscription, and a common subscription block ending at
Alexander TOKI. That block omits the later signatories on *Acta* p. 701, the
continuation notice, and the official attestations. The appendix is not part
of the bounded articles 1--25.

## Exact artifacts, extent, and rights

Three exact Holy See artifacts control the normalized records:

| Artifact | Extent | SHA-256 |
| --- | ---: | --- |
| English *Perfectae caritatis* HTML response | 36,410 bytes | `6dd0dbb8aa07acdeb82bde4bb34be72de67cecef7e132e3300c839ffa00a0654` |
| Latin *Perfectae caritatis* HTML response | 40,389 bytes | `83ab4ab6d80b45939697bd0d5ca638e06a42fc7b72fa21a61a9db7bde8ecfbac` |
| Holy See AAS 58 OCR PDF | 1,279 pages; 5,944,403 bytes | `69c27224cde7f27547e18c544f5b99064793ada9509ebc902b20fa548e15bac8` |

The English response was byte-identical on the checked `www`, `press`, and
`content/dam` routes. Known delivery defects include article 1's
“ministry-the building”; article 2's malformed list marker “e )”; article 11's
missing punctuation after “not Religious institutes” and “everywhere in and”;
article 13's missing separator between Matthew 25:34--46 and James 2:15--16;
article 15's “cf.Rom.” and “to-the diversity”; and article 19's “have recently
established,” with “been” omitted. These are recorded artifact defects, not
silently repaired source text.

The Latin response was byte-identical on the checked `www` and `content/dam`
routes; the corresponding `press` route returned no witness. Known delivery
defects include article 7's “Ecclesia e decus”; article 15's “Rom. 57, 5” for
Romans 5:5 and “Io. 13 35”; “ALEXANDER TOKI” for TOKIC; and missing terminal
punctuation after Cardinal MORANO. The web edition's numbered-body boundary
excludes the appended promulgation and subscription apparatus.

In the exact *Acta* artifact, the Decree occupies printed and artifact PDF
pp. 702--712. Printed p. 701 finishes the common subscriptions and official
attestations for the acts promulgated on 28 October; p. 702 begins the Decree
and article 1; p. 712 contains article 25, the promulgation formula and date,
Paul VI's subscription, a reference to the common subscriptions on
pp. 696--701, and the sole Ambrose note; and p. 713 begins *Optatam totius*.
The shared subscription pages are not absorbed into the Decree's constituent
segment. The OCR is a locating aid rather than an independently authoritative
transcription.

The Vatican portal's legal notice did not establish repository redistribution
permission. The HTML and PDF artifacts are therefore `restricted`,
nonretained, and nonindexable. The repository stores exact hashes, byte or
page extent, provenance, boundaries, and dependency records, but not their
payloads.

## Expansive availability and bounded use

The complete dated English and Latin web states and complete Latin *Acta*
constituent are centrally identifiable for later work-wide examination. That
availability does not imply that a publication inspected or relied on every
article.

The reusable English records separate the complete articles 1--25 from five
presently used semantic units:

- article 2 controls the return-to-sources, adaptation, and prior spiritual
  renewal principles;
- articles 3--4 control the authorized breadth and governance of revision;
- articles 5--6 control special consecration and the foundations of prayer;
- articles 12--15 control chastity, poverty, obedience, and common life; and
- article 17 controls both the habit as an outward mark and the requirement
  to change unsuitable habits.

The complete English, Latin web, and Latin *Acta* body records remain
available without a verified complete-body consumer.

## Source-of-source non-inheritance

The Decree's text and sole note expose Scripture, other conciliar teaching,
and Ambrose as research leads. A publication using one numbered range does
not thereby become a direct consumer of every work named there.

Likewise, normalization of *Perfectae caritatis* does not verify or inherit
Paul VI's distinct *Ecclesiae Sanctae*, institute chapter records, apostolic
visitation findings, CARA or NRVC data, histories of particular institutes,
or the publication's causal judgments about institutional contraction. The
Latin web appendix and common *Acta* subscription pages are not inherited
merely because a publication cites the Decree.

## Reviewed consumer and exclusions

Six binding rows in `articles/faith/council-missal-and-crisis` now share the
normalized identities. Five are fingerprinted verified uses of the exact
English groups above. The sixth is a work-level catalog binding for title,
decree genre, promulgation date, and subject in the sixteen-document
inventory; it does not claim inspection of the complete body.

The passage bindings control the publication's account of renewal principles,
authorized revision, and constitutive elements retained within adaptation.
They do not assign the Decree's authority to later implementation measures,
particular institute decisions, empirical trends, or causal conclusions.

No consumer inherits the complete English or Latin bodies, either HTML
artifact as an undifferentiated source, the Latin *Acta* constituent, the
common subscriptions, *Ecclesiae Sanctae*, or the Decree's source-of-source
leads merely because those witnesses are now reusable.

## Reverse use and mutation proof

The unmodified graph validates. Sixteen isolated copies of the actual source
tree then received valid metadata-only mutations:

| Mutated node | Stale fingerprints | Publications | Unexpected diagnostics |
| --- | ---: | ---: | ---: |
| *Perfectae caritatis* work | 5 | 1 | 0 |
| English edition | 5 | 1 | 0 |
| English artifact | 5 | 1 | 0 |
| English articles 1--25 passage | 0 | 0 | 0 |
| English article 2 passage | 1 | 1 | 0 |
| English articles 3--4 passage | 1 | 1 | 0 |
| English articles 5--6 passage | 1 | 1 | 0 |
| English articles 12--15 passage | 1 | 1 | 0 |
| English article 17 passage | 1 | 1 | 0 |
| Latin web edition | 0 | 0 | 0 |
| Latin web artifact | 0 | 0 | 0 |
| Latin web articles 1--25 passage | 0 | 0 | 0 |
| Latin AAS edition | 0 | 0 | 0 |
| Latin AAS articles 1--25 passage | 0 | 0 | 0 |
| Latin AAS constituent segment | 0 | 0 | 0 |
| Existing AAS 58 container artifact | 2 | 2 | 0 |

Each narrow passage mutation invalidates only its exact verified consumer.
The English artifact, edition, and work each reach all five verified rows in
the one publication, while complete-body and Latin-witness mutations reach
none. Central completeness therefore remains distinct from publication use.

The shared AAS 58 mutation reaches exactly two pre-existing rows in two other
publications: the Ninth Sunday after Pentecost guide's *Presbyterorum
ordinis* article 13 witness and the La Salette study's Index notification
witness. Those rows were explicitly re-reviewed and repinned after the AAS
artifact note changed. This proves real container reuse and propagation
without conflating any constituent with the gazette or with another act.

## Textual corrections and acceptance state

The proof tightens the council article's reader reference from the overbroad
and incomplete “2--4, 6--15, and 17” to the actually controlling “2--6,
12--15, and 17,” adds the direct official link, and retains both sides of the
habit and obedience rules in the prose. Its research audit now distinguishes
the Decree's renewal principles, authorized revision, retained constitutive
elements, and the separate *Ecclesiae Sanctae* implementation evidence.

The validated source graph contains 63 artifacts, 4 corpora, 72 editions,
178 passages, 28 segments, 35 works, and 524 bindings. The family ledger
assigns the Decree's fifteen new identities to `family.vatican-ii.acts` while
reusing the already canonical AAS 58 artifact owned by
`family.acta.aas-ass`. Remaining conciliar acts, *Ecclesiae Sanctae*, and the
separate complete sixteen-document search corpus remain open for later
proofs.

The settled two-pass build produced a 52-page PDF with SHA-256
`c19f3b6aa75c0ebd394f1e6e6b5d30c6ccbf28da6ac96a9251ea54c43e96aebd`.
The final log contained no fatal error, unresolved reference, overflow,
underflow, rerun, or layout warning. Generation metadata, PDF structure and
metadata, Letter page size, embedded/subsetted fonts with Unicode maps, and
nonempty text extraction passed. Review rasters were generated through
`scripts/pdf-review`; every physical page was visually inspected, with the
revised religious-life prose, reference, dense tables, and terminal metadata
and rights matter checked at full size. The reviewed build was installed at
its mirrored `doc/` path and verified byte-identical. No prior exact-byte
distribution clearance attaches to this changed render.
These are internal source and production checks, not external specialist or
ecclesiastical approval.
