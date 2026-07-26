# Source Audit

All acquisitions and checks below were made on 2026-07-25 unless stated otherwise. Exact artifact
identities, hashes, rights bases and passage ranges are registered under `src/sources/works/`; this
file records what was done with them for this publication and what was not.

## Artifacts acquired and checked

| Artifact | Identity check | What was read |
| --- | --- | --- |
| *Missale Romanum*, editio typica tertia, digitally typeset secondary reproduction, 828 pp., SHA-256 `0b458944…5523d7` | re-acquired independently for this leaf; its SHA-256 matched the value already registered in the repository from an earlier acquisition | the ranges listed in the edition manifest |
| *Ordo lectionum Missae*, editio typica altera 1981, page-image scan, 600 pp., SHA-256 `ed4bc14e…f7fd0d` | newly registered for this leaf; hash computed on acquisition | *Praenotanda* 65, 66, 69, 103, 104 and both decrees, each rendered at 190-200 dpi and read as an image |
| Acta Apostolicae Sedis 62 (1970), Holy See OCR PDF, 963 pp., SHA-256 `35c99b4f…45b8bd` | newly registered; hash computed on acquisition | printed pp. 651-663, the complete instruction *Calendaria particularia* |
| *Sacrosanctum Concilium*, Holy See Latin web state, SHA-256 `a0e7f540…568fb3` | re-acquired; hash matched the registered value | arts. 102-111 and the appended calendar declaration |
| *Codex Iuris Canonici*, Book IV, Holy See Latin web state, SHA-256 `853b93dd…4e4b27` | re-acquired; hash matched the registered value | can. 1246 §§1-2 |
| USCCB *Liturgical Calendar* 2026, 61 pp., SHA-256 `4bd9add0…372d02` | newly registered | front matter pp. 7-9 and the daily entries needed to fix week numbering |
| USCCB *Liturgical Calendar* 2027, 63 pp., SHA-256 `d7997b57…8074ce` | newly registered | same ranges |
| USCCB *Liturgical Calendar* 2028, 61 pp., SHA-256 `2115e024…663316` | newly registered | same ranges |

## Verification events

1. **Image collation of the Lectionary loci.** The OCR text layer of the 1981 scan is defective in
   places: it mangles the footnote reference number attached to n. 66 and corrupts several lines of
   n. 104, including the opening clause of its numbered rule. Every passage used
   in the publication was therefore rendered as an image and read there. The published Latin follows
   the image, not the text layer. This is the reason the OCR layer is registered as a discovery aid
   and the artifact is marked non-indexable.
2. **Recomputation of the *Tabella temporaria*.** All twenty-four rows for 2000-2023 were parsed
   from the artifact and recomputed from the Gregorian computus and the norms, field by field:
   Sunday cycle pair, Ash Wednesday, Easter, Ascension, Pentecost, last Ordinary Time day before
   Lent, last pre-Lent week number, first resumed day, first resumed week number, First Sunday of
   Advent. Nineteen rows agree in every field. Five rows - 2004, 2008, 2012, 2016, 2020 - give both
   February dates one day early; the printed Ash Wednesday in each is a Tuesday. The sixth leap year
   in range, 2000, whose Ash Wednesday falls on 8 March, agrees in every field. The week numbers
   agree in all twenty-four rows. The page image of the table was inspected to confirm that the
   discrepancy is in the artifact's values and not an artefact of text extraction; that inspection
   also disclosed that the artifact renders the printed ruled table as running lines.
3. **Three years checked against the territorial calendar.** For 2026, 2027 and 2028 the following
   were computed from the norms and then compared with the Secretariat's calendar: the two First
   Sundays of Advent bounding the year, Ash Wednesday, Easter, the Thursday and Sunday Ascension,
   Pentecost, the Sunday Body and Blood of Christ, Christ the King, the Epiphany and Baptism Sundays,
   the pre-Lenten Sunday numbering, the label of the Monday after Pentecost, the first numbered
   Sunday after Pentecost, and both Lectionary cycle labels with their intervals. All agreed. In
   2026 the Secretariat's Liturgy of the Hours table independently shows the same omission by
   assigning volume III to "Weeks 1 to 6" and then "Weeks 8 to 17".
4. **Range check of the arithmetic.** The Ordinary Time computation was run for every year from 1900
   to 2100. `L` ranges 4-9, `R` ranges 6-11, `R − L` is always 1 or 2, the omitted week is always one
   of V to X, and 137 of 201 years are thirty-three-week years. The equivalence of Universal Norms 40
   with the "fourth Sunday before 25 December" formula was checked over the same range and holds in
   every year.
5. **Cycle formulas checked at their origin.** The 1969 decree names series B and series II for the
   liturgical year beginning 30 November 1969. That year ends in civil 1970; 1970 leaves remainder 2
   on division by three, giving B, and is even, giving Cycle II. Both published formulas reproduce
   the promulgated starting point.

6. **Independent audit, 2026-07-26.** A second agent session re-ran the whole verification from
   scratch rather than accepting the results above, and re-acquired the two artifacts it needed. The
   *Missale Romanum* reproduction and the USCCB 2026 calendar were downloaded again and both hashed
   byte-identical to the values registered here. Every Latin passage published from the Missal
   artifact — Universal Norms 1, 3, 4, 5, 10, 14, 15, 16, 43, 44, 48, 49, 52, 55, 56 f, 59 with the
   complete Table of Liturgical Days, 60, 61; the *Tempus per annum* rubrics 1-3; the *In Baptismate
   Domini* rubric; the January rank-convention footnote; the *Hebdomada I* and *Hebdomada XXXIV*
   headings; the Christmas ferial heading; the Epiphany rubric; and General Instruction 355, 357,
   358, 372, 374, 375 — was re-read at its locus and matched the published wording. The twelve-year
   computed table, the three worked years entry by entry, the 1900-2100 range results, and all
   twenty-four *Tabella temporaria* rows were recomputed independently and reproduced every
   published figure. Three defects were found and corrected, and are recorded below.

## Defects found by the independent audit and corrected

1. **Liturgy of the Hours span misread (published claim, corrected).** The 2026 worked year stated
   that the Secretariat assigns volume III to "Weeks 1 to 6" *from 30 November* to 17 February. The
   table on p. 8 of the 2026 calendar assigns 30 November 2025 - 11 January 2026 to volume I
   (Advent, Christmas) and 12 January - 17 February to volume III; the row boundary had been read
   one line high. The publication now gives the span as 12 January to 17 February and also reports
   the volume IV row. The corroboration the sentence was making — the gap between weeks 6 and 8 —
   is unaffected.
2. **Misattributed General Instruction article (published claim, corrected).** The first synthesis
   block attributed the caution against omitting the assigned weekday readings, with its reason that
   the Church desires a richer table of God's word, to General Instruction 358. It stands at
   General Instruction 355, as the same publication states correctly in its section on the table of
   liturgical days. Article 358 carries the neighbouring rule that the ferial readings are ordinarily
   taken on the days to which they are assigned. Both are now cited at their own numbers.
3. **Loose citation of the exclusions attaching to a solemnity (published claim, corrected).** The
   grade table cited General Instruction 372 and 374 for the exclusion of ritual Masses, Masses for
   various needs and votive Masses. In the artifact, 372 prohibits ritual Masses on solemnities, 374
   excludes solemnities from the grave-need Mass, and it is 375 that confines votive Masses to
   weekdays in Ordinary Time. The three are now cited separately, and passage records for 372 and
   374 were registered, 375 having already been registered.

Two smaller matters of quotation precision were also settled against the artifact. Universal Norms 1
is quoted only as far as its third sentence and now carries an ellipsis. The provision displacing the
Baptism of the Lord to Monday was described as printed identically in two places; the *In Baptismate
Domini* rubric reads *quæ die 7 vel 8 ianuarii occurrit* while the footnote under January in the
General Roman Calendar reads *quæ incidit die 7 vel 8 ianuarii occurrit*. The publication now quotes
the rubric and reports the variant.

## Consequential negative results

- **No ecclesiastical statement of the Easter computus.** The 2002 typical edition was searched for
  "tabella", "epacta", "numerus aureus", "littera dominicalis" and "computus"; the only hit is the
  *Tabella temporaria* itself. The conciliar declaration presupposes the Gregorian computation
  without stating it. The publication states the rule as an inherited rule of the Gregorian calendar
  and says so.
- **Appendix I of the Missal artifact is empty.** The artifact prints the heading `APPENDIX I -
  CANTUS VARII IN ORDINE MISSAE OCCURRENTES` and then proceeds directly to Appendix II. The formula
  *Annuntiatio Paschae festorumque mobilium*, listed in the edition's own index at p. 1247, could
  therefore not be read. The publication cites the Epiphany rubric that points to it and records the
  omission.
- **Two Roman acts not reached.** The Holy See's portal was queried for the Latin text of the 2018
  decree inscribing the Blessed Virgin Mary, Mother of the Church, and for the 1998 notification on
  the Immaculate Heart. Neither was served at the paths tried. Both are reported in the publication
  from the territorial calendar and marked as reported.
- **USCCB complementary-norm page refused access.** The Conference page carrying the complementary
  norm to canon 1246 §2 returned HTTP 403 to this session. Its effect is reported from the
  Secretariat's 2026 calendar.
- **No amendment to the Table of Liturgical Days after 1969 located.** Bounded over the sources
  consulted.

## Rejected and unused leads

- The approved English translations of the Universal Norms and of the Introduction to the Lectionary
  published by the Bishops' Conference of England and Wales were available and were deliberately not
  quoted: the Latin was used instead, and no approved translation appears in the publication.
- Commercial and devotional calendars, aggregation sites and search-engine summaries were not used
  for any claim.

## Discrepancies preserved rather than resolved

1. The leap-year February dates of the *Tabella temporaria*, described above. The publication states
   the balance of probability as a labelled project judgment with its counterargument, and rests no
   other claim on it.
2. Universal Norms 33 ends Christmas Time at "the Sunday after 6 January", while the Missal's own
   ferial heading runs the season's weekday Masses "to the Saturday before the Feast of the Baptism
   of the Lord" and its rubric moves the Baptism to Monday when the Epiphany falls on 7 or 8 January.
   The publication reports both and explains which governs which use.
3. Universal Norms 44 ends Ordinary Time "before Evening Prayer I of the First Sunday of Advent";
   the Missal's rubric 1 ends it "on the Saturday before the First Sunday of Advent". The publication
   reports both and states that the difference is one liturgical evening.
4. The Secretariat states the Sunday cycle interval by its first and last Sundays and the weekday
   cycle interval by its first and last weekdays. Neither is the liturgical year's own boundary. The
   publication reports the practice and explains it rather than harmonising it.
