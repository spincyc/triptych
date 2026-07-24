# Dei Verbum and AAS 58 Reuse Review

Reviewed on 2026-07-23.

This record documents the completed bounded normalization of *Dei Verbum*
within `family.vatican-ii.acts`, the volume 58 component of
`family.acta.aas-ass`, and one unrelated constituent of the same official
gazette artifact. It makes complete official witnesses centrally identifiable
for later expansive examination, binds current publications only at the loci
they actually use, and proves cross-publication propagation by mutating
run-local copies of the real source graph. The canonical manifests and
publication-local bindings remain the machine-enforced records.

## Identity boundaries

The graph distinguishes the intellectual work, its container, and its
expressions:

- *Dei Verbum* is the separately promulgated dogmatic constitution;
- *Acta Apostolicae Sedis* volume 58 (1966) is the official-gazette container;
- the Latin AAS constituent, dated Latin Holy See web state, and dated English
  Holy See web state are distinct editions;
- the separately titled 15 November 1965 *Notificatio* concerning the
  Constitution's theological qualification is a distinct work;
- the two-paragraph Doctrinal Commission declaration of 6 March 1964 is a
  distinct work reproduced in both this notification and the earlier *Lumen
  gentium* `Notificationes`, with separate AAS 58 and AAS 57 witnesses; and
- the Sacred Congregation for the Doctrine of the Faith's 14 June 1966
  notification concerning the Index of Prohibited Books is another distinct
  work on printed AAS p. 445.

The last item is an intentional shared-container edge. La Salette uses the
Index notification, not *Dei Verbum*, for its claim about the 1966 change in
the Index's legal force. Both works reuse the one AAS 58 artifact without
collapsing their identities, authorities, dates, or loci.

## Exact artifacts, extent, and rights

Three exact Holy See artifacts control the normalized records:

| Artifact | Extent | SHA-256 |
| --- | ---: | --- |
| English *Dei Verbum* HTML response | 43,095 bytes | `e5eac5f655389e3c54295985be85e5a4ce9f55f0165e8e8ee9ce6167fedb8e5f` |
| Latin *Dei Verbum* HTML response | 46,303 bytes | `164f55e1a7512c7d8032199bf98a491b54e0467597b49faab4fee4e000ef06fc` |
| Holy See AAS 58 OCR PDF | 1,279 pages; 5,944,403 bytes | `69c27224cde7f27547e18c544f5b99064793ada9509ebc902b20fa548e15bac8` |

The complete AAS *Dei Verbum* constituent begins on printed p. 817. Numbered
articles 1--26 end on p. 830, followed by the promulgation formula,
subscriptions, and attestations through p. 835. The distinct *Notificatio*
occupies p. 836. The Index notification is complete on p. 445; the preceding
act ends on p. 444 and the next begins on p. 446. These boundaries were checked
against the page images. The AAS OCR remains a locating aid rather than an
independently authoritative transcription.

The Vatican portal's legal notice did not establish repository redistribution
permission. All three artifact identities are therefore `restricted` and
nonretained: the repository stores exact hashes, byte or page extent,
provenance, boundaries, and dependency records, but not the payloads.

One source-local discrepancy remains explicit. The English article 15 note
gives AAS 29 (1937), p. 51 for the cited encyclical locus, while both the Latin
web and AAS witnesses give p. 151. The proof preserves the received English
state rather than silently correcting it or claiming a critical collation.

## Expansive availability and bounded use

The full dated English and Latin web states and the complete Latin AAS
constituent are centrally identifiable for later work-wide examination.
That availability does not imply that every consumer searched or verified the
whole Constitution.

The English passage records cover articles 1--26, 2--4, 8, 10, 11--12, and
21. The whole-text node supports the council article's bounded negative
control; the narrower nodes govern claims about Revelation's fullness in
Christ, Tradition, inspiration and interpretation, Scripture in the Church,
and the Church's reception of the divine word. The AAS branch separately
records the complete numbered Latin text. The notification branch records the
complete notification, while the declaration branch records its embedded
two-paragraph work through two AAS reproduction witnesses. They have the same
substantive wording; AAS 57 prints a comma after `definit` before `quae` that
AAS 58 omits.

Article 12 note 6 cites Augustine, *De civitate Dei* XVII.6.2. That
source-of-source relation is visible in the passage record, but a publication
using *Dei Verbum* 11--12 is not thereby represented as having inspected
Augustine directly.

## Reviewed consumers and exclusions

Twenty-two *Dei Verbum* binding rows across fourteen publications now share
the normalized identities. Twenty rows across twelve publications are
fingerprinted verified uses. The Ascension and Mount Carmel novenas retain
their honest broader references as catalog-only edition bindings because the
present work did not promote those broad ranges to verified readings.

The direct consumers are the council and Freemasonry articles; the two
novenas; the postconciliar Order of Mass; the heresies reference; the
apparitions, Champion, Fatima, Guadalupe, La Salette, Lourdes, Marian-dogmas,
and Rosary studies. La Salette also has one separately verified binding to the
complete 1966 Index notification at AAS p. 445.

Review corrected the reader-facing or audit trace where needed:

- the council article now names its exact positive loci and qualifies its
  complete-English-text non-entailment finding;
- Freemasonry, the Order of Mass, and the heresies reference now point to the
  exact used passages;
- the novenas retain broader, visibly linked bibliographic references without
  overstating verification;
- Fatima, Lourdes, Marian Dogmas, and La Salette record the checked loci in
  their local audits; and
- La Salette records the new direct p. 445 page-image inspection rather than
  retroactively attributing it to its earlier AAS audit.

## Reverse use and mutation proof

The unmodified graph validates. Seven isolated copies of the actual source tree
then received valid metadata-only mutations:

| Mutated node | Stale fingerprints | Publications | Unexpected diagnostics |
| --- | ---: | ---: | ---: |
| English *Dei Verbum* artifact | 20 | 12 | 0 |
| English articles 2--4 passage | 10 | 10 | 0 |
| English articles 11--12 passage | 2 | 2 | 0 |
| AAS 58 artifact | 1 | 1 | 0 |
| Declaration's AAS 57 passage | 1 | 1 | 0 |
| Declaration's AAS 58 passage | 0 | 0 | 0 |
| Declaration work | 1 | 1 | 0 |

The AAS mutation changed every dependent canonical-source fingerprint and
invalidated the one publication binding that currently depends on that
artifact: La Salette's p. 445 Index notification. The *Dei Verbum* AAS
constituent remains reusable canonical evidence without being falsely
represented as the direct witness behind English-web consumer bindings.
Passage mutations invalidate only their exact consumers, while the artifact
mutation reaches every verified descendant of the English delivery state.
The declaration-work mutation reaches the council article through its selected
AAS 57 witness. Mutating the parallel AAS 58 passage reaches no publication,
which is the intended negative control: registering a second witness makes it
available for comparison without falsely making it evidence for the existing
AAS 57-based binding.

## Publication and acceptance results

Six rendered publications changed. Two novena companions were also rebuilt
because they share canonical material; their bytes did not change.

| Publication | Pages | Installed PDF SHA-256 |
| --- | ---: | --- |
| *Council, Missal, and Crisis* | 51 | `7f0c312bbd07646fc8500949a20a2ca026e2d3633e97e905f4150e6c96d07a70` |
| *Freemasonry and the Catholic Church* | 46 | `50f9743aed3fc17f327beafcff06cdbb9120b2ae8152922ec71db2af8b00edd4` |
| *The First Novena: From Ascension to Pentecost* | 27 | `bacd86f6427e07c4ceda205789871dd4b44fd11e3d0905aa7738a55e3b559a1e` |
| *The Novena of Our Lady of Mount Carmel* | 29 | `2ae6e63c1363f7340a49f060769cb3a79fdd520d84a936a15406ed9d6395f812` |
| *The Order of Mass: A Mystagogy of the Postconciliar Roman Rite* | 77 | `71fe67ded09165b272a37eeff4b46552757fbd1439bad0b157e66ead8fc2222a` |
| *Heresies in Catholic History: A Comprehensive Documentary Survey* | 81 | `2cc01a3c2bd2f10c07511732752789081eff8a127fb2545768c6db3bd184e99f` |
| Ascension daily-prayer companion, unchanged | 11 | `675ae37d807d9ff0fadf4c1d5951480018f0ed6b56773b56493fd9b9c363c1ce` |
| Mount Carmel daily-prayer companion, unchanged | 12 | `d6eaf8220ff47fe26618c9dc4d3b0ae3e18e9770585514b9a55874f3c2d91c2c` |

All eight documents settled through two TeX passes without fatal errors,
undefined references or citations, rerun requests, overflow, underfull boxes,
package warnings, or other layout warnings. All 334 full-resolution page
rasters were individually inspected. No clipping, collision, blank or missing
page, broken structure, unreadable text, stranded heading, or anomalous layout
remained. `qpdf --check` passed for each changed PDF, and every installed
changed PDF is byte-identical to its reviewed build.

The completed source graph contains 47 artifacts, 4 corpora, 46 editions, 121
passages, 19 segments, 26 works, and 461 bindings. The family ledger assigns
the AAS 58 container, *Dei Verbum*, its notification, and the distinct Index
notification explicitly. It also replaces duplicate notification-owned
subpassages with one declaration work and two exact reproduction witnesses.
The remaining conciliar acts and AAS volumes stay open for later family
proofs. The separate 15 November 1966 interpretive decree cited by La Salette
also remains a later normalization task rather than being folded into the
14 June notification. These are internal source and production checks, not
external specialist or ecclesiastical approval.
