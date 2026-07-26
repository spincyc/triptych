# Source Audit

Acquisition and collation for this leaf were performed on 2026-07-25; the independent re-audit,
recomputation, and the identity correction recorded below on 2026-07-26. Exact artifact identities,
hashes, rights bases, and page ranges are registered under `src/sources/works/`; this file records
what was done with them for this publication and what was not.

## Artifacts used

| Artifact | Registered identity | Identity check | What was read |
| --- | --- | --- | --- |
| *Acta Apostolicae Sedis* 52 (1960), the Holy See's own OCR PDF | `artifact.holy-see.acta-apostolicae-sedis.volume-52-1960.vatican-ocr-pdf-c734079d`, SHA-256 `c734079d…4702` | hash recomputed on the retained working copy during the re-audit and matched the registered value byte for byte | printed pp. 593-596 (the two promulgating acts); pp. 597-621 (*Rubricae generales*, nn. 1-137) in full; the Missal chapters named in the edition manifest; *Variationes*, Caput I nn. 1-12 and Caput II n. 13; pp. 598 and 599 additionally as rendered page images |
| *Missale Romanum*, editio typica 1962, Church Music Association of America facsimile | `artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf`, SHA-256 `648fdb8f…518a` | re-downloaded during preparation of this edition and hashed byte-identical to the already-registered value | the ranges named in the edition manifest, with the calendar pages and paschal tables read as rendered page images |
| Pre-1955 comparison Missal, Internet Archive DjVuTXT derivative | `artifact.catholic-church.missale-romanum.unidentified-pre-1955-witness-ia-1947.ia-djvu-ocr-724a04fa`, SHA-256 `724a04fa…4bcb` | hash recomputed on the retained working copy during the re-audit and matched | title page, copyright line, and approval leaf; the resumption rubric; the Ember Day note; *Additiones et Variationes* nn. on occurrence and on the number of orations; the general rubrics scanned for a precedence table |
| Benziger *editio iuxta typicam* 1962, Internet Archive DjVuTXT derivative | `artifact.catholic-church.missale-romanum.benziger-iuxta-typicam-1962.ia-djvu-ocr`, SHA-256 `2a2da44d…85ce` | hash recomputed on the retained working copy and matched the already-registered value | the front-matter Ember Day note only |

No payload of any of these is retained in the repository. All four carry `rights_status =
"unresolved"`; quotation is limited to the rules the publication states.

## Method

Optical text layers were used to **locate** passages and never to **establish** a reading. Every
reading reported as a divergence was read in a rendered page image at 260 to 450 dpi, on both sides
of the comparison. Computations were performed independently from the Gregorian ecclesiastical rule
and then checked against the Missal's own printed tables; where they disagree, the disagreement is
reported and not resolved by preference.

## Verification events

1. **Latin loci re-read against the Acta.** The following were re-read in the Acta text for the
   re-audit and match the publication's quotations: nn. 4, 7, 8, 9-20 (the whole Sunday chapter),
   64, 91 (the complete twenty-eight-line table), 95, 100-102, 109, 110, 111 a-d, 112 a-d, 113, 114.
   Missal-side: the trigger rubric printed after the Twenty-third Sunday after Pentecost and the
   front-matter note *De anno et eius partibus*.
2. **The four Acta/Missal divergences confirmed.** In the Acta text: n. 14 is printed with the
   numeral **11** between correct 13 and 15; nn. 15 and 16 both read *servetur norma, quae
   nn. 101-105 traditur*; n. 18 d reads *et XVII, quae inscribitur VI*. The Missal reads 14,
   *nn. 104-105*, and *XXVII* respectively. Each Acta reading is impossible on its face and each
   Missal reading is not. The volume's own *Corrigenda* records one correction, to p. 179, and does
   not reach pp. 598-599.
3. **The Missal decree's date divergence confirmed.** The 23 June 1962 decree recites *Motu proprio
   "Rubricarum instructum" diei 23 iulii anno 1960 … posteroque die … promulgato*; the same volume
   reprints the letter with its own date of 25 July 1960, and the promulgating decree is of 26 July.
   23 July plus one day is not 26 July, so the decree is inconsistent with the book carrying it.
4. **Computation recomputed independently.** Easter, Septuagesima, Ash Wednesday, the Passion
   Sundays, Palm Sunday, Low Sunday, the Rogation days, the vigils of the Ascension and Pentecost,
   the Ascension, Pentecost, Trinity, Corpus Christi, the Most Sacred Heart, the First Sunday of
   Advent, the three sets of Ember days, Christ the King, the Twenty-third Sunday after Pentecost,
   the last Sunday after Pentecost, and the counts *E*, *P*, and *S* were recomputed from the
   Gregorian ecclesiastical rule for 1900-2100 and compared with every dated figure the publication
   prints. Results are in the evidence map. The distributions, the extreme years, and every anchor
   in the four worked years agree.
5. **One dating error found and corrected.** An earlier revision stated that 19 March 1962 falls on
   the Monday after the **First** Sunday of Lent. Ash Wednesday 1962 was 7 March, so the Sundays of
   Lent were 11, 18, and 25 March and 19 March is the Monday after the **Second**. Corrected in
   `sections/85-worked-years.tex`; the rubrical analysis attached to the date was unaffected, since
   19 March 1962 is a Lenten feria of the III class either way.
6. **One evidence ceiling found to be wrong and corrected.** An earlier revision, and the source
   records behind it, stated that the pre-1955 comparison witness "carries no publisher, imprint,
   approval leaf, or typical-edition relation". That is true of the hosting item's metadata and
   false of the scan. The book's own opening leaves name Benziger Brothers, Inc., New York, printers
   to the Holy See and the Sacred Congregation of Rites; declare it *editio IV iuxta typicam
   Vaticanam*, *a Pio X reformatum, Benedicti XV auctoritate vulgatum*; carry a copyright line dated
   1942 and 1944; carry an approval leaf subscribed by Francis Joseph, Archbishop of New York, at
   New York on 8 December 1942, reciting conformity with the typical edition and with the decree of
   the Sacred Congregation of Rites of 9 January 1942; and reprint the Congregation's decree of
   25 July 1920 declaring the Vatican edition typical. The witness is therefore an identified
   licensed edition conformed to the 1920 typical edition, of unestablished printing year. The
   publication's ceiling, references, collation section, and synthesis were rewritten accordingly,
   and the edition and artifact records were corrected. The hosting item's "1947" remains
   uncorroborated and the directory slug was left unchanged to avoid breaking bindings.
7. **The Missal-side exclusivity test run.** Because the witness turned out to be identified, the
   test the synthesis names as decisive could be run on the Missal side. The pre-1955 *Rubricae
   generales Missalis* and *Additiones et Variationes* in that witness carry no table of precedence
   and no exclusivity clause; they resolve occurrence by the comparative *Officium nobilius*. The
   pre-1955 tables of occurrence and concurrence belonged to the Breviary, which this witness is
   not, so the Breviary side of the test remains unrun. Reported as a bounded negative result.
8. **Three further readings recovered from the same witness** and cited at their places: the
   pre-1960 resumption of an impeded Sunday's Mass on a free weekday of the following week
   (*Additiones et Variationes*, *De occurrentia et de translatione festorum*, n. 6), which n. 14 of
   the 1960 code abolishes; the pre-1960 ceiling requiring that orations *septenarium numerum non
   excedant, atque imparem praeterea numerum*, against which Missal rubrics n. 435's flat ceiling of
   three is measured; and the pre-1955 form of the Ember Saturday ordination rule.
9. **The September Ember change corroborated from a second 1960-code book.** The Benziger *editio
   iuxta typicam* of 1962 prints *post dominicam III septembris*, agreeing with the Vatican typical
   edition against the earlier Benziger printing. Two independently produced books conformed to the
   1960 code therefore agree against the pre-1955 wording, so the divergence is between states of
   the rule and not between compositors.
10. **The 1996 cell of the *Tabella temporaria*.** The printed value 16 is outside the possible
    range; the same book's perpetual *Tabula paschalis antiqua reformata* gives 26 for the same
    combination; and computation agrees with the perpetual table (26 May to 1 December is 189 days,
    that is 27 weeks, so *P* = 26). Reported as a defect of the temporary table, not corrected
    silently.

## Rejected leads and things not done

- No dated Ordo under the 1960 rubrics was located or read, for any year. This is why the
  twenty-three-Sunday case and the classification of the Dedication of the Archbasilica remain open.
- A machine tally of the Acta's own *Calendarium* was run and was not reliable enough to publish; no
  count of III class entries or commemorations is asserted anywhere.
- No second exemplar of either controlling printing was consulted, so a defect peculiar to the copy
  scanned cannot be excluded from the collation findings.
- No official ecclesiastical statement of the paschal computus was located. The rule used is the
  standard Gregorian ecclesiastical rule; its use is justified in the publication only by agreement
  with the Missal's own printed tables over the fifty-two dated rows checked, not by asserting a
  Church text for it.
- Devotional and commercial 1962 calendars were not used, as finding aids or otherwise.

## Discrepancies carried into publication

| Discrepancy | Where reported | Disposition |
| --- | --- | --- |
| Acta n. 14 numbered 11 | collation section | Acta misprint |
| Acta nn. 15, 16 cite nn. 101-105 for concurrence | collation section | Missal reading substantively right; concurrence is nn. 103-105 |
| Acta n. 18 d reads XVII for XXVII | collation section | Acta misprint |
| 1962 Missal decree dates *Rubricarum instructum* to 23 July | collation section | Missal misprint; internally inconsistent |
| *Tabella temporaria* prints 16 for 1996 | collation section | printing or scanning defect; perpetual table and computation both give 26 |
| September Ember dating differs between the pre-1955 and the 1960-code books | collation section | change observed; instrument and date not established |
