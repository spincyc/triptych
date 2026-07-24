# *Nostra Aetate* and AAS 58 Reuse Review

Reviewed on 2026-07-24.

This record documents the bounded normalization of *Nostra aetate* within
`family.vatican-ii.acts` and its reuse of the volume 58 component of
`family.acta.aas-ass`. It makes complete official witnesses centrally
identifiable for later expansive examination, binds current publications only
at the loci they actually use, and proves cross-publication propagation by
mutating run-local copies of the real source graph. The canonical manifests
and publication-local bindings remain the machine-enforced records.

## Identity boundaries

The graph distinguishes the Declaration, its expressions, and its
official-gazette container:

- *Nostra aetate* is one intellectual work, solemnly promulgated on 28 October
  1965 and comprising numbered articles 1--5;
- the dated English and Latin Vatican web states are separate editions and
  exact HTML artifacts;
- the Latin constituent printed in *Acta Apostolicae Sedis* 58 (1966) is a
  separate edition represented as one segment of the existing exact volume
  artifact; and
- *Acta Apostolicae Sedis* volume 58 remains an official-gazette container
  containing many distinct acts, not another identity for the Declaration.

The English delivery contains the complete numbered body and notes but omits
the promulgation and subscription material. The Latin web delivery continues
after the Declaration's body, promulgation formula, date, and Paul VI
subscription with separately bounded material headed *Vacatio legis* and an
incomplete shared subscription block. Those appendices are not part of the
Declaration's numbered-body passage.

## Exact artifacts, extent, and rights

Three exact Holy See artifacts control the normalized records:

| Artifact | Extent | SHA-256 |
| --- | ---: | --- |
| English *Nostra aetate* HTML response | 17,231 bytes | `c730506f26d197c6150b41d521cc16c015c21afdbd7ac60c30254a2ed39c3069` |
| Latin *Nostra aetate* HTML response | 23,616 bytes | `1c8cae6653f213d2585f0839b48260431dfa6a6f62024a4b4cc90988b177b6b4` |
| Holy See AAS 58 OCR PDF | 1,279 pages; 5,944,403 bytes | `69c27224cde7f27547e18c544f5b99064793ada9509ebc902b20fa548e15bac8` |

The English response was byte-identical across the checked `www`, `press`,
and `content/dam` hosts. It contains articles 1--5 and notes 1--15. Known
delivery defects include “all- powerful,” “Christ-Abraham's sons according to
faith (6)-are,” “Gentiles. making,” “calls He issues-such,” and note 5's
presentation of Gregory VII's *Epistola* III.21 as “letter XXI” with an
imprecise *Patrologia Latina* citation. These are recorded artifact defects,
not silently repaired source text.

The Latin response was byte-identical on the checked `www` and `content/dam`
hosts; the corresponding `press` route returned no witness. Its known local
defects include “Genti” for “Gentium,” “Gregorios” for “Gregorius,” and
“TOKI”/“TOKIC” corruption. The web edition boundary excludes the appended
material described above.

In the exact *Acta* artifact, the Declaration occupies printed pp. 740--744.
Printed p. 739 ends *Gravissimum educationis*, while p. 745 opens a new issue
and *Christi Matri*. Page 744 contains article 5 and the promulgation formula,
then points to the common council subscriptions on pp. 696--701. Those shared
pages are not absorbed into the Declaration's constituent segment. The OCR is
a locating aid rather than an independently authoritative transcription.

The Vatican portal's legal notice did not establish repository redistribution
permission. The HTML and PDF artifacts are therefore `restricted`,
nonretained, and nonindexable. The repository stores exact hashes, byte or
page extent, provenance, boundaries, and dependency records, but not their
payloads.

## Expansive availability and bounded use

The complete dated English and Latin web states and complete Latin *Acta*
constituent are centrally identifiable for later work-wide examination. That
availability does not imply that every consumer inspected or relied on the
whole Declaration.

The reusable English passage records cover articles 1--5, 2, 4, and 5. The
narrower records govern the current claims about truth and holiness in other
religions, the Jewish people and antisemitism, and discrimination in general.
The complete English and *Acta* body records remain available without a
verified publication consumer. The Latin web state is likewise cataloged as a
complete witness without manufacturing a publication-level claim of direct
use.

## Source-of-source non-inheritance

The Declaration's notes expose Scripture, another conciliar document, and a
papal letter as leads. A publication using one Declaration article does not
thereby become a direct consumer of every work named in that article or its
notes. Likewise:

- article 2's note does not make a consumer a direct user of
  2 Corinthians 5:18--19;
- article 4 does not make a consumer a direct user of every scriptural locus
  or Pauline passage supporting its account of the Church's bond with the
  Jewish people;
- article 5's appeal to human dignity does not itself establish every
  theological, moral, civil, or canonical rule concerning discrimination; and
- the Latin web appendices and AAS common-subscription pages are not inherited
  merely because a publication cites *Nostra aetate*.

This preserves first-class source discovery while preventing the graph from
claiming inspection or evidentiary dependence that did not occur.

## Reviewed consumers and exclusions

Six binding rows across two publications now share the normalized identities.
Five are fingerprinted verified uses:

- the council article uses English article 2 for the Declaration's
  interreligious teaching, article 4 for its rejection of collective Jewish
  guilt and antisemitism, and article 5 for its general rejection of
  discrimination; and
- the Aquinas biography uses articles 4 and 5 to distinguish the Church's
  present teaching about the Jewish people from its general condemnation of
  discrimination.

The sixth row is the council article's work-level catalog binding for title,
genre, promulgation date, and subject in its sixteen-document inventory. It
does not claim inspection of the complete body.

No consumer inherits the complete English or Latin bodies, the Latin web
artifact or appendices, the Latin AAS constituent, the common council
subscriptions, or the Declaration's source-of-source notes merely because
those witnesses are now reusable.

## Reverse use and mutation proof

The unmodified graph validates. Ten isolated copies of the actual source tree
then received valid metadata-only mutations:

| Mutated node | Stale fingerprints | Publications | Unexpected diagnostics |
| --- | ---: | ---: | ---: |
| English *Nostra aetate* artifact | 5 | 2 | 0 |
| English articles 1--5 passage | 0 | 0 | 0 |
| English article 2 passage | 1 | 1 | 0 |
| English article 4 passage | 2 | 2 | 0 |
| English article 5 passage | 2 | 2 | 0 |
| Latin web artifact | 0 | 0 | 0 |
| *Nostra aetate* work | 5 | 2 | 0 |
| Latin AAS articles 1--5 passage | 0 | 0 | 0 |
| Latin AAS constituent segment | 0 | 0 | 0 |
| Existing AAS 58 container artifact | 2 | 2 | 0 |

Passage mutations invalidate only their exact verified consumers. Article 2
reaches only the council article; articles 4 and 5 each reach the council
article and Aquinas biography. The English artifact and work each reach all
five verified rows across both publications, while the complete bodies and
Latin witnesses reach none. Central completeness therefore remains distinct
from publication use.

The shared AAS 58 mutation reaches exactly two pre-existing rows across two
other publications: the Ninth Sunday after Pentecost guide's
*Presbyterorum ordinis* article 13 witness and the La Salette study's Index
notification witness. Those rows were explicitly re-reviewed and repinned
after the AAS artifact note changed. This proves real container reuse and
propagation without conflating any constituent with the gazette or with
another act.

## Textual corrections and acceptance state

The proof produced two reader-facing source calibrations:

- the council article now distinguishes article 2's recognition of what is
  true and holy in other religions, article 4's teaching about Jewish
  collective guilt and antisemitism, and article 5's general condemnation of
  discrimination; and
- the Aquinas biography now grounds its account of present Catholic teaching
  about the Jewish people in article 4 and its broader discrimination
  boundary in article 5, rather than treating either article as a substitute
  for the other.

Settled technical builds produced a 51-page council article with SHA-256
`36c88276e5b887b4272c35c2755c2a40f5ba8e450ef669b1b009917c74a46b9f`
and a 22-page Aquinas biography with SHA-256
`05d1b1b792c5774e0aa10822e9722d3a844e442a09c54e5573bd5913fa2c275a`.
The final logs contained no fatal errors, undefined references, overfull or
underfull boxes, unresolved rerun requests, or layout warnings. Generation
metadata, PDF structure and metadata, Letter page size, embedded and subsetted
fonts with Unicode maps, and nonempty text extraction passed. Review rasters
were generated through `scripts/pdf-review`, and every physical page of both
publications was visually inspected. Full-size checks covered the revised
conciliar claims, Aquinas's reception section, references, dense pages, and
terminal metadata. The two reviewed builds were installed at their mirrored
`doc/` paths and verified byte-identical. No prior exact-byte release
clearance attaches to these changed bytes.

The completed source graph contains 59 artifacts, 4 corpora, 66 editions, 164
passages, 26 segments, 33 works, and 514 bindings. The family ledger assigns
the Declaration's identities to `family.vatican-ii.acts` while reusing the
already canonical AAS 58 artifact owned by `family.acta.aas-ass`. Remaining
conciliar acts and the separate complete sixteen-document search corpus stay
open for later proofs. These are internal source and production checks, not
external specialist or ecclesiastical approval.
