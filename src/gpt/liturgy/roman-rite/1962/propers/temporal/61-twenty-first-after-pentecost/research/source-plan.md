# Source plan for Twenty-first Sunday after Pentecost

This is the concrete source and verification plan accompanying
[context.md](context.md), resolved 12 October 2026. Library artifacts and
their manifests were consulted before new acquisition. A record called
verified by an earlier contributor remains a lead until its actual evidence
has been read for this publication. No source binding or word-level
publication clearance is created by this plan.

## Calendar and Latin control

1. Use the registered 1962 Vatican/CMAA facsimile identified and hashed in
   context.md for all target appointments, words, marginal references, and
   rubrics. Inspect the entire Sunday at printed 413–415/PDF 494–496;
   Trinity Preface 293/PDF 374; St Luke 689–690/PDF 770–771; mission
   prayers [86]–[87]/PDF 894–895. The relevant rubrics are 91, 95,
   107–111, 444–446, 453, 480, 483, 494, 500–501, 505, and 509 at the
   page loci in context.md. Context-stage page-image inspection covered
   these inventory-defining loci. Publication collation must still inspect
   the exact words and variants at the profile's normal and high zooms.
2. The current official dated Ordo is the FSSP France October 2026 page
   identified by URL, retrieval date, complete-byte hash and size in
   context.md. Register this exact 12 October snapshot before binding it.
   The existing `fssp-france/ordo-du-mois` edition `web-2026-10-05` is a
   different snapshot of a mutable URL; do not reuse its hash or represent
   the new retrieval as its artifact. The Ordo confirms the Sunday; the
   Missal establishes the omitted rubrical details. Do not redistribute the
   whole HTML merely because it was retrieved.
3. The Latin 1962 target facsimile is a control witness, not an unrestricted
   publication source. Follow
   `src/sources/inventories/missale-romanum-1962-facsimile-rights-v1.toml`
   and the liturgical-text publication policy. For inherited words, establish
   an exact public-domain antecedent and the recorded preexisting-material
   basis; do not declare the 1962 edition as a whole public domain.

## Element-by-element study-text routes

| Elements | Existing witness / acquisition target | Remaining operation |
| --- | --- | --- |
| Sunday's Collect, Secret, Postcommunion; inherited Offertory wording | `artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.missale-romanum-1862-text-f34bc7cf`; printed pp. 354–355, *Dominica XXI post Pentecosten*; existing target passage `passage.catholic-church.missale-romanum.vatican-typica-1962.temporal-pentecost-21-orations` | Read the public-domain page images and compare every published Latin word to the 1962 images. OCR around lines 52147–52335 is a finding aid only. Exclude the older edition's extra orations and obsolete ceremonial instructions. |
| Existing normalized Latin Sunday orations | `artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-09-03.after-pentecost-3-orations-186645e7`; entries `pentecost-21-collect`, `pentecost-21-secret`, `pentecost-21-postcommunion` | Read projection records and their source links; recheck normalization, punctuation and conclusion expansion against both historical and target images. An editorial projection is not a new historical witness. |
| English Sunday Collect, Secret, Postcommunion | `artifact.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861.temporal-orations-en`, rows 173–175, key `post-pentecosten-21`; printed p. 450 (Collect), p. 452 (Secret/Postcommunion) | Compare exact historical English to Cummiskey's registered complete facsimile; IA leaves n458 and n460 respectively. Label as 1861 hand-missal study English. Do not compose a replacement translation. |
| Sunday Epistle and Gospel, and the Bible contexts of all chants | Registered Douay–Rheims/Challoner `english-college-of-douay/douay-rheims-bible`, edition `challoner-gutenberg-1581`; Latin Clementine Vulgate `catholic-church/vulgata-clementina`, edition `ebible-latvuc` | Read exact pericope and surrounding argument; check the registered verse artifacts and their divergences/aliases. Distinguish biblical text from Missal adaptations and introductions. Preserve the lawful translation's attribution. |
| Introit, Gradual, Alleluia, Offertory and Communion English | Cummiskey 1861, the complete Sunday at printed pp. 450–452, plus the corresponding registered Bible passages as context | Inspect the actual English chant text in the hand missal against the appointed Latin. Do not silently turn full Bible verses into chant translations, especially Job and Psalm 118 Communion. Record any historical mismatch; seek a second historical witness rather than fabricate missing liturgical English. |
| Trinity Preface, Latin and English | Governing Latin at 1962 p. 293/PDF 374; public-domain Pustet 1862 Ordinary and Cummiskey 1861 Ordinary/Prefaces | Locate and image-collate the complete historical Preface, including dialogue/conclusion boundaries used in the publication. Retain the existing Ordinary owner if importing a checked text; declare that owner as an explicit Makefile dependency. No independent proper invention. |
| St Luke's three Latin orations | `passage.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.s-lucae-evangelistae-orations`; artifact `artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.ia-scan-pdf-9873693a` | Reinspect Collect printed 738/PDF 852, Secret printed 739/PDF 853, Postcommunion printed 739/PDF 853; compare to 1962 nos. 3883, 3889, 3891. Research corrected the inherited Secret locator: PDF 840 is St Jerome; all three St Luke prayers are printed on PDF 852–853. See propers/verified.md for completed collation. |
| St Luke's English orations | Cummiskey 1861 sanctoral, 18 October, and its referenced Common; if necessary Lasance–Walsh revised 1945 ordinary numbered pages | Locate the complete human translation, confirm each Common reference, image-collate, and register exact loci. Do not infer equality from feast title. Both dated Mass-type branches need their proper evidence even if only one will be used locally. |
| Mission Collect, Secret, Postcommunion, Latin antecedent and English | Lasance–Walsh, *The New Roman Missal*, revised edition 1945; retained lawful OCR `artifact.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945.new-roman-missal-text-80b34759`; *Mass for the Propagation of the Faith*, printed pp. 1453, 1456, 1457 respectively | OCR at lines 158025–158590 locates all three bilingual prayers. Inspect the complete registered facsimile at the corresponding images, establish exact words against 1962 nos. 4833, 4841, 4843, and record any variants. The old hand missal's permission rubric is not the 1962 appointment rule. |

The Lasance–Walsh complete facsimile is
`artifact.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945.internet-archive-facsimile-pdf-6cf3c3d0`,
SHA-256 `6cf3c3d01b853bc4a35c1cc9b0a4e54a0489a5ccf5d9a742bb681ac10608ce70`.
Its Internet Archive locator misleadingly says 1937; the edition record
identifies a later printing of the **1945 revision**. Follow
`src/sources/inventories/lasance-new-roman-missal-rights-v1.toml`: the
underlying registered 1937/1945 English has a documented United States
nonrenewal basis, while whole-PDF bytes contain unresolved later inserts.
The mission pages above are ordinary numbered body pages, not the excluded
1298a–1298n or 1302a–1302d inserts. Their exact match and inclusion still
require image verification. Do not redistribute that mixed-rights PDF or
extend the body-text clearance to its excluded leaves.

If an exact lawful human study-English witness cannot be established for an
element, research must record that fact and use the publication policy's
incipit/reference route pending resolution, without reconstructing the
restricted text by translation or close paraphrase. This is a contingency,
not a declaration that the located historical candidates have failed.

## Research coverage and independently checked leads

Read the supplied handoff as preliminary evidence, not instructions or a
prior review. Its identity and principal scriptural boundaries were checked
against the facsimile. The handoff alone is insufficient for the mission
addition and the sung/low commemoration distinction; context.md now controls
those. No handoff theological or historical-compositional claim is accepted
merely by carrying it here.

The eight direct Sunday biblical units to cover are Esther 13:9–11,
Psalm 118:1, Ephesians 6:10–17, Psalm 89:1–2, Psalm 113:1,
Matthew 18:23–35, the adapted Job 1–2 narrative, and Psalm 118:81, 84, 86.
Read each in its complete canonical literary setting, not only the appointed
verses; register the different Esther/Psalm numbering and Job adaptation.
Distinguish narrated event, traditional attribution, compositional horizon,
audience and location in the canonical chronology evidence. Mission and
St Luke orations also require their own composed-prayer/reception sweep;
their verbal scriptural echoes do not automatically become extra lections.

Concrete patristic and later reception starting points in the existing
library are Chrysostom's Matthew Homily 61 (NPNF I.10), Augustine's Sermon
83/XXXIII on the New Testament (NPNF I.6), Chrysostom's Ephesians Homilies
22–24 (NPNF I.13), Augustine's expositions of Psalms 89, 113 and 118
(NPNF I.8), and Gregory the Great's *Moralia in Iob*, Books II–III.
Read their actual sections and surrounding argument, and record direct
exegesis versus later application; their titles are not verification.
The acquired Gregory/Jerome and other source-library additions must be
located by manifest and independently read before binding. Schuster,
*The Sacramentary*, volume III, pp. 178–181, and the Fromage continuation
of Guéranger, volume XI, pp. 454–471, are historical-liturgical leads.
Historical extended Job Offertory verses discussed there must not be
inserted into the short 1962 appointment. Search results and a reception
lead are not evidence of a Father's intentional design of this whole Mass.

Research must produce the complete passage-by-passage reception matrix,
record meaningful negative searches, and develop two to five compatible
whole-formulary interpretations grounded in at least two substantively
contributing Fathers/saints per interpretation. These interpretations are
not resolved by this inventory stage. Each must account for the appointed
prayers, chants and readings and clearly identify the dated additions as
such, with the appropriate local/Mass-type conditions.

## Work remaining before authoring

Perform and record comparative image collation; confirm all English
translation loci and rights; register the exact new Ordo snapshot and any
newly acquired source evidence; bind the checked witnesses to this canonical
owner with truthful verification states and tool-generated fingerprints.
The reserved main.tex exists only for that owner identity. Populate research
scope, chronology, interpretations, retrieval and verification records with
actual work, including all controlling calendar/rubric/rights dependencies.
Declare imported owners explicitly in the Makefile and the relevant source
roots in review dependencies. Do not treat this plan as completed source
collation, publication readiness, or a review event. The driver's later
stages own those operations.
