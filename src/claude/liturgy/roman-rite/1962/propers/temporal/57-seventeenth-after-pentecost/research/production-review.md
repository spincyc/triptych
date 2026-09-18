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

Every controlling claim, agreement and narrow disagreement the study carries is
preserved: Augustine against Cassiodorus on the speaker of Ps 101; Jerome
against Augustine on Daniel's own sins; the two lines of exegesis at Eph 4:6,
with Chrysostom and Theodoret credited only with the three relations of the one
God and Father and never with the distribution among the Persons; Hilary beside
Augustine on where the servant's mercy begins; Bellarmine against Rupert and
Durandus on what the Introit's *iudicium* names; and the statement, wherever
Rupert and Durandus are used, that their office read Luke 14.

**Substantive word count: 4,624 words** (4,250 with the content of the
`\latin{}` quotations removed), counted over the two argumentative components,
the themes section and the commentary, through Pandoc's LaTeX AST with headings
and page markers removed, then counted as whitespace-separated plain-text
words. It excludes the map, the overview rows, the dossier sheet, the scope
note and the References. Against the study's 13,106 words over six components
this is about a third of the argument, selected and re-integrated rather than
abstracted. The finished PDF is 12 physical pages, inside the 10–12-page
requirement.

Two leaf-local presentation environments were added to `format.tex` for this
companion and are used by no research component: `concisemaptable`, the study's
three-column map one step smaller, and `conciseoverview`, the two-column
overview. Their column widths are chosen so that both tables rule to the same
measure on the first page. Nothing else in `format.tex` changed, and the study's
own rendering is unaffected.

The shared generation record now carries a second contribution for this stage
and the revision timestamp `2026-09-18T20:40:00Z`. The expansive study was
rebuilt at that timestamp and is unchanged at 38 pages.

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
SHA-256 `ee9b7e7a4c8eb52410f1a4970bb11d4de9138a872fdb58e0354406e3602bfeb9`, at
the revision timestamp `2026-09-18T20:40:00Z`; a copy of it with the log, the
auxiliary file, the extracted text and their digests is kept beneath this
stage's own artifact directory in the run, with the page rasters in a child of
their own. The expansive study rebuilt at the same timestamp is SHA-256
`4e50803c658b03a5c2503d4adcce99114a60a273e8f57db5735af0e221b62226`.

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
3. No other upstream defect was found while deriving. The study's three
   readings, its comparison and its element-by-element settings answered every
   question the concise argument needed, and the standing research advisory
   `RES-018` on Chrysostom's gloss at Eph 4:6 is observed here as it is in the
   study: the NPNF English alone is quoted, and Chrysostom is credited with an
   argument about the Son and never with the distribution of the three phrases
   among the Persons.
