# Sacrosanctum Concilium and AAS 56 Reuse Review

Reviewed on 2026-07-23.

This record documents the completed bounded normalization of *Sacrosanctum
Concilium* within `family.vatican-ii.acts` and the volume 56 component of
`family.acta.aas-ass`. It makes complete official witnesses centrally
identifiable for expansive later examination, binds current publications at
the loci they actually use, calibrates broader negative controls, and tests
cross-publication change propagation. The canonical source records and
publication-local bindings remain the machine-enforced identities and evidence
states.

## Work, container, editions, and exact artifacts

The model distinguishes the separately promulgated Constitution from its
official-gazette container and from particular language expressions:

- *Acta Apostolicae Sedis* is the official-gazette series, with volume 56
  (1964) as the container edition;
- *Sacrosanctum Concilium* is the separately promulgated constitution;
- the Latin AAS constituent, dated Latin Holy See web state, and dated English
  Holy See web state are distinct editions; and
- article 2 in the Latin web and AAS editions has separate passage identities
  because the associated note describes the same Missal prayer with different
  editorial wording.

Three exact official artifacts control the normalized records:

| Artifact | Extent | SHA-256 |
| --- | ---: | --- |
| Holy See English HTML response | 91,960 bytes | `3cfc290b5445086fc2be06b47ed6cb86ee3bc3e90bdbb2b5454889dfd76fd96e` |
| Holy See Latin HTML response | 89,918 bytes | `a0e7f540d4e55a04840b799386049542906675b0e505a6959e516ecd34568fb3` |
| Holy See AAS 56 OCR PDF | 1,146 pages; 5,106,458 bytes | `e1f8b49df099a6c9ecabca7f0b9cfb75b7cfec825acbbe6c22ecfdbae2338094` |

The English archive, press, and content-delivery routes returned the same
91,960-byte response. The three Latin routes likewise returned one
89,918-byte response. Each set therefore has one artifact identity rather than
duplicate route-based records.

The AAS audit corrected a commonly repeated abbreviated extent. The complete
*Sacrosanctum Concilium* constituent occupies printed and artifact pp. 97--138,
not merely pp. 97--134. Numbered articles 1--130 occupy pp. 97--133; the
calendar appendix occupies pp. 133--134; promulgation begins on p. 134; and
subscriptions and attestations continue through p. 138. The next work begins
on p. 139. Article 2 and its first note span pp. 97--98. The AAS note identifies
the source as `Secreta dominicae IX post Pentecostem`; the Latin web note calls
it an `oratio super oblata`.

The Vatican portal rights review did not establish repository redistribution
permission. All three artifacts are exact restricted, nonretained identities
and are not tracked as payloads. The AAS OCR layer remains a locating aid, not
an independently authoritative transcription.

## Expansive availability and bounded examination

The complete English and Latin web states, the complete Latin AAS constituent,
the complete numbered Latin text, and the calendar appendix are centrally
identifiable for later work-wide examination. Their presence does not claim
that every consumer searched, read, or verified the whole Constitution.

Twenty English passage records cover the exact or intentionally broad current
uses: articles 5--8, 5--7, 7, 10, 13, 14, 21--23, 26--35, 26--27, 36--40,
47--58, 47--48, 50, 56, 59--82, 59--61, 91, 102--111, 106, and 112--116.
Overlapping broad and narrow nodes are deliberate: a broad discovery or
negative-control scope can remain available while a claim binds the smaller
verified locus.

The sacramental treatise illustrates the distinction. Its directly checked
uses bind articles 5--7, 10, 26--27, and 59--61. Articles 59--82 remain a
cataloged bibliographic lead; articles 62--82 are not silently upgraded to a
verified reading. The council article's complete-text audit is another
deliberately bounded control: it covers the official English numbered
normative text, articles 1--130 and the appendix, while excluding titles,
notes, and subscriptions and making no claim of cross-language collation.

## Consumer integration and trace calibration

Fifty-six binding rows across twelve publications now reuse the normalized
work. The consumers are the council and due-return articles; the Ascension and
Mount Carmel novenas; the Vulgate history; the 1962 Ordinary and
Ninth-after-Pentecost guide; *Two Missals, One Sacrifice*; the postconciliar
Order of Mass; the postconciliar liturgical-calendar reference; the Marian
apparitions reference; and the sacramental treatise.

The audit preserved three meaningful exclusions:

- the sacramental at-a-glance companion imports no surface that depends on
  *Sacrosanctum Concilium*, so it does not receive a decorative inherited
  binding;
- the FSSP record reports a 2000 response that itself cites article 57 and is
  therefore a source-of-source trace, not direct use of the Constitution; and
- occurrences of `SC` meaning the *Sources Chrétiennes* series are not
  misclassified as *Sacrosanctum Concilium*.

Comparison of local traces with the official witnesses corrected or clarified
the current records:

- the council article now uses the canonical Holy See URL, includes articles
  37--40 in its adaptation and authority analysis, and states the limits of
  its complete-English-text negative control;
- that bounded control found no explicit mandate in articles 1--130 and the
  appendix for total abolition of Latin, total vernacularization, celebration
  toward the people, Communion in the hand, multiple or new Eucharistic
  Prayers, or replacement of the Offertory; it is expressly not a prohibition
  of those developments or an exclusion of later authority;
- the Ascension novena narrows its reference from articles 10--13 to article
  13;
- the 1962 Ordinary replaces a broad articles 47--58 trace with its actual
  uses of articles 7, 14, 47--48, 50, and 56;
- *Two Missals, One Sacrifice* separates its positive paragraph controls from
  its bounded whole-English-text negative control;
- the postconciliar Order of Mass records the exact used union as articles
  5--8, 10, 14, 21--24, 26--35, and 47--58;
- the apparition reference adds article 13 beside article 10 for the
  subordinate orientation of popular piety to the liturgy; and
- the sacramental scope distinguishes exact direct uses from its broader
  cataloged articles 59--82 lead.

## Reverse use, impact, and mutation proof

Reverse-use inspection reports 56 binding rows across 12 publications for the
work. Work-level impact reports 86 rows: the same publication fan-out plus 30
dependent canonical source records. More narrowly:

| Source node | Binding rows | Publications | Impact rows |
| --- | ---: | ---: | ---: |
| English official HTML artifact and descendants | 54 | 11 | 74 |
| AAS 56 PDF artifact and descendants | 1 | 1 | 5 |
| Latin official HTML artifact and descendants | 1 | 1 | 2 |
| English articles 47--48 | 5 | 5 | 5 |
| English article 13 | 3 | 3 | 3 |
| English article 10 | 5 | 5 | 5 |

Three isolated copies of the source tree tested dependency staleness with
valid metadata-only mutations:

- changing the English HTML artifact invalidated exactly 53 fingerprints
  across 11 publications; the fifty-fourth row is the intentionally
  catalog-only articles 59--82 lead and has no verification fingerprint;
- changing the AAS 56 artifact invalidated exactly 1 fingerprint in the
  Ninth-after-Pentecost guide; and
- changing the articles 47--48 passage invalidated exactly 5 fingerprints
  across 5 publications.

Each mutated tree failed only on the expected fingerprint requirements. The
unmodified graph validates.

## Publication and acceptance results

Five PDFs changed because the calibrated traces or rendered references affect
their publication text. All five settled through two TeX passes without fatal
errors, undefined references or citations, rerun requests, overfull or
underfull boxes, badness reports, or other layout warnings. The first visual
pass found one final line of a callout stranded at the top of the next page;
a claim-preserving prose tightening removed the widow and the corrected
51-page article received a full post-fix review. Repository-generated page
rasters and contact sheets covered all 241 final pages. Dense tables, callout
boxes, references, terminal metadata, and every changed surface were also
checked at full resolution; no clipping, collisions, blank or missing pages,
illegibility, or anomalous layout remained.

| Publication | Pages | Installed PDF SHA-256 |
| --- | ---: | --- |
| *Council, Missal, and Crisis* | 51 | `8cfe9e1b32be4719d47fa03d12b6bc30870762914176bf7f0d9ab046b6e10556` |
| *The First Novena: From Ascension to Pentecost* | 27 | `cb0ea1a6ddd66b82e8b722e32e4669003312ee565aacfc8b767dfa5ec7e65853` |
| *The Ordinary and Order of the Mass* | 42 | `4b1945c54f5dce7b136976d0da4c0d98b7615c40b9adefd8335af6261687e565` |
| *The Order of Mass: A Mystagogy of the Postconciliar Roman Rite* | 77 | `cf3a0164af8100f16752905d59164356d564577256e289c92de4a136f649b174` |
| *Marian Apparitions in Catholic Ecclesial Judgment* | 44 | `0b0b6a2c1d8a1a0005992c6a844c26c84fa618350f5d701621d2209c4fe0349b` |

The final graph validates with 44 artifacts, 4 corpora, 38 editions, 111
passages, 14 segments, 22 works, and 438 bindings. The refreshed family ledger
assigns the AAS 56 container and *Sacrosanctum Concilium* records explicitly
while leaving other conciliar acts and AAS volumes pending. Each changed
installed PDF is byte-identical to its reviewed build. These are internal
source and production checks, not external specialist or ecclesiastical
approval, and no release clearance is claimed.
