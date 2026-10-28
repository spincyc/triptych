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

## Author-study, iteration 2 (27 October 2026)

**Findings repaired.** Six blocking findings carried from the iteration-1
study review (STU-002 to STU-007), all against the study's prose:

- STU-002 (each interpretation omitted appointed texts, and the comparison
  admitted the division). Each interpretation now shows, in proportion, how
  the texts it had passed over bear on its reading. The first says how the
  Gospel's blessings and the Communion's clean of heart bear on who the
  sealed are, and touches the Alleluia, the Secret and the commemorated
  Secret; the second takes up the Lesson's multitude in white robes and
  palms as the way's end (Bede's robes as baptism and the palms as the
  cross's triumph, marked as this interpretation's own inference) and
  touches the Secret, the Postcommunion and the commemorated orations; the
  third reads the Lesson's crowd before the throne as the promise shown
  kept, and touches the Introit (Bellarmine's "special duty of the just")
  and the Communion (the vision of God, Bellarmine's higher sense). The
  comparison table's row is renamed from "Texts it starts from" to "Where
  its question presses hardest", the shared-texts paragraph now says the
  three meet in the same texts and read them differently, and the closing
  admission is gone.
- STU-003 (a four-Father agreement on the beatitude tenses that the
  witnesses do not hold). The summary sentence is replaced: the
  two-present, six-future observation is stated once as this study's own,
  and each Father's resolution is set out separately — Augustine (the
  promises can be fulfilled in this life, as in the apostles; the change
  into the angelic form after it), Aquinas (begun on the way, completed in
  the homeland), Chrysostom (both here and there), Hilary (the vision for
  those perfected and changed) — with Hilary's difference from Augustine
  kept. The anagogical sense is divided per witness.
- STU-004 (Aquinas's temporal sense omitted). *Super Psalmos* 33 n. 10 is
  now given whole: spiritual goods first, then bodily goods (contentment
  with what one has, Phil 4:11–12, and God's help in necessity, *Item Deus
  quaerentibus se subvenit in necessitate*), then the objection in
  Augustine's name and the physician answer. The clause was verified in the
  registered Parma vol. 14 OCR artifact (physical line 42640, between the
  contentment clause and *Sed objicit Augustinus*; the OCR reads
  "qtiaerenlihus"). The difficulty and the comparison now say that a
  temporal sense is kept by Bellarmine, as the humbler meaning, and by
  Aquinas, as God's help in necessity; "every witness refuses" and
  "Bellarmine alone" are gone.
- STU-005 (Fathers credited with the study's synthesis). The opening and
  the three interpretation openings now credit each Father only with the
  clause he states at his locus — Bede's number as the whole Church and
  the seal as the sign of the cross, Augustine's rejoicing in the Lord and
  not in themselves; each of the four on the Beatitudes with his own
  clause, none of them said to comment on the feast; Basil's lack of
  nothing for any virtue and the perfect good as God himself — and the
  feast-level conclusions stand in the study's own voice ("Read together,
  …"). Basil's position is now consistent between 40 and 50.
- STU-006 (procedural and disclaiming clauses). Removed from the body of
  05, 10, 20, 30, 40 and 50, including the finding's given rewrites
  ("Taken together, Bede's two comments give the number as the Church's
  completeness and the multitude as its extent"; "The feast's prayer asks
  for the saints' defence, and the Sunday's asks for protection from human
  dangers"; "The witnesses still disagree on the census, on the land of
  the meek and on the rich who lack"). The translation-register and
  compilation bounds remain in the scope appendix, where they already
  stood.
- STU-007 (maxim closers and staged antitheses). The restating closers are
  cut and the antitheses made positive, including the finding's given
  rewrites ("For Aquinas, the want of the God-fearing is given for their
  health"; "Their answers differ in what they say is promised: God himself
  (Basil, Bellarmine), the virtues (Augustine), and want that serves
  salvation (Aquinas)"; "In each interpretation holiness begins in what
  God gives: the seal, the humility of the first beatitude, the fear the
  Gradual commands").

**Scope and extent.** No section, element key, interpretation or citation
was added or removed, and the comparison keeps its table, with the one row
renamed. Measured with one simple method (LaTeX markup excluded,
approximate), the prose is now: opening 1,530; appointed texts 3,140; each
element 2,290; the three interpretations 2,640, 2,360 and 2,430; comparison
875; Scriptural Date and Location 850; scope and References 1,355 — about
17,470 words in all, against the iteration-0 record's 16,760. The method
lands within about eighty words of the earlier figures on the unchanged
sections; the real movement is the roughly 560 words the repairs add to the
three interpretations and the comparison, less the smaller register cuts in
the opening, the appointed texts and the element section. The proof grows
by one page, to 30 physical pages, within the 20–50-page extent.

**Author proof.** `make doc` with the Claude provider settled with no
undefined references, no overfull or underfull boxes and no hyperref
warnings; the manifest and generation-metadata checks passed;
`check-proper-components` in the artifacts phase for the research edition
passed; the content preflight for the research edition, including the
house-voice gate, passed over its eleven reader-facing files; and the
web-edition conversion probe completed, with all fourteen
`proper-<element-key>` anchors present exactly once. The contact sheet and
the nine pages carrying changed passages (3, 11, 14, 15, 16, 20, 22, 23 and
25) were inspected at raster resolution. The proof PDF is
`build/claude/liturgy/roman-rite/1962/propers/temporal/f02-all-saints.pdf`,
sha256 `57b4974370fdb2864fb959230232c00fb1d717e7e2346f7d6e0c468db906584a`
(30 pages); proof copies, logs and rasters are under this run's
`artifacts/author-study-2/`. The generation record carries this iteration's
contribution and a fresh revision timestamp.

**Defects reported for other owners.** Those listed under iteration 0 stand
unchanged. One new research-record defect: `research/scope.md`'s passage
record for Aquinas's *Super Psalmos* on Ps 33:9–11 (and the §5.2 synthesis
that follows it) omits the temporal clause the Parma text carries at n. 10
(*Item Deus quaerentibus se subvenit in necessitate*), which stands in the
registered artifact
`src/sources/works/thomas-aquinas/opera-omnia-volume-14/editions/1863-parma/artifacts/ia-complete-ocr-02c6dc25/aquinas-parma14.txt`
at physical line 42640, between the contentment clause and *Sed objicit
Augustinus* (the OCR reads "qtiaerenlihus"). The study now quotes the
clause from the artifact; the scope record should be reconciled by the
research owner.

## Author-study, iteration 3 (27 October 2026)

**Finding repaired.** One blocking finding carried from the iteration-2
study review (STU-013, repair target: study): the STU-001 research repair
had landed in the research records, but its study-side consequence had not,
and the first interpretation still rested its Lesson argument on Bede alone
behind a false sentence.

- The false sentence in section 20 (of Augustine, that "he says nothing of
  the seal or the number") is corrected. The Augustine subsection is
  retitled "St Augustine: the whole body of the saints, rejoicing in the
  Lord" and presents his three brief loci on the Lesson's chapter as the
  short applications they are, never as an Augustinian commentary on the
  chapter: *De doctrina christiana* III.35.51 (twelve into twelve is 144,
  the number "used in the Apocalypse to signify the whole body of the
  saints", with the Tichonius attribution caveat kept), *Letter XCIII* §30,
  and Sermon LXI (Benedictine CXI) 1.
- Victorinus of Pettau now stands as the first interpretation's second
  developed witness on the Lesson, in his own subsection ("Victorinus of
  Pettau: the angel as Elias, the number in the last times",
  `sec:sealed-victorinus`): on 7:2 the ascending angel is Elias, the
  precursor of Antichrist's times, not the Lord incarnate; on 12:6 the
  144,000 are those who believe at Elias's preaching in the last times; on
  7:9 the uncounted crowd is the elect out of all believers, Jews and
  nations, cleansed by baptism in the Lamb's blood — agreeing with Bede on
  the crowd, disagreeing on the angel and the number, with "Nor must we
  look for order in the numbers" quoted. The ANF editors' recension
  caution is given with the quotations: corrupted and interpolated
  manuscripts, the Genseric interpolation, a possible later Augustinian
  corrector, an uncertain author, and the gaps at verses 3–8 and 10–12.
- Cyprian's martyrs-only reading (*Ad Fortunatum* §11) is introduced where
  Bede comments on 7:14, as the rival reading Bede there refuses, and the
  opening paragraph of the section names both new witnesses and their
  roles.
- A new paragraph in "The strongest difficulty" states the patristic
  disagreement outright — on the number (Bede's and Augustine's whole
  Church against Victorinus's believers of the last times), on the crowd
  (the one Church against Cyprian's innumerable martyrs) and on the angel
  (the Lord incarnate against Elias) — and the four-senses Allegorical and
  Moral rows are updated to match. A pointer after Bede's comment on 7:3
  sends the reader to Victorinus's subsection.
- The comparison's "Where its witnesses differ" row for the first
  interpretation now leads with the patristic disagreement before the
  reception one, and the comparison's closing sentence reads "The witnesses
  still disagree on the number, the crowd and the angel, on the census, on
  the land of the meek and on the rich who lack."
- Neither Victorinus nor Cyprian carries an interpretation (neither has an
  author-standing row). The comparison's "Principal authors" row for the
  first interpretation reads "Bede, with Augustine on the Lesson and the
  psalms"; `proper-components.toml` lists both new witnesses among the
  lane's authors, with the carrying authors unchanged (Bede, Augustine of
  Hippo).
- The reception paragraph and the References of section 90 follow the body:
  the reception paragraph names Augustine's three loci, the Victorinus
  recension caution and Cyprian's place as the rival Bede rejects, and says
  that neither carries; the References gain entries for *De doctrina
  christiana* III.35.50–51 (NPNF I.2) and *Letter XCIII* §30 (NPNF I.1),
  add Sermon LXI (Benedictine CXI) 1 to the volume-6 entry, and add Cyprian,
  *Ad Fortunatum* §11 (ANF V) and Victorinus, *Commentary on the
  Apocalypse* on 7:2, 7:9 and 12:6 with the editors' elucidations (ANF VII).
  Every new quotation was verified against the registered artifacts before
  use.

**Advisories cleared.** All four advisory findings of the packet:

- STU-008: the element section now says that all the angels, standing round
  the throne, the ancients and the four living creatures, fall on their
  faces and adore God.
- STU-009: the second interpretation's Communion question is answered with
  a marked inference (the vision of God, sonship, the kingdom, and the
  Communion's place in the Mass), with the continuation's "the three last
  beatitudes" remark noted.
- STU-010: the Offertory's wording history is told once, in the appointed
  texts; where the third interpretation uses it, a clause refers to it.
- STU-012: the citation now reads "(*Super Matt.* cap. 5, lect. 1)" and
  says what Aquinas quotes from Chrysostom ("Non dicit a paganis, et pro
  fide, sed propter iustitiam"); the References entry follows with "cap. 5,
  lect. 1".

**Scope and extent.** No section, element key or interpretation was added
or removed; the first interpretation gains one subsection (Victorinus) and
the References gain the entries the body now cites. Measured with one
simple method (comments and LaTeX markup excluded, approximate), the prose
is now: opening 1,554; appointed texts 3,248; each element 2,319; the three
interpretations 3,718, 2,505 and 2,418; comparison 939; Scriptural Date and
Location 868; scope and References 1,568 — about 19,140 words in all,
against the iteration-2 record's 17,470. The method reads within about 110
words of the earlier figures on the unchanged sections; the real movement
is the roughly 1,050 words the repairs add to the first interpretation
(the Victorinus subsection alone is about 460) and the smaller additions to
the second and third interpretations, the comparison and the apparatus.
The proof grows by two pages, to 32 physical pages, within the 20–50-page
extent.

**Author proof.** `make doc` with the Claude provider settled with no
undefined references, no overfull or underfull boxes and no hyperref
warnings; the manifest and generation-metadata checks passed;
`check-proper-components` in the artifacts phase for the research edition
passed; the content preflight for the research edition, including the
house-voice gate, passed (references-used: 26 entries, all used; 33 loci,
all cited); and the web-edition conversion probe completed, with all
fourteen `proper-<element-key>` anchors present exactly once. The eleven
pages carrying changed passages (11, 15, 16, 18, 20, 21, 24, 26, 27, 30 and
31) were inspected at raster resolution. The proof PDF is
`build/claude/liturgy/roman-rite/1962/propers/temporal/f02-all-saints.pdf`,
sha256 `b438f15ccea57ee730af92385a15ba3559a621835dd0a8167bbd6c4c157453d7`
(32 pages); proof copies, logs and rasters are under this run's
`artifacts/author-study-3/`. The generation record carries this
iteration's contribution and a fresh revision timestamp.

**Defects reported for other owners.** Those listed under iterations 0 and
2 stand unchanged; this iteration found no new one.
## Derive-synthesis, iteration 0 (27 October 2026)

**Scope.** The concise synthesis (`synthesis.tex`) of the same Mass, derived
from the accepted expansive study with nothing evidence-dependent added: the
page-1 inventory of the fourteen said elements with its rubrical note and
the four overview rows; the page-2 Scriptural Date and Location table on the
same eight generated `orientation-v2` rows, placed once in the generator's
order; the two-page thematic orientation in the order of the Mass; the
integrated commentary organized by the questions the texts raise, setting
the three interpretations' witnesses beside one another (the sealed and the
crowd, with Victorinus under the ANF editors' recension caution and
Cyprian's martyrs-only reading kept as the rival Bede rejects; the
Beatitudes and the question of tense, with the Augustine--Hilary difference
kept and Hilary's phrase quoted with its *scilicet*; the Gradual's promise
tested by hunger and death; the Church on the way and at rest, including
the commemorated Sunday's three orations); the closing comparison; and the
terminal scope note and References. The Preface stays deliberately
unresolved: both candidates (Trinity, p. 293, no. 1082; common, p. 297,
no. 1086) are named, neither asserted, neither text given, and no sentence
builds on either.

**Element keys.** The same fourteen, mapped on page 1 in the order of the
Mass; the `preface` row names the two readings and asserts neither.

**Extent.** 12 physical pages (letter, Latin Modern, 11 pt), within the
10--12-page extent of the `interpretive-pagination-v1` contract, with every
marker on its assigned physical page (inventory and overview complete on
page 1, the chronology alone on page 2, the themes spanning pages 3--4, the
commentary opening on page 5). Approximate word counts by component, LaTeX
markup excluded: synthesis entrypoint 263; inventory 501; overview 299;
date-location 363; themes 1,371; commentary 5,003; scope and References
1,423 — about 9,220 words in all.

**Author proof.** `make doc` with the Claude provider settled with no
undefined references, no overfull or underfull boxes and no hyperref
warnings; the generation-metadata check passed; `check-proper-components`
in the artifacts phase for the synthesis edition passed (twelve physical
pages, every marker on its contract page); and the content preflight for
the synthesis edition passed on every check, including house-voice,
structural-meta-labels and references-used (22 entries, all used; 27 loci,
all cited). All twelve pages were inspected at raster resolution. The proof
PDF is
`build/claude/liturgy/roman-rite/1962/propers/temporal/f02-all-saints-synthesis.pdf`,
sha256 `adca664fed12b1a3ec337a3b8b614275bab4b334c2d6d55c1983c4a1c61aa67e`
(12 pages); proof copies, the aux, the build log and rasters are under this
run's `artifacts/derive-synthesis-0000/`. The generation record carries
this stage's contribution and a fresh revision timestamp.

**Defects reported for other owners.** One, for the study's owner: the
expansive study twice says "the seven orations" (`sections/05-appointed-texts.tex`
and `sections/90-apparatus.tex`), but only six orations exist in this
occurrence — the feast's Collect, Secret and Postcommunion and the
commemorated Sunday's three — and only six Lasance oration English blocks
are printed. The accepted study was not edited; the synthesis says "the
orations" without a count.

## Derive-homily, iteration 0 (27 October 2026)

**Scope.** The homily (`homily.tex`), *All Saints: The Way the Saints
Walked*, for an adult parish assembly at the occurrence of Sunday 1 November
2026, derived from the expansive study as its review accepted it at iteration
3 and the concise study as its review accepted it at iteration 0. Its two
components, which the manifest already declared, were written: `homily-body`
(`sections/homily/10-homily.tex`), the spoken text, continuous preaching with
no heading, direction to a preacher or citation inside the speech; and
`homily-note` (`sections/homily/90-note.tex`), the terminal note on sources
and delivery with its References, read aloud by nobody. The entrypoint
imports `common/preamble`, `common/propers-format` and `common/propers-homily`
in that order, then the leaf's `format.tex`; it uses the shared full-width
`\propertitle`, encloses only the literal import of the spoken component in
`properhomily`, and sets the note after the environment's closing page break
with `\runninghead`. No font, geometry, title or column setting is
overridden. The manifest, the research and propers records, and the expansive
and concise components were not changed. The shared generation record carries
a new revision timestamp and this stage's contribution. An earlier Claude
leaf's homily files (f01-christ-the-king) were consulted for their file
mechanics only; nothing of their content was used.

**The argument, and the profile's test.** The homily takes its spine from the
second reading, `beatitudes-way-of-the-saints`, and borrows from the first
and third, the combination the study's comparison calls layered rather than
rival.

- *Governing question.* Who are the saints this feast keeps, and how does
  anyone come to be among them? The Lesson answers who (the sealed and the
  uncounted crowd), the Gospel answers how (the eight blessings as the way),
  and the Gradual, the Offertory and the prayers answer the objection the
  way raises (the promise tested by hunger and death, and the crowned
  interceding for the journeying).
- *Decisive turn, and the textual detail that makes it.* Apoc 7:4 and 7:9:
  John *hears* the number of the sealed, a hundred and forty-four thousand,
  and then *sees* "a great multitude, which no man could number". With Bede
  (*Explanatio Apocalypsis* I, on 7:4), the definite number signifies the
  innumerable multitude of the whole Church, so the feast's company is not a
  closed quota but God's complete reckoning of a crowd gathered from every
  nation — which changes the listener's understanding of the feast from the
  veneration of a remote elite to the Church's sight of her own whole number,
  into which the Alleluia's invitation ("all you that labor and are
  burdened", Mt 11:28) calls everyone, and on which the Gospel's first
  blessing (the poor in spirit) is the first step. Beside it: the present
  tense of Mt 5:3 and 5:10 (*ipsorum est regnum caelorum*), read with
  Aquinas's begun-on-the-way and completed-in-the-homeland (*Super Matt.*
  cap. 5, lect. 1), and the Communion's re-singing of Mt 5:8–10 where the
  Sacrament is received.
- *Text-substitution test.* The argument depends on this Lesson's heard
  number and seen crowd (Apoc 7:4, 9) and its robes and palms (7:9); on this
  Gospel's eight blessings in their order and tenses (Mt 5:1–12a) and the
  Communion's repetition of three of them (Mt 5:8–10); on the Gradual's
  promise and its omitted foil (Ps 33:10–11); on the Offertory's "seemed to
  die" (Wis 3:1–3 as adapted); on the Alleluia's "all" (Mt 11:28); and on
  this occurrence's prayers: the Collect's one celebration and multiplied
  intercessors, the commemorated Sunday Collect's frailty, and the
  Postcommunion's unceasing prayer. With unrelated readings the argument
  would not survive.

**Bounds kept.**

- The patristic disputes the study records are not hidden and not raised:
  the speech follows Bede on the number, the crowd and the seal and does not
  mention Victorinus's angel and number or Cyprian's martyrs-only reading;
  it claims only Aquinas's via/patria distinction for the promises, deciding
  nothing between Augustine's in-this-life fulfilment and Hilary's
  reservation of the vision to the perfected.
- No Father is credited with a join he does not make; the note lists the
  homily's own connections (the Introit's angels beside the Lesson's, the
  Alleluia as the gathering invitation, "God loses none of his own", the
  altar sentence, the commemorated Collect as poverty of spirit in petition,
  and the Communion's three blessings as the way's end pledged, which adopts
  the second reading's marked inference).
- The Preface question stays unsettled: the note names both candidates (the
  Trinity Preface, p. 293, no. 1082; the common Preface, p. 297, no. 1086),
  asserts neither, and the speech uses neither and builds nothing on either.
- Nothing of the commemorated Sunday is used beyond its Collect; the orations
  are spoken of without a count (the "seven orations" defect of the accepted
  study, already reported by the derive-synthesis stage, is not repeated
  here). Hilary's disputed phrase is not quoted. The Offertory is quoted in
  the Lasance English of the adapted antiphon, without its closing alleluia
  and with no claim about the wording's age. No unsung context beyond the
  texts named in the note is used; the elder's question and answer (Apoc
  7:13–14), which the Lesson does not read, stay outside the speech.
- No English of a liturgical text was composed: the Introit, Offertory,
  Secret, commemorated Collect and Postcommunion are quoted in the Lasance
  English, in phrases, and otherwise described. No anecdote, personal
  experience, clerical identity, miraculous story or attributed quotation was
  manufactured; no prayer was composed, and the one response given to the
  assembly (making the commemorated Collect's petition their own) directs the
  hearer's own prayer, said once, from the text the argument has been about.

**Verification performed at this stage.** Every quotation was read in the
accepted study's appointed texts and interpretation sections, which print the
reviewed witnesses' words: the Missal's Latin and its Douay and Lasance
English in `sections/05-appointed-texts.tex`; Bede, Augustine, Chrysostom,
Basil, Aquinas, Schuster and Durandus as the study quotes them
(`sections/20-sealed-number-uncounted-crowd.tex`,
`30-beatitudes-way-of-the-saints.tex`, `40-no-want-just-in-gods-hand.tex`),
each at the locus `research/interpretations.md` and `research/scope.md`
record. No new source-dependent claim was added to either study; the speech
introduces no claim that is not in the reviewed leaf, and its own joins are
confined to the list in the note.

**Extent and delivery.** The spoken body runs to about 1,445 words (comments
and LaTeX markup stripped), some 11.1 to 12.0 minutes at an unhurried 120 to
130 words a minute by arithmetic alone; it has not been delivered aloud or
timed. It was read through in full, on the page, for sense and oral clarity.

**Proof.** `make doc` with the Claude provider settled with no fatal errors,
no undefined references, no overfull or underfull boxes and no hyperref
warnings in the LaTeX log; the anchor check reported "0 contents lines, 0
bookmarks, every one on its own anchor"; the manifest check reported "Proper
component manifests valid: 1"; the generation-metadata check reported "1
canonical record(s), 0 inherited record(s)". `check-proper-components` in the
artifacts phase for the homily edition passed. The component-contract gate
(`_proper_study.py check`, phase content, edition homily, with the
presentation, format, authority and both orientation requirements) passed.
All twelve content-preflight gates for the homily edition passed:
references-used (11 entries, every one used in the body), identifiers-resolve
(the leaf prints no source identifier), bindings-valid (47 bindings, every id
registered and fingerprinted), restricted-not-reproduced (7 restricted
sources, none reproduced), relation-coverage (3 interpretive lanes, each
declaring all four senses and whole-proper component coverage),
unquoted-not-quoted, structural-meta-labels, house-voice,
chronology-record-current, chronology-annotations-current,
chronology-claims-supported, and provenance-matches-run against this run's
identity. Every page was inspected at raster resolution: the full-width title
block carries "A homily" on its own line; the spoken body runs in two columns
with no heading before it and ends at the Communion's closing beatitude; the
note stands after the environment's closing page break under the running
head "Sources and Delivery", with the References block and the revision
timestamp and rights colophon on the final page; page numbers are lowercase
roman. The proof PDF is
`build/claude/liturgy/roman-rite/1962/propers/temporal/f02-all-saints-homily.pdf`,
sha256 `53f0ea66ead5b95adb97e314f83cc1fbc5bbb2c9044c2f93e4a97dce09ccf957`
(4 pages); proof copies, logs and rasters are under this run's
`artifacts/derive-homily-0000/`. The generation record carries this stage's
contribution and the revision timestamp 2026-10-27T09:33:31Z.

**Defects reported for other owners.** None new. The standing reports of the
earlier stages (the study's "the seven orations", the shared appointment
test, calendar-entry, formulary-loci, author-standing, provenance-ledger,
translation-register and ordo-record items) remain with their owners; the
homily touches none of them.

## Derive-homily, iteration 1 (27 October 2026)

**Finding repaired.** One blocking finding forwarded from the iteration-0
homily review (HOM-001, repair target: homily): the terminal note's account
of the route of Gal 3:29 did not match the words actually spoken. The
required result admitted two repairs; this iteration took option (a),
correcting the note and leaving the reviewed spoken body untouched:

- The route paragraph's Douay list no longer carries Gal 3:29, and now
  states that the speech's "if ye be Christ's, then are ye Abraham's seed"
  is quoted as Bede cites the verse in his comment on the heard number, in
  E. Marshall's English of the *Explanatio*, with the Douay wording ("if
  you be Christ's, then are you the seed of Abraham") given for contrast.
- The References entry for the Douay--Rheims drops Gal 3:29 from its locus
  list; the Bede entry now records that the quotation is Bede's citation of
  the verse at 7:4, quoted as Marshall renders it; the exact-loci sentence
  on Bede follows ("7:4 (the number, with his citation of Gal 3:29)").
- The spoken words stand as reviewed: the speech introduces the clause as
  St Paul's, which it is, and the finding held the speech itself fine. The
  word count (about 1,445) and the timing paragraph are unchanged.

**Verification performed at this stage.** The spoken clause was compared
word for word against the two candidate routes in the repository's own
corpora: the Douay--Rheims (Challoner) reads "And if you be Christ's, then
are you the seed of Abraham, heirs according to the promise"
(`src/sources/bibles/douay-rheims/chapters/Gal/3.json`, verse 29, and the
registered Challoner-Gutenberg artifact `55-galatians.tsv`), while E.
Marshall's 1878 English of Bede reads "For, he says, 'if ye be Christ's,
then are ye Abraham's seed.'" (registered passage record
`src/sources/works/bede/explanatio-apocalypsis/editions/1878-marshall-parker/passages/1-7-4.toml`,
on Apoc 7:4). The spoken words are Marshall's, verbatim, inside the Bede
passage the sentence is quoting; the note now says so. Every other route
statement in the note was rechecked against the finding's assurance that
the remaining routes were verified and are unaffected; no other change was
made to the note, the speech, the entrypoint or the manifest.

**Proof.** `make doc` with the Claude provider settled with no fatal
errors, no undefined references, no overfull or underfull boxes and no
hyperref warnings in the LaTeX log; the anchor check reported "0 contents
lines, 0 bookmarks, every one on its own anchor"; the manifest check
reported "Proper component manifests valid: 1"; the generation-metadata
check reported "1 canonical record(s), 0 inherited record(s)".
`check-proper-components` in the artifacts phase for the homily edition
passed. The component-contract gate (`_proper_study.py check`, phase
content, edition homily, with the presentation, format, authority and both
orientation requirements) passed. The content preflight for the homily
edition passed on every check, including references-used (11 entries, every
one used in the body), house-voice (3 reader-facing files), bindings-valid,
restricted-not-reproduced (47 bound sources, 7 restricted, none
reproduced), relation-coverage, identifiers-resolve, unquoted-not-quoted,
structural-meta-labels, the three chronology checks, and
provenance-matches-run against this run's identity. All four pages were
inspected at raster resolution: pages 1--2 carry the spoken body unchanged;
page 3 carries the corrected route paragraph and exact loci; page 4 carries
the corrected References, the fresh revision timestamp and the colophon.
The proof PDF is
`build/claude/liturgy/roman-rite/1962/propers/temporal/f02-all-saints-homily.pdf`,
sha256 `792836934fc5f992722a39cf49d1556bc4da94e86a0b3e77ad54b5be2f1b8cfa`
(4 pages); proof copies, the build log and rasters are under this run's
`artifacts/derive-homily-0001/`. The generation record carries this
iteration's contribution and the revision timestamp 2026-10-27T10:17:15Z.

**Defects reported for other owners.** None new; the standing reports of
the earlier stages remain with their owners.

## Build-artifacts, iteration 0 (27 October 2026)

**Scope.** Final builds of all three editions of the accepted leaf for
visual review: the expansive study (`main.tex`), the concise synthesis
(`synthesis.tex`) and the standalone homily (`homily.tex`). No source,
prose, evidence or layout edit was made at this stage; the three
documents' text stands as accepted.

**Builds.** `make doc` with the Claude provider for each of
`f02-all-saints`, `f02-all-saints-synthesis` and `f02-all-saints-homily`
settled with exit 0. The study and synthesis re-rendered because the
shared `generation-metadata.tex` render input was finalized at
derive-homily iteration 1 after their last builds; the homily was already
at fixed point and its bytes are unchanged from its accepted proof.
Extracted text of the re-rendered study and synthesis differs from the
author-study-3 and derive-synthesis-0000 proofs only in the rendered
"Last revised (UTC)" line, which all three editions now carry as
2026-10-27T10:17:15Z.

**Log, font and extraction inspection.** All three LaTeX logs carry no
fatal error, no undefined reference or citation, no overfull or underfull
box (zero of each) and no LaTeX warning. The re-rendered editions'
anchor checks reported "every one on its own anchor" (study 62 contents
lines, synthesis 14) and their manifest checks "Proper component
manifests valid: 1"; the homily was at fixed point and its build emitted
only the validation lines. Every build's generation-metadata check
reported "1 canonical record(s), 0 inherited record(s)". `pdffonts` shows every font embedded
(subset Type 1 Latin Modern) in all three PDFs. `pdftotext` extraction
confirms the settled physical-page markers of the concise opening: the
complete proper inventory and exactly four overview sense rows on
physical page 1; Scriptural Date and Location alone on page 2; The
Propers: Themes and Movement on pages 3--4; The Propers: Detailed
Commentary beginning on page 5. Extents: study 32 pages (within 20--50),
synthesis 12 pages (within 10--12, terminal apparatus included), homily
4 pages.

**Snapshot and rasters.** `_proper_study.py snapshot --provider claude`
(exit 0) recorded the exact PDF and render-input snapshot in
`research/artifacts.json` (schema 2): the three PDF hashes, the 27
render-input hashes and the study/synthesis auxiliary pagination
evidence. `tools/tpt pdf-review` (exit 0) rendered bounded page rasters
of all three PDFs into this run's
`artifacts/build-artifacts-0000/rasters/`: 32, 12 and 4 full pages with
matching thumbnails and 2, 1 and 1 contact sheets, under
`review-run.json` (schema triptych-pdf-review-v3-explicit-font).

**Proofs.** Study
`build/claude/liturgy/roman-rite/1962/propers/temporal/f02-all-saints.pdf`,
sha256 `3d6f91d0b5acdab1bbd105f4fa6e6943783649a34f2a82dc1ca60604d6ebd7c6`
(32 pages); synthesis
`build/claude/liturgy/roman-rite/1962/propers/temporal/f02-all-saints-synthesis.pdf`,
sha256 `7ad32f84edbfd16bdc9414f341b3f9ec1e4f588d9296341562fc19a3cdc23cf8`
(12 pages); homily
`build/claude/liturgy/roman-rite/1962/propers/temporal/f02-all-saints-homily.pdf`,
sha256 `792836934fc5f992722a39cf49d1556bc4da94e86a0b3e77ad54b5be2f1b8cfa`
(4 pages, byte-identical to the accepted derive-homily-0001 proof). PDF
copies, the three LaTeX logs, the three aux files and `hashes.txt` are
kept with the rasters under this run's `artifacts/build-artifacts-0000/`.

**Remaining limitations.** No page has been visually inspected at this
stage; a fresh worker inspects every page after the upstream seals and
artifact checks pass. The PDFs are not installed. Semantic review of the
rendered documents belongs to the visual reviewer.

**Defects reported for other owners.** None new; the standing reports of
the earlier stages remain with their owners.

## Install-publication, iteration 0 (27 October 2026)

**Scope.** Installation and wiring of the three accepted editions and the
reviewed canonical web edition; no source, prose, evidence or layout edit was
made at this stage, and the three documents' text stands as accepted.

**Artifact snapshot.** Confirmed current before installation: the three
`build/claude/.../f02-all-saints*.pdf` hashes equalled the accepted
`research/artifacts.json` (schema 2) snapshot exactly, and the reviewed
`build/web/claude/.../f02-all-saints.md` equalled the
`research/web-artifact.json` receipt (sha256
`2fd1fa1611e393281e1c98ffe228b1185f4528a075ae8d2dbfdd7aeb11f0c856`).

**PDF installation.** `make install-doc DOC=<id> PROVIDER=claude` for
`f02-all-saints`, `f02-all-saints-synthesis` and `f02-all-saints-homily`, each
run with its declared dependencies and checks (exit 0; the metadata
validation line reported "1 canonical record(s), 0 inherited record(s)" for
each; no edition retypeset). Installed and build bytes are identical to the
accepted proofs: study `3d6f91d0b5acdab1bbd105f4fa6e6943783649a34f2a82dc1ca60604d6ebd7c6`,
synthesis `7ad32f84edbfd16bdc9414f341b3f9ec1e4f588d9296341562fc19a3cdc23cf8`,
homily `792836934fc5f992722a39cf49d1556bc4da94e86a0b3e77ad54b5be2f1b8cfa`,
each verified at both `build/claude/liturgy/roman-rite/1962/propers/temporal/`
and `pdf/claude/liturgy/roman-rite/1962/propers/temporal/`.

**Web installation.** The reviewed canonical Markdown was installed byte for
byte (`install -m 0644`, `cmp` clean) to
`web/claude/liturgy/roman-rite/1962/propers/temporal/f02-all-saints.md`,
sha256 `2fd1fa1611e393281e1c98ffe228b1185f4528a075ae8d2dbfdd7aeb11f0c856`.
Per the dispatch terms, which reserve every git index operation to the
driver, the file was left unstaged; the publication gate proves it tracked
with `git ls-files --error-unmatch` once the driver stages it. No companion
web authority was created.

**Release records.** `make add-publication ... PROVIDER=claude STATUS=alpha`
created `release/publications/claude/liturgy/roman-rite/1962/propers/temporal/f02-all-saints.json`,
`-synthesis.json` and `-homily.json`, each schema_version 1, catalog
`library/traditional-latin-mass.md`, status `alpha`, authorization
`perpetual-public-repository-2026`. No prior record existed for any of the
three IDs.

**Catalog wiring.** In `library/traditional-latin-mass.md`, the F02 row's
Claude cell of "Feasts Replacing a Sunday" now links the Full PDF, Synthesis
PDF, Homily PDF and Read (canonical web) in the schema-2 manifest's
output-label order; the ChatGPT cell and every other row and cycle are
unchanged. Exactly one canonical publication marker was added,
`<!-- triptych-publication-id: claude:liturgy/roman-rite/1962/propers/temporal/f02-all-saints -->`,
by the primary-provider rule of `release/public-alpha.json` (provider `gpt`).

**Deterministic inventories.** `make document-catalogue` rewrote
`src/web/data/structure/documents/corpus.json` (154 works, 216 documents,
280 issues, 7,226 pages); the diff adds this family's three entries and
nothing else. `make refresh-release-bindings ADOPT=1 ONLY="<eleven paths>"`
re-recorded exactly this production's paths: the two wiring targets
(`library/traditional-latin-mass.md`, the installed web Markdown), the
regenerated catalogue, and the eight source-projection files this run's
research stage had acquired or regenerated without refreshing their bindings
(the FSSP France, FSSPX and ICRSP ordos, the ICRSP textes-de-la-messe, the
Missale Meum calendar, the Murphy rubrics edition, the Migne PL 35 edition
record and the sources index). The rights record's current site-source table
and `rights_record_sha256` were re-recorded by the same tool. No other
production's path was adopted.

**Proof.** The publication-phase check
(`scripts/_proper_study.py check --phase publication` with the presentation,
format, authority and both orientation requirements) passed every test
before the index check: scope, the schema-2 artifact snapshot against
current build bytes and render inputs, generation metadata for all three
editions, installed-equals-build for all three PDFs, the three release
records against the standing authorization, exactly one catalog row linking
all four outputs, the catalog cell provider rule, exactly one publication
marker, the web receipt against the reviewed conversion, and
installed-equals-reviewed for the web edition. Its sole failure is
`git ls-files --error-unmatch` on the installed web Markdown, which the
driver stages per the dispatch terms. The scoped public-alpha check
(`tools/tpt public-alpha check --provider claude --document
liturgy/roman-rite/1962/propers/temporal/f02-all-saints`) exited 0: "global
source, release and authorization records valid: 280 publications";
installed-PDF scope exactly this family's three outputs. The document
catalogue gate (`document-library check --provider claude --document ...`
and `structure --check`) exited 0: three titles confirmed against the built
PDFs, corpus.json current. `make check-release-bindings` exited 0 with
"exact: 0 stale binding(s)". `make check-web-editions-current` exited 0:
"Tracked web editions match current sources." Every python and make command
ran with the pinned virtualenv (Markdown 3.10.3, PyYAML 6.0.3) first on
PATH.

**Remaining limitations.** Acceptance is the terminal publication gate's
decision; this stage does not claim it. The installed web Markdown awaits
the driver's staging before the gate's tracked-file proof can pass.

**Defects reported for other owners.** None new; the standing reports of
the earlier stages remain with their owners.
