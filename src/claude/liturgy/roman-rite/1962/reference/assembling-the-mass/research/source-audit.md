# Source Audit

## Acquisition and identity

| Artifact | SHA-256 | Acquired | Check |
| --- | --- | --- | --- |
| CMAA facsimile of the 1962 Vatican typical *Missale Romanum*, 1,088-page PDF | `648fdb8f…3518a` | 2026-07-26 | Downloaded and hashed; the digest matches the registered artifact record exactly |
| *Acta Apostolicae Sedis* 52 (1960), Holy See scan, 1,132 pages | `c734079d…4702` | 2026-07-26 | Downloaded and hashed; matches the registered artifact record exactly |
| Internet Archive optical transcription of the Benziger 1962 *editio iuxta typicam* | `2a2da44d…585ce` | 2026-07-26 | Downloaded and hashed; matches the registered artifact record exactly |
| Cummiskey 1861 temporal orations, tracked project transcription | `13c2ad6d…f389c9` | in repository | Read in place |
| Douay-Rheims Challoner, tracked per-book transcription, John | in repository | in repository | Read in place |

No artifact bytes were installed into this leaf. Nothing was retained outside the run-owned
temporary tree except the tracked records.

## What was read, and how

**Page images.** Every rule quoted in Latin in the publication was read as a rendered page
image, not merely in an optical text layer:

- Missal facsimile at 260 dpi, artifact pages 10, 15, 16, 18 (bottom crop), 21, 26, 27, 29,
  31, 32, 33, 545, 786.
- *Acta* at 200 dpi, printed pages 708 and 709.

**Optical text layer with layout preserved.** The remainder of the code in both witnesses, the
*Ritus servandus*, the *Ordo Missae*, the prefaces, and the individual formularies named in the
worked cases were read from a two-column-aware text extraction of the same exact artifacts. The
Missal facsimile's optical layer is a 2007 ABBYY product and contains recognition errors
(`Rubrics` for *Rubricae*, `turn` for *tum*, `Missa? festivae` for *Missae festivae*); no
wording in the publication rests on it alone.

**Locating aid.** The Benziger transcription was used only to find where the front-matter
rubrics begin. It controls nothing.

## Findings that changed the publication

1. **The artifact-page offset is +2.** The facsimile's artifact page 13 carries printed p. XV
   and artifact page 34 carries printed p. XXXVI, established from the running heads. Any
   citation that assumes artifact page equals printed folio is wrong by two.
2. **The code as the Missal prints it ends at n. 530.** Checked in both witnesses; the last
   rubric in each is `Usus accendendi cereum … servetur`.
3. **The Missal does not print part two of the code.** Artifact page 18 carries
   `II. - RUBRICAE GENERALES BREVIARII ROMANI (nn. 138-268)` followed by `Hic omittuntur`, read
   as a page image. This is what makes RGMR 431 a unusable from the Missal alone and is the
   reason the *Acta* had to be acquired. It became §10.5 of the publication and the note at the
   head of Section 8.
4. **The Missal does not print the *Tabella occurrentiae*, the *Tabella concurrentiae* or the
   *Notanda*** that follow the code in the *Acta* at pp. 703–705. Established by searching the
   Missal's whole extracted text for those headings and finding only
   `TABELLA DIERUM LITURGICORUM`. Recorded in the publication's Section 3.
5. **The Purification question is closed by the Missal's own rubric.** Artifact page 545 prints,
   under the title of 2 February, `Festum Purificationis beatae Mariae Virginis habetur tamquam
   festum Domini`. Read as a page image. This turned a question the publication was going to
   leave open into §10.4, corroborated by RGMR 484 a and RGMR 495.
6. **RGMR 407 corroborates the reading of RGMR 406 b.** Its clause about an external solemnity
   held on a Sunday presupposes a Sunday on which the funeral Mass would otherwise be possible.
   That argument is the publication's own and is stated as such in §10.1.
7. **The Sacred Heart's Mass has no Tract.** The feast Mass, artifact pages 460–461, prints a
   Gradual and Alleluia only, because the feast never falls between Septuagesima and Easter. A
   votive of the Sacred Heart in Lent therefore meets a slot the Missal does not fill. The
   publication says so in Section 6 and, for that reason, sets Case 4 in Advent rather than in
   Lent.

## Corrections made on re-audit

A second pass re-read the controlling witnesses independently of the drafting pass, recomputed
every civil date from the Gregorian Easter, and re-checked each cited locus. Three defects were
found and corrected; the remainder of the publication survived the check unchanged.

1. **The Gospel of Case 1a was the neighbouring day's.** The draft gave Io. 7, 1–13 for the
   Wednesday after Passion Sunday. That is the Gospel of the *Feria III*, printed pp. 121–122.
   The Wednesday's Gospel, on printed p. 123, is Io. 10, 22–38, *Facta sunt Encaenia in
   Ierosolymis*. Read as extracted text of artifact pages 202–204 with the two-column layout
   preserved. Corrected in the publication and in `worked-cases.md`, which now also records the
   lesson, Gradual and Tract so that the slot is checkable.
2. **Three rubrics were cited under the wrong part of the code.** The code numbers its three
   parts continuously to 530; nn. 439, 518 and 522 are in the third part, *Rubricae generales
   Missalis Romani*, and were cited as `RG` — a shorthand this work defines for the first part,
   which ends at n. 137. Corrected to `RGMR` in five places in the publication and three in the
   research records. The reading of each rubric was unaffected and was re-verified: RGMR 439 is
   the *hanc / hodiernam / praesentem diem* rule; RGMR 518 b names the three Masses of Christmas
   and the Mass of the Annunciation; RGMR 522 b is the choir's genuflection at *Et Verbum caro
   factum est*.
3. **The second part had no shorthand of its own.** nn. 237–238, the Te Deum rule, were also
   cited as `RG`, with a note at each use that they belong to the second part. A third
   shorthand, `RGBR` (*Rubricae generales Breviarii Romani*, nn. 138–268), now carries them, so
   no number is cited under a part that does not contain it. The rule itself was re-read in the
   *Acta*: the volume's own table of contents places nn. 237–239 at printed p. 637, and the text
   there matches the summary the publication prints at the head of Section 8.

One further record was tightened: the facsimile's artifact-to-printed page offset is +2 in the
roman-numbered front matter but +81 in the arabic-numbered body, and `edition-manifest.md` had
stated only the first as though it held throughout.

## Discrepancies noted and not resolved here

- The source-library edition record
  `edition.catholic-church.rubricae-breviarii-et-missalis-romani.latin-missale-romanum-vatican-typica-1962`
  describes the code as `nn. 269-535` and `pp. XIII-XLIII`. Reading the pages establishes
  nn. 269–530 and pp. XII–XXXVI (artifact pages 10–34). The work record carries the same
  `269-535`. That record belongs to another publication's source work and was not edited from
  here; the discrepancy is recorded in this leaf's binding context so that a reviewer sees it.
- The same edition carried no segment record when these bindings were written, so this
  publication pins its extent on the artifact rather than on a segment.

## Consequential negative results

- No Preface is assigned *tamquam de Tempore* for the ferial days of Advent, for Septuagesima
  to Quinquagesima, or for the weeks *per annum*. Searched the whole of RGMR 484–499; the only
  day-based seasonal assignment outside those stretches is RGMR 494 b's, which names Sundays.
  Hence the Common Preface result in Case 1b.
- RGMR 406 contains no reference to second-class Sundays and no reference to rows 14–28 of the
  precedence table. Checked against the rubric's own text.
- The 1962 Missal contains no rule supplying a Tract for a votive Mass whose formulary prints
  none. Searched the Missal's general rubrics for the Septuagesima Alleluia/Tract substitution
  and found it only in the per-Mass directions printed with individual formularies.

These are bounded results about the exact texts read. They are not claims about what a
rubrical commentary or an authorised response may supply, and no commentary was consulted.

## Build, review and conversion

- **Build.** Two settled `pdflatex` passes from `src/claude` with `TEXINPUTS=..:`, matching the
  repository recipe. The final log is free of warnings, overfull and underfull boxes, undefined
  references and errors. The document settles at **40 pages** across consecutive passes.
- **Page review.** Rasters generated with `scripts/pdf-review` into a run-owned directory.
  Every one of the 40 pages was inspected at full size. Three layout faults were found and
  fixed: the sixteen-preface table was rebuilt with a wider third column after the Nativity row
  produced a ragged column two lines wide; consecutive paragraphs inside the synthesis, contested
  and worked-case boxes were butted together because `tcolorbox` zeroes `\parskip`, and the
  paragraph separation was restored inside those environments; and the reference tables' first
  column touched the second, which was fixed by widening the column separation. The final-page
  rights colophon is readable, unclipped, non-overlapping and creates no rights-only page. The
  re-audit above repeated the two-pass build and the full 40-page raster review after its
  corrections; the log remained free of warnings, overfull and underfull boxes, undefined
  references and errors, the document still settles at 40 pages, and no further layout fault
  was found.
- **Gates.** `scripts/check-web-edition` and `scripts/web-edition` were run against this leaf;
  results are recorded below. `scripts/source-library validate` reports no error for this
  leaf's bindings or for the source record added by it.
- **Not done here.** The PDF was not installed to `doc/`, no catalog page was edited, and
  nothing was committed. Those are separate authorizations.

## Review boundary

This is a source audit performed by the authoring agent. It is not independent specialist,
theological, canonical or liturgical review; it is not an Ordo; and it is not an ecclesiastical
approval. No result in the publication has been checked against a published Ordo for the year
it names, and no rubrical manual or authorised-response collection was consulted.
