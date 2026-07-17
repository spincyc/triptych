# Assembling the Mass — Source Audit

## Audit date and object

- **Audit date:** 2026-07-13.
- **Object audited:** the calendar-selection and Mass-assembly system promulgated in 1960 and printed in the 1962 typical *Missale Romanum*.
- **Publication claim:** an edition-specific study method, not an official Ordo, ceremonial, translation, or current permission.

## Primary-source audit

### 1. Promulgating act

The official Vatican Latin page for John XXIII's *Rubricarum instructum* was consulted at:

`https://www.vatican.va/content/john-xxiii/la/motu_proprio/documents/hf_j-xxiii_motu-proprio_19600725_rubricarum-instructum.html`

It controls the identity, authority, and date of the new rubrical corpus. The publication does not attribute the twenty-eight-position table or individual Mass rules directly to the motu proprio; it cites the code that the act approves.

### 2. Official AAS corpus

The official Vatican object is *Acta Apostolicae Sedis* 52 (1960), 593–740:

`https://www.vatican.va/archive/aas/documents/AAS-52-1960-ocr.pdf`

The following page map was used:

- *Rubricarum instructum*: 593–595;
- code nn. 1–137: 597–620;
- precedence table n. 91: 610–612;
- Missal rubrics nn. 269–530: 643–685;
- occurrence/concurrence tables and notes: 703–705.

The AAS OCR is a navigation layer, not a substitute for the official page. Its relevant numbering was cross-checked against the identical numbered text incorporated into the 1962 Missal facsimile.

### 3. 1962 typical-Missal facsimile

The public 1,088-page facsimile at `https://media.churchmusicassociation.org/pdf/missale62.pdf` was downloaded and consulted. Audit identity:

- title metadata: `Missale Romanum 1962`;
- byte size: 82,815,941;
- SHA-256: `648fdb8fe830ed65a08aa4a95de6f94424c533ddf2398c8fc26b18735fd3518a`;
- image/OCR producer metadata: ABBYY FineReader, 2007; this digitization metadata is not the publication date of the liturgical book.

The incorporated *Rubricae generales Missalis Romani* were searched by number and the following facsimile page images were visually inspected at original rendered detail:

| Facsimile PDF page | Material checked |
|---:|---|
| 14 | nn. 78–91; BVM Saturday, Major Litanies, start of precedence table |
| 16 | nn. 96–112; Annunciation / All Souls seats, reposition, concurrence, commemoration kinds and limits |
| 20 | nn. 284–300; calendar use, conventual Mass, resumed Sundays, preceding-Sunday ferias, Ember ordination rule |
| 22 | nn. 315–334; votive source selection, same-Person rule, impeded votive, color and one-Mass restrictions |
| 24 | nn. 351–365; exposition and external solemnity definition, legal bases, date, and number of Masses |
| 25 | nn. 366–381; public/particular votives and Nuptial admission/prohibition |
| 26 | nn. 381–398; Nuptial total prohibition, III/IV votives, First Thursday/Friday/Saturday, Requiem definitions |
| 27 | nn. 396–412; Requiem prayers, *Dies irae*, All Souls ordering, funeral prohibitions, death-day Requiems |
| 31 | nn. 461–479; optional prayers, Ember lessons, chants, homily, Creed, Offertory |
| 32 | nn. 480–503; prayer order, Preface hierarchy, Sacred Heart/Marian and seasonal Prefaces, proper Canon forms |
| 33 | nn. 504–514; Communion, prayer over people, dismissal, blessing, Last Gospel, audible and sung execution |

The complete calendar rules, remaining Mass-category rubrics, *Ritus servandus*, *Ordo Missae*, Canon, and relevant formulary headings were navigated in the same facsimile. The table above identifies the highest-risk propositions selected for an explicit image audit; it is not a claim that OCR alone controlled unlisted material.

## Repository companion audit

### Ordinary of the Mass

The source and research records under `src/gpt/liturgy/roman-rite/1962/ordinary/00-ordinary-of-the-mass/` were used to verify the boundary between stable Order, variable proper, seasonal intervention, and historical exposition. This assembly manual does not import that work's editorial “thirty-three units” as an official Missal taxonomy; its own twenty-six slots are expressly a practical worksheet.

### Nuptial Mass

`src/gpt/liturgy/roman-rite/1962/propers/ritual/m01-nuptial-mass/propers/verified.md` was checked for the complete 1962 formulary boundary and insertion points:

- *Propitiare, Domine* and *Deus, qui potestate* after the Pater and before *Libera nos*;
- Communion of the spouses after the celebrant receives the Precious Blood;
- *Deus Abraham* after *Ite, missa est* and before the general blessing.

The manual cites the governing general rubrics 378–381 and summarizes only the insertion architecture; the verified proper record remains the fuller textual control.

## High-risk findings and resolutions

| Question | Finding | Resolution in publication |
|---|---|---|
| Are there IV-class feasts? | Code 35–37 classifies feasts I–III; IV belongs to other day and Mass categories. | Repeated warning and separate day/Mass taxonomy. |
| Does “higher class” alone solve occurrence? | Table 91 orders universal/proper and day kinds within the same class; nn. 92–102 separately determine the loser. | Full twenty-eight positions plus a distinct loser-disposition step. |
| Does a II-class saint transfer when accidentally impeded? | General accidental-transfer right in n. 95 belongs to I-class feasts; perpetual reposition is separate. | Cases 6, 9, and 14 distinguish the two. |
| Is First Friday automatic? | Nn. 384–386 require III/IV day, specified place, exercises that day, and a two-Mass ceiling. | Cases 21–22 test all four day classes and the unqualified IV-votive path. |
| Is First Saturday BVM Saturday? | N. 78 creates a IV-class Office; n. 385c creates a III-class Immaculate-Heart votive; n. 317 prevents blending. | Cases 23–24 present separate paths. |
| Does external solemnity transfer the Office? | N. 356 defines it as celebration *without* the Office; nn. 359–360 set date and Mass count. | Case 26 keeps Sunday Office and classifies the Mass as II-class votive. |
| Is every funeral barred on Sunday? | N.393 first bars every Requiem in its listed exposition and one-Mass conflicts; n.406 bars table positions 1–6 and named feasts; n.407 adds a Sunday external solemnity. An ordinary position-15 Sunday is not itself listed. | Case 27 states the conditional 1960 textual result and requires current competent authority. |
| Does every Passiontide Mass omit Psalm 42 and the Introit doxology? | Nn. 425a and 428 say *Missae de Tempore*. | Case 32 preserves them in a superior saint's Mass while applying the seasonal Preface separately. |
| Can a commemoration change readings or Preface? | Nn. 106–114 and 480/505 give prayer triads; n. 483 denies a Preface effect. | Assembly map and every case confine commemorations to prayers. |
| Do octave Canon forms follow only the octave Mass? | N.501 and the annotated Canon texts apply the Christmas *Communicantes*, and the Easter/Pentecost *Communicantes* and *Hanc igitur*, in other Masses even with a proper Preface. | Case 33 treats the exact forms as a genuine overlay without inventing a Christmas *Hanc igitur*. |

## Secondary scholarship and working aids

No secondary handbook was needed to establish the normative algorithm, and no secondary source is cited as if it promulgated a rubric. The reference is intentionally source-first. Historical scholarship on the development of the 1960 reform would be appropriate in a history of the rubrics, but it is outside this practical assembly manual and was not used to create permissions.

OCR text extraction was used as a finding aid to locate rubric numbers and compare repeated terms. It was rejected whenever columns merged, ligatures failed, or a condition crossed a page boundary; the page image then controlled. No automated calendar engine was used to generate a civil-year case.

## Rejected or non-controlling leads

- pre-1960 handbooks and rank charts, because their doubles, semidoubles, octaves, and commemoration rules do not govern the 1962 edition;
- later Roman Missals and anticipated-evening-Mass conventions;
- devotional booklets that state First Friday or First Saturday requests but do not grant a liturgical Mass class;
- unsourced websites, crowd-sourced calendars, and automated Ordines as primary authority;
- a claimed local patron, title, dedication, or indult without the approved proper calendar or grant;
- the inference that a Mass's votive class is a new row in table 91;
- the inference that concurrence at Vespers selects the morning or evening Mass.

## Known limits and review state

- Particular-calendar cases remain logical conditionals and are not verified for any real place.
- Present canonical authorization remains deliberately unresolved and outside scope.
- A second calculation independently recomputed all thirty-five cases from the raw premises and numbered rubrics, with particular attention to Cases 12, 16, 26, 27, 30, and 31. The corrections it identified were incorporated before the final build; the ledger records this completed internal review without representing it as credentialed external or ecclesiastical review.
- Local-calendar cases remain conditionals until the competent approved calendar, supplement, or indult is supplied, and present-law authorization remains outside this edition-historical manual.

## Build and publication record

Initial drafting record created 2026-07-13. After the independent case calculation and final source change, the document was built for two settling passes with `pdflatex` in the repository build tree. The result is a 42-page, US-letter PDF. The final log has no undefined references, overfull or underfull boxes, LaTeX/package warnings, fatal errors, or rerun request.

`pdfinfo` reports the intended title and substantive subject. `qpdf --check` reports no syntax or stream-encoding errors. Every listed font is embedded, subset, and Unicode-mapped. The repository metadata validator accepts the source/PDF pair as one canonical record and finds the model, qualifier, runtime, date, title, and subject present in the required form.

All forty-two physical pages were rasterized and visually reviewed after the final source change, both individually and in three contact sheets. No clipped text, collision, unintended blank page, malformed table, broken checkbox, illegible worksheet, or page-order defect was found. The reviewed PDF was installed in its mirrored catalog path and compared byte-for-byte with the build artifact. Catalog integration and repository guidance were reviewed with the same publication stage; commit integration is recorded by version control rather than asserted in this pre-commit source record.
