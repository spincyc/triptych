# Source plan for Twenty-first Sunday after Pentecost

This is the concrete source and verification plan accompanying
[context.md](context.md), independently re-resolved 13 October 2026. Library
artifacts and their manifests were consulted before new acquisition. A record called
verified by an earlier contributor remains a lead until its actual evidence
has been read for this publication. No source binding or word-level
publication clearance is created by this plan. The existing manuscript,
collation, bindings, chronology and interpretation records remain evidence
to inspect; their existence supplies neither a new verification event nor a
transferred review verdict.

## Calendar and Latin control

1. Use the registered 1962 Vatican/CMAA facsimile identified and hashed in
   context.md for all target appointments, words, marginal references, and
   rubrics. Inspect the entire Sunday at printed 413–415/PDF 494–496;
   Trinity Preface 293/PDF 374; St Luke 689–690/PDF 770–771; mission
   prayers [86]–[87]/PDF 894–895. The relevant rubrics are 91, 95,
   107–111, 369, 444–446, 453, 480, 483, 494, 500–501, 505, and 509 at the
   page loci in context.md. Context-stage page-image inspection covered
   these inventory-defining loci. Publication collation must still inspect
   the exact words and variants at the profile's normal and high zooms.
2. The dated Ordo is the FSSP France October 2026 page identified in
   context.md. Its complete 12 October delivery is already registered and
   bound as `artifact.fssp-france.ordo-du-mois.web-2026-10-12.html-e5207e58`.
   Its bytes and appointed entry were independently rechecked for this
   context. The complete 13 October live delivery confirms the same entry
   but has a different hash; if research elects to adopt it as a controlling
   artifact, register it separately before binding it. Do not mechanically
   replace the existing artifact hash or verification date. The Ordo confirms
   the Sunday; the Missal establishes the omitted rubrical details. No
   redistribution basis for the modern HTML is asserted.
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
| Introit, Gradual, Alleluia, Offertory and Communion English | Registered Douay–Rheims/Challoner passages identified in `propers/verified.md`; Cummiskey 1861, printed pp. 450–452, is a historical comparison witness | Follow the 1962 profile's Scripture route. The present collation supplies exact Bible comparators, not synthetic English antiphons. Recheck omissions, additions and introductions against the appointed Latin, especially Esther, Job and Psalm 118; never splice Bible phrases into a new chant translation. |
| Trinity Preface, Latin and English | Governing Latin at 1962 p. 293/PDF 374; Cummiskey 1861 Latin and English, printed xxviii–xxix / PDF 39–40, with registered `praefationes-la` and `praefationes-en` artifacts | Recheck the common-opening/Trinity-continuation seam and historical wording. The existing collation records Quam in both Latin witnesses and quotidie/cotidie as a spelling difference. Dialogue and Sanctus remain Ordinary elements. Declare an explicit Makefile dependency if importing an authored Ordinary owner. |
| St Luke's three Latin orations | `passage.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.s-lucae-evangelistae-orations`; artifact `artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.ia-scan-pdf-9873693a` | Reinspect Collect printed 738/PDF 852, Secret printed 739/PDF 853, Postcommunion printed 739/PDF 853; compare to 1962 nos. 3883, 3889, 3891. Research corrected the inherited Secret locator: PDF 840 is St Jerome; all three St Luke prayers are printed on PDF 852–853. See propers/verified.md for completed collation. |
| St Luke's English orations | Cummiskey 1861, printed 677–678 / PDF 686–687; registered `artifact.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861.s-lucae-checked-english` | All three complete prayers have a retained extract and exact facsimile loci in the existing collation. Independently compare those pages before adopting the historical English. No Common substitution is needed for this witness. Both dated Mass-type branches retain their evidence. |
| Mission Collect, Secret, Postcommunion, Latin antecedent and English | Lasance–Walsh, *The New Roman Missal*, revised edition 1945; *Mass for the Propagation of the Faith*, printed 1453, 1456, 1457 / PDF 1474, 1477, 1478; registered `artifact.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945.pro-fidei-propagatione-checked-orations` | Read the existing bilingual extract and independently inspect its source images against 1962 nos. 4833, 4841, 4843. Preserve the English translator's choices and historical abbreviated conclusions. The hand missal's permission rubric is not the 1962 appointment rule. |

The Lasance–Walsh complete facsimile is
`artifact.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945.internet-archive-facsimile-pdf-6cf3c3d0`,
SHA-256 `6cf3c3d01b853bc4a35c1cc9b0a4e54a0489a5ccf5d9a742bb681ac10608ce70`.
Its Internet Archive locator misleadingly says 1937; the edition record
identifies a later printing of the **1945 revision**. Follow
`src/sources/inventories/lasance-new-roman-missal-rights-v1.toml`: the
underlying registered 1937/1945 English has a documented United States
nonrenewal basis, while whole-PDF bytes contain unresolved later inserts.
The mission pages above are ordinary numbered body pages, not the excluded
1298a–1298n or 1302a–1302d inserts. Their exact match and inclusion are
recorded by the earlier collation and require independent inspection before
new adoption. Do not redistribute that mixed-rights PDF or
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
addition and the sung/low commemoration distinction; the independently read
Missal rubrics establish those in context.md. No handoff theological or
historical-compositional claim is accepted merely by carrying it here.

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

Independently inspect the existing comparative collation and its source
images; confirm the English loci and the recorded rights routes before
adopting their words. Preserve historical verification dates rather than
restamping them, and record only checks actually repeated. Register any
newly adopted delivery before binding it, with tool-generated fingerprints.
The existing `main.tex` is a manuscript, not a reservation scaffold, and is
left intact at this stage. The same canonical leaf owns all three documents.

Research must reassess `scope.md`, `interpretations.md`, the generated
chronology and its controlling sources, `propers/retrieved.txt`,
`propers/verified.md`, `source-bindings.toml` and `review-dependencies.toml`.
Audit every adopted calendar, rubric and rights authority through its actual
source owner. No authored liturgical text is imported from another proper
owner by this context or plan. If later authoring imports such an owner,
declare it as an explicit Makefile dependency; keep evidence dependencies in
the research declaration. This plan establishes a concrete route for every
element, not publication readiness or a completed research review.
