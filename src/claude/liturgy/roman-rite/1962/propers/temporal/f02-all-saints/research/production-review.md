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

## Author-study, run `450355254538c1ba`, iteration 0 (28 October 2026)

This run is `proper-study` v15, run `450355254538c1ba`, seeded at commit
`4f52b9ade338f9a9f4f39f312aa45989a0baf2ca`. Its research stage (iterations
0 to 3) rebuilt `research/scope.md` and `research/interpretations.md`, and
this dispatch rewrote the study from them. The sections above record the
earlier run.

**Scope.** The opening now sets out the three questions as the research
frames them. In the appointed texts, the notes were corrected: six orations,
the history of the Offertory's wording (the *malitiae* chant before 1570,
1570 *mortis*, no *alleluia* through 1909, first seen in Mame 1922), the
Gradual's psalter form, and the Preface subsection, which gives both readings
of the rubrics with the contrast among RGMR 486 b to 494 b and the dated
ICRSP direction. Each element's setting was rewritten from the reception
matrix: Ménard's codex, Monte Suavicino, Leonine and Gelasian for the
Collect's two variant readings; Bernard's sermons for the feast; the
disagreement over the burden of Mt 11:28; Fromage's French, quoted and
rendered. All three interpretations were rewritten on their recorded
authors. The first draws on Bede, on Augustine (Sermon LXI and *Ench.* 29)
and on Gregory and Aquinas for the number. The second draws on Augustine,
Chrysostom, Aquinas, Hilary and Rabanus Maurus. The third draws on Basil,
Augustine (with *Enarr.* 87 n. 5 on Wis 3:1), Aquinas and Bellarmine. The
comparison was rewritten. In the scope appendix, the search bound of the
Preface is stated plainly; the reading now covers Bernard; Rabanus is treated
as a compiler credited only with words marked as his own; and the rights
paragraph lists the editions. The References were rebuilt by kind. In the
manifest, Rabanus Maurus was added to the carrying authors of the second
lane, and the lanes' `authors` lists were brought to the names with a
standing row that each interpretation draws on. Durandus and Gregory were
dropped from the third lane, and the lane comment was corrected.
The generation record carries this run's provenance and a fresh revision
timestamp. Its contribution lines were left as they stood.

**Extent.** 32 physical pages. Approximate word counts by component, LaTeX
commands excluded: opening 1,540; appointed texts 3,480 (the set Latin and
English included); each element 3,120; the three interpretations 2,780,
2,530 and 2,300; comparison 710; Scriptural Date and Location 840; scope and
References 1,960. The exposition proper (opening, each element,
interpretations and comparison) is about 12,990 words. That is above the
profile's planning range of 6,000 to 10,000; the range is not a quota, and
the PDF is within the 20 to 50 pages allowed.

**Source limits carried into the study.** The Lasance English of the
Lesson's and Gospel's openings and of the Offertory is quoted on the
Lasance's attribution only. Between 1909 and 1922 no printing was read, so
the entry of the Offertory's *alleluia* is bounded only by those two dates.
The direction between *intercessoribus* and *intercessionibus* is not
established. The 1604 Collect is unreadable on its text layer. Not read:
Cassiodorus, Theodoret and Athanasius on the psalms (held in remote volumes
only, not fetched), Jerome on Mt 5, Aquinas on Mt 11, Gregory of Nyssa (not
held), and the *Glossa* (known only through Bonaventure). Bellarmine is read
in an abridged English, and Aquinas on the Psalms and Bonaventure in OCR.
The Victorinus recension is uncertain. Bernard, Bonaventure, Alphonsus,
Victorinus, Cyprian and Bruno of Würzburg have no standing row and are cited
in support only. English beside Latin or French from an edition with no
English is the study's own rendering, and the scope appendix says so.

**Author proof.** `make doc` with the Claude provider completed with no
undefined references, no overfull or underfull boxes and no warnings in the
log; the manifest and generation-metadata checks passed.
`check-proper-components` in the artifacts phase for the research edition
passed. Every content preflight check for the research edition passed,
including house-voice over eleven reader-facing files and references-used
(39 entries); `provenance-matches-run` passed for this run. The web-edition
conversion probe completed. Every page was inspected at contact-sheet
resolution, and the comparison table and the References at page resolution.

**Defects reported for other owners (not repaired here).**
`propers.yaml` `omnium-sanctorum` encodes Mt 5:1-12 and Wis 3:1-3 entire, and
it has no Preface case. `test_ordinary_appointments.py` asserts the common
Preface. The Latin provenance and translations ledgers have no scriptural
rows, and `formulary-loci.yaml` is empty for both formularies.
`author-standing-v1.toml` has no rows for Bernard, Victorinus, Cyprian,
Bonaventure, Alphonsus Liguori, Peter of Celle or Bruno of Würzburg. The
chronology generator labels the Lesson "Revelation".
`passage-commentary-index.yaml` has no mapping for Wis 3:1-3. The Victorinus
containment bound omits chapters 7 and 12. Bede has no passage records for
Apoc 7:1-3. The FSSPX ordo record declares English where the responses are
French. The remaining items of `research/scope.md` section 10 stand with
their owners.

## Author-study, run `450355254538c1ba`, iteration 1 (28 October 2026)

This iteration repaired the eight blocking findings of the study's cold review
(STU-001 to STU-008) and cleared the four advisories (STU-009 to STU-012).

**Findings repaired.**

- STU-001: the repeated inference formula ("this interpretation takes …", "on
  this interpretation", "on the same assumption") and the sentences certifying
  whose inference a connection is were rewritten. Each inference the study
  draws is marked once, where it is drawn, by a conditional or "read with";
  the reviewer's three plain rewrites (the Introit's one praise, the Gradual
  as the first step, the end of the third interpretation's Gospel sentence)
  were adopted. Sentences whose subject is a source and that say where its
  comment stands were kept.
- STU-002: the three closing sections that gave every text of the Mass a part
  were recast with content titles ("The angels' feast and the many who pray";
  "Joy, peace, and three beatitudes sung again"; "Joy in the Lord they
  have"). Each keeps the connections a Father or commentator bears (the
  Collect with Durandus and Fromage; the Offertory with the *Glossa*,
  Alphonsus and Fromage, and the Communion with Fromage; the Introit with
  Augustine, Basil, Aquinas and the Cassiodorus extract). The Sunday's three
  orations, the Preface and the other texts each interpretation touches
  lightly now have a clause saying what they say, without a role in the
  thesis.
- STU-003: each interpretation's opening credits each author only with what he
  says of his passage and states the thesis once as the study's; Basil's and
  Augustine's clauses in the third are separated. The comparison table now
  gives a per-author row and a separate row for the interpretation's own
  answer.
- STU-004: the comparison's "Reached by inference" row names exactly the
  inferences the revised interpretations draw: the first, the Introit, the
  Gradual and the Alleluia; the second, the Gradual and the Lesson; the third,
  the joining of the Offertory to the Gradual. The paragraphs below the table
  agree with it.
- STU-005: Chrysostom's image is the golden chain (*Hom. in Matt.* 15.9) in the
  heading, body and moral sense. His place in the present-and-future question
  rests on Hom. 15.4 ("Both here and there") and 15.5 ("not as limiting the
  rewards to things present …"), read in the NPNF I.10 text; Hom. 38.3 is kept
  to the meekness and rest of Mt 11:29.
- STU-006: each repeated quotation has one full home, and is named elsewhere
  in a clause with a pointer: Bernard's sermo 5 n. 3 and Augustine's objector
  in the third interpretation; Augustine's "those promises" in the second;
  Bede's "innumerable multitude", Durandus's reason and Fromage on the
  Introit's angels in the first; Chrysostom's "not this or that person" and
  the commentators on the Introit verse in the element settings; Fromage on
  the Communion and on the Offertory, and Bernard's reconciliations, in the
  second; Bonaventure and Schuster on the Offertory in the third. The second
  interpretation's survey of the burden of Mt 11:28 was cut to Chrysostom's
  and Augustine's call to begin from humility, and the burden dispute left
  the comparison table.
- STU-007: the six subsection headings lost their "The question" and "The
  strongest difficulty" prefixes.
- STU-008: the three appointed-text notes attribute the Lasance English
  plainly; the account of the translation register stands only in the scope
  appendix.

**Advisories.** STU-009: Durandus's other Alleluia, the Gregorian
Antiphonary's other Alleluia and Communion, the medieval proper Preface, the
reuse for St Cyriacus and St Hippolytus and the Sarum common of the Gradual
were removed from the body; one clause of the scope appendix records
Durandus's Alleluia. STU-010: the Gradual's setting gives Augustine's
objection as he states it (the man who seeks the Lord daily and has nothing,
while the wicked rich die in their riches, *Enarr.* 33 s. 2 n. 14, Migne
Latin text). STU-011: Aquinas reports three opinions on the number; the first
interpretation's moral sense gives Bernard's "Illorum lauda virtutem, quorum
jam certa victoria est" (sermo 5 n. 3, PL 183 OCR at the image-read locus);
the third's literal sense no longer places the psalmist at Geth; the
comparison distinguishes Augustine's "can be fulfilled" from Aquinas's
"begun". STU-012: the orientation table's place cells give only occurrence
and place, and the Psalms note says that David's reign is the reference
point of the attribution, not a date of composition.

**Manifest.** The second lane's `authors` now lists Bede (for his first
account of Apoc 7:9) and no longer lists Jerome, Gregory the Great or Sicard
of Cremona, whose comments left that interpretation; the third lane no longer
lists Chrysostom. Carrying authors are unchanged.

**Extent.** 31 physical pages. Approximate word counts by component, LaTeX
commands excluded: opening 1,530; appointed texts 3,310 (Latin and English
included); each element 2,760; the three interpretations 2,560, 2,400 and
2,200; comparison 810; Scriptural Date and Location 830; scope and References
1,970. The exposition proper is about 12,260 words, above the planning range
of 6,000 to 10,000, which is not a quota; the PDF is within 20 to 50 pages.

**Source limits.** Unchanged from iteration 0.

**Author proof.** `make doc` with the Claude provider completed with no
undefined references, no overfull or underfull boxes and no LaTeX warnings;
the manifest and generation-metadata checks passed;
`check-proper-components` in the artifacts phase for the research edition
passed; every content preflight check for the research edition passed
(house-voice over eleven files; references-used, 39 entries and 30 loci;
structural-meta-labels, 70 labels), and `provenance-matches-run` passed for
this run. The web-edition conversion probe completed. Every page was
inspected at contact-sheet resolution, and the comparison table and the last
page at page resolution. The generation record carries a fresh revision
timestamp.

**Defect reported for the research owner (not repaired here).**
`research/scope.md` section 3.7 ("the ladder of the beatitudes (8988-8995)")
and `research/interpretations.md` section 3 (Chrysostom, "the beatitudes are
a ladder") describe *Hom. in Matt.* 15 with a word the source does not use:
the cited NPNF lines contain no ladder, and Chrysostom's image, in 15.9, is
"a sort of golden chain". The defects reported for other owners under
iteration 0 stand.

## Derive-synthesis, run `450355254538c1ba`, iteration 0 (28 October 2026)

**Scope.** The concise study (`synthesis.tex`), derived from the expansive
study as the study review accepted it at iteration 1, with its six
synthesis-only components under `sections/concise/`, which the manifest
already declared: the page-1 map of the fourteen said elements (the feast's
ten texts, the Sunday's three commemorated orations and the Preface locator
naming both readings of the rubrics) and the four overview senses; the page-2
Scriptural Date and Location on the eight generated `orientation-v2` rows,
each with the study appendix's reviewed place phrase, and a note beneath
pointing to that appendix; the two-page Themes and Movement, in the order of
the Mass; the integrated commentary; the concise scope appendix and
References. The manifest, the research, propers and context records and the
expansive study were not changed. The shared generation record carries a new
revision timestamp; its provenance line already named this run.

**Commentary.** Eight units, organized by question rather than by element:
one Church under a number and beyond number (Bede set beside the anonymous
*Expositio* and Victorinus; the Introit's praise, the Collect's and
Postcommunion's intercession and the Gradual's saints, each inference marked
where drawn); the number known to God (Augustine, Gregory and Aquinas
compared); whether the multitude shows that salvation is easy (Cyprian and
Schuster against Augustine); the way of the Beatitudes and its first step
(Augustine's steps and gifts, Chrysostom's chain, Bernard's reconciliations,
the Communion's three in each order); the time of the rewards (Augustine,
Chrysostom, Aquinas, Rabanus and Bernard against Hilary, with the Offertory's
peace); what the God-fearing cannot lack (Basil and Augustine against
Aquinas and Bellarmine, and Bernard on the command); the just in God's hand
(Augustine and Bonaventure, and the Schuster, Alphonsus and Bonaventure
difference over whose souls); and the three answers compared, with their four
senses where they differ.

**Extent.** 12 physical pages (letter, Latin Modern, 11 pt). Approximate
words, LaTeX stripped, quoted Latin and English included: inventory and its
note 370; overview 200; page-2 place phrases and note 255; Themes and
Movement 1,500; commentary 4,305; scope appendix and References 1,300. The
substantive body (page 1 through the commentary) is about 6,630 words.

**Placement.** The settled auxiliary file places the inventory, the overview
and its four sense markers on physical page 1, the chronology on page 2, the
themes from page 3 to page 4, and the commentary's start on page 5.

**Fidelity to the reviewed study.** Every claim, attribution and quotation is
the expansive study's, re-read there; the concise study adds no source and no
locus the study does not cite. Per the three-document profile, the history of
the formulary's own texts (the Collect's sacramentary antecedents and its
variant reading, the Introit's earlier assignment, the Lesson's earlier use
and the Offertory's printing history) and Durandus's other Alleluia are left
out. The study review's advisories were not repeated: Aquinas meets St Paul's
words without the objection being called Paul's (STU-015 a); Bellarmine is
not denied a link (STU-015 b); "None of these authors divides the rewards by
those tenses" (STU-015 c); the concise scope appendix gives the works not read
without the retrieval reasons (STU-015 d); the difficulty and the
disagreements are stated without certifying clauses (STU-014); and the
orations and Preface that an interpretation does not use get no closing roll
of clauses (STU-013).

**Proof.** Built with `make doc` (provider `claude`), settled with no
overfull or underfull box, undefined reference or rerun warning. PDF SHA-256
`718e6791cfad460e3c36c2d66efb32824171ec9fbe6b297bca0fb63e29416c34`, 12 pages.
Every page was inspected at page resolution, and the page-2 lookup from
passage to occurrence, place and date was made for each of the eight rows.

**Author checks run.** `tools/check-proper-components --phase artifacts
--edition synthesis`; the synthesis-preflight component contract with all
five `--require-*` options; and every `check-content-preflight` check of the
synthesis preflight, including references-used (27 entries, 25 loci),
house-voice (8 files), structural-meta-labels (22 labels), the three
chronology checks and provenance-matches-run. All pass.

**Carried for other owners.** The generated passage labels print
"Revelation" and "Matthew 5:1--12" (chronology tool and calendar entry); the
page-2 note gives the reader the Apocalypse and the Missal's 5:12a. The shared
format sets a section's running head on the last page of the preceding
section where the section starts mid-page (pp. 10 and 11 of this proof). The
defects reported for other owners at author-study stand.

## Derive-synthesis, run `450355254538c1ba`, iteration 1 (28 October 2026)

**Scope.** Repair of the concise review's blocking finding SYN-001, with the
advisories SYN-002, SYN-003 and SYN-004 (a) cleared in the files touched.
Changed: `sections/concise/10-commentary.tex` (rewritten),
`sections/concise/04-themes.tex` and `sections/concise/03-date-location.tex`
(advisory edits), and the revision timestamp of the shared generation record.
Pages 1--4 keep their content and markers. The manifest, the research,
propers and context records and the expansive study were not changed.

**SYN-001 (repaired).** The commentary no longer follows the expansive
study's order or reprints its comparison. It is built on three questions that
more than one interpretation answers, with the authorities of the different
interpretations set side by side inside each: (1) who the saints of the feast
are (Bede, the anonymous *Expositio* and Victorinus on the number, the angel
and the multitude; Bede's first account of the palm-bearers beside the eighth
beatitude and Bernard on poverty as martyrdom; Augustine against Cyprian and
Schuster on whether the multitude makes salvation easy; Augustine, Gregory and
Aquinas on the number God knows; Bernard on the Gradual's saints and
Chrysostom on the Alleluia's "all"; Bede's praise, the Introit's
*collaudatio* and the feast's prayers); (2) what the fear of the Lord is and
what it is promised (Augustine's steps and gifts with Rabanus's copied verse,
Chrysostom's chain and both Fathers on Mt 11:29, Bernard's reconciliations and
the Communion; Basil, Aquinas and Bernard on the fear the saint keeps; Basil
and Augustine against Aquinas and Bellarmine on bodily need); (3) when and
where the reward is had (the Beatitudes' tenses; Augustine, Chrysostom,
Aquinas, Rabanus, Bernard and Basil on the present against Hilary; the
Offertory's peace in the *Glossa*, Alphonsus and Fromage; Augustine's and
Bonaventure's hand of God and the Schuster, Alphonsus and Bonaventure
difference; the third interpretation's reading of the Offertory with the
Gradual). Each interpretation's controlling claim is stated where its unit
reaches it. The close compares only the four senses, with the first
interpretation's moral sense attributed to Bernard. The claim-local
qualifications are kept: Bede "does not say in so many words"; Victorinus's
uncertain text; Bernard does not comment on the Mass Gradual; Rabanus credited
only with words he marks as his own; Bonaventure's *mortis*; Aquinas's Secret
not said on this day. No source or locus was added. With quotations removed,
about 16% of the commentary's own prose (505 of 3,244 words) lies in
eight-word runs shared with sections 00--50 of the study, chiefly the
qualifications above, glosses of quoted Latin and citation strings.

**Advisories.** SYN-002 (a), (b) in the themes pages and (c), (d) in the
rewritten commentary; SYN-003 (a), (c), (e) in the commentary, (b) and (d) in
the themes pages (Bede's seal now in his words; Durandus's form
*intercessionibus* noted beside him); SYN-004 (a) in the page-2 note. SYN-004
(b) was left: the place phrases reprint the reviewed study appendix, and
changing them belongs with that appendix.

**Extent.** 11 physical pages. Approximate words, LaTeX stripped, quoted
Latin and English included: inventory and note 400; overview 205; page-2 rows
and note 305; Themes and Movement 1,500; commentary 4,000; scope appendix and
References 1,400. The substantive body (page 1 through the commentary) is
about 6,400 words.

**Placement.** The settled auxiliary file places the inventory, the overview
and its four sense markers on physical page 1, the chronology on page 2, the
themes from page 3 to page 4, and the commentary's start on page 5.

**Proof.** Built with `make doc` (provider `claude`), settled with no
overfull or underfull box, undefined reference or rerun warning. PDF SHA-256
`abb35a858397b9e5ef9ca8ec06dd678edd5e0a85474b1eaa2539e44995db7eff`, 11 pages.
Every page was inspected at contact-sheet resolution and pages 4 and 9 at page
resolution.

**Author checks run.** `tools/check-proper-components --phase artifacts
--edition synthesis`; the synthesis-preflight component contract with all
five `--require-*` options; and every `check-content-preflight` check of the
synthesis preflight, including references-used (27 entries, 23 loci),
house-voice (8 files), structural-meta-labels (18 labels), the three
chronology checks and provenance-matches-run. All pass.

**Carried for other owners.** The shared format's running head on the page
where a section starts mid-page still names the next section (page 9 of this
proof prints "Scope and References" above the end of the commentary). The
generated passage labels and the other defects carried at iteration 0 stand.

## Derive-homily, run `450355254538c1ba`, iteration 0 (28 October 2026)

**Scope.** The homily (`homily.tex`), written after both studies passed their
reviews, with its two homily-only components under `sections/homily/`, which
the manifest already declared: the spoken body (`10-homily.tex`) and the
terminal note with its References (`90-note.tex`). The entrypoint imports
`common/preamble`, `common/propers-format` and `common/propers-homily` in that
order, sets the shared full-width title, and encloses only the spoken
component in `properhomily`; the note follows the environment's page break.
The manifest, the research, propers and context records, the expansive study
and the concise study were not changed. The shared generation record carries
a new revision timestamp; its provenance line already named this run.

**Audience and argument.** An adult parish assembly at the Mass of the feast
said on Sunday 1 November 2026. The speech asks once how the Gradual's
promise, "there is no want to them that fear him", can be true of saints who
went hungry and were put to death, and answers it from the third
interpretation (Augustine's objector, Basil's dilemma and "God himself",
Aquinas's help in need and physician, with their difference over bodily goods
kept; Augustine's gloss on the Offertory's first clause; Bernard on the verse
as sung in the night office). From the second interpretation it takes the
present tense of the first and eighth beatitudes, Chrysostom's "Both here and
there", and Augustine's fear of the Lord at the first step; from the first,
only the Lesson's multitude and the saints' intercession in the Collect and
Postcommunion, with Bernard on their veneration. Bellarmine, Hilary's
emphasis, the dispute over whose souls the Offertory names and the number of
the saved are left to the studies. The Gospel, the Lesson, the Gradual, the
Offertory and the Communion are Scripture the speech uses; the Introit,
Collect, Secret and Postcommunion are the prayer. The Alleluia, the Preface
and the Sunday's three commemorated orations are not used.

**What the text changes.** The listener's assumption is that a promise of no
want to those who fear God is a promise to be kept from want, and that the
saints' poverty and deaths show it failing. The decisive textual detail is
the tense of Mt 5:3 and 5:10: the first and eighth beatitudes say of the poor
in spirit and of the persecuted, in the present, "theirs is the kingdom of
heaven", while the six between promise in the future. Set beside the
Gradual's *nihil deest timentibus eum* (Ps 33:10), and beside Basil's reading
of v. 11, it makes the promise one of a good held while bread and safety are
lacking; the Offertory's just, who "seemed to die", have it at the end. The
speech states this as what the texts say, in the preacher's voice. With
unrelated readings the argument does not survive: each step rests on Ps
33:10-11 (with the omitted 11a), Mt 5:3 and 5:10, Wis 2:20 and 3:1-3, or Apoc
7:9-10.

**The homily's own connections.** The terminal note lists them and credits
them to no Father: the Gradual read with the two present-tense beatitudes;
the Gradual and the Offertory taken together (the third interpretation's own
inference); the Secret's *iustorum* taken for the saints of the feast; the
Lesson's multitude said to include the Gospel's poor and persecuted and the
Offertory's just; the Gradual's "all ye his saints" said to be spoken to the
assembly, from Bernard's words on the night office; Basil's "God himself" set
beside the Eucharist, which Basil does not say; Augustine's objector as the
pattern of the response; Basil on Ps 32:1 read with the Introit antiphon.
The half-verse the Gradual omits (Ps 33:11a) is quoted from the Douay and
said to be omitted; Augustine's comment on it (the living bread) is not used.

**Length and pace.** The spoken body is about 1,400 words (1,401 by a plain
word count of the component with LaTeX commands removed), about 10.8 to 11.7
minutes at an unhurried 120 to 130 words a minute. That is an estimate by
arithmetic; no one has delivered or timed the homily. It was read through in
full, silently, for sense and ease of speech; no audible rehearsal took place.

**Proof.** Built with `make doc` (provider `claude`), settled with no
overfull or underfull box, undefined reference or rerun warning; every font
embedded (Latin Modern). PDF SHA-256
`fde1946bac776bd192c5d825497b529d142a3494884b422b79387a1f5c37faff`, 4 pages
(letter): the spoken body in two columns on pages 1-2, the note on page 3, the
References, revision timestamp and rights colophon on page 4. Every page was
inspected at page resolution.

**Author checks run.** `tools/check-proper-components` in the content and
artifacts phases for the homily edition; every `check-content-preflight`
check for the homily edition, including references-used (8 entries),
house-voice (3 files), structural-meta-labels (9 labels), bindings-valid,
restricted-not-reproduced and provenance-matches-run for this run. All pass.
`make check-sources` now passes the document catalogue's homily entrypoint
test; it still fails, as expected at this stage, on the installed PDFs, which
are older than the sources, and on the stale publication-inventory hashes of
the leaf's files, both of which belong to the install and publication stages.

**Carried for other owners.** None new. The defects reported at author-study
and derive-synthesis stand.

## Derive-homily, run `450355254538c1ba`, iteration 1 (28 October 2026)

**Scope.** The repair of the homily review's four blocking findings
(HOM-001 to HOM-004) and its two advisories (HOM-005, HOM-006), in the spoken
body (`sections/homily/10-homily.tex`), the terminal note
(`sections/homily/90-note.tex`) and the entrypoint's PDF subject line. The
manifest, the research, propers and context records, the expansive study and
the concise study were not changed. The shared generation record carries a
new revision timestamp; its provenance line already named this run.

**HOM-001 (the Gospel's qualifiers).** Every paraphrase of Mt 5:3, 5:6 and
5:10 now keeps the Gospel's words: the poor in spirit, those who hunger and
thirst after justice, those who suffer persecution for justice' sake. The
speech no longer says that the kingdom belongs to the poor or the hungry as
such. The Gradual and the Gospel are joined through Augustine's pairing of
the fear of the Lord with the poor in spirit (*De serm. Dom.* I.3.10, the poor
in spirit "not puffed up, while the soul submits itself to divine authority";
I.4.11, "The fear of God corresponds to the humble, of whom it is here said,
'Blessed are the poor in spirit'", NPNF I.6): on his reading the Gradual's man
who fears the Lord and the Gospel's poor in spirit are the same humble man, and
the speech takes the Gradual's "nothing is lacking" and the first beatitude's
present "theirs is the kingdom" as one promise, marked in the speech as the
preacher's inference ("We may take these as one promise"). That the kingdom
belongs to those persecuted for justice' sake while they suffer it is read
from the present tense of Mt 5:10. The saints' bodily want is answered by
Basil and Aquinas, not by the first beatitude. Bernard's voluntary poverty
(sermo 1 n. 15) and Schuster's remark were not used. The note's list of the
homily's own connections describes the join as rewritten.

**HOM-002 (Augustine's hearer).** The speech now reports Augustine as the
locus has him (*Enarr. in Ps.* 33 s. 2 n. 14, Migne Latin, read at the locus
in the registered Wikisource text): he puts the complaint in the heart of one
of his hearers ("et dicis in animo tuo"), tells him not to say it ("Attende,
et noli dicere"), admits only that, taken by the letter, the verse seems to
deceive, and warns that whoever reasons so is caught in a snare, seeking
perishable food on earth and not the true reward in heaven ("Sic cogitantem
suffocat laqueus scandali. Escam enim mortalem quaerit in terra, et veram
mercedem non quaerit in coelo"). "Heard that objection from his own people",
"grants the man his point" and "mistaken only" are gone. The response keeps
the hearer's daily practice as its pattern, after the speech has reported
Augustine's verdict, and the note records that use as the homily's own: the
snare and the "noli dicere" go beyond what the expansive study reports, and
the note says so.

**HOM-003 (the closing run of authorities).** The paragraphs from the
Lesson to the response were rewritten so that the preacher carries each step.
Bernard's night-office words are given plainly (the saints in glory no longer
need the command, because they no longer fear; it is said to us), with one
short quotation, "Meanwhile our whole beatitude is to fear God", and his
contrast with the saints' feast in joy and praise (sermo 5 n. 3). Augustine's
scheme is explained where it is first used, in the Gospel step (he matches the
beatitudes with the gifts of the Holy Spirit; the fear of the Lord and the
poor in spirit each come first, and both are humility), so no "first step" is
left unexplained later. Basil's sentence on fear is plain speech. Bernard's
n. 5 is given with its reasoning (the saints do not need our honours; we keep
their memory for our own sake, because it makes us want to be with them), and
one sentence states the connection to the Collect and Postcommunion: "So the
prayers of this Mass ask for us."

**HOM-004 (repetition and the reversal).** The sentence restating the
present-tense beatitudes as a reversal, the restatement of the Offertory
antiphon, and the three-part "went without ... did not go without God"
sentence are gone, with the "go without" wording throughout. The Gradual and
the Offertory are put together once: the Offertory shows the good the just
man kept when men took his life; he is in God's hand, and God himself, as
Basil said, is the good the Gradual promised.

**Advisories.** HOM-005: the Aquinas sentence was split, 1 Cor 4:11 is
rendered "to that very hour", and the explanation of when the Secret is said
was dropped. HOM-006: the note now states which patristic words are quoted
(Augustine's hearer's complaint, Augustine's gloss on Ps 87, now in quotation
marks in the speech, Bernard's "our whole beatitude", Chrysostom's "Both here
and there") and which are paraphrased, and says plainly that the Offertory is
the Lasance's English of the antiphon, quoted without its closing *Alleluia*.

**What the text changes.** The listener's assumption is that a promise of no
want to those who fear God is a promise to be kept from want, and that the
saints' poverty and deaths show it failing. The decisive textual detail is the
present tense of Mt 5:3 and 5:10, "theirs is the kingdom of heaven", said of
the poor in spirit and of those persecuted for justice' sake, read with
Augustine's pairing of the poor in spirit and the fear of the Lord: the man
the Gradual tells to fear is the man to whom the kingdom already belongs.
With Basil's "God himself" and the Offertory's just in God's hand, the
promise is one of a good held while bread and safety are lacking. With
unrelated readings the argument does not survive: each step rests on Ps
33:10-11 (with the omitted 11a), Mt 5:3, 5:10, Wis 2:20 and 3:1-3, or Apoc
7:9-10.

**Length and pace.** The spoken body is about 1,360 words (1,359 by a plain
word count of the component with LaTeX commands removed), about 10.5 to 11.3
minutes at an unhurried 120 to 130 words a minute. That is an estimate by
arithmetic; no one has delivered or timed the homily. It was read through in
full, silently, for sense and ease of speech; no audible rehearsal took place.

**Proof.** Built with `make doc` (provider `claude`), settled with no
overfull or underfull box, undefined reference or rerun warning; every font
embedded (Latin Modern). PDF SHA-256
`9114d448930550081e6db81281e5d1efa60257dfadfc6a6a608c84d5e789e79b`, 4 pages
(letter): the spoken body in two columns on pages 1-2, the note on page 3, the
end of the note, the References, revision timestamp and rights colophon on
page 4. Every page was inspected.

**Author checks run.** `tools/check-proper-components` in the content and
artifacts phases for the homily edition; every `check-content-preflight`
check for the homily edition, including references-used (8 entries),
house-voice (3 files), structural-meta-labels (9 labels), bindings-valid,
restricted-not-reproduced, and provenance-matches-run for this run. All pass.
`make check-sources` fails, as expected at this stage, on the stale
publication-inventory hashes of the leaf's files, which belong to the
publication stage.

**Carried for other owners.** None new. The defects reported at author-study
and derive-synthesis stand.

## Build-artifacts, run `450355254538c1ba`, iteration 0 (28 October 2026)

**Scope.** The three documents built for visual review with `make doc`
(provider `claude`) from the sources as their reviews left them. No source,
manifest, research or generation-metadata file was edited at this stage: there
were no layout repairs, so no content seal is affected and the revision
timestamp stands as the derive-homily stage set it.

**Artifacts.**

| Output | Path | Pages | SHA-256 |
| --- | --- | --- | --- |
| Expansive study | `build/claude/liturgy/roman-rite/1962/propers/temporal/f02-all-saints.pdf` | 31 | `215c58fa6f029ed11b31c130a6c59cb0686bf82c1691ed8ea811bca1a61dbd4a` |
| Concise study | `build/claude/liturgy/roman-rite/1962/propers/temporal/f02-all-saints-synthesis.pdf` | 11 | `99dfb13bfbf465534362eaaf8a3e543566091444d99749409211bf77e49a0bb5` |
| Homily | `build/claude/liturgy/roman-rite/1962/propers/temporal/f02-all-saints-homily.pdf` | 4 | `9114d448930550081e6db81281e5d1efa60257dfadfc6a6a608c84d5e789e79b` |

All three are US letter, PDF 1.7, unencrypted. The expansive study's 31 pages
lie within 20–50 and the concise study's 11 within 10–12. The homily's bytes
are identical to the derive-homily iteration 1 proof.

**Concise opening (physical pages, from the settled auxiliary file).**
Inventory start and end, overview start and end and all four sense markers
(literal, allegorical, moral, anagogical) on page 1; chronology start and end
on page 2; themes starting on page 3 and ending on page 4; commentary starting
on page 5. Auxiliary SHA-256
`803e9a36861d8b0511c6cba755827c30416f3f67a56ca7f6f4fe94ee7aa36140`.

**Logs.** Each build settled within the Makefile's passes. None of the three
final logs, nor the full build output, carries an error, overfull or underfull
box, undefined or multiply defined reference, rerun request, missing character
or font warning. The Makefile's own checks passed: contents lines each on their
own anchor (61 in the expansive study, 13 in the concise study), proper
component manifest valid, generation metadata valid.

**Fonts and structure.** Every font in all three PDFs is an embedded, subset
Type 1 Latin Modern face (13, 14 and 11 font objects respectively). Each PDF
parses without error in Ghostscript and `pdfinfo`. The PDFs are untagged.

**Extraction.** `pdftotext -layout` gives one page per physical page in each
file (19,272, 7,967 and 3,006 words including apparatus), with no unresolved
`??`, stray control sequence or replacement character.

**Checks.** `tools/check-proper-components` in the artifacts phase for the
research, synthesis and homily editions passes. The snapshot
(`scripts/_proper_study.py snapshot`) wrote `research/artifacts.json` with the
three PDF hashes above, both pagination auxiliaries and the declared render
inputs. Page rasters and contact sheets were generated with
`tools/tpt pdf-review` into the run's build-artifacts iteration 0 directory,
and the logs, auxiliaries, contents file and extracted texts were kept beside
them, outside the raster directory.

**Remaining limitations.** At this stage the pages were seen only on the
contact sheets, at reduced size; no overlap, empty page or stranded colophon
appears there, and the visual review must still inspect every page at page
resolution and perform the passage-to-occurrence/place/date lookup on the
concise page 2 table. PDF structure was checked by parse, not by a dedicated
validator. The installed PDFs and the publication inventory are not touched
here; they belong to the install and publication stages.

**Carried for other owners.** None new. The defects reported at author-study
and derive-synthesis stand.

## Derive-synthesis, run `450355254538c1ba`, iteration 2 (28 October 2026)

**Scope.** Repair of the visual review's blocking finding VIS-001 in the
concise study, with its advisory VIS-003 cleared in the file touched. Changed:
`synthesis.tex` (a `\Needspace{12\baselineskip}` before the apparatus import,
with its comment), `sections/concise/10-commentary.tex` (one closing quotation
mark), and the revision timestamp of the shared generation record, whose
provenance line already named this run. The manifest, the research, propers
and context records, the expansive study and the homily were not changed.

**VIS-001 (repaired).** The apparatus sets `\runninghead{Scope and
References}` before its section heading, so the mark fell at the foot of
page 9 and the heading moved to page 10. The guard now ends the page before
the mark whenever the appendix cannot start where the commentary ends, as the
expansive study's guards do before its sections. Page 9 is headed "Detailed
Commentary" and "Scope and References" first appears on page 10, where the
appendix begins. This clears the running-head defect carried for the shared
format's owner at iteration 1, for this document; the shared format itself
was not changed.

**VIS-003 (advisory, cleared).** The Aquinas quotation on page 6 now closes
the inner single quotation before the outer double one (“happiness,’” in the
words"). The text layer has 100 opening and 100 closing double quotation
marks.

**Extent.** Unchanged: 11 physical pages, and the word counts of iteration 1
stand (substantive body, page 1 through the commentary, about 6,400 words);
the repair changes no word.

**Placement.** The settled auxiliary file places the inventory, the overview
and its four sense markers on physical page 1, the chronology on page 2, the
themes from page 3 to page 4, and the commentary's start on page 5, as before.
The extracted text differs from the iteration-1 proof only in the quotation
mark, the page-9 running head and the revision timestamp.

**Proof.** Built with `make doc` (provider `claude`), settled with no
overfull or underfull box, undefined reference or rerun warning. PDF SHA-256
`b60a84535a2b3bc6e79fafe4d237f5c340a5ffa0e40fb584662a9609cf75e71e`, 11 pages.
Every page was inspected on the contact sheet, pages 9 to 11 at page
resolution, and the page-6 quotation in a 400-dpi crop.

**Author checks run.** `tools/check-proper-components --phase artifacts
--edition synthesis`; every `check-content-preflight` check of the synthesis
edition, including references-used (27 entries, 23 loci), house-voice
(8 files), structural-meta-labels (18 labels), the three chronology checks and
provenance-matches-run. All pass.

**Carried for other owners.** VIS-002 (advisory) stands in the expansive
study: `sections/20-sealed-number-uncounted-crowd.tex` misnests the same
Aquinas quotation's closing marks, and that file belongs to the study's owner.
The defects reported at author-study and derive-synthesis otherwise stand.

## Derive-homily, run `450355254538c1ba`, iteration 2 (28 October 2026)

**Scope.** The homily derived again after the concise study's repair at
derive-synthesis iteration 2 and its passing review. That repair changed one
quotation mark and a page guard in the concise study; the expansive study was
not changed, and nothing the homily relies on moved. The homily was read
against both studies as they now stand and revised in place: the spoken body
(`sections/homily/10-homily.tex`), the terminal note and References
(`sections/homily/90-note.tex`), and the entrypoint's PDF subject line. The
revision clears the four advisories of the homily review at iteration 1
(HOM-007 to HOM-010), which no packet forwarded. The manifest, the research,
propers and context records, the expansive study and the concise study were
not changed. The shared generation record carries a new revision timestamp;
its provenance line already named this run.

**What changed in the speech.**

- The join of the Gradual and the Gospel is drawn in the preacher's voice:
  if the fear of the Lord belongs to the poor in spirit, the man the Gradual
  tells to fear is the man the Gospel calls poor in spirit, and to that one
  man the Gradual promises that nothing is lacking and the Gospel that the
  kingdom is his now. "On his reading" and "We may take these as one promise"
  are gone (HOM-007). Augustine's count of the gifts is said to run upward
  from the lowest, so that the fear of the Lord stands first (*De serm. Dom.*
  I.4.11, "if we reckon as it were in a gradually ascending series, there the
  fear of God is first"), which a hearer who knows Isa 11:2-3 from wisdom
  downward would otherwise mishear (HOM-010).
- The join of the Gradual and the Offertory is drawn the same way: the wicked
  put the just man to death and he is in God's hand; God himself, Basil said,
  is the good the Gradual promised; so the just man kept that good. The
  Offertory is no longer credited with the inference (HOM-007).
- The physician is credited to Augustine as Aquinas reports him. At *In Ps.*
  33 n. 10 (Parma vol. 14 p. 206, registered OCR physical lines 42642-42652)
  Aquinas writes "Sed objicit Augustinus in serm. Dom. in mont." with 1 Cor
  4:11, and "Et dicit quod Deus est nutritor et medicus"; Augustine, *De serm.
  Dom.* II.17.58 (NPNF I.6, registered text physical lines 5850-5878), answers
  St Paul's hunger with "that Physician" who sets such things before us and
  takes them away "just as He judges it expedient for us". The speech now says
  that Augustine had met the objection and that Thomas gives Augustine's
  answer; Thomas keeps the spiritual goods and the help in need, which are his
  own at n. 10, and the difference between Basil and Aquinas over bodily goods
  stands (HOM-009). The note's loci, the References and the PDF subject
  follow.
- Aquinas's sentence now reads "takes the verse first as a promise of the
  goods of the spirit" (HOM-010).
- Augustine's answer to his hearer is given from the locus: after the snare
  (n. 14) he tells the man not to understand the verse so, and says that the
  goods are spiritual (n. 15, "Noli ergo sic intelligere. Et quomodo
  intelligam? In bonis spiritualibus", Migne Latin, read at the locus in the
  registered Wikisource text). The earlier "he tells the man not to say it"
  rested on n. 14's "Attende, et noli dicere", which Augustine says before he
  quotes the verse, of the man who fears God and is poor while the rich man
  prospers; n. 15's words follow the snare and answer the verse itself.
- Basil on fear is joined to Bernard's point by Basil's own reading of
  *non est inopia*: whoever is kept by fear from every shameful act lacks
  nothing he needs for any virtue (*Hom. in Ps.* 33 n. 6, "Timenti itaque non
  est inopia; hoc est ..."), so the sentence no longer stands appended without
  a bearing (HOM-008).
- The close gives one response, said once: seek the Lord as faithfully as
  Augustine's hearer did, and seek him for himself. The hearer's fault is
  named from n. 14 (he measured what he had against the rich man's goods:
  "ego timeo Dominum, ille non timendo quantum acquisivit"). The second
  imperative, the repeated warrant from Aquinas and the Communion paragraph's
  closing restatement of the thesis are gone; the paragraph says how the
  Communion's vision relates to the Christ received (he gives himself at the
  altar, hidden under the sacrament; the clean of heart will one day see him
  face to face). The thesis is stated in the conclusion once (HOM-008).

**What the text changes.** The listener's assumption is that a promise of no
want to those who fear God is a promise to be kept from want, and that the
saints' poverty and deaths show it failing. The decisive textual detail is the
present tense of Mt 5:3 and 5:10, "theirs is the kingdom of heaven", said of
the poor in spirit and of those persecuted for justice' sake, read with
Augustine's gift of the fear of the Lord to the poor in spirit (*De serm.
Dom.* I.4.11): the man the Gradual tells to fear is the man to whom the
kingdom already belongs. With Basil's "God himself" and the Offertory's just
in God's hand, the promise is one of a good held while bread and safety are
lacking. With unrelated readings the argument does not survive: each step
rests on Ps 33:10-11 (with the omitted 11a), Mt 5:3, 5:10, Wis 2:20 and 3:1-3,
or Apoc 7:9-10.

**Length and pace.** The spoken body is about 1,370 words (1,367 by a plain
word count of the component with comments and LaTeX commands removed), about
10.5 to 11.4 minutes at an unhurried 120 to 130 words a minute. That is an
estimate by arithmetic; no one has delivered or timed the homily. It was read
through in full, silently, for sense and ease of speech; no audible rehearsal
took place.

**Proof.** Built with `make doc` (provider `claude`), settled with no
overfull or underfull box, undefined reference or rerun warning; every font
embedded (Latin Modern Type 1). PDF SHA-256
`a6630b389583e729bbaa18103fb48364e2767d47485ecbddeb4ddbef4d3bc2ac`, 4 pages
(letter): the spoken body in two columns on pages 1-2, the note on page 3,
the end of the note, the References, revision timestamp and rights colophon
on page 4. Every page was inspected.

**Author checks run.** `tools/check-proper-components` in the content and
artifacts phases for the homily edition, and the content-phase
`scripts/_proper_study.py check` with the presentation, format, authority and
orientation requirements; every `check-content-preflight` check of the homily
edition, including references-used (8 entries), house-voice (3 files),
structural-meta-labels (9 labels), bindings-valid, restricted-not-reproduced,
unquoted-not-quoted and provenance-matches-run for this run. All pass. The
artifacts-phase `_proper_study.py check` reports that the built PDFs and
render inputs differ from the visual-review snapshot in
`research/artifacts.json`, as they must until the build stage snapshots them
again. `make check-sources` fails, as expected at this stage, on the stale
publication-inventory hashes of the leaf's files, which belong to the
publication stage.

**Carried for other owners.** The physician that the expansive study
(`sections/40-no-want-just-in-gods-hand.tex`, the Aquinas paragraph and the
closing comparison of the four Fathers), the concise study
(`sections/concise/10-commentary.tex`, the Aquinas answer), `research/scope.md`
(the Aquinas entry of the Gradual's reception) and `research/interpretations.md`
(Reading C, Aquinas) credit to Aquinas is, on Aquinas's own report at *In Ps.*
33 n. 10, Augustine's (*De serm. Dom.* II.17.58), adopted by Aquinas. The
argument and the Basil-Aquinas difference are unaffected; the attribution
belongs to the research and study owners when those records are next revised.
The defects reported at author-study and derive-synthesis otherwise stand.

## Build-artifacts, run `450355254538c1ba`, iteration 1 (28 October 2026)

**Scope.** The three documents built again for visual review with `make doc`
(provider `claude`) from the sources as their reviews left them, after the
concise study's repair at derive-synthesis iteration 2 and the homily's at
derive-homily iteration 2. No source, manifest, research or generation-metadata
file was edited at this stage: there were no layout repairs, so no content seal
is affected and the revision timestamp stands as the derive-homily stage set it.

**Artifacts.**

| Output | Path | Pages | SHA-256 |
| --- | --- | --- | --- |
| Expansive study | `build/claude/liturgy/roman-rite/1962/propers/temporal/f02-all-saints.pdf` | 31 | `08f8c5e99572d5f8a9584555c47b901bc32abd09fdf74dd5d7094f387143c3bc` |
| Concise study | `build/claude/liturgy/roman-rite/1962/propers/temporal/f02-all-saints-synthesis.pdf` | 11 | `fb899d0258fe16641fb2be454eb088f37fd41011012fe599b5fb2d5ac397c881` |
| Homily | `build/claude/liturgy/roman-rite/1962/propers/temporal/f02-all-saints-homily.pdf` | 4 | `a6630b389583e729bbaa18103fb48364e2767d47485ecbddeb4ddbef4d3bc2ac` |

All three are US letter, PDF 1.7, unencrypted. The expansive study's 31 pages
lie within 20–50 and the concise study's 11 within 10–12. The homily's bytes
are identical to the derive-homily iteration 2 proof.

**Concise opening (physical pages, from the settled auxiliary file).**
Inventory start and end, overview start and end and all four sense markers
(literal, allegorical, moral, anagogical) on page 1; chronology start and end
on page 2; themes starting on page 3 and ending on page 4; commentary starting
on page 5. Auxiliary SHA-256
`803e9a36861d8b0511c6cba755827c30416f3f67a56ca7f6f4fe94ee7aa36140`; the
expansive study's auxiliary SHA-256 is
`935e267e37a10be62da920538d2396ccf8fe31812ab7f9cfaf77b2ca8f965d31`.

**Logs.** Each build settled within the Makefile's passes. None of the three
final logs carries an error, overfull or underfull box, undefined or multiply
defined reference, rerun request or font warning. The Makefile's own checks
passed: contents lines each on their own anchor (61 in the expansive study, 13
in the concise study), proper component manifest valid, generation metadata
valid. Two engine messages that are not warnings remain in the expansive
study's log: TeX's "ignored: Infinite glue shrinkage found in box being split"
at page 3, where the opening's map table breaks and carries its last row
(Commemoration Postcommunion) to the top of page 4, a message the same shared
map produces at the same place in other leaves; and microtype's information
that small-caps character 029 has no protrusion setting. Neither moves text.

**Fonts and structure.** Every font in all three PDFs is an embedded, subset
Type 1 Latin Modern face (13, 14 and 11 font objects respectively). Each PDF
parses without error in Ghostscript and `pdfinfo`. The PDFs are untagged.

**Extraction.** `pdftotext -layout` gives one page per physical page in each
file (19,272, 7,966 and 3,261 words including apparatus), with no unresolved
`??`, stray control sequence or replacement character.

**Checks.** `tools/check-proper-components` in the artifacts phase for the
research, synthesis and homily editions passes, and so does the artifacts-phase
`scripts/_proper_study.py check` with the presentation, format, authority,
orientation-v2 and source-disposition requirements. The snapshot
(`scripts/_proper_study.py snapshot`) wrote `research/artifacts.json` with the
three PDF hashes above, both pagination auxiliaries and the declared render
inputs. Page rasters and contact sheets were generated with
`tools/tpt pdf-review` into the run's build-artifacts iteration 1 directory,
and the logs, auxiliaries, contents file, build output and extracted texts were
kept beside them, outside the raster directory.

**Remaining limitations.** At this stage the pages were seen on the contact
sheets, at reduced size, and page 3 of the expansive study at page resolution;
no overlap, empty page or stranded colophon appears there. The visual review
must still inspect every page at page resolution and perform the
passage-to-occurrence/place/date lookup on the concise page 2 table. PDF
structure was checked by parse, not by a dedicated validator. The installed
PDFs and the publication inventory are not touched here; they belong to the
install and publication stages.

**Carried for other owners.** None new. The defects reported at author-study,
derive-synthesis and derive-homily stand.

## Install-publication, run `450355254538c1ba`, iteration 0 (28 October 2026)

**Completed reviews.** The engine's recorded results for this run, by stage.
The SHA-256 is that of the accepting result as the run state records it.

| Review | Iterations and dispositions | Accepting result SHA-256 |
| --- | --- | --- |
| Research review | 0–2 changes required (8, 3 and 1 blocking findings); 3 pass, 1 advisory | `b887ef96c17a26f7cc0c8d3b4a6433e00d54ccae714756986c5629079fcb3031` |
| Study review | 0 changes required (8 blocking); 1 pass, 3 advisories | `f8656645fcd76073e70afd14beee7a124a2ab3e32674fb32cdaef3d524461af4` |
| Synthesis review | 0 changes required (1 blocking); 1 pass, 5 advisories; 2 pass after the visual-review repair, 5 advisories | `a0b860d80fca979ca4e5d7afee0861e9636b6da49a7a5595b22fa1f677f6739a` |
| Homily review | 0 changes required (4 blocking); 1 pass, 4 advisories; 2 pass on the re-derived homily, 2 advisories | `a0823a8e73897679ed453c76ceec26f54fcbc64d00f0db1bca12637eae76689f` |
| Artifact gates | 0 pass; 1 pass on the rebuilt artifacts | `8d6a7c139b783c8489d67a5012f7cc8e3099b15e615f90603c523961611646cd` |
| Visual review | 0 changes required (1 blocking, 1 accepted); 1 pass, 2 advisories, VIS-004 and VIS-006 accepted | `7b5574541e91c111ba1a5618a0b3bbda1de4b888a71c38a1c618e9732927588a` |
| Web review | 0 pass, no findings | `33afae0c6252ca8334d7ac0a4d4527776d0ceabb78269ad0c460c3922a91adb8` |

**Snapshot.** Before installation every render input, both pagination
auxiliaries and the three PDF hashes in `research/artifacts.json` matched the
tree, and the artifacts-phase `scripts/_proper_study.py check` passed with the
presentation, format, authority and orientation-v2 requirements.

**Installed PDFs.** `make install-doc PROVIDER=claude` for the bare ID,
`-synthesis` and `-homily`, with the normal recipes and checks; the build
PDFs were already current, so nothing was retypeset. Each build and installed
PDF equals its reviewed SHA-256:

| Output | Installed path | SHA-256 |
| --- | --- | --- |
| Expansive study | `pdf/claude/liturgy/roman-rite/1962/propers/temporal/f02-all-saints.pdf` | `08f8c5e99572d5f8a9584555c47b901bc32abd09fdf74dd5d7094f387143c3bc` |
| Concise study | `pdf/claude/liturgy/roman-rite/1962/propers/temporal/f02-all-saints-synthesis.pdf` | `fb899d0258fe16641fb2be454eb088f37fd41011012fe599b5fb2d5ac397c881` |
| Homily | `pdf/claude/liturgy/roman-rite/1962/propers/temporal/f02-all-saints-homily.pdf` | `a6630b389583e729bbaa18103fb48364e2767d47485ecbddeb4ddbef4d3bc2ac` |

**Web edition.** The reviewed conversion
`build/web/claude/liturgy/roman-rite/1962/propers/temporal/f02-all-saints.md`
was installed byte for byte at
`web/claude/liturgy/roman-rite/1962/propers/temporal/f02-all-saints.md`
(SHA-256 `cbe405ad17c9ba6be5d64d37891a282e99700df9a1ded3528ab595931cf0438c`,
equal to `research/web-artifact.json`) and staged.

**Release records and catalog.** The three records under
`release/publications/claude/liturgy/roman-rite/1962/propers/temporal/`
already name the exact IDs, `library/traditional-latin-mass.md`, `alpha` and
the standing authorization `perpetual-public-repository-2026`;
`make add-publication` refused to overwrite them and they are unchanged. The
F02 row's Claude cell already links Full PDF, Synthesis PDF, Homily PDF and
Read in the manifest's label order (the manifest declares `complete` and
`Full PDF`), and the page carries the leaf's Claude publication marker;
neither was changed. The document catalogue was regenerated with
`tools/tpt document-library structure`; its changes are confined to this
leaf's entry (page counts 31 and 11, the homily's title and subject, the
generation record and revision timestamp) and the aggregate counts derived
from it. Release bindings were refreshed with
`make refresh-release-bindings ONLY=...` for the catalogue, the installed web
edition and the source-projection files this run's source registration
changed, and with `ADOPT=1` for only the three new source-projection editions
it created; the tool rewrote the rights record's site-source table and its
hash for those same paths.

**Checks.** Before handing over, the publication-phase
`scripts/_proper_study.py check`, `make check-release-bindings` (0 stale),
`tools/tpt public-alpha check` scoped to this leaf, both document-library
checks and `make check-web-editions-current` passed. The program gate decides
acceptance.
