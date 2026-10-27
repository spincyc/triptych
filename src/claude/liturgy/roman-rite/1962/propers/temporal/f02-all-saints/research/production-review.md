# Production review record

Run-specific production and review facts for the Claude 1962 leaf
`liturgy/roman-rite/1962/propers/temporal/f02-all-saints` (catalog `F02`,
*In festo omnium Sanctorum*), `proper-study` v15, run `427e2f58bb897a16`,
seeded at commit `c7dfb84c76a057079251e8c918243b787fa69494`. Research and its
cold review precede this record; their evidence is `research/scope.md`,
`research/interpretations.md`, `research/context.md` and `propers/verified.md`,
which this record does not restate.

## Author-study, iteration 0 (27 October 2026)

**Scope.** The expansive study (`main.tex`) of the Mass of All Saints said on
Sunday 1 November 2026 in the universal 1962 calendar, with the commemoration
of the Twenty-third Sunday after Pentecost: the opening with the occurrence,
the three questions and an element map; the appointed Latin of the fourteen
said elements (the feast's ten texts and the Sunday's three commemorated
orations, with a Preface locator) with their public-domain English; the
element-by-element settings; three interpretations of the whole formulary
(`sealed-number-uncounted-crowd`, `beatitudes-way-of-the-saints`,
`no-want-just-in-gods-hand`), each with its own four senses; a comparison; the
Scriptural Date and Location appendix on the eight generated `orientation-v2`
rows; the scope appendix and References. The schema-2
`proper-components.toml` declares the future concise and homily components and
the `interpretive-pagination-v1` presentation roles; the leaf-local
`format.tex`, `web-edition.toml` (eligible) and `generation-metadata.tex` were
written.

**Element keys.** Fourteen, in the order of the Mass: `introit`, `collect`,
`commemoration-collect`, `lesson`, `gradual`, `alleluia`, `gospel`,
`offertory`, `secret`, `commemoration-secret`, `preface`, `communion`,
`postcommunion`, `commemoration-postcommunion`. The `preface` anchor stands at a
locator that names the Trinity Preface (p. 293, no. 1082) and the common
Preface (p. 297, no. 1086) as the two readings of RGMR 482, 483, 494 b and 498,
gives neither text and asserts neither, as `research/context.md` leaves the
question.

**Extent.** 29 physical pages (letter, Latin Modern, 11 pt). Approximate prose
word counts by component, LaTeX markup excluded: opening 1,540; appointed texts
3,060 (the set Latin and English included); each element 2,350; the three
interpretations 2,450, 2,150 and 2,270; comparison 800; Scriptural Date and
Location 860; scope and References 1,280. The exposition proper (opening, each
element, interpretations and comparison) is about 11,550 words, somewhat above
the profile's 6,000–10,000 planning range; the range is not a quota, and the
PDF is within the 20–50-page extent.

**Interpretations and their carrying authors.** First: Bede and Augustine of
Hippo, with Gregory the Great as cited by Fromage, Schuster and Durandus in
support. Second: Augustine of Hippo, John Chrysostom, Thomas Aquinas and
Hilary of Poitiers, with Rabanus Maurus as a compiler of Augustine. Third:
Basil of Caesarea, Robert Bellarmine, Augustine of Hippo and Thomas Aquinas,
with Gregory the Great, Chrysostom, Schuster and Durandus on particular
claims. Schuster, Lucien Fromage and William Durandus carry no interpretation.
Augustine is not presented as commenting on the Lesson's chapter.

**Source limits carried into the study.** The Lasance English of the Lesson's
and the Gospel's liturgical openings and of the Offertory is quoted on the
Lasance's attribution and disclosed as not checked against the repository's
translation register, which has no row for the Lasance's scriptural English.
The history of the Offertory's wording rests on the 1570 text layer and on the
OCR text layers of the 1604, 1862 and 1889 printings; when its *alleluia*
entered is stated as not established. Jerome on Matthew, Bernard's All Saints
sermons and Gregory of Nyssa on the Beatitudes are named in the scope appendix
as not read. The NABRE is used only as the chronology corpus cites it, in
summary. Bellarmine's verse numbers for Psalm 33 are given as his, one lower
than the Vulgate's.

**Author proof.** `make doc` with the Claude provider settled with no
undefined references, no overfull or underfull boxes and no hyperref warnings;
the manifest and generation-metadata checks passed. `check-proper-components`
in the artifacts phase for the research edition passed. The web-edition
conversion probe completed and wrote its Markdown. Every page of the proof
was inspected at contact-sheet resolution.

**Defects reported for other owners (not repaired here).** The shared
appointment test asserts the common Preface for this Mass without an
authority; the calendar entry `omnium-sanctorum` has no Sunday Preface case,
marks its scriptural bodies' wording as not established and gives over-wide
ranges for the Gradual, Gospel and Offertory, which the chronology loci
inherit (the Gospel row prints Mt 5:1–12 for the Missal's 5:1–12a, and the
Psalm 33 superscription row reaches Ps 55 by inheritance); the formulary-loci
record lists no commentators; the author-standing inventory lacks rows for
Bernard, Victorinus, Cyprian, Gregory of Nyssa, Alphonsus, Athanasius, Peter of
Celle and Murphy; Bede on Apoc 7:2–3 has only a whole-text layer and no
passage records; the Latin provenance ledger lacks the six scriptural rows; the
Lasance scriptural English has no inventory row; the PL 202 containment record
lacks Peter of Celle; the FSSPX ordo record does not list French among its
languages. Research advisories RES-006 and RES-014 to RES-018 remain with the
research owner.

## Author-study, iteration 1 (27 October 2026)

**Finding repaired.** The house-voice gate (`GATE-HOUSE-VOICE`) refused four
reader sentences, all in the research edition: two in the appointed texts
that made the repository the possessor of the translation register, one that
told the Preface's negative result as a search "consulted for this study",
and one in the third interpretation that dated the Offertory's *alleluia* by
"the printings read for this study". Each was rewritten with a source, a text
or a fact as its subject, and nothing it stated was dropped:

- The Lasance English of the Lesson's opening and of the Offertory is still
  quoted on the Lasance's attribution alone, and the body still says that the
  register of translations behind the Lasance English of the Introit and the
  orations has no entry for it; the scope appendix's statement of the same
  bound is unchanged.
- The Preface note now states that neither reading is settled by the rubrics
  it cites, and keeps the sentence that the interpretations rest on neither
  Preface's words. The fuller search bound (the other rubrical sources
  searched, as `research/scope.md` lists them, none settling the case) moved
  to the scope appendix's paragraph on edition, formulary and occurrence.
- The third interpretation names the five Missal printings over which the
  Mame of 1922 is the first to show the *alleluia* (1570, 1604, 1862, 1889 and
  1922), the same denominator the appointed-texts note on the Offertory gives.

**Scope and extent.** No section, interpretation, element key, citation or
research claim changed. The substantive word count moves by fewer than
thirty words from the iteration-0 figures above. The proof remains 29
physical pages.

**Author proof.** `make doc` with the Claude provider settled with no
undefined references, no overfull or underfull boxes and no hyperref
warnings; the manifest and generation-metadata checks passed;
`check-proper-components` in the artifacts phase for the research edition
passed; the house-voice preflight for the research edition passed over its
eleven reader-facing files; and the web-edition conversion probe completed.
The five pages carrying the changed sentences (6, 8, 9, 23 and 27) were
inspected at raster resolution. The generation record carries this
iteration's contribution and a fresh revision timestamp.

**Defects reported for other owners.** Those listed under iteration 0 stand
unchanged; this iteration found no new one.
