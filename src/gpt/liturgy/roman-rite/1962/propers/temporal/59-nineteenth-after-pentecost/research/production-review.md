# Production review

## Author study — iteration 0

Run `b686b7a44f0e35e7`, workflow `proper-study` version 7. The expansive
study was authored on 28 September 2026 from the reviewed research for the
1962 Nineteenth Sunday after Pentecost, general-calendar occurrence
4 October 2026. This record covers author verification only. Independent
study review, companion derivation, the final shared-timestamp build, and
publication review remain subsequent workflow work.

### Completed scope

The study contains the complete ten-element inventory and historical study
texts, detailed commentary on every element, and two whole-formulary readings:
“The Invited People Clothed in Charity” and “The Renewal of Hands, Words, and
Desires.” Each has its own literal, allegorical, moral, and anagogical
conclusion. Augustine and Gregory carry the first reading; Chrysostom and
Bellarmine carry the second. Aquinas and Schuster contribute the bounded
arguments identified in the notes. Whole-Mass connections are editorial
syntheses except where Schuster directly treats this Sunday.

The canonical chronology is rendered in a terminal historical appendix,
followed by scope and qualifications, used references, the revision timestamp,
and rights colophon. Schema 2 declares all three intended entrypoints and
future concise and homily components; only the research components are
implemented at this stage. Canonical web eligibility is declared, without
claiming a generated web edition has been reviewed.

### Substantive length

The substantive opening, element commentary, two developed readings, their
sense distillations, and concluding comparison contain approximately **6,930
words**. This conservative source count excludes the inventory map, appointed
texts, all footnotes, heading and sense labels, TeX command names, chronology,
terminal scope, bibliography, provenance, and rights colophon. Alphabetic
words with internal apostrophes or hyphens count as one token. Breakdown:
opening 257; element commentary 2,447; charity reading 1,891; renewal reading
2,059; comparison 276. The settled PDF has **20 physical pages**, including
all terminal apparatus.

### Source limits preserved

The appointed Latin follows the reviewed 1962 witness and its public-domain
1862 antecedent. Cummiskey 1861 supplies the Introit antiphon and three
orations in historical English; Douay–Rheims–Challoner supplies biblical
English without reconstructing the Latin's liturgical additions or adapted
verb forms. The target 1962 edition is not declared public domain. Ordinary
texts are not reproduced; the Creed and Trinity Preface are appointments.

The reception sweep is bounded by the reviewed works, not exhaustive. The
study preserves Gregory's imperfect-charity distinction and his alternative
relations between Matthew's and Luke's feasts; it does not invent a universal
wedding-garment custom or a numerical salvation rate. Gregory's weaving image
uses upper and lower supports. Aquinas's inspected OCR supports paraphrase,
not a newly established critical text. Schuster's theological interpretation
does not establish ancient compilation history. The historical chronology
keeps competing composition proposals distinct, records the Gospel event date
as unresolved, and does not convert a broad Psalter boundary into a date for
each psalm's occasion. Reviewed research records were not revised by this
authoring stage.

### Author proof verification

The required `make doc` build and the research-edition component artifact
check passed. Research-edition content preflight also passed: 27 source
bindings resolve; the seven scriptural elements preserve the current
chronology projection; both lanes declare complete element and sense coverage;
and no bound restricted source is reproduced. The references are a manually
checked description list; the automatic references-used check recognizes zero
formal bibliography entries and therefore supplies no positive citation-use
audit for that list.

All 20 pages were inspected at page-raster scale with a contact-sheet overview;
changed pages were reinspected after pagination repairs. The opening map is
complete on page 1, the chronology dossier is together on page 18, and the
final references, timestamp, and rights colophon share page 20. Sparse
text-only spill pages were removed. No clipping, overlap, missing glyph,
or stranded heading was found in the settled proof. The final LaTeX log has
no warnings, undefined references, overfull boxes, or underfull boxes.
`pdfinfo` reports US Letter pages; `pdffonts` reports all 15 fonts embedded,
all from Latin Modern. The shared format supplies 11-point text, 0.75-inch
margins, and monochrome output.

The proof displays revision timestamp **2026-09-28T15:13:28Z**. The exact
cold-review copy is `study-author-proof.pdf` in run `b686b7a44f0e35e7`'s
`author-study-0000` artifact directory; its SHA-256 is
`f628a1b3635f1ef63ad1998de786d76dcddf0073bffce0afffacd81613674aad`.
The run directory also retains build and check logs, PDF information,
font evidence, and the dedicated replaceable raster child. This author
inspection does not replace the later independent visual evaluation.
