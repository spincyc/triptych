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

## Author study — iteration 1

The study was revised on 28 September 2026 after research iteration 2.
The complete research scope, interpretation map and existing study components
were read. The acquired USCCB Ephesians introduction was independently read,
including its destination discussion and complete authorship paragraph;
the generated chronology comparison was checked against that evidence.

The historical appendix now explains the grounds for questioning direct
Pauline authorship and distinguishes the secretary under Paul's direction
from the later-disciple hypothesis. Only the latter receives the separately
displayed approximate interval. The traditional captivity alternatives,
uncertain composition location, destination proposals, and distinction between
writer and recipients remain visible. This incorporates the study-owner
follow-through identified as STU-CHR-001 in the reviewed research. The
references now cite the USCCB introduction's paragraphs 3–4 and correct
Gregory's Wikisource index URL, addressing STU-CIT-001. No reviewed research,
chronology projection, source binding, appointed text, or interpretive lane
was changed by this author stage.

The complete two-reading study remains **6,930 substantive words**, independently
recounted using the exclusions and token rule above. Its five counted components
retain the same breakdown. The historical appendix's redundant concluding
recap was shortened so its dossier and conclusion remain together on page 18;
the qualifications remain in the dossier and scope appendix. The final
proof remains **20 physical pages**. All pages were inspected as page rasters,
with the three changed terminal pages reinspected after that pagination
adjustment. Raster hashes establish that pages 1–17 were unchanged between
the two proofs inspected during this stage. No clipping, overlapping text,
missing glyph, or isolated heading was found. The final page contains the
references, one visible timestamp and the compact rights colophon.

The required author build and research component artifact check passed.
Research content preflight passed with 28 valid bindings, both whole-formulary
lanes, and the complete generated chronology for seven scriptural elements.
The manual bibliography retains the earlier automatic-check limitation:
the references-used check recognizes no formal bibliography entries. The
final LaTeX log has no warnings, undefined references, overfull boxes or
underfull boxes. PDF inspection confirms US Letter and 15 embedded Latin
Modern fonts. The current Ephesians evidence is paraphrased; no protected
liturgical English or newly composed prayer was added. Earlier source limits
remain as recorded above and in the reviewed research.

The exact run-provenance check passed. The broader `make check-sources`
command reached successful source-library validation but stopped in its
document-catalogue prerequisite because the manifest's future `homily.tex`
does not yet exist. This is the current author-study stage boundary, not a
completed global gate; the companion and later publication stages must
complete that check after their entrypoints exist. Shared inventory refresh
and integration remain with the workflow coordinator.

Finalized render timestamp: **2026-09-28T15:59:54Z**. The exact cold-review
copy is `study-author-proof.pdf` in this run's `author-study-0001` artifact
directory, SHA-256
`8d8e64a2ae4348ec9fb31e6e1cef189f80914c32f613c3ad451133fa2728f68c`.
Build diagnostics, component/content checks, word-count evidence, extracted
text, PDF/font information and a dedicated raster child accompany that copy.
This is author verification; the independent study verdict, companion
derivations, final shared-timestamp build and independent visual review are
separate subsequent events.

## Derive synthesis — iteration 0

The concise study, **Charity and the Renewed Life**, was derived on
28 September 2026 from the accepted expansive study and its reviewed
research. It implements the six already-declared synthesis components and
the literal imports in `synthesis.tex`. The common manifest already named
the correct synthesis-only membership, presentation roles, element coverage
and generated-chronology reference; no manifest repair was necessary.
The accepted study, chronology, evidence bindings and interpretation records
were not revised. The shared generation record now identifies this
contribution and the render-source finalization time **2026-09-28T16:26:54Z**.

The complete ten-element map and exactly four overview sense rows occupy
physical page 1. The canonical chronology, including all traditional
alternatives, both critical comparisons and the unresolved Gospel event
date, occupies page 2 alone. Its concise explanations retain the distinct
Aramaic/Greek Matthew objects and the conditional later-disciple Ephesians
interval. The source-grounded thematic movement occupies pages 3–4;
developed interleaved commentary begins on page 5. Six cross-proper
questions compare fruitful belonging with renewed action, preserving
Augustine's and Gregory's different arguments for charity, Chrysostom's
particular social commands, Bellarmine's grace/obedience distinction,
Gregory's imperfect-charity consolation and the actual reception differences.
No new evidence-dependent claim or additional research source was introduced.

The substantive themes and commentary contain **3,719 words**: 1,081 in
the thematic movement and 2,638 in the developed commentary. This source
count excludes footnotes, headings, zref labels, TeX commands, the inventory,
overview, chronology and terminal apparatus. Alphabetic words with internal
apostrophes or hyphens count as one. The settled author proof has **10
physical pages**, including all terminal content.

The required `make doc` author build and synthesis-edition component
artifact check passed. The settled auxiliary record proves inventory and
overview on page 1, chronology on page 2, themes on pages 3–4 and commentary
starting on page 5. Synthesis content preflight passed: 28 bindings resolve,
all seven chronology cells retain generated annotations, and the
house-voice, structural, rights and declared-coverage checks pass. The
manual description-list bibliography was compared with its uses; the
automatic references-used check recognizes no formal entries and does not
supply a positive audit of that list.

All ten page rasters were inspected; changed pages were reinspected after
strengthening the thematic exposition and attaching two footnote markers
to their preceding sentences. No clipping, overlap, missing glyph,
stranded heading or detached marker remains. The shared title, map,
overview and dossier forms retain house typography. Both thematic pages
are substantively filled, the chronology remains legible, and the final
references, single timestamp and compact rights colophon share page 10.
The final LaTeX log contains no warnings, undefined references, overfull
or underfull boxes. PDF inspection confirms US Letter, 17 embedded Latin
Modern font entries and 462,675 bytes, below the size-review thresholds.

The exact reviewer proof is retained in run `b686b7a44f0e35e7` under
`artifacts/derive-synthesis-0000/`, outside its dedicated replaceable
`rasters/` child:

| Artifact | SHA-256 |
| --- | --- |
| `synthesis-author-proof.pdf` | `a440660d94998ea71c70791b3d67eb2c16ab89d7000a46f3312091499553fac2` |
| `synthesis-author-proof.aux` | `5fa40538283f0773f66967f7302f515865ba94edee61c1d71b60e74cdf1873bd` |
| `synthesis-author-proof.log` | `4b2193be3777edf4b50940fd5a3b1d0c79b5cc8e8b22b32f27cf25c1afd1d518` |

The artifact directory also holds the recorder file, extracted text,
word-count method and totals, build and component/content check logs,
font/PDF information and `proof-manifest.json` with exact repository-relative
paths and hashes. This is author verification only; independent concise
review, homily derivation, the final three-document shared-timestamp build
and cold visual evaluation remain separate workflow events. No PDF was
installed at this stage.

The broader `make check-sources` reached successful source-library
validation, then stopped at the document-catalogue prerequisite because the
declared future `homily.tex` is not yet implemented. That global gate must
be completed after the homily stage. Shared source inventories, catalog
integration, commits and workflow advancement remain with the coordinator.
