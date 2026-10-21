# Production review record

Run-specific production and review facts for the Claude 1962 leaf
`liturgy/roman-rite/1962/propers/temporal/f01-christ-the-king` (catalog `F01`,
*D. N. Iesu Christi Regis*), `proper-study` v12, run `7397c12187517ff2`,
seeded at commit `9b87d598b34870344f3df756982af1ff5990d993`. Research and its
cold review (research-review iteration 2, PASS) precede this record; their
evidence is `research/scope.md`, `research/interpretations.md`,
`research/context.md` and `propers/verified.md`, which this record does not
restate.

## Author-study, iteration 0 (19 October 2026)

**Scope.** The expansive study (`main.tex`) of the Mass said on Sunday
25 October 2026: opening with the occurrence and an element map; the appointed
Latin of the eleven said elements (the proper Preface among them) with their
public-domain English; the votive Tract and the paschal Alleluia set out under
their rubrics as printed text for other days; the element-by-element settings;
three readings of the whole formulary (`lamb-receives-the-kingdom`,
`kingdom-not-from-hence`, `kingdom-handed-over`), each with its own four
senses; a comparison; the Scriptural Date and Location appendix on the nine
generated `orientation-v2` rows; the scope appendix and References. The
schema-2 `proper-components.toml` declares the future concise and homily
components and the `interpretive-pagination-v1` presentation roles; the
leaf-local `format.tex`, `web-edition.toml` (eligible) and
`generation-metadata.tex` were written.

**Element keys.** Eleven: the said elements in liturgical order, with
`preface`. The Tract (no. 3943) and the paschal Alleluia (no. 3944) can never
be said on the feast, which falls on the last Sunday of October; they are not
manifest elements and carry no proper anchor. The chronology projection still
carries the Tract (the shared calendar entry is unchanged in this run), so its
two rows print in the appendix with the rubric's label of
`research/scope.md` §8.2, and the paschal Alleluia is accounted for in the
Daniel composition row's phrase (§8.3).

**Extent.** 32 physical pages (letter, Latin Modern, 11 pt). Approximate prose
word counts by component, LaTeX and the set Latin and English blocks
excluded: opening 1,650; appointed-text notes 1,190; each element 3,690; the
three readings 2,950, 3,250 and 2,600; comparison 730; Scriptural Date and
Location 1,250; scope and References 1,390. The exposition proper (opening
through comparison) is about 16,000 words, above the profile's 6,000–10,000
planning range; the range is not a quota, and the PDF stays well within the
20–50-page extent.

**Readings and their carrying authors.** First reading: Hilary of Poitiers,
Thomas Aquinas, Bede. Second: Augustine of Hippo, John Chrysostom, Robert
Bellarmine. Third: Augustine of Hippo, Hilary of Poitiers. Cassiodorus and
Theodoret (ecclesiastical writers), Cyril of Alexandria, Cyril of Jerusalem,
the Hippolytus scholia and Victorinus (no standing rows) support claims only.
Schuster is cited element by element; the only join between two elements
credited to him is the Gradual with the Alleluia as *the double chant*.
Augustine's *Letter* 185 is cited with its Donatist occasion stated;
Schuster's p. 203 paragraph on papal deposition is not used.

**Loci re-read while authoring.** Beyond the research record, these quotations
were checked against the same witnesses before use: Augustine, *Tract. in Io.*
115.1–4 (section numbers and wording, tracked NPNF I.7 text); *En. in Ps.*
2.6–9, 28.10–11 and 71.13–14 (tracked NPNF I.8 text); *De Trinitate* I.8.15–17
and I.10.20–21 (the research stage's copy of the New Advent page), which fixed
the section of each quotation; Hilary, *Tract. in Ps.* 2.30–33 (research
copy of the registered CSEL 22 OCR, SHA-256 matched), which placed the Acts
13:33 argument in §30, *accepit ergo hereditatem* in §31 and *ut esset, quod
fuerat ante* in §33, correcting the iteration's first draft; Hilary, *De
Trin.* XI.39–40 and Cyril of Jerusalem, *Catech.* 15.27–30 (tracked NPNF
texts); Chrysostom, *Hom. in Io.* 83.4 and 84.1 (research copies of the New
Advent pages); Aquinas, *Super Ps.* 2 nn. 5–6, 9 (research copy of the
registered `cps02` page), which corrected the minister/lord clause to its
Peter-and-Paul form; Cassiodorus on Ps 2 and 71 (research copies), which gave
the Ps 71:11 Latin *reges adorabunt, qui putantur adorandi; gentes autem
servire, quae terrenos dominos habere noscuntur*; Augustine, *Letter* 185.19–20
(research copy). Every Douay–Rheims verse quoted was read in the tracked
Challoner verse texts.

**Source limits carried into the study.** As `research/scope.md` §§7 and 11
record: no witness comments on Apoc 5:12's *accipere divinitatem* itself; the
composed Collect, Secret, Preface and Postcommunion have no patristic
commentary as texts; Bellarmine is read in O'Sullivan's abridged English;
Cassiodorus, Aquinas and parts of Theodoret are read in web transcriptions or
text layers; *Quas primas* is cited by number in the Holy See's English.

**Proof.** Built with `make doc` (provider `claude`), settled with no
overfull box, undefined reference or rerun warning. PDF SHA-256
`2d4e34d556a7256eeaa1b31d2c2fcd17fdf0c641e05904961f5e3f997eaf217a`, 32 pages,
fonts all embedded Latin Modern, revision timestamp 2026-10-19T18:45:07Z.
Every page was inspected at reduced size; the forced page break before the
readings was replaced by a space check so that no section leaves a half-empty
page or a sparse spill page. The last orientation row
(Apocalypse) of the study's appendix table runs onto the following page;
the concise page 2 is a separate composition.

**Author checks run.** `tools/check-proper-components --phase artifacts
--edition research` (pass); the study-preflight component contract with
`--require-presentation --require-format --require-authority
--require-orientation --require-orientation-v2` (pass); `check-content-preflight`
references-used, identifiers-resolve, bindings-valid, restricted-not-reproduced,
relation-coverage, unquoted-not-quoted, structural-meta-labels, house-voice,
chronology-record-current, chronology-annotations-current,
chronology-claims-supported and provenance-matches-run (all pass); and the
canonical web-edition probe with pandoc and the pinned Python Markdown (pass,
all eleven proper anchors present).

**Defects reported for their owners, not repaired here.**

- *Web converter (`tools/web-edition`).* An orientation row whose
  occurrence-and-place phrase carries `\textit` or `\emph`, which
  `check-content-preflight` admits in that argument, fails the converter's
  "generated chronology annotation payload shortfall" audit, because
  `normalize_audit_text` unwraps `\textbf` but not the italic forms. The study
  sets its quoted titles and phrases in those rows in quotation marks instead.
- *Shared calendar entry `christ-the-king`* (as `research/scope.md` §10): the
  Tract is stored without its votive condition and the paschal Alleluia is
  absent, which is why the Tract's rows print on page 2.
- The other shared-record reports of `research/scope.md` §10 stand unchanged
  (Ps 71:1 numbering, the Challoner Ps 28 verse division, chronology-corpus
  gaps at the trial before Pilate and Dan 7:1, ledger and registry rows).

## Author-study, iteration 1 (19 October 2026)

**Scope.** Repair of the study review's two blocking findings, with the
advisories that could be cleared in the same files. No research, propers or
instance record was changed.

- *STU-001 (process narration in the body).* The sentences that stated the
  research record's citation rules or the study's own handling of its
  witnesses were rewritten to state the material: the two placings of the
  Communion's session stand attributed to Augustine and Bellarmine without
  comment; *Letter* 185's distinction is given as Augustine's, drawn in
  defence of the laws against the Donatist schism; the close of the second
  reading's difficulty says what the witnesses and *Quas primas* hold;
  Schuster's treatment of the Preface is stated as a fact of his commentary;
  Augustine and Hilary are named without the manifest's authority term (the
  comparison table's row is now "Principal witnesses"); and Augustine's
  readings of Ps 2:7 (eternal generation) and Jn 18:37 (birth from the Virgin)
  are stated once, positively, in the comparison. Two further sentences of the
  same kind in the third and first readings were also rewritten.
- *STU-002 (comparative claims).* The comparison now places the difference
  between the first and second readings at the Gospel (a dominion received in
  the trial, against a power from above that needs nothing given), states that
  the Jn 18:37 split runs between the second reading's own principal witnesses
  and is where the first meets its objection, and says what each answer
  changes; the second reading now names that split and says that its argument
  rests on Jn 18:36 and the hearers of 18:37. The table's objection cell for
  the third reading is the teaching that the reign ends, which Cyril of
  Jerusalem opposes and Jerome answers from Dan 7:14; the internal differences
  of all three readings stand in a new row, "Differences among its
  witnesses". The shared claim about the cross is limited to what each
  reading says of it, and Hilary's contributions are counted to all three
  readings.
- *Advisories cleared.* STU-003: the first reading quotes the full clause of
  Hilary, *Tract. in Ps.* 2.33 (*in deum namque, quia nullum ultra deum nomen
  est, prouehitur*), read on the research stage's crop of CSEL 22 p. 62 (IA
  page image n91), and states once, as the reading's application of Hilary's
  and Bede's reasoning, what the Introit's *accipere … divinitatem* means.
  STU-004: the Gospel sentence on Jn 18:36 was rewritten. STU-005: the element
  section now names Schuster on the Gradual and the Communion, Augustine's
  "Carnal thyself" and Jerome on Dan 7:13–14 and points forward, leaving the
  quotation to the reading that develops it; the second reading no longer
  repeats Schuster's Postcommunion quotation. STU-006: the Introit's doxology
  is assigned to Apoc 1:6; the Postcommunion's uniqueness is narrowed to
  making the faithful soldiers; Hilary's two statements on the inheritance and
  the handing over are cited separately and their identification is given as
  the reading's own. STU-007 (a) and (b): the two orientation phrases were
  reworded.
- *Not repaired, for its owner.* STU-007 (c): the Tract's historical-setting
  note cannot state the Haydock qualification (Worthington's Davidic
  alternative and the Fathers' reading of Christ's kingdom) until
  `research/scope.md` §8.4 records it; this is the research-record gap of
  research-review advisory RES-014. The comparison paragraph of
  `research/interpretations.md` §5 still carries the wording the study review
  found untrue of the readings as written ("B as the place where the king
  testifies before Pilate"; "Hilary to A and C"; the column "Witness against
  it, kept" holding the third reading's internal differences); the study no
  longer follows it there.

**Extent.** 33 physical pages. Approximate words after the repair (LaTeX
stripped, set Latin and English blocks included where they fall in these
files): each element 3,700; the three readings 3,080, 3,350 and 2,630;
comparison 1,010.

**Proof.** Built with `make doc` (provider `claude`), no overfull or underfull
box, undefined reference or rerun warning. PDF SHA-256
`0af471dc75d583ebd1aa9a00db65ff9881976dc5f2f3b044ed1c94f36f97699f`, 33 pages,
fonts all embedded, revision timestamp 2026-10-19T19:13:18Z. Every page was
inspected at reduced size and the comparison pages at reading size.

**Author checks run.** `tools/check-proper-components --phase artifacts
--edition research`; the study-preflight component contract with all five
`--require-*` options; every `check-content-preflight` check of the study
preflight, including house-voice, structural-meta-labels and
provenance-matches-run; and the canonical web-edition probe with pandoc and the
pinned Python Markdown. All pass.

## Derive-synthesis, iteration 0 (19 October 2026)

**Scope.** The concise study (`synthesis.tex`), derived from the expansive
study as the study review accepted it at iteration 1, with its six
synthesis-only components under `sections/concise/`, which the manifest
already declared: the page-1 map of the eleven said elements (the votive Tract
and paschal Alleluia named beneath it as never said on the feast) and the four
overview senses; the page-2 Scriptural Date and Location on the nine generated
`orientation-v2` rows, each with the study appendix's reviewed place phrase
(the Daniel composition row's last sentence points to that appendix for
Gigot's later dating instead of "below"); the two-page Themes and Movement;
the integrated commentary; the concise scope appendix and References. The
manifest, the research, propers and instance records and the expansive study
were not changed. The shared generation record carries a new revision
timestamp and the stage's contribution.

**Commentary.** Six units, organized by question rather than by element: what
the Lamb receives and why the Son must ask (first reading, with Chrysostom's
objection); the prisoner whose kingdom is everywhere (second reading, with the
first and second readings compared at the Gospel and the Jn 18:37 split
inside the second); what the kings and nations owe (conversion, office,
judgment; the Postcommunion's soldiers); the kingdom handed over (third
reading, with the Augustine and Hilary difference on the subjection); when
the King sits (the Communion's flood and session, read by all three
readings); and the three readings' shared ground, four senses and limits
compared.

**Extent.** 12 physical pages (letter, Latin Modern, 11 pt). Approximate
words, LaTeX stripped, quoted Latin and English included: inventory and its
note 370; overview 195; page-2 place phrases 280; Themes and Movement 1,520;
commentary 4,880; scope appendix and References 1,260. The substantive body
(page 1 through the commentary) is about 7,250 words.

**Placement.** The settled auxiliary file places the inventory, the overview
and its four sense markers on physical page 1, the chronology on page 2, the
themes from page 3 to page 4, and the commentary's start on page 5.

**Fidelity to the reviewed study.** Every claim, attribution and quotation is
the expansive study's, re-read there. The study review's advisories that touch
the concise were applied: Aquinas is quoted *hoc exemplum voluit ostendere per
Christum*, without *et* (STU-009 a); Augustine's address to the kings at
*En. in Ps.* 2.9 is not used, since he offers it as an alternative reading
(STU-009 b); the first and second readings are contrasted as a dominion
received as man against a power whose origin and means are not from the world
and which needs no servants (STU-008 a); the third reading's two internal
differences are stated, not only named (STU-008 b); Hilary's *De Trin.*
XI.40 is quoted in its printed order (RES-013 a); and nothing is credited to
Schuster on the Secret (RES-013 b). The comparison follows the study, not
`research/interpretations.md` §5 (STU-010).

**Proof.** Built with `make doc` (provider `claude`), settled with no overfull
or underfull box, undefined reference or rerun warning, fonts all embedded.
PDF SHA-256
`e799cfedfa175b51d4eb4c417662a5985d78402c97965785437e347528292bb5`,
12 pages, revision timestamp 2026-10-19T19:49:33Z. Every page was inspected at reduced size,
and the page-2 lookup from passage to occurrence, place and date was made for
each row.

**Author checks run.** `tools/check-proper-components --phase artifacts
--edition synthesis`; the synthesis-preflight component contract with all
five `--require-*` options; and every `check-content-preflight` check of the
synthesis preflight, including references-used (26 entries, 22 loci),
house-voice, structural-meta-labels, the three chronology checks and
provenance-matches-run. All pass.

**Carried for the shared-record owners.** STU-007 (c) and RES-014 still stand:
the Tract's historical-setting row prints on page 2 under the rubric's label
without the Haydock qualification, which `research/scope.md` §8.4 does not
record. The web-converter defect on italic place phrases and the shared
calendar entry's votive Tract, both reported at author-study iteration 0, are
unchanged.

## Derive-synthesis, iteration 1 (19 October 2026)

**Scope.** Repair of the synthesis review's findings in the concise
components only: Themes and Movement, the commentary, the scope appendix and
the References. The entrypoint, the manifest, page 1, page 2, the research,
propers and instance records and the expansive study were not changed. The
shared generation record carries a new revision timestamp and this
iteration's contribution.

**SYN-001 (blocking).** The Communion sentence on page 4 now places the omitted
text as `propers/verified.md` §10 records it: the flood clause stands before
the first sung half-verse, and the strength given to his people between the
two; the antiphon leaves both unsung.

**Advisories.** SYN-002: Jerome is credited only with his reading of Dan
7:13–14 by Phil 2:6–8, and its extension to every text of receiving is the
commentary's own step; Hilary "does not make" the resurrection the beginning
of the Sonship. SYN-003: the Douay–Rheims entry gives the Challoner text's
own numbering (Ps 28:1, 10; 71:1–2, 8, 11, 20) and adds the loci page 2
quotes or uses (Ps 88:1, 39–45; Dan 1:1–6; 7:1; Jn 18:28; Col 1:2; 4:3, 18;
Apoc 1:9), each checked against the tracked Challoner text; the scope
appendix states in one sentence that psalms are cited in the Missal's
numbering and where the Challoner division differs; the Haydock entry names
its commentary on the seventieth psalm; Ps 71:2 is quoted with the witness's
comma. SYN-004: the servants contrast is stated once on page 4, in the terms
of Jn 18:36, and the Postcommunion's development is left to the commentary,
which also now states it in the Gospel's terms. SYN-005: Augustine's two loci
are said to concern two births and not to conflict.

**Extent.** 12 physical pages. Approximate words, LaTeX stripped, quoted
Latin and English included: inventory and its note 370; overview 195; page-2
place phrases 280; Themes and Movement 1,510; commentary 4,910; scope
appendix and References 1,320. The substantive body (page 1 through the
commentary) is about 7,270 words.

**Placement.** The settled auxiliary file places the inventory, the overview
and its four sense markers on physical page 1, the chronology on page 2, the
themes from page 3 to page 4, and the commentary's start on page 5.

**Proof.** Built with `make doc` (provider `claude`), settled with no overfull
or underfull box, undefined reference or rerun warning, fonts all embedded.
PDF SHA-256
`6e68e1328308d3d4883a900d7e5fc949d7b95e4a386550e62f0cd2c36db6dca8`,
12 pages, revision timestamp 2026-10-19T20:10:32Z. Every page was inspected
on the contact sheet, and pages 4, 11 and 12 at full size.

**Author checks run.** `tools/check-proper-components --phase artifacts
--edition synthesis`; the synthesis-preflight component contract with all
five `--require-*` options; and every `check-content-preflight` check of the
synthesis preflight, including references-used (26 entries, 31 loci),
house-voice, structural-meta-labels, the three chronology checks and
provenance-matches-run. All pass.

**Carried for the shared-record owners.** Unchanged from iteration 0: STU-007
(c) and RES-014 (the Tract's historical-setting row without the Haydock
qualification), the web-converter defect on italic place phrases, and the
shared calendar entry's votive Tract.

## Derive-homily, iteration 0 (19 October 2026)

**Scope.** The homily (`homily.tex`), *Our Lord Jesus Christ the King: The
Kingdom Not from Hence*, for an adult parish assembly at the occurrence of
Sunday 25 October 2026, derived from the expansive study as its review
accepted it at iteration 1 and the concise study as its review accepted it at
iteration 1. Its two components, which the manifest already declared, were
written: `homily-body` (`sections/homily/10-homily.tex`), the spoken text,
continuous preaching with no heading, direction to a preacher or citation
inside the speech; and `homily-note` (`sections/homily/90-note.tex`), the
terminal note on sources and delivery with its References, read aloud by
nobody. The entrypoint imports `common/preamble`, `common/propers-format` and
`common/propers-homily` in that order, then the leaf's `format.tex`; it uses
the shared full-width `\propertitle`, encloses only the literal import of the
spoken component in `properhomily`, and sets the note after the environment's
closing page break with `\runninghead`. No font, geometry, title or column
setting is overridden. The manifest, the research, propers and instance
records, and the expansive and concise components were not changed. The
shared generation record carries a new revision timestamp and this stage's
contribution. An earlier Claude leaf's homily files were consulted for their
file mechanics only; nothing of their content was used.

**The argument, and the profile's test.** The homily follows the second
reading, `kingdom-not-from-hence`, with the first reading's cross, as
`research/interpretations.md` §6 suggests; from the third reading it takes
only Schuster's note on the Communion.

- *Governing question.* The Gospel's King says his kingdom is not of this
  world, while the Introit and Gradual give him the throne of heaven and the
  homage of all kings: which is it, and does his kingdom reach the hearer's
  Monday?
- *Image.* The bound prisoner alone with Pilate in the governor's hall, set
  against the throne of the Lamb in the Introit. It returns at the bound King
  made captive by consenting, at the King's own weapons in Pilate's hall, at
  the two thrones of the Communion, and at the close, where the hall's
  counter-question is put to the hearers and the Introit's acclamation is
  said of the prisoner.
- *Decisive turn, and the textual detail that makes it.* *Regnum meum non est
  de hoc mundo … nunc autem regnum meum non est hinc* (Jn 18:36): "of" and
  "from hence" name the kingdom's origin, not its location (Augustine, *Tract.
  in Io.* 115.2), so that it is not from here and yet here, because
  everywhere (Aquinas, *Super Io.* 18 lect. 6). With the servants who would
  strive (18:36) and the hearers of the truth (18:37), this changes the
  familiar division of Sunday from Monday, in which "not of this world" is
  heard as "somewhere else", into a kingdom that reaches every office the
  hearer holds, entered by hearing and not by force.
- *Text-substitution test.* The question, image and turn depend on this
  Gospel's *de*, *ex* and *hinc*, its servants who do not strive, its
  counter-question and its hearers of the truth; on the Gradual's kings and
  the psalm's poor (Ps 71:8, 11, 12), the Introit's Lamb and its verse of
  judgment given to the king, the Epistle's *transtulit*, the Collect's wound
  and most loving dominion, the Offertory's *Postula a me*, the Secret's
  victim and gifts of unity and peace, the Preface's kingdom of truth, the
  Postcommunion's soldiers under the standard, and the Communion's session
  and peace. With unrelated readings the argument would not survive.

**Bounds kept.**

- The first reading's difficulty is kept: the speech says, with Chrysostom,
  that Christ was born a King and received nothing in addition, and places
  the receiving in the humanity ("The kingdom is his by birth. As man, he wins
  the nations in that hall"); it never makes the kingship begin in the trial
  or at Easter, and does not touch the Introit's *accipere divinitatem*.
- No Father is credited with a join he does not make. The joins listed in the
  note are the homily's own: the Monday outside no kingdom, the Secret's gifts
  as the remedy of the Collect's wound, the extension of the kings' office to
  every household, classroom, ward and vote, the Introit's verse taken as a
  prayer fit for every such office, the King's own weapons, Schuster's two
  separate notes set together beside the Introit's throne, and the
  counter-question put to the hearers. The Postcommunion's warfare as a share
  in the victory over sin is the second reading's synthesis from Chrysostom
  and Hilary, and is spoken as such, not as Schuster's.
- Augustine's *Letter* 185 and *Quas primas* are not used; the kings' two
  places come from *En. in Ps.* 71.13–14, where Augustine sets them himself.
  Schuster's p. 203 is not used. "Christ's kingdom takes no one's throne from
  him" states the second reading's conclusion without Schuster's sentence.
- No unsung context outside the Gospel's own chapter and the Gradual's next
  verse is used: neither "What is truth?" (18:38) nor the trial's sequel, no
  other Mass, no compilation history and no other Sunday. The votive Tract and
  paschal Alleluia are named only in the note.
- No English of a liturgical text was composed. The orations and the Preface
  are quoted only in the Lasance English, in phrases, and otherwise
  described; the Secret is described as the prayer said quietly over the
  gifts. The Introit's verse offered to the hearers as their own prayer is the
  Douay text of the psalm. The speech ends as preaching, with the Douay words
  of Apoc 5:12 and 1:6, and no recited prayer. No anecdote, personal
  experience, clerical identity, miraculous story or attributed quotation was
  manufactured.

**Verification performed at this stage.** Every Douay–Rheims verse quoted or
used was read in the tracked Challoner chapter texts (Jn 18:1, 3, 12, 28,
33–37; Apoc 1:6; 5:12; Ps 2:8; 28:10; 71:2, 8, 11, 12; Col 1:13; Dan 7:14).
Ps 71:12, which the studies do not quote, is the reason Augustine gives for
the kings' homage at *En. in Ps.* 71.14 (`research/scope.md` §3.4) and was
read there. Chrysostom's three passages (*Hom. in Io.* 83.4: the weakness of
kingship, "By consenting, and giving Himself up", the empire from above) were
re-read in the research stage's copy of the New Advent page. The Lasance
phrases are quoted as `propers/verified.md` records them from the page
images; Augustine's, Bellarmine's and Schuster's English is quoted as the
accepted study prints it and as `research/scope.md` records it (§§3.1, 3.3,
3.4, 3.7, 3.9); Aquinas and Hilary are paraphrased as the study gives them.
No new source-dependent claim was added to either study.

**Extent and delivery.** The spoken body runs to about 1,470 words (LaTeX and
comments stripped), some 11.3 to 12.2 minutes at 120 to 130 words a minute by
arithmetic alone; it has not been delivered aloud or timed. It was read
through in full, silently, for sense and oral clarity. The first draft ran to
about 1,900 words and was shortened to the default length by cutting repeated
summaries and secondary quotations.

**Proof.** Built with `make doc` (provider `claude`), settled with no overfull
or underfull box, undefined reference or rerun warning. PDF SHA-256
`135104188244d48d735be63dbddd3fc4d9bb856bcfc74d47f3c7752f09fd7419`, 4 pages
(two-column spoken text on pages 1–2, the note on page 3, the References,
revision timestamp and rights colophon on page 4), fonts all embedded Latin
Modern, revision timestamp 2026-10-19T20:36:47Z. Every page was inspected.

**Author checks run.** The homily-preflight component contract
(`scripts/_proper_study.py check --phase content --edition homily` with all
five `--require-*` options); `tools/check-proper-components --phase artifacts
--edition homily`; every `check-content-preflight` check of the homily
preflight, including references-used (11 entries), unquoted-not-quoted,
structural-meta-labels, house-voice, the three chronology checks and
provenance-matches-run; and the homily review seal. All pass.

**Carried for the shared-record owners.** Unchanged: STU-007 (c) and RES-014
(the Tract's historical-setting row without the Haydock qualification), the
web-converter defect on italic place phrases, and the shared calendar entry's
votive Tract. The homily touches none of them.

## Build-artifacts, iteration 0 (19 October 2026)

**Scope.** The three artifacts were built with `make doc` (provider `claude`)
for review: the expansive study, the concise study and the homily. No source,
prose, evidence, manifest or generation record was changed; no layout repair
was needed. The study and the concise study were rebuilt against the shared
generation record as the homily stage left it; the homily was already current
with its declared inputs and was not rebuilt.

| Artifact | Physical pages | PDF SHA-256 |
| --- | --- | --- |
| `f01-christ-the-king.pdf` (expansive study) | 33 | `444c7e0c622e97a87146cd7553db1fc40f6d416638cc700bc2c75b1879dc17cc` |
| `f01-christ-the-king-synthesis.pdf` (concise study) | 12 | `b6d09cd2bc470578fbce8f1c2acaa633f837894735b2738cde8c6392525d54b9` |
| `f01-christ-the-king-homily.pdf` (homily) | 4 | `135104188244d48d735be63dbddd3fc4d9bb856bcfc74d47f3c7752f09fd7419` |

**Logs.** All three logs settled with no fatal error, overfull or underfull
box, undefined reference or citation, rerun request, font warning or missing
character. The study's outline has 55 contents lines and the concise study's
15, each on its own anchor; component manifest and generation metadata
validation passed in each build.

**Fonts and structure.** Letter pages, PDF 1.7, unencrypted, with the titles
set in the document information. Every font in all three PDFs is an embedded,
subset Type 1 Latin Modern face with a Unicode map (13, 14 and 12 faces).

**Extraction.** Text extracts cleanly from all three, with no replacement
character and no unresolved `??` reference. On the concise study's extracted
pages, page 1 carries the element map and the four sense rows, page 2 the
Scriptural Date and Location, pages 3–4 the Themes and Movement, and page 5
opens the Detailed Commentary.

**Placement.** The settled concise auxiliary file places the inventory, the
overview and its four sense markers on physical page 1, the chronology on
page 2, the themes from page 3 to page 4, and the commentary's start on page
5; the last physical page is 12.

**Snapshot and rasters.** The artifact snapshot `research/artifacts.json`
records the three PDFs, the two auxiliary files and the declared render
inputs; it is a record of bytes, not of review. Page rasters and contact
sheets were made with the repository's PDF review helper for the visual
review. The artifact-phase snapshot check and the component check of each
edition pass.

**Remaining limitations.** No page has yet been visually reviewed; the
contact sheets were looked at only to confirm that the builds are complete.
The expansive study's last page carries the end of the References and the
rights colophon on about half a page. The shared-record defects carried by
the earlier entries (STU-007 (c) and RES-014, the web converter's italic
place phrases, the shared calendar entry's votive Tract) are unchanged.

## Generate-web, iteration 0 (19 October 2026)

**Scope.** The canonical study alone was converted, with the packet's command:

```sh
tools/tpt web-edition --provider claude --output build/web liturgy/roman-rite/1962/propers/temporal/f01-christ-the-king
```

It ran under a scratch virtual environment holding the repository's pinned
Python-Markdown 3.10.3 (the host carries 3.11), with pandoc, and succeeded on
its first invocation, with `tools/web-edition` SHA-256
`79813bc8795be960024f2e18fe32b1f2bf6d600d2bbd4c61438968fbadf59ce3` and
`scripts/web-shim.tex` SHA-256
`33abd8946680492c3d45785bbf7c39afea1c047d62bed8b57fd0b0e13a56545e`. The
converter wrote
`build/web/claude/liturgy/roman-rite/1962/propers/temporal/f01-christ-the-king.md`
directly: 129,148 bytes, SHA-256
`e7bc1c594ffc3f63b40493237770ab232ad338a46ef6c9a3000abefe4041af22`, not
edited after generation. No source, prose, evidence, manifest, generation
record, declaration or shared tool was changed at this stage, and no
conversion or declaration defect needed repair.

**Gates.** The converter exited zero; it refuses, rather than writes, an
edition that fails any of the audits `guidance/web-editions.md` describes,
among them the schema-2 anchor, undefined-command, paragraph, quotation, list,
table-row and title-block audits.
`tools/tpt check-web-edition --provider claude --document
liturgy/roman-rite/1962/propers/temporal/f01-christ-the-king` validates the
leaf's declaration (eligible, no blocking construct), and the provider-wide
declaration check passes.

**Fidelity reading.** The whole generated Markdown was read against the
section files. The title block carries all four fields of `\propertitle` and
the `[TOC]` marker stands at the source position of `\tableofcontents`. The
ten level-two and forty-five level-three headings of the Markdown are exactly
the headings of the nine section files, in order; the fifty-two source labels
and the three generated lane anchors are each present once as a heading
anchor, and the eleven appointed-text anchors `proper-introit` through
`proper-postcommunion` match the manifest's `element_keys`. The thirteen Latin
texts and fourteen English witnesses of the appointed texts, the Tract and the
paschal Alleluia among them, render as separate quotations with their witness
lines. The three readings stand under their own headings, each closing with
its own literal, allegorical, moral and anagogical senses as definition terms
and bodies. All three tables carry every row: the eleven-row element map, the
seven-row comparison, and the nine orientation-v2 rows of the Scriptural Date
and Location appendix with their computed dates, followed by the five passage
notes. The scope appendix and all thirty References entries are present. The
leaf has no footnote, endnote, edition conditional or external link other
than the colophon's licence link.

**Terminal matter.** The revision display reads `Last revised (UTC):
2026-10-19T20:36:47Z`, the shared generation record's timestamp, and the
rights colophon follows it. No model identity, effort, agent or contribution
history from `generation-metadata.tex` appears in the output. No
render-relevant source changed, so the recorded revision time stands.

**Receipt.** `python3 scripts/_proper_study.py snapshot-web --provider claude
--document liturgy/roman-rite/1962/propers/temporal/f01-christ-the-king`
recorded the generated bytes in `research/web-artifact.json`, whose digest
matches the Markdown that now stands. It records conversion identity, not
approval: no independent web review has read these bytes. No synthesis or
homily web leaf was made; nothing was installed beneath `web/`, and no release
record or catalog was created or edited.

**Carried for the shared-record owners.** Unchanged: STU-007 (c) and RES-014
(the Tract's historical-setting row without the Haydock qualification), the
web-converter defect on italic place phrases (the study's orientation phrases
use quotation marks instead), and the shared calendar entry's votive Tract.

## Reviews and gates recorded by the engine

These are the engine's own recorded results for run `7397c12187517ff2`, as the
run holds them when installation begins. No acceptance is claimed beyond them;
the terminal publication gates have not yet run. Each result's SHA-256 is the
hash the engine recorded for that result, and each was re-hashed from the run
directory and matched. Worker stages and program preflights, all PASS, are not
repeated here.

| Stage, iteration | Result | Findings and observations | Result SHA-256 |
| --- | --- | --- | --- |
| research-review 0 | CHANGES_REQUIRED | blocking RES-001 to RES-003; advisory RES-004 to RES-007; three observations | `3515a9a6fe290d2e5839d56fdc7f3d7baf91b536d64c7374882daf5c3c1ecdc6` |
| research-review 1 | CHANGES_REQUIRED | blocking RES-008; advisory RES-009 to RES-011; six observations | `7ea01cd782b5384b5c3115034b46ceed43e728a742701ec50b933e3eef76076b` |
| research-review 2 | PASS | advisory RES-012 to RES-014; six observations | `e83c6bad128f2538b0d46f35b02c1e6068e852adaf37692139bff302d05836bb` |
| study-review 0 | CHANGES_REQUIRED | blocking STU-001, STU-002; advisory STU-003 to STU-007; two observations | `fcafc0014797e1f3f90974410d8274e4fb1f9e0a424e1b6d1ffdc7a86f006bcb` |
| study-review 1 | PASS | advisory STU-005, STU-007 to STU-009; accepted STU-010; two observations | `38749986d483a0e9a118dec1316a6d32f2764a2435dc50ba42ee494c11f47f8b` |
| synthesis-review 0 | CHANGES_REQUIRED | blocking SYN-001; advisory SYN-002 to SYN-005; four observations | `971b41120e9fd74dbd3d6899a1fe5944a2a79b2b868cc61f229668b78929a94b` |
| synthesis-review 1 | PASS | accepted SYN-006; advisory SYN-007; five observations | `713cc5507ac59393f087608109a041c216e1b658ed2fdf310d47c16b855bbc03` |
| homily-review 0 | PASS | advisory HOM-001 to HOM-005 | `5376ed1e20f58a3c0b52723e413f10ec14c82e211a0450aa5ffc0db4836407a2` |
| artifact-gates 0 | PASS | none | `97af5c9c6c70bfc4459030f6b4c4d3ef1c5d44f458a9759ff4ab5fcbb5607d3c` |
| visual-review 0 | PASS | advisory VIS-001, VIS-002; one observation | `8581c6c79a5e7fef124aafc249163e1ac6d0b607f8248e7beefc3edbcba90a08` |
| generate-web 0 | PASS | worker stage | `534801969f2a6ad789e6786b33b3ade25f04706a7503201d2d59f9b4f9b39899` |
| web-review 0 | PASS | none; two observations | `7de96e7c398ce31779e4669b2627791afe854184db42f878f5db19f02ebbc6bf` |

The stages after the artifact build, in brief:

- **Artifact gates, iteration 0.** `_proper_study.py check --phase artifacts`
  with `--date 2026-10-25` and the five `--require` flags passed against the
  snapshot in `research/artifacts.json`.
- **Visual review, iteration 0.** PASS with two advisories: VIS-001, the
  eleven-row element map of the study split ten rows to one across pages 3
  and 4, and VIS-002, the shared format's first-mark right running head. The
  observation concerns the visual-review fragment, not this leaf.
- **Generate-web, iteration 0.** The canonical study alone was converted under
  the pinned Markdown 3.10.3. `research/web-artifact.json` records the
  conversion at SHA-256
  `e7bc1c594ffc3f63b40493237770ab232ad338a46ef6c9a3000abefe4041af22`.
- **Web review, iteration 0.** No finding. The two observations are the site
  stylesheet's horizontal scrolling of the element map and comparison tables
  at phone width, and the generated chronology passage labels, which belong to
  the shared chronology generator.

## Install-publication, iteration 0 — 19 October 2026

The worker is a Claude Code harness subagent running as `claude-opus-5-5[1m]`,
dispatched at reasoning effort `high`. No reviewed source, generation
timestamp or receipt was changed at this stage.

### Installed PDFs

The snapshot was confirmed current before anything was installed.
`_proper_study.py check --phase artifacts --require-presentation
--require-format --require-authority --require-orientation
--require-orientation-v2 --date 2026-10-25` exited 0, and all 32 hashes in
`research/artifacts.json` (three PDFs, 27 render inputs and two pagination
`.aux` files) matched the files on disk, as did the web receipt in
`research/web-artifact.json`. The three PDFs were then installed with the
normal recipe, one at a time. Nothing was suppressed: no `-o`, no `-t`, no
timestamp change and no source edit.

```sh
make install-doc DOC=liturgy/roman-rite/1962/propers/temporal/f01-christ-the-king PROVIDER=claude
make install-doc DOC=liturgy/roman-rite/1962/propers/temporal/f01-christ-the-king-synthesis PROVIDER=claude
make install-doc DOC=liturgy/roman-rite/1962/propers/temporal/f01-christ-the-king-homily PROVIDER=claude
```

Each run validated the generation metadata and copied the bytes. Nothing was
retypeset: the build PDFs keep their build-artifacts times, and the two
pagination `.aux` files still hash to the values that stage recorded. The
build PDF and the installed PDF each hash to the value that the build, the
artifact gates and the visual review recorded:

| Output | Pages | Bytes | SHA-256 (build and installed) |
| --- | ---: | ---: | --- |
| `f01-christ-the-king.pdf` | 33 | 474,184 | `444c7e0c622e97a87146cd7553db1fc40f6d416638cc700bc2c75b1879dc17cc` |
| `f01-christ-the-king-synthesis.pdf` | 12 | 380,693 | `b6d09cd2bc470578fbce8f1c2acaa633f837894735b2738cde8c6392525d54b9` |
| `f01-christ-the-king-homily.pdf` | 4 | 282,720 | `135104188244d48d735be63dbddd3fc4d9bb856bcfc74d47f3c7752f09fd7419` |

No hash differs, so no artifact defect is reported and no review boundary is
reopened.

### Web edition, release records and wiring

The reviewed conversion
`build/web/claude/liturgy/roman-rite/1962/propers/temporal/f01-christ-the-king.md`
was installed byte for byte at
`web/claude/liturgy/roman-rite/1962/propers/temporal/f01-christ-the-king.md`:
129,148 bytes, SHA-256
`e7bc1c594ffc3f63b40493237770ab232ad338a46ef6c9a3000abefe4041af22`, the value
`research/web-artifact.json` and the web review record. The installing worker
runs no git state change; the run's driver stages the file so the publication
gate can prove it is tracked. No synthesis or homily web edition exists; the
canonical study is the only web authority.

`make add-publication ID=<id> CATALOG=library/traditional-latin-mass.md
PROVIDER=claude STATUS=alpha` created one release record per PDF under
`release/publications/claude/liturgy/roman-rite/1962/propers/temporal/`. No
record for this identity existed beforehand. Each has schema version 1, its
own output id, the 1962 catalog, status `alpha` and the standing
authorization `perpetual-public-repository-2026`.

In `library/traditional-latin-mass.md`, the Claude cell of the existing `F01`
row under "Feasts Replacing a Sunday" changed from `Planned` to Full PDF,
Synthesis PDF, Homily PDF and Read. That is the order of the schema-2
manifest's `canonical_label`, `synthesis_label` and `homily_label`, followed
by the canonical web page. The ChatGPT cell, every other row and every other
catalog page are untouched, and no companion row was added.
`release/public-alpha.json` names `gpt` as the primary provider, so the one
new canonical marker carries the provider prefix,
`claude:liturgy/roman-rite/1962/propers/temporal/f01-christ-the-king`. It
stands at the end of the page's single marker block, which precedes the
Sunday table and its "Feasts Replacing a Sunday" subsection.

### Catalogue, reader projections and release bindings

`make document-catalogue` regenerated
`src/web/data/structure/documents/corpus.json`. Every change belongs to this
leaf. A new work is added for this identity with its Claude edition: the
study, with the concise study and the homily under `also`, and the web page.
Works moved from 151 to 152 (the liturgy section from 58 to 59), documents
from 211 to 212, issues from 265 to 268 and pages from 7,133 to 7,166; the
Claude provider tally moved from 62 to 63 and `claude-opus-5-5[1m]` from 95 to
96 documents.

This run registered the 1925 volume 17 edition and artifact of the *Acta
Apostolicae Sedis* under `src/sources/` at its research stage, and the source
library's reader projection had not been regenerated: `make
check-source-reader` reported `src/web/data/structure/sources` drifted at that
edition and at `index.json`. `make source-projection` rewrote it; the only
changes are the new edition file
`src/web/data/structure/sources/editions/holy-see/acta-apostolicae-sedis/1925-volume-17-1925.json`
and, in `index.json`, that edition's entry under the existing work and the
counts it adds (editions 1,093 to 1,094, artifacts 3,003 to 3,004, and one
more edition each in the `mul`, twentieth-century and public-domain facets).
`make check-source-reader` then reported the projection current.

`make check-release-bindings` then reported seven stale bindings, all of them
this production's: the catalog page, the document projection, the two source
projection files, the new web edition, and the 1962 and pre-1955 propers
projections `src/web/data/structure/propers/roman-1962.json` and
`roman-pre-1955.json`. The last two were regenerated with this run's
authorized calendar correction (the Communion cited as Ps 28:10–11) and
committed with it, without their release bindings being re-recorded; `make
check-propers-structure` reports both current with the calendar. The refresh
followed the repository's scoped rule, naming exactly those seven paths:
`make refresh-release-bindings ADOPT=1 ONLY="<the seven paths>"` adopted the
two new files, re-recorded the other five, and rewrote the rights table and
its digest. `make check-release-bindings` then reported no stale binding.
Nothing outside those seven paths was re-recorded.

The Claude publication inventory
(`src/sources/inventories/claude-publications-v1.toml`) does not yet carry
this publication, and the AAS 17 registration leaves the pinned
`canonical_catalog_snapshot` of
`src/sources/inventories/source-family-migration-v1.toml` stale. Under the
maintainer's authorization both refreshes are the run driver's, after the
publication gates accept; this stage did not run them. Until then `make
check-publication-inventories` reports the publication and its source-bearing
files missing from the Claude inventory.

### Publication-gate commands run by this stage

These are this stage's own runs of the terminal gate commands, in the pinned
Markdown 3.10.3 environment, before the driver stages or commits anything.
They are not an acceptance.

- `_proper_study.py check --phase publication --require-presentation
  --require-format --require-authority --require-orientation
  --require-orientation-v2 --date 2026-10-25` passes every check up to the
  tracked-file test, then refuses while the web edition is unstaged: git does
  not know
  `web/claude/liturgy/roman-rite/1962/propers/temporal/f01-christ-the-king.md`.
  The check that follows it, `tools/check-web-edition --provider claude
  --document <leaf>`, exits 0 when run alone. The gate's own run follows the
  driver's staging.
- `make check-release-bindings` reports no stale binding.
- `tools/tpt public-alpha check --provider claude --document <leaf>` exits 0:
  the scoped policy is valid for the three outputs, and the global source,
  release and authorization records are valid for 268 publications.
- `tools/tpt document-library check --provider claude --document <leaf>` and
  `tools/tpt document-library structure --check` exit 0, and the projection
  is current.
- `make check-web-editions-current` exits 0: tracked web editions match
  current sources.

### Outstanding

The driver's staging of the installed web edition, of the new source
projection file and of this stage's other tracked writes; the terminal
publication gates; and, after acceptance, the driver's refresh of the Claude
publication inventory and the source-family ledger.

## Register revision, 21 October 2026 (outside a workflow run)

The maintainer judged the three documents to read with unearned profundity,
empty significance, jargon and hokey application. The cause, the guidance and
`proper-study` version-14 changes, and the verification are recorded in
`workflows/reviews/register-remediation-2026-10-21/RECORD.md`. This entry
records what changed in this leaf. No workflow run produced it; the
generation record keeps run `7397c12187517ff2` as the provenance of the
documents and adds a contribution for the revision.

- **Scope.** Wording of reader prose only, in the study's sections 00, 05, 10,
  20, 30, 40, 50 and the notes of 80; the concise study's 03 (one phrase), 04,
  10 and 90; the homily's spoken body and terminal note; and the subtitle and
  PDF subject strings of the three entrypoints. The interpretations are called
  interpretations in reader prose. The closing walks of the three
  interpretations no longer certify that every text takes its place; they say
  what each text says and which author bears on it. The homily's Monday
  device, maxim closers and stock call are gone; it makes one response, in the
  second person, from Augustine's two places for the kings.
- **Preserved.** Every quotation, Latin phrase, work, locus and page reference
  of the accepted text, except the comparison's catalogue of which Father
  contributes to which interpretation (those works are cited elsewhere) and
  six quoted table-column labels in the date notes. No generated chronology
  row, row id, date or chronology macro changed.
- **Corrections found in review.** An independent fidelity review found
  three errors the first revision introduced (an inference credited to
  Augustine, the study's "bounded by place" gloss credited to Aquinas, two
  stale cross-references in the homily note) and twelve imprecisions; a second
  cold review of the corrections found five residues and three further
  instances, all corrected. Two inaccuracies older than the revision were also
  corrected: Pilate's first question inside the hall is "Art thou the king of
  the Jews?" (Jn 18:33), and the Secret asks that the Son give unity and peace
  (*ipse… concedat*).
- **Extent.** Reader-prose words, before and after: expansive study sections
  00–50, about 15,600 → 15,700; concise themes and commentary, about 6,500 →
  6,450; homily spoken body about 1,460 → 1,440 (about 11 to 12 minutes at an
  unhurried 120 to 130 words a minute, by arithmetic alone).
- **Builds.** 33, 12 and 4 physical pages, no undefined references or
  overfull boxes. Concise pages 1–5 keep the fixed opening; pages 3–4 are full.
  Every page of the three PDFs was inspected as a raster; no blocking defect.
- **Checks.** `check-proper-components --phase artifacts` passes for the three
  editions. `check-content-preflight` reports the same errors as before the
  revision in every edition: the chronology record and annotations are no
  longer what the chronology corpus produces, an owner matter that predates
  this revision. house-voice, structural-meta-labels and references-used pass.
  The web edition is regenerated under Markdown 3.10.3;
  `check-web-editions-current`, `check-release-bindings`,
  `check-document-catalogue`, `check-web-edition` and the scoped
  `public-alpha check` pass.
- **Not done.** No push, merge or deployment.
