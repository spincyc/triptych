# Lumen Gentium and AAS 57 Reuse Review

Reviewed on 2026-07-23.

This record documents the completed bounded normalization of *Lumen gentium*
within `family.vatican-ii.acts` and the volume 57 component of
`family.acta.aas-ass`. It identifies complete official witnesses for expansive
later examination, keeps the Constitution and its appended interpretive
apparatus distinct, binds current publications at the loci they actually use,
and tests cross-publication change propagation. The canonical source records
and publication-local bindings remain the machine-enforced identities and
evidence states.

## Work, container, editions, and exact artifacts

The model preserves several identities that a flat Vatican II bibliography
would collapse:

- *Acta Apostolicae Sedis* is the official-gazette series, with volume 57
  (1965) as the container edition;
- *Lumen gentium* is the separately promulgated dogmatic constitution;
- the `Notificationes` delivered by the Council's Secretary General at the
  123rd General Congregation on 16 November 1964 are a separate work;
- at this proof checkpoint, the Doctrinal Commission declaration of 6 March
  1964 was represented as a reusable subpassage within those
  `Notificationes`; the later *Dei Verbum* and AAS 58 proof promotes it to a
  separate work with distinct AAS 57 and AAS 58 reproduction witnesses; and
- the four-part *Nota explicativa praevia* is another separately titled work
  following the `Notificationes`.

Three exact official artifacts control the normalized records:

| Artifact | Extent | SHA-256 |
| --- | ---: | --- |
| Holy See English HTML response | 204,163 bytes | `579d2ef71c6e03321131739409d7db26aeea8c118da8e466ba0deb6c333980ef` |
| Holy See Latin HTML response | 192,411 bytes | `0a828abb4be1de13b600bbc9bbae32832ed5ce4dad940629f57aae54c679fe23` |
| Holy See AAS 57 OCR PDF | 1,094 pages; 4,983,675 bytes | `bd6d813da15fd67d4e227de8e9a12660359192c65d580cd785c8dcbddd8cd94f` |

The English archive, press, and content-delivery routes returned the same
204,163-byte response and therefore share one artifact identity rather than
three duplicate records. Both web responses contain the complete Constitution,
subscriptions, notes, `Notificationes`, and preliminary explanatory note. The
AAS constituent occupies printed and artifact pp. 5--71; its numbered
paragraphs 1--69 occupy pp. 5--67. The `Notificationes` occupy the bounded
constituent on p. 72, and the *Nota explicativa praevia* begins partway down
p. 72 and ends with its signature block on p. 75.

The Vatican portal rights review did not establish repository redistribution
permission. The three artifacts are therefore exact restricted identities and
are not retained as tracked payloads. The AAS OCR layer remains a locating aid,
not an independently authoritative transcription.

## Expansive availability and bounded examination

The complete English and Latin web states, the full Latin AAS constituent, and
the complete numbered Latin text are centrally identifiable for future
work-wide examination. Their presence deliberately does not claim that every
consumer searched, read, or verified the whole Constitution.

Current high-reuse English passage records cover paragraphs 10--11, 52--69,
53, 56, and 60--62. Paragraphs 53 and 56 support exact Mariological loci;
60--62 supports the recurring claim about Christ's unique mediation and Mary's
received, subordinate maternal role; and 10--11 supports claims concerning the
common and ministerial priesthood. The complete chapter VIII passage remains
available for broader discovery without substituting for those narrower
records.

Seven Mariology bibliographies retain chapter VIII, paragraphs 52--69, only as
a cataloged broad lead. Their exact audited claims bind narrower verified
passages separately. This makes a larger source available without upgrading a
whole-chapter citation into a whole-chapter inspection claim.

## Consumer integration and trace calibration

Twenty-three direct consumers and one inherited sacramental companion now
reuse the normalized work. They comprise three articles, two biographies, two
novenas, five liturgical studies, ten Mariology publications, the sacramental
treatise, and its at-a-glance companion. Every direct textual occurrence found
in the audit has a publication-local binding; the at-a-glance companion
records its shared-fragment dependency explicitly.

The audit also preserved meaningful exclusions:

- FSSP and SSPX research records that merely report another source's
  *Lumen gentium* reference are not treated as Constitution consumers;
- the heresies reference list no longer carries an unused *Lumen gentium*
  entry, while its actually used *Dei Verbum*, *Gaudium et spes*, and
  *Unitatis redintegratio* entries remain;
- the Ascension daily-prayer companion contains no independent
  *Lumen gentium* claim; and
- the complete chapter VIII passage has no false publication-level
  `verified` use.

Comparison of the local traces with the official witnesses corrected or
clarified eight records:

- the council article now distinguishes the 16 November Secretary General
  `Notificationes` from the embedded 6 March Doctrinal Commission
  declaration, adds paragraph 16, and uses the canonical Holy See URL;
- the Ninth-after-Pentecost guide says paragraph 3 clearly reuses the Secret's
  wording without an explicit source note, while *Sacrosanctum Concilium* 2
  and *Presbyterorum ordinis* 13 explicitly identify that Secret;
- the Ascension novena narrows its *Lumen gentium* reference to paragraphs 4
  and 60--62;
- the 1962 Ordinary audit records its paragraph 60--62 use;
- *Two Missals, One Sacrifice* narrows its citation to paragraph 10;
- the Marian-dogmas audit records its paragraph 8 use;
- the sacramental scope distinguishes exact uses of paragraphs 10, 20--22,
  and 26 and a shared summary of 18--29 from its broader bibliography; and
- the unused heresies citation is removed rather than given a decorative
  source binding.

## Reverse use, impact, and mutation proof

Reverse-use inspection reports 59 binding rows across 24 publications for the
work. Work-level impact reports 71 rows: the same publication fan-out plus 12
dependent source records. More narrowly:

| Source node | Binding rows | Publications |
| --- | ---: | ---: |
| English official HTML artifact and descendants | 50 | 23 |
| AAS 57 PDF artifact and descendants | 4 | 2 |
| English paragraphs 60--62 | 12 | 12 |

Three isolated copies of the source tree tested dependency staleness with
valid metadata-only mutations:

- changing the English HTML artifact invalidated exactly 50 fingerprints
  across 23 publications;
- changing the AAS 57 artifact invalidated exactly 4 fingerprints across 2
  publications; and
- changing the paragraphs 60--62 passage invalidated exactly 12 fingerprints
  across 12 publications.

Each mutated tree failed only on the expected fingerprint requirements. The
unmodified graph validates.

## Publication and acceptance results

Five PDFs changed because the trace corrections or rendered references affect
their publication text. Settled builds, repository-generated page rasters, and
contact sheets were reviewed. The first pass found an orphaned references
heading and three metadata spill pages; the corrected builds keep the Ninth
heading with its first entry, leave an 11.45-point measured footer clearance,
flow the Ascension appendix without a sparse carryover, and keep terminal
metadata on the preceding page in the two long studies. Every page was
covered by the full-document review or a targeted post-fix recheck.

| Publication | Pages | Installed PDF SHA-256 |
| --- | ---: | --- |
| *The Council, the Missal, and the Crisis* | 51 | `dbb98ad4cf3a1e7de76cd8f4444c8ab1c350575cd77bd54e5b0b240dd423c41d` |
| *The First Novena: From Ascension to Pentecost* | 27 | `5a5329d2257333a189f42a39e2c124a556f44d3d28eba3cd80ca2a70ddde3798` |
| *Ninth Sunday after Pentecost* | 10 | `51f0c3f28274e65bca18792193ded6dd5f10e9e200988b44412b5d29a2f152b9` |
| *Two Missals, One Sacrifice* | 46 | `5ba86c4734a874fe0a7117bc0f350c667974895c1b63504a1bbfd0f5ed97ba05` |
| *Heresies in Catholic History* | 81 | `51001351b72a54fe00e93abc061bbc51009757023b681746504699859b64f35a` |

The five changed publications account for 215 reviewed pages. The 11-page
Ascension daily-prayer companion was also rebuilt and reviewed because the
build graph checks its inherited metadata dependency; it remained
byte-identical to the installed PDF, so no sixth publication revision is
claimed.

The final graph validates with 41 artifacts, 4 corpora, 34 editions, 87
passages, 13 segments, 21 works, and 382 bindings. `make check-sources` passes;
the source-library, inventory, and family-migration suites pass all 85 tests.
The refreshed family ledger assigns the AAS 57 container to its two actual
publication owners and the Vatican II family to the audited consumers while
leaving other conciliar acts and AAS volumes explicitly pending. Each changed
installed PDF is byte-identical to its reviewed build. These are internal
source and production checks, not external specialist or ecclesiastical
approval, and no release clearance is claimed.
