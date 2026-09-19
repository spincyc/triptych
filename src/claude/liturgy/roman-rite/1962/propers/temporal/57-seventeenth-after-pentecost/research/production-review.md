# Production and review record

## Author-study

Authored 18 September 2026 in `proper-study` v3, run `1e02dc05f2df9940`, seeded
at commit `72616eb9cc25c7ea7cc061c0e82efffc8b5ea882`, at iteration 0, and
repaired at iteration 1 of the same run and seed. The canonical study is
*The Seventeenth Sunday after Pentecost*, the Mass *Dominica decima septima post
Pentecosten*, II classis, of the 1962 *Missale Romanum*, pp. 398–400,
nos. 1602–1611, in the universal calendar, for the occurrence of 20 September
2026.

The expansive study has an opening on the Sunday's two questions with a
ten-row map of the appointed elements; the complete appointed Latin of all ten
elements with the public-domain English of each (Douay–Rheims Challoner for
Scripture, the 1861 Cummiskey hand missal for the three orations), and a note
at every place where the Missal's adaptation leaves the English without a
counterpart; an element-by-element section giving each text its literary,
textual and liturgical setting; three readings of the whole formulary, each
carrying all ten element keys and closing with its own four senses; a
comparison of the three; a terminal Scriptural Date and Location appendix built
on the generated chronology projection; the scope appendix; and References.

The three readings are those recorded in `research/interpretations.md`:

- `whole-heart-one-body` — the whole heart for the one God, and the one body
  that love gathers. Witnesses developed: Augustine (*De doctrina christiana*
  I.22, I.27, I.30; *De moribus* I.11.18; *En. in Ps.* 32, 75, 101),
  Chrysostom (*In Mt.* 71; *In Eph.* 9–11), Gregory the Great (*Hom. in Ev.*
  38.10), Jerome (*In Eph.* II), Theodoret (*In Eph.* 4:1–6), Aquinas (*Super
  Eph.* c. 4 lect. 1; *Super Mt.* c. 22 lect. 4), Cassiodorus.
- `son-and-lord-of-david` — David's son and David's Lord, and the one God
  confessed in his Word and Spirit. Witnesses developed: Jerome (*In Mt.* IV;
  *In Eph.* II), Augustine (*En. in Ps.* 109; 32 II s. 2, 5; 101 s. 1),
  Chrysostom (*In Mt.* 71; *In Eph.* 11), Aquinas (*Super Mt.* c. 22 lect. 4;
  *Super Eph.* c. 4 lect. 2; *Super Ps.* 32 n. 5), Irenaeus (*Adv. haer.*
  I.22.1), Basil (*De Spiritu Sancto* 16.38), Cassiodorus, Bellarmine, with
  Durandus as a liturgical witness.
- `just-judge-merciful-hearer` — the humbled people praying with Daniel for
  mercy. Witnesses developed: Augustine (*En. in Ps.* 118 s. 26, 28; 101; 75;
  109; *De pecc. mer.* II.13), Hilary (*Tract. in Ps.* 118, *Ain* 10, *Sade*
  1), Cassiodorus, Jerome (*In Dan.* 9), Aquinas (*Super Phil.* c. 4),
  Bellarmine, and Rupert and Durandus for the chants of their own office.

Material disagreements are carried where the research records them: Augustine
against Cassiodorus on the speaker of Ps 101; Jerome against Augustine on
Daniel's own sins; the two lines of exegesis at Eph 4:6 (Jerome and Aquinas
distributing the phrases to the Persons; Chrysostom and Theodoret reading three
relations of the one God and Father); Hilary beside Augustine on where the
servant's mercy begins; Chrysostom and Jerome on why the lawyer asked; and
Bellarmine against the medieval commentators on what the Introit's *iudicium*
names. No witness is credited with a reading of the whole 1962 Mass; Rupert and
Durandus are used for the chants they share with it, and their Luke 14 Gospel is
stated wherever they are cited.

**Substantive word count: 13,106 words** (12,185 with the content of the
`\latin{}` quotations removed). The count converts the six argumentative
components — opening, element-by-element setting, the three readings, and the
comparison — through Pandoc's LaTeX AST with headings and the map, comparison
and dossier tables removed, then counts whitespace-separated plain-text words.
It excludes the appointed-text component, the Scriptural Date and Location
appendix, the scope appendix and References. The total stands above the
profile's 6,000–10,000-word planning range, which the profile states is a range
and not a quota: three readings that each carry all ten appointed elements and
close with four senses account for about 9,200 words of it, and the
element-by-element settings, which carry the textual, historical and liturgical
facts the readings then use, for about 2,700 more. The finished PDF is 38
physical pages, inside the 20–50-page requirement.

At iteration 0 the same count stood at 13,031 words and the PDF at 37 pages;
the iteration-1 recount reproduces 13,031 exactly on the pre-repair text, so the
whole of the 75-word difference is the repaired sentence in the comparison. The
parenthetical Latin figure is not comparable across the two iterations:
iteration 0 recorded 12,237 by a removal rule this record did not state, and
iteration 1 removes the brace-matched content of every `\latin{}` span in the
counted components.

## The iteration-1 repair

One blocking finding reached this stage from an earlier evaluation, `STU-001`,
against the first paragraph of `sections/50-comparison.tex`. The paragraph
asserted that all three readings "call on the Council of Trent for the doctrine
of the sacrament those prayers ask to receive". That is true of
`whole-heart-one-body`, which cites sess. XIII, cap. 2 for the Eucharist as the
sign of the one body, and of `just-judge-merciful-hearer`, which cites the same
chapter for the antidote against daily faults. It is not true of
`son-and-lord-of-david`: neither "Trent" nor "Tridentin" occurs in
`sections/30-son-and-lord-of-david.tex`, whose treatment of the orations rests
on the Collect's *te solum Deum*, the Secret's *maiestas* beside the Preface
the Missal directs after it, and the Postcommunion's *sanctificationes*.

The repair keeps the true half of the sentence and restricts the Trent clause to
the two readings that use it, then says positively what the second reading does
with the same three orations. No Trent citation was added to the second reading,
and no research record was altered to make the old sentence true: the finding's
observation that `research/interpretations.md` §4.1 states the shared feature
more loosely ("use Trent only as doctrinal illumination") stands as the research
stage wrote it, and is left to that owner. Nothing else in the study changed.

The paragraph grew by 75 words, the References spilled onto one further page,
and the study is now 38 pages rather than 37. `sections/50-comparison.tex` is the
only source file this iteration touched besides `generation-metadata.tex`, whose
revision timestamp and model-contribution note were brought up to date because a
render-relevant source changed.

## Component manifest and the concise companion

`proper-components.toml` is schema 2 with
`presentation_contract = "interpretive-pagination-v1"`. It declares eight
research components, five synthesis components and two homily components, and
the three interpretive lanes with their authors, senses, element coverage and
source-audit paths. Only the research components have been authored.

The `[presentation]` chronology role names `concise-date-location`, a synthesis
component the concise author will write, rather than the study's own
`scriptural-date-location` appendix. The reason is a tooling constraint, not a
judgment about the dossier: the canonical web converter reads the generated
chronology definitions from the research entrypoint's preamble, while the
concise page-2 owner must import them in its own file and hold the
`\chronodate` cells directly; one shared file cannot do both without importing
the generated file twice, which LaTeX refuses. The reviewed home of the
chronology is therefore the study's terminal appendix, and the concise page 2
reprints its dates, relation labels and unresolved states unchanged. This is
reported for the workflow owner as well: a leaf that adopts the presentation
contract and declares canonical web eligibility cannot share one chronology
component between the two editions.

Canonical web eligibility is declared for the study alone. The shared
generation record carries this packet's workflow, version, digest, run id and
seed commit, with `unknown` for the install commit.

## Sources and limits retained

The author read the reviewed `research/context.md`, `research/scope.md`,
`research/interpretations.md`, `research/source-bindings.toml`,
`research/chronology.toml`, the generated annotations and
`propers/verified.md`, and re-read the retained evidence for the quotations it
prints: Chrysostom's homilies 71 and 9–11 and Augustine's *De doctrina
christiana*, *De peccatorum meritis* and *Enarrationes* (Pss 32, 101, 109) in
the tracked texts; Gregory's homily 38, Jerome on Daniel, Irenaeus, Bellarmine,
Cassiodorus on Ps 101, Aquinas on Ephesians, Rupert, Schuster and Guéranger in
their tracked deliveries; and the Douay–Rheims, Clementine, Brenton and Revised
Version verse texts for every verse quoted. Quotations from witnesses the
research stage read in unregistered deliveries or in optical layers (Jerome on
Matthew and on Ephesians, Theodoret, Hilary, Cassiodorus on Pss 32, 75 and 118,
Augustine on Pss 75 and 118, Aquinas on Matthew and on the Psalms, Basil,
Durandus) stand as that stage recorded them at their loci.

Limits carried into the study's own scope appendix: the Communion's *omnes*
before *reges* is unexplained; the Latin version behind the Offertory's
compilation is unidentified; Greek psalm exegesis, Greek exegesis of Daniel 9
and any Doctor's commentary on Daniel were not reached; Hilary was read at two
strophes of Ps 118 only; Bellarmine only in O'Sullivan's abridged English; no
critical edition of the sacramentaries, no manuscript, no Roman-psalter edition
and no Old Latin Daniel was consulted; the chant evidence is a database view of
Hesbert's *Sextuplex*. The chronology holds no traditional date for the four
psalms and no critical figure for Daniel, Matthew or Ephesians, so the page
names those positions in words; the Gospel's narrated event is undated.

No English of a liturgical text has been composed here: the orations and the
Preface are quoted from the 1861 Cummiskey translation, the Scripture from the
Douay–Rheims, and the Latin of prayers is explained but never rendered.
English glosses of patristic Latin are printed without quotation marks beside
the Latin they gloss.

## Research defects reported for the cold reviewer

1. The standing research-review advisory `RES-018` concerns Chrysostom's
   *In Eph.* hom. 11 at Eph 4:6: Migne's Greek reads φησιν, "he says", where
   the NPNF English has "this they own". The study quotes the NPNF English
   alone and cites NPNF 1.13 for it; it does not print the Greek or credit
   Chrysostom with a distribution of the three phrases among the Persons. The
   advisory stands against `research/scope.md` §§3.3 and 4.5 and
   `research/interpretations.md` §2.1, which this stage does not edit.
2. No other research defect was found while writing. The reception matrix,
   the disagreement register and the chronology audit answered every question
   the prose needed.

## Author proof and checks

`make doc DOC=liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost PROVIDER=claude`
settles in two passes. The final log has no overfull or underfull box, no
warning, no undefined reference and no rerun request. The PDF has 38 pages,
letter size, Palatino (TeX Gyre Pagella) at 11 points on 15-point leading with a
5.9-inch measure; all seven font resources are embedded, subsetted and
Unicode-mapped. `tools/check-proper-components --provider claude --document
… --phase artifacts --edition research` passes, as do
`python3 scripts/_proper_study.py check … --phase content --edition research
--require-presentation`, every `check-content-preflight` check the study gate
names (references-used, identifiers-resolve, bindings-valid,
restricted-not-reproduced, relation-coverage, unquoted-not-quoted,
structural-meta-labels, house-voice, the three chronology checks and
provenance-matches-run), `check-generation-metadata` and `check-web-edition`.
A trial run of `tools/web-edition` converts the leaf without loss and carries
the ten `proper-<element-key>` anchors.

The settled proof is
`build/claude/liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost.pdf`,
SHA-256 `1895c260216d888caf566fb85cc245cf236fcf620156dd24b2bcbf53bc2fa985`, at the
revision timestamp `2026-09-18T19:53:35Z`; a copy of it with the log, the
auxiliary file, the extracted text and their digests is kept beneath this
run's stage artifact directory, with the page rasters in a child of their own.
It supersedes the iteration-0 proof, SHA-256
`f48f4e66d8048188ad4dc83e7d026e6f6920b51989f9adfdab7ab68c7a01d427` at
`2026-09-18T18:56:24Z`, which remains beneath that iteration's own directory.

At iteration 0 the author inspected the two contact sheets and the individual
rasters of the title and contents page, the appointed-text pages, the dossier
sheet and the final page; layout revision there removed a two-line spill page at
the end of the third reading, a quarter-full page at the end of the appointed
texts, and a second page of the dossier sheet, which now stands whole on one
page. At iteration 1 the author re-rendered all 38 pages, read both contact
sheets again and the individual rasters of the two comparison pages and the
final page, and confirmed that the repaired paragraph sets without a spill, that
the comparison table still stands whole beneath it, and that the revision
timestamp and the rights colophon still share the last page. The proof shows no
clipping, collision, missing text or heading-only page. This is an author proof
inspection, not the independent visual evaluation, which follows the
shared-timestamp three-document build.

## Derive-synthesis

Authored 18 September 2026 in `proper-study` v3, run `1e02dc05f2df9940`, seeded
at commit `72616eb9cc25c7ea7cc061c0e82efffc8b5ea882`, at iteration 0. The
concise companion is *The Seventeenth Sunday after Pentecost: A Concise Study
of the Proper in the 1962 Roman Missal*, built from `synthesis.tex` and derived
from the accepted expansive study of this same leaf. No research record and no
component of the study was edited for it.

The six synthesis components were written at this stage:

- `concise-inventory` (`sections/concise/01-inventory.tex`) — the complete map
  of the ten appointed elements in the order of the Mass, with a rubrical note
  that the Mass has one oration, admits no optional text, and takes the Trinity
  Preface by rubric.
- `concise-overview` (`sections/concise/02-overview.tex`) — exactly four
  overview rows, Literal, Allegorical, Moral and Anagogical, drawn from the
  senses the three readings share (`research/interpretations.md` §4.4). They
  orient and do not replace each reading's own four senses.
- `concise-date-location` (`sections/concise/03-date-location.tex`) — the
  Scriptural Date and Location sheet, importing the generated chronology
  annotations once and carrying one `\chronodate` cell for each of the seven
  appointed Scriptures. The dates, relation labels, disputed alternatives and
  unresolved states are the study's own, unchanged; the explanatory rows are
  compressed so that the sheet occupies exactly one physical page.
- `concise-themes` (`sections/concise/04-themes.tex`) — *The Propers: Themes
  and Movement*, two full pages opening with a direct thesis and following the
  formulary from the Introit's confession to the Communion's vows, with the
  history by which the parts reached the day.
- `concise-commentary` (`sections/concise/10-commentary.tex`) — *The Propers:
  Detailed Commentary*, six cross-proper questions, each drawing on several
  elements and setting the three readings' answers beside one another: the two
  commandments and what holds them together; Christ's own question; the
  Epistle's sevenfold *unus* and the division at its last verse; the Gradual's
  respond and versicle; the voice in which the people prays (Alleluia,
  Offertory, Introit); and vows, healing and the end the Mass looks to.
- `concise-apparatus` (`sections/concise/90-apparatus.tex`) — the scope note
  and the References for the sources this companion actually uses.

Every controlling claim and agreement the study carries is preserved, and five
of the six narrow disagreements its comparison section lists: Augustine against
Cassiodorus on the speaker of Ps 101; Jerome against Augustine on Daniel's own
sins; the two lines of exegesis at Eph 4:6, with Chrysostom and Theodoret
credited only with the three relations of the one God and Father and never with
the distribution among the Persons; Hilary beside Augustine on where the
servant's mercy begins; and Bellarmine against Rupert and Durandus on what the
Introit's *iudicium* names. The statement that Rupert's and Durandus's office
read Luke 14 stands wherever they are used. The sixth disagreement, Chrysostom
and Jerome giving different reasons for the lawyer's question
(`sections/10-each-element.tex`), is the one this compression set aside: the
commentary keeps Chrysostom's reason, that the question came "from having no
charity, from pining with envy", and does not print Jerome's, that the question
was captious because every commandment of God is great. Nothing in the concise
argument turns on it, and the expansive study carries both.

**Substantive word count: 4,616 words** (4,241 with the content of the
`\latin{}` quotations removed), counted over the two argumentative components,
the themes section and the commentary, through Pandoc's LaTeX AST with headings
and page markers removed, then counted as whitespace-separated plain-text
words. It excludes the map, the overview rows, the dossier sheet, the scope
note and the References. The iteration-1 script gives 4,614 (4,240) on the
pre-repair text of both components, where iteration 0 recorded 4,624 (4,250);
the repair's own net gain is therefore two words, and the ten-word offset lies
between the two rounds' counting scripts and not in the text. Against the
study's 13,106 words over six components this is about a third of the argument,
selected and re-integrated rather than abstracted. The finished PDF is 12
physical pages, inside the 10–12-page requirement.

Two leaf-local presentation environments were added to `format.tex` for this
companion and are used by no research component: `concisemaptable`, the study's
three-column map one step smaller, and `conciseoverview`, the two-column
overview. Their column widths are chosen so that both tables rule to the same
measure on the first page. Nothing else in `format.tex` changed, and the study's
own rendering is unaffected.

The shared generation record now carries a second contribution for this stage
and the revision timestamp `2026-09-18T21:30:00Z`. The expansive study was
rebuilt at that timestamp and is unchanged at 38 pages.

## The concise iteration-1 repair

One blocking finding reached this stage, `SYN-001`, against the References of
`sections/concise/90-apparatus.tex`. The concise References had been pruned
from the study's and the pruning went wrong in both directions: two claims the
concise body makes had no locus to check them against, and three loci the
companion no longer used were still carried.

Both missing loci were added from the study's own References, which already
held them, so no research was reopened and no new evidence-dependent claim
entered the companion. Wilson's *Gelasian Sacramentary* is now cited at p. 359
(appendix, *Hebd. xxi post Pentecosten*) as well as at pp. 231–232, so that the
themes section's Frankish Gelasian orations can be verified at the Mass that
carries them rather than at the Old Gelasian one. The 1962 Missal is now cited
at p. [57] (no. 4613) as well as at the pages already listed, so that the
commentary's observation about the capitalized *Spíritu* in the votive Mass of
the Holy Spirit can be checked; `propers/verified.md` §4 names the same locus
and `research/scope.md` carries it.

Two unused loci were removed. *Rubricae generales* 115 governs how far an
oration's conclusion is printed, and nothing in this companion turns on it: its
own scope note cites RG 91, 111 b, 127 b and RGMR 427, 434 b, 494 b only.
Gregory's *Homiliae in Evangelia* 38.9 went with the twice-dyed scarlet the
compression had cut, and the entry now reads 38.10, the homily the commentary
actually quotes. The third, Bellarmine on Ps 118, was resolved the other way
the finding allowed: rather than drop the locus, the commentary restored the
disagreement that used it, so that Bellarmine's reading of the Introit's
*iudicium* as the law now stands beside Rupert's and Durandus's judgment that
exalts the humble, with the study's own measure that the two "differ in what
the Introit's word names, not in what they believe of God"
(`sections/40-just-judge-merciful-hearer.tex`). The References entry is
narrowed to Ps 118:137, the verse whose *iudicium* Bellarmine glosses; his
reading of v. 124 remains in the expansive study and is not used here.

Five standing advisories were handed to this stage and four were cleared in the
same files. `SYN-002`: the themes section said the sevenfold *unus* stands in
four verses of the Epistle and it stands in three, Eph 4:4–6, which is what the
same component says two pages earlier; the sentence now reads "three verses".
`SYN-003`: Gregory's parable of the king's marriage feast does not stand just
before this Gospel — the tribute to Caesar and the Sadducees' question
intervene — and the sentence now places it "earlier in Matthew 22", keeping the
correct statement that Gregory expounds the parable and cites the commandment
in Mark's form. `SYN-005`: two editorial superlatives that were not in the
study, and that pulled against each other, are gone; the division at Eph 4:6 is
stated in the study's own words, "two lines of exegesis, and neither denies the
other", and the Alleluia's witnesses now "differ over whose voice it is"
without competing for a superlative. `SYN-006`: the anagogical row on the first
page now reads "for Rupert of Deutz reading these chants with Luke 14", so that
a reader of the orientation rows alone is not met by a Lucan banquet in the
anagogical sense of a Mass whose Gospel is Mt 22:34–46. `SYN-004` was cleared
by the restoration described above, and this record's own claim about preserved
disagreements was corrected at the same time: it had asserted that every narrow
disagreement survived, and one, Chrysostom and Jerome on why the lawyer asked,
did not.

Six source files changed: the four concise components, `generation-metadata.tex`
for the revision timestamp and the contribution note, and this record. The
commentary also carries four small tightenings of settled prose — one at the
close of Eph 4:6, two in the Gradual versicle's paragraph and one at the
Alleluia — made to hold the finished PDF at twelve physical pages against the
growth the repairs brought; none removes a source, a locus or a qualification. A first
build of the repairs ran to thirteen pages, with only the revision timestamp
and the rights colophon on the last; the tightenings brought the References back
inside page 12.

## Author proof and checks for the concise companion

`make doc DOC=liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost-synthesis PROVIDER=claude`
settles in two passes. The final log has no overfull or underfull box, no
warning, no undefined reference and no rerun request. The PDF has 12 pages,
letter size, Palatino (TeX Gyre Pagella) with Latin Modern Mono for the record
paths; all nine font resources are embedded, subsetted and Unicode-mapped, and
the document info carries the title, the subject and the tracked ModDate with
no build-derived CreationDate.

The settled auxiliary file records the physical pages the presentation contract
fixes: inventory and overview markers on page 1, the four sense markers on page
1, chronology start and end on page 2, themes start on page 3 and end on page 4,
and commentary start on page 5. `tools/check-proper-components --provider claude
--document … --phase artifacts --edition synthesis` passes, as do
`python3 scripts/_proper_study.py check … --phase content --edition synthesis
--require-presentation` and every `check-content-preflight` check the synthesis
gate names for this edition (references-used, identifiers-resolve,
bindings-valid, restricted-not-reproduced, relation-coverage,
unquoted-not-quoted, structural-meta-labels, house-voice, the three chronology
checks and provenance-matches-run).

The settled proof is
`build/claude/liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost-synthesis.pdf`,
SHA-256 `e13fc7a23f9906cb08b3a44ca9b0faf2fad41722ee8d2808986d4296f8594f53`, at
the revision timestamp `2026-09-18T21:30:00Z`; a copy of it with the log, the
auxiliary file, the extracted text and their digests is kept beneath this
stage's own artifact directory in the run, with the page rasters in a child of
their own. The expansive study rebuilt at the same timestamp is SHA-256
`1cf3b731721ca56ad188b0effd5943761b832a49cd0944f84614ed3e6af5baf1`. At
iteration 0 the proof was SHA-256
`ee9b7e7a4c8eb52410f1a4970bb11d4de9138a872fdb58e0354406e3602bfeb9` at the
revision timestamp `2026-09-18T20:40:00Z`, with the study at
`4e50803c658b03a5c2503d4adcce99114a60a273e8f57db5735af0e221b62226`; the
settled auxiliary file is byte-identical across the two iterations, so the
fixed physical pages did not move.

The author read the contact sheet and the individual rasters of the first page,
the dossier sheet, the References page and the final page, and read the
extracted text of all twelve pages. The proof shows no clipping, collision,
missing text, blank page or heading-only page; the map and the four overview
rows rule to the same measure on page 1; the dossier stands whole on page 2;
the themes section fills pages 3 and 4; and the revision timestamp and the
rights colophon share the last page with the end of the References. This is an
author proof inspection, not the independent visual evaluation, which follows
the shared-timestamp three-document build.

## Upstream observations reported for the cold reviewer

1. The author-study record above states that layout revision at iteration 0 left
   the study's Scriptural Date and Location sheet standing "whole on one page".
   In the study as it now builds, that sheet runs from page 33 onto page 34,
   where the long-table head repeats above the Epistle dossier. The study itself
   is under no one-page rule for a terminal appendix, so this is an inaccuracy
   in the record rather than a defect in the document; it is reported and not
   repaired, because `research/production-review.md` above this section belongs
   to the author-study owner.
2. The same record states that `proper-components.toml` declares "eight research
   components, five synthesis components and two homily components". The
   manifest declares nine research components, six synthesis components and two
   homily components. Reported, not repaired, for the same reason.
3. The sentence the concise commentary repaired at iteration 1 for `SYN-003`
   stands unrepaired in the study, where `sections/20-whole-heart-one-body.tex`
   still says that Gregory expounds "the parable that stands just before this
   Gospel in Matthew". Two pericopes intervene, the tribute to Caesar and the
   Sadducees' question. This is the study-review advisory `STU-003`, still
   standing against its own owner; the concise copy was corrected here because
   this stage owns it, and the study's copy is reported and not touched.
4. No other upstream defect was found while deriving. The study's three
   readings, its comparison and its element-by-element settings answered every
   question the concise argument needed, and the standing research advisory
   `RES-018` on Chrysostom's gloss at Eph 4:6 is observed here as it is in the
   study: the NPNF English alone is quoted, and Chrysostom is credited with an
   argument about the Son and never with the distribution of the three phrases
   among the Persons.

## Derive-homily

Authored 18 September 2026 in `proper-study` v3, run `1e02dc05f2df9940`, seeded
at commit `72616eb9cc25c7ea7cc061c0e82efffc8b5ea882`, at iteration 0, and
repaired at iterations 1, 2 and 3 of the same run and seed. The
homily is *The Seventeenth Sunday after Pentecost: The Commandment and the
Question*, built from `homily.tex`, addressed to an adult parish assembly for
the occurrence of 20 September 2026, and derived from the two accepted studies
of this same leaf. No research record and no component of either study was
edited for it.

The two homily components the manifest declares were written at this stage:

- `homily-body` (`sections/homily/10-homily.tex`) — the spoken text, continuous
  preaching with no heading, no direction to a preacher and no citation inside
  the speech. It opens on the three questions asked in the Temple and the
  silence that ends the Gospel, expounds the whole heart of the great commandment and
  the second commandment "like to this", turns on Christ's own question and the
  answer the Church gives it, reads the Epistle's sevenfold *unus* as the form
  that love takes in a people, hears the Collect asking as a gift what the
  Gospel commands, sets the Introit's plea for mercy and the Offertory's prayer
  of Daniel as the posture in which all of it is received, returns to the
  opening silence at the Creed, and ends on the Communion's vows and the
  Postcommunion's eternal remedy.
- `homily-note` (`sections/homily/90-note.tex`) — the terminal note and the
  References, read by nobody aloud: the audience and occasion, the spoken word
  count with the pace it implies, the relation to the three reviewed readings,
  the route by which each quoted English reaches the page, and the exact loci
  of the four passages the speech attributes.

The argument is a compatible combination of the first two reviewed readings,
`whole-heart-one-body` and `son-and-lord-of-david`, joined at St John
Chrysostom's own reading of the Gospel's two halves in *In Mt.* hom. 71, with
the Introit and the Offertory of `just-judge-merciful-hearer` supplying the
prayer in which the other two are received. This is the combination
`research/interpretations.md` §4.5 records as available, and the homily keeps
within the attributions that section allows: Chrysostom for the join of the two
halves and for "like to this", Augustine for the undivided heart (*De doctrina
christiana* I.22.21, in the chapter block I.22.20–21 the passage record
inspects) and for David's son and David's Lord (*En. in Ps.* 109,
3–6), Jerome for Daniel praying as one of his own people (*In Dan.* on 9:5).
The whole-formulary reading that follows from Chrysostom's join is editorial
and the terminal note says so; no Father is credited with it. Four appointed
elements carry the argument — Gospel, Epistle, Collect, Introit — with the
Offertory, the Communion and the Postcommunion drawn in, and the Gradual, the
Alleluia and the Secret left to the studies. The manifest declares all ten
element keys on both homily components because the component checker requires
the `homily` component to declare complete coverage; the speech is under no
obligation to inventory every minor proper, and the note states which elements
it uses.

No English of a liturgical text was composed. The Collect and the
Postcommunion are quoted from the 1861 Cummiskey translation, Scripture from
the Douay–Rheims at the canonical verses, and Augustine's *De doctrina
christiana* and Chrysostom's homily from the Nicene and Post-Nicene Fathers.
The Offertory antiphon, which no Douay verse renders, is described and not
translated. Augustine on Ps 109 and Jerome on Daniel are reported from their
Latin, with Jerome's *quia unus e populo est* printed beside its gloss. The
Creed is named and not quoted. No anecdote, personal experience, clerical
identity, miraculous story or attributed quotation was manufactured.

**Spoken word count: 1,429 words** (1,406 at iteration 0, 1,445 at iteration
1, 1,437 at iteration 2). The count is taken over
`sections/homily/10-homily.tex` alone with comments removed, `\latin{}`
contents kept, every other macro dropped and the remainder counted as
whitespace-separated words carrying a letter. At an unhurried preaching pace
of 120 to 130 words a minute that is 11.0 to 11.9 minutes, and 13.0 minutes at
110; the profile asks for approximately 10–12 minutes. The figure is
arithmetic on the word count and not a timed delivery: nobody has spoken these
words and no rehearsal was audible. The prose was read through in full for
sense, sentence length and ease of speech.

### Presentation, and a departure from the starting values

The three-document profile offers 12.5–13 points on 18-point leading for
homily-mode text as a starting point and asks that the actual pages be judged
rather than the numbers kept as a quota. At 12.8 on 18 with 0.75em between
paragraphs the speech ran to four pages of which the last carried two
paragraphs and was otherwise empty. At 12.5 on 17 with 0.6em it occupies three
well-filled pages, ending with a modest bottom margin; the relative leading is
then the same 1.36 the studies use at 11 points, and the type is a point and a
half larger than theirs. The body is set unjustified, unindented and with a
clear space between paragraphs so that a speaker can leave the page and find
his place again, and the four movements are separated by a wider space. The
terminal note and References return to the leaf's ordinary 11-point type and
begin on a fresh page, so that the speech and the apparatus cannot be read into
one another. The References carry a `\Needspace` guard: the seven entries need
about fourteen lines and the note leaves about seven at the foot of its page,
so the list stands whole on the last page rather than breaking after its first
entry. Nothing in `format.tex` was changed for this companion.

The shared generation record now carries a third contribution for this stage
and, after the iteration-3 repair, the revision timestamp
`2026-09-19T00:05:00Z` (`2026-09-18T23:59:00Z` after iteration 2,
`2026-09-18T23:55:00Z` after iteration 1). The
expansive study and the
concise study were rebuilt at that timestamp and are unchanged at 38 and 12
physical pages; the concise study's settled auxiliary file still records
inventory and overview and the four sense markers on physical page 1,
chronology on 2, themes from 3 to 4 and commentary beginning on 5.

## The homily iteration-1 repair

Two blocking findings reached this stage, both against the homily's own
components, and both were repaired there; no study component, research record
or source record was touched.

`HOM-001`, against the opening of `sections/homily/10-homily.tex`. The speech
had opened on "Two questions are asked in today's Gospel, and only one of them
is answered", and had said that when our Lord asks "What think you of Christ?
Whose son is he?" the men who came to trap him have nothing to say. Mt 22:42
says they answer, "David's", and the silence of v. 46 falls after the further
question of v. 45, "If David then call him Lord, how is he his son?"; the
speech's own third movement then said so, three minutes later. The opening now
counts the three questions the pericope actually asks — the lawyer's at v. 36,
our Lord's at v. 42, and the one at v. 45 that follows on their answer —
narrates the answer "David's" where the Gospel gives it, and rests the frame of
the unanswered question on v. 45, which is the verse the silence belongs to.
Two later sentences were brought into line with it: the third movement no
longer reports the answer as news ("Their answer was true and one step short")
and names Augustine's distinction as "the answer nobody in the Temple would
give", and the return to the silence in the fourth movement now asks the
question that produced it, "How can the one David calls Lord be David's son?",
in place of "Whose son is he?", which the Gospel answers. Mt 22:45 is now
quoted, and the note's list of canonical verses adds it. The studies' count of
"two questions" is a count of the two exchanges in the Temple and is not
disturbed: the Gospel carries three interrogatives, the second and third inside
one exchange, and the expansive study's own opening narrates all of them.

`HOM-002`, against the Exact loci paragraph and the References of
`sections/homily/90-note.tex`. Augustine's "no part of our life is to be
unoccupied, and to afford room, as it were, for the wish to enjoy some other
object" was cited as *De doctrina christiana* I.22.20 in both places. In the
retained CCEL transcription of the NPNF1 2 English the note declares as its
route, the sentence stands in paragraph 21 of Book I chapter 22 — which opens
"21. Neither ought any one to have joy in himself" — together with the channel
and current image the speech paraphrases; paragraph 20 opens "Among all these
things, then" and carries neither. The passage record
`passage.augustine.de-doctrina-christiana.ccel-web-2026-09-17.i-22-20-21` and
both studies already carried the block as I.22.20–21. The Exact loci paragraph
now reads I.22.21, naming the block I.22.20–21 it sits in, and the References
entry reads I.22.20–21, which is the span the research record inspected and the
span the two studies cite.

Both standing advisories were cleared in the same files. `HOM-003`: the
Epistle was quoted with Eph 4:4b elided behind an ellipsis, which is silent in
delivery, and the listener was then told "Seven times in three verses he says
the word one" after hearing six. The nine elided words are restored — "as you
are called in one hope of your calling" — so the quotation carries all seven,
and the one hope it supplies is taken up at the close, where the eternal remedy
of the Postcommunion is now "finished in the one hope of our calling".
`HOM-004`: "we will bring bread and wine to this altar" set a procession of the
faithful in parallel with the Creed they will in fact stand and say, and the
1962 rite has no such procession. The sentence now reads "then bread and wine
will be carried to this altar and offered, and we shall offer with them", which
states the corporate offering the passage always meant without promising an
action this Mass does not contain. The unobjectionable "when the gifts are
carried up" earlier in the same movement is unchanged.

Four source files changed: the two homily components, `homily.tex` for the PDF
subject, which had described the Gospel as carrying two questions, and
`generation-metadata.tex` for the revision timestamp and the contribution note;
this record is the fifth. As first written the repairs took the spoken body
from 1,406 words to 1,498, and that build ran to six pages, with four lines of
the last paragraph stranded on a fourth page of speech. Tightenings of settled
prose brought it to 1,445 words and back to three well-filled pages: one
sentence that restated what the repaired opening now says ("That is why a man
who asked for one commandment was handed two"), one connective the Matthew
quotation immediately repeats ("To that nobody says anything"), the second
printing of "What think you of Christ? Whose son is he?" in the third movement,
and smaller compressions in the opening and in the Epistle, Introit and Collect
paragraphs. None removes a source, a locus, an attribution or a
qualification. The presentation values are unchanged at 12.5 points on
17-point leading with 0.6em between paragraphs.

## The homily iteration-2 repair

One blocking finding reached this stage, `HOM-005`, against the Collect
paragraph of the fourth movement in `sections/homily/10-homily.tex`, and it was
repaired there. No study component, research record or source record was
touched.

The paragraph had staged a correction of the English it quotes. Having given
the Collect as "and with a clean heart follow thee, the only true God", it told
the assembly that where that old English says "with a clean heart" the Latin
says *mente*, with the mind, "the Gospel's own word", and went on that the
prayer "asks God for precisely what the Gospel commands of us". The turn does
not survive the Gospel the homily has already preached. Mt 22:37 names heart,
soul and mind together, and the speech's own second movement makes "Three
times, whole" its emphasis, so "heart" is the Gospel's word exactly as *mente*
is; Augustine's gloss, preached in that same movement, refuses the division of
the commandment into faculties among which one might be shown to be the right
one; and the wording singled out as the authentic one is in fact the later one,
since the Old Gelasian reads *te solum Dominum puro corde* and Wilson's
apparatus records *pura mente* only for Pamelius's Gregorian (§2.3 of
`research/scope.md`). No clause of the passage was false; the impression it
left was, and it was left at the pulpit, where nobody can check it.

The philological turn is gone, and nothing of the prayer's transmission history
was imported in its place: that qualification belongs to
`sections/10-each-element.tex` and `sections/concise/04-themes.tex`, which both
already carry it, and the speech satisfies the evidence rule by asserting no
textual fit rather than by explaining one away. After the Collect is quoted the
paragraph now reads: "Kept clear of what corrupts us, and following God alone:
that is the one current again, and no second channel. The prayer is older than
its place in this Sunday's Mass and was not composed for this Gospel, and still
it asks of God what the Gospel commands of us." The Collect's two petitions are
restated in the terms of Augustine's one-current image from the second
movement, which is where this homily's argument already stood; the convergence
is asserted as convergence, with the disclaimer of composition kept, so no
compiler's design is claimed; and the sentence the paragraph exists for — that
the commandment comes to us as a command and goes back to God as a petition —
is untouched.

Three source files changed: `sections/homily/10-homily.tex`,
`sections/homily/90-note.tex` for the word count, and
`generation-metadata.tex` for the revision timestamp and the contribution note;
this record is the fourth. The spoken body fell from 1,445 words to 1,437,
which leaves the note's pace estimate as it stood, and the proof is still five
pages with the speech ending on page 3. The presentation values are unchanged
at 12.5 points on 17-point leading with 0.6em between paragraphs.

## The homily iteration-3 repair

One blocking finding reached this stage, `HOM-006`, against the same Collect
paragraph of the fourth movement in `sections/homily/10-homily.tex`, and it was
repaired there. The two advisories handed down beside it, `HOM-007` and
`HOM-008`, were cleared in the same file while the author was in it. No study
component, research record or source record was touched.

`HOM-006`. After quoting the Collect the paragraph told the assembly that "The
prayer is older than its place in this Sunday's Mass and was not composed for
this Gospel, and still it asks of God what the Gospel commands of us." Both
halves of the clause are true and both are sourced — §2.3 of
`research/scope.md` and the Collect's source row carry the transmission — and
truth was never the question. The clause does in reader-facing prose what the
1962 profile's Evidence and Claim Discipline forbids: it denies a compiler's
intention the speech nowhere asserts, and the "and still" construction makes
the disclaiming function explicit. That rule and the three-document profile's
"The formulary is a compilation" agree that the evidence rule is satisfied by
not asserting a compiler's design, not by disclaiming one from the pulpit; and
a statement of the prayer's transmission relative to the formulary is
apparatus, which the homily profile keeps out of the speech. The sentence now
reads "The prayer asks of God what the Gospel commands of us." The Collect
quotation, the restatement in the terms of Augustine's one current and no
second channel, and the sentence the paragraph exists for — that the
commandment comes to us as a command and goes back to God as a petition,
because we cannot manufacture it ourselves — stand unchanged. The prayer's
transmission keeps the two reviewed homes that already carry it as documented
history, `sections/10-each-element.tex` and `sections/concise/04-themes.tex`.
The iteration-2 entry above records the disclaimer as deliberately retained;
that reasoning was wrong on both profiles, and this entry supersedes it.

`HOM-007`, advisory, cleared. The second movement glossed Chrysostom's "this
makes the way for that, and by it is again established" as "The love of the
neighbour opens the road to the love of God, and then keeps the road open",
which gives both of his clauses to love of neighbour and drops the return
direction. The tracked NPNF1 10 text of *In Mt.* hom. 71 runs its four proof
texts both ways — Jn 3:20 and 1 Tim 6:10 from neighbour-love to God-love, Ps
53:1 and Jn 14:15 from God-love to neighbour-love — and the sentences that
follow state both. The gloss now reads: "The love of the neighbour opens the
road to the love of God; and the love of God, in its turn, re-establishes the
love of the neighbour. Each holds the other up." That is the mutual
establishment `research/interpretations.md` names as Chrysostom's own
mechanism, and the returning direction is the one the fourth movement then
leans on when it says that the one God loved with an undivided heart has one
body in this world.

`HOM-008`, advisory, cleared. The fifth movement called the Postcommunion "The
last prayer of this Mass". The Conclusion row of the rite table in
`research/context.md` records what follows it at this occurrence: *Ite, missa
est*, the *Placeat*, the blessing and the last Gospel (RGMR 507–509; *Ordo
Missae* nos. 1132–1139), all of which the assembly would see before leaving.
The sentence now opens "The prayer after Communion asks that …", which names
the oration without a claim about where the Mass ends; the two Cummiskey
fragments and the rest of the paragraph are untouched.

Three source files changed: `sections/homily/10-homily.tex`,
`sections/homily/90-note.tex` for the word count and the pace it implies, and
`generation-metadata.tex` for the revision timestamp and the contribution note;
this record is the fourth. The spoken body fell from 1,437 words to 1,429, and
the proof is still five pages with the speech ending on page 3. The Collect
paragraph still turns the page, now leaving two lines at the foot of page 2 and
carrying five to page 3. The presentation values are unchanged at 12.5 points
on 17-point leading with 0.6em between paragraphs.

## Author proof and checks for the homily

`make doc DOC=liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost-homily PROVIDER=claude`
settles in two passes. The final log has no overfull or underfull box, no
warning, no undefined reference and no rerun request. The PDF has 5 pages,
letter size, Palatino (TeX Gyre Pagella) with Latin Modern Mono for the
colophon's record paths; all six font resources are embedded, subsetted and
Unicode-mapped, and the document info carries the title, the subject and the
tracked ModDate with no build-derived CreationDate.

`python3 scripts/_proper_study.py check … --phase content --edition homily
--require-presentation` passes, as do every `check-content-preflight` check the
homily gate names for this edition (references-used, identifiers-resolve,
bindings-valid, restricted-not-reproduced, relation-coverage,
unquoted-not-quoted, structural-meta-labels, house-voice, the three chronology
checks and provenance-matches-run), `tools/check-proper-components --phase
artifacts --edition homily` and `check-generation-metadata`. The
references-used check reports seven entries, every one used in the body.

The settled proof after the iteration-3 repair is
`build/claude/liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost-homily.pdf`,
SHA-256 `9381b74ae96790703b8463854329fb60cb3d36bd16118f67399396aab704103e`, at
the revision timestamp `2026-09-19T00:05:00Z`; a copy of it with the log, the
auxiliary file, the extracted text and their digests is kept beneath this
stage's own artifact directory in the run, with the page rasters in a child of
their own. Rebuilding it from a removed auxiliary file reproduces those exact
bytes. The two studies rebuilt at the same timestamp are SHA-256
`717a83e990ee864d1422058218254fa5039ce4bb367174570d8efbb1c19070c9` (expansive)
and `8ac6eeda33cbf71d74f168aeeab7d0b3bbdee86f2d9db1ea51af6a132983abcd`
(concise); they differ from the earlier proofs only in the printed revision
timestamp, and remain at 38 and 12 physical pages. The iteration-2 homily proof
was SHA-256 `b6dfec59fc0b6e433a739753cdb700427794399cdd5f05d44662fbe4552127a2`
at `2026-09-18T23:59:00Z`, the iteration-1 proof
`998c8acddf84dc54eae73506fc1f496d0417492c05ccff7cdb491dfeec82729a`
at `2026-09-18T23:55:00Z`, and the iteration-0 proof
`147c2a09612898551fe3a6439c48df3ef19acdcf68ab675b287bbe5265b10060`
at `2026-09-18T23:20:00Z`.

The author read the contact sheet and the individual rasters of all five pages,
and the extracted text of all five, at iteration 0, after the iteration-1
repair, after the iteration-2 repair and again after the iteration-3 repair.
The proof shows no clipping,
collision,
missing text, blank page or heading-only page; no paragraph is broken across a
page with a single line stranded; the speech ends on page 3 and the note begins
on page 4; and the References, the revision timestamp and the rights colophon
share page 5. The Collect paragraph still turns the page between pages 2 and
3, as it did before the repair, and after the iteration-3 repair leaves two
lines at the foot of page 2 and carries five to page 3. The six font resources
are embedded, subsetted and Unicode-mapped in this proof as in the earlier
ones. This is an author proof inspection, not the independent visual
evaluation, which follows the shared-timestamp three-document build.

## Upstream observations reported for the homily's cold reviewer

1. No new upstream defect was found while deriving. The two studies, the three
   readings and `research/interpretations.md` §4.5 answered every question the
   homily needed, and the loci it prints were already carried in the study's
   own References.
2. The standing advisories on the studies do not reach this speech. `STU-003`,
   on the placement of Gregory's parable in Matthew 22, stands against the
   expansive study; Gregory is not used here. `RES-018`, on Chrysostom's gloss
   at Eph 4:6, does not arise: the homily quotes Chrysostom only from *In Mt.*
   hom. 71 and says nothing of the three phrases of Eph 4:6. `SYN-007`, on the
   concise study counting the word "one" at sites that do not carry it, was
   held in view: the only count the homily makes is of the Epistle's sevenfold
   *unus* in Eph 4:4–6, and the Collect's *te solum Deum* and the Gospel's
   identification of the one God are named for what they are rather than
   counted as occurrences of a word.
3. The iteration-1 repair found no upstream defect either, and reported none
   silently repaired. `HOM-002` was a homily-only slip: the block Augustine's
   sentence stands in is cited as I.22.20–21 by `research/scope.md` §3.6, by
   `research/interpretations.md`, by the passage record and by both studies,
   and only the homily's note narrowed it to I.22.20. `HOM-001` was likewise
   the homily's own: `sections/00-opening.tex`,
   `sections/30-son-and-lord-of-david.tex` and
   `research/interpretations.md` §2.2 all narrate the exchange correctly.
   Nothing outside `sections/homily/`, `homily.tex` and
   `generation-metadata.tex` was edited at this iteration.
4. The iteration-2 repair found no upstream defect and reports none. `HOM-005`
   was the homily's own over-reading: the Collect's transmission is stated
   correctly and with its qualification in `research/scope.md` §2.3, in
   `sections/10-each-element.tex` and in `sections/concise/04-themes.tex`, all
   of which say that the 1962 *pura mente* is the later form and that the older
   *puro corde* would have met the Gospel's *ex toto corde tuo* as *mente*
   meets its *in tota mente tua*. Only the speech had dropped the
   qualification and built a turn on what was left. Nothing outside
   `sections/homily/`, `generation-metadata.tex` and this record was edited at
   this iteration.
5. The iteration-3 repair silently repaired no upstream defect, and reports one
   observation for the homily's cold reviewer to route to its owner. `HOM-006`
   and `HOM-008` were the speech's own: the studies assert no compiler's design
   for the Collect and state its transmission positively, and the phrase "the
   last prayer of this Mass" occurs in no research record and in neither study.
   `HOM-007` is not only the speech's. The accepted expansive study glosses the
   same sentence of *In Mt.* hom. 71 at `sections/20-whole-heart-one-body.tex`
   as "Love of neighbour opens the road to the love of God, and the love of God
   is in turn confirmed by it", which runs both of Chrysostom's clauses from
   neighbour-love and so does not report the return direction his "by it is
   again established" carries — the second commandment established by the
   first, as his Ps 53:1 and Jn 14:15 proof texts show. `research/interpretations.md`
   names the mechanism "mutual establishment" and distinguishes it from
   Augustine's ordering to God on that ground. The homily's gloss is repaired
   here; the study's sentence is settled reviewed prose this stage may not
   edit, and is reported rather than touched. Nothing outside
   `sections/homily/`, `generation-metadata.tex` and this record was edited at
   this iteration.
