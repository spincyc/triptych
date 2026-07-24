# *Ad Gentes* and AAS 58 Reuse Review

Reviewed on 2026-07-24.

This record documents the bounded normalization of *Ad gentes* within
`family.vatican-ii.acts` and its reuse of the volume 58 component of
`family.acta.aas-ass`. It makes complete official witnesses centrally
identifiable for later expansive examination, binds current publications only
at the loci they actually use, and proves cross-publication propagation by
mutating run-local copies of the real source graph. The canonical manifests
and publication-local bindings remain the machine-enforced records.

## Identity boundaries

The graph distinguishes the Decree, its expressions, and its official-gazette
container:

- *Ad gentes* is one intellectual work, solemnly promulgated on 7 December
  1965 and comprising numbered articles 1--42;
- the dated English and Latin Vatican web states are separate editions and
  exact HTML artifacts;
- the Latin constituent printed in *Acta Apostolicae Sedis* 58 (1966) is a
  separate edition represented as one segment of the existing exact volume
  artifact; and
- *Acta Apostolicae Sedis* volume 58 remains an official-gazette container
  containing many distinct acts, not another identity for the Decree.

The English delivery contains the complete preface, numbered body, six
chapters, conclusion, and chapter-separated notes, but no promulgation or
subscription material. The Latin web delivery continues after the numbered
body with a duplicated promulgation formula, date, Paul VI subscription, and
an incomplete shared subscription block ending with Cardinal Callori di
Vignale. That appended apparatus is not part of the numbered-body passage.

## Exact artifacts, extent, and rights

Three exact Holy See artifacts control the normalized records:

| Artifact | Extent | SHA-256 |
| --- | ---: | --- |
| English *Ad gentes* HTML response | 122,003 bytes | `1ab5c4fea2ab2a5864bd81e60b0524b8ad447c08e3d22ae483b84819aaef5387` |
| Latin *Ad gentes* HTML response | 156,429 bytes | `e2a7e4b201176422045e122ad33b98e471e870b5b1d2ae2131a094e8aed94539` |
| Holy See AAS 58 OCR PDF | 1,279 pages; 5,944,403 bytes | `69c27224cde7f27547e18c544f5b99064793ada9509ebc902b20fa548e15bac8` |

The English response was byte-identical on the checked `www` and
`content/dam` routes; the corresponding `press` route returned no witness.
Known delivery defects include article 1's unclosed quotation and “overseer:
of the ages”; article 2's “His life and His cry” where the Latin has *vita et
gloria*; article 4's “Acts of the Apostles took again,” omitted note marker 9,
and malformed “a giving life, soul-like”; article 5's “disciples of a
nations”; article 7's “1 Tim. 2:45”; recurrent *Lumen gentium* labels pointing
to *Dei Verbum*; recurrent *Rerum Ecclesiae* labels pointing to *Ex corde
Ecclesiae*; and note 24's corruption of Augustine, *De civitate Dei* 19.17 as
“St. Augustine 7, City of God, 1917.” These are recorded artifact defects, not
silently repaired source text.

The Latin response was byte-identical on the checked `www` and `content/dam`
routes; the corresponding `press` route returned no witness. Its known local
defects include article 41's “sunti illi laici,” note 102's AAS 51 (1919) for
1959, note 135's *Princeps Pastorum* link mislabeled *Lumen gentium*, and note
165's AAS 28 (1926) for volume 18. The web edition's numbered-body boundary
excludes the appended apparatus described above.

In the exact *Acta* artifact, the Decree occupies printed and artifact PDF
pp. 947--990. Printed p. 946 ends the *Dignitatis humanae* subscription
apparatus, while p. 991 begins *Presbyterorum ordinis*. Page 990 contains
article 42, the promulgation formula and date, Paul VI's subscription, a
pointer to the common council subscriptions on pp. 941--946, and an editorial
asterisk citing Paul VI's distinct *Munus Apostolicum*. The referenced
subscriptions and motu proprio are not absorbed into the Decree's constituent
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
availability does not imply that every consumer inspected or relied on the
whole Decree.

The reusable English passage records cover articles 1--42, 2, 4, and 7. The
narrower records govern the current claims about the Church's missionary
nature, Pentecost's ecclesial and missionary dimensions, and the continuing
necessity of mission alongside the inculpable-ignorance qualification. The
complete English and *Acta* body records remain available without a verified
publication consumer. The Latin web state is likewise cataloged as a complete
witness without manufacturing a publication-level claim of direct use.

## Source-of-source non-inheritance

The Decree's notes expose Scripture, other conciliar acts, papal acts,
patristic texts, and modern studies as leads. A publication using one Decree
article does not thereby become a direct consumer of every work named in that
article or its notes. In particular:

- article 2 does not make a consumer a direct user of every Trinitarian,
  biblical, or patristic source behind the Decree's account of mission;
- article 4 does not make the Pentecost novena a direct user of every Acts,
  Pauline, *Lumen gentium*, or papal locus cited in the article or its notes;
- article 7 does not independently verify its malformed “1 Tim. 2:45” delivery
  or make the council article a direct consumer of that scriptural locus;
- note 24's corrupted *City of God* reference remains only a lead and does not
  create a use of Augustine or inherit the repository's normalized
  *De civitate Dei* corpus; and
- the Latin web appendices, AAS common-subscription pages, and separately
  cited *Munus Apostolicum* are not inherited merely because a publication
  cites *Ad gentes*.

This preserves first-class source discovery while preventing the graph from
claiming inspection or evidentiary dependence that did not occur.

## Reviewed consumers and exclusions

Four binding rows across two publications now share the normalized identities.
Three are fingerprinted verified uses:

- the council article uses English article 2 for the Church's missionary
  nature and article 7 for mission's continuing necessity alongside its
  inculpable-ignorance qualification; and
- the Ascension-to-Pentecost novena uses English article 4 for its bounded
  synthesis of Pentecost's public manifestation of the Church, the Gospel's
  spread among the nations, the Spirit's hierarchical and charismatic gifts,
  ecclesial unity, and missionary impulse.

The fourth row is the council article's work-level catalog binding for title,
genre, promulgation date, and subject in its sixteen-document inventory. It
does not claim inspection of the complete body.

No consumer inherits the complete English or Latin bodies, either Latin or
English artifact as an undifferentiated source, the Latin AAS constituent,
the common council subscriptions, *Munus Apostolicum*, or the Decree's
source-of-source notes merely because those witnesses are now reusable.

## Reverse use and mutation proof

The unmodified graph validates. Fourteen isolated copies of the actual source
tree then received valid metadata-only mutations:

| Mutated node | Stale fingerprints | Publications | Unexpected diagnostics |
| --- | ---: | ---: | ---: |
| *Ad gentes* work | 3 | 2 | 0 |
| English edition | 3 | 2 | 0 |
| English artifact | 3 | 2 | 0 |
| English articles 1--42 passage | 0 | 0 | 0 |
| English article 2 passage | 1 | 1 | 0 |
| English article 4 passage | 1 | 1 | 0 |
| English article 7 passage | 1 | 1 | 0 |
| Latin web edition | 0 | 0 | 0 |
| Latin web artifact | 0 | 0 | 0 |
| Latin web articles 1--42 passage | 0 | 0 | 0 |
| Latin AAS edition | 0 | 0 | 0 |
| Latin AAS articles 1--42 passage | 0 | 0 | 0 |
| Latin AAS constituent segment | 0 | 0 | 0 |
| Existing AAS 58 container artifact | 2 | 2 | 0 |

Passage mutations invalidate only their exact verified consumers: article 2
and article 7 each reach only the council article, while article 4 reaches
only the novena. The English artifact, edition, and work each reach all three
verified rows across both publications, while the complete bodies and Latin
witnesses reach none. Central completeness therefore remains distinct from
publication use.

The shared AAS 58 mutation reaches exactly two pre-existing rows across two
other publications: the Ninth Sunday after Pentecost guide's
*Presbyterorum ordinis* article 13 witness and the La Salette study's Index
notification witness. Those rows were explicitly re-reviewed and repinned
after the AAS artifact note changed. This proves real container reuse and
propagation without conflating any constituent with the gazette or with
another act.

## Textual corrections and acceptance state

The proof produced two reader-facing source calibrations:

- the council article now keeps article 7's missionary necessity beside its
  qualification concerning those inculpably ignorant of the Gospel and uses
  article 2, rather than an undifferentiated citation to the Decree, for the
  Church's missionary nature; and
- the novena now links article 4 directly and limits that article to its
  Pentecostal, ecclesial, and missionary synthesis rather than using it for
  the Spirit's divinity, procession, or the whole doctrine of sanctification.

Settled technical builds produced a 51-page council article with SHA-256
`922fab6dd188581ddfa8be7abde244ea13697d503d4d68feea59a26874f7268c`,
a 27-page full novena with SHA-256
`73e11c6ad7f64c16ab813ac095c746f42f0c44ae252e2bd51829b2a3b26fca51`,
and an unchanged 11-page daily-prayer companion with SHA-256
`675ae37d807d9ff0fadf4c1d5951480018f0ed6b56773b56493fd9b9c363c1ce`.
The final logs contained no fatal errors, undefined references, overfull or
underfull boxes, unresolved rerun requests, or layout warnings. Generation
metadata, PDF structure and metadata, Letter page size, embedded and subsetted
fonts with Unicode maps, and nonempty text extraction passed. The companion
remains byte-identical to its installed PDF, and the changed source set does
not touch any canonical prayer fragment. Review rasters were generated through
`scripts/pdf-review`, and every physical page of all three publications was
visually inspected. Full-size checks covered the revised conciliar claim,
both changed reference pages, terminal metadata and rights matter, and the
companion's status page. The two changed builds were installed at their
mirrored `doc/` paths and verified byte-identical; the companion remained
byte-identical throughout. No prior exact-byte distribution clearance
attaches to the changed council article or full novena.

The validated source graph contains 61 artifacts, 4 corpora, 69 editions, 170
passages, 27 segments, 34 works, and 518 bindings. The family ledger assigns
the Decree's identities to `family.vatican-ii.acts` while reusing the already
canonical AAS 58 artifact owned by `family.acta.aas-ass`. Remaining conciliar
acts and the separate complete sixteen-document search corpus stay open for
later proofs. These are internal source and production checks, not external
specialist or ecclesiastical approval.
