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

**Substantive word count: 13,918 words** (13,081 with the content of the
`\latin{}` quotations removed). The count converts the six argumentative
components — opening, element-by-element setting, the three readings, and the
comparison — through Pandoc's LaTeX AST with headings and the map, comparison
and dossier tables removed, then counts whitespace-separated plain-text words.
The leaf's own inline commands are declared to Pandoc before the conversion,
because Pandoc silently drops the argument of a command it has not been given
and `\latin{}` and `\work{}` carry a large part of what these components say.
The figures this record stated through iteration 6, 13,106 and 12,185, came
from an implementation that does not reproduce here, so the absolute is
discontinuous at this iteration; within any one round only that round's own
before-and-after delta is comparable. It excludes the appointed-text component,
the Scriptural Date and Location appendix, the scope appendix and References.
The total stands above the profile's 6,000–10,000-word planning range, which
the profile states is a range and not a quota: three readings that each carry
all ten appointed elements and close with four senses account for 9,448 words
of it, and the element-by-element settings, which carry the textual, historical
and liturgical facts the readings then use, for 2,710 more. The finished PDF is
38 physical pages, inside the 20–50-page requirement.

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
`presentation_contract = "interpretive-pagination-v1"`. It declares nine
research components, six synthesis components and two homily components, and
the three interpretive lanes with their authors, senses, element coverage and
source-audit paths. Only the research components were authored at this stage;
the concise and homily components were declared here and written later by the
stages that own them. (The counts read "eight" and "five" until iteration 2.
The manifest always declared nine and six; the figures were a miscount in this
record, reported by the concise author and repaired here.)

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
strophes of Ps 118 only; Bellarmine only in O'Sullivan's abridged English, and
that in the tracked eCatholic2000 transcription rather than the 1866 printing; no
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
texts, and a second page of the dossier sheet, which stood whole on one page at
that iteration. (It does not at iterations 1 and 2: the 75 words added to the
comparison moved the sheet down, and it has run onto a second page ever since.
The iteration-1 record kept the iteration-0 sentence without rechecking it; the
concise author found the error and it is corrected here and at iteration 2
below.) At iteration 1 the author re-rendered all 38 pages, read both contact
sheets again and the individual rasters of the two comparison pages and the
final page, and confirmed that the repaired paragraph sets without a spill, that
the comparison table still stands whole beneath it, and that the revision
timestamp and the rights colophon still share the last page. The proof shows no
clipping, collision, missing text or heading-only page. This is an author proof
inspection, not the independent visual evaluation, which follows the
shared-timestamp three-document build.

## The iteration-2 repair

One blocking finding reached this stage, `STALE-STUDY-REVIEW`, raised by the
`review-inputs` check of the terminal artifact gate against `study-review`:
*current input bytes differ from the accepted review*.

**What had drifted.** The study review seals nineteen files. Eighteen were
unchanged. The nineteenth, the leaf-local `format.tex`, was
`d7cba8a2b3b1c67fbe423ee22b4b2f6c99a73481128868db883fba0e97c7105e` when
`study-review` accepted the study at iteration 1, and
`151f7b2bed32adc252192ebfd063b5ab341976affdd80ce8105f2abc236776e8` when the
gate ran. `format.tex` is shared by the three entrypoints, and the concise
author added two presentation environments to it — `concisemaptable` and
`conciseoverview` — during the concise authoring stage that the study's own
acceptance started, for the concise companion's first physical page, and
recorded the addition in that stage's own result. No study component and no
research record had changed. The study is not the stage that edited the file, but it is
the stage that owns it, so the repair is addressed here.

**Adopted, not restored.** The two environments are used by
`sections/concise/01-inventory.tex` and `sections/concise/02-overview.tex` and
by nothing else; the study's own output was unaffected when they were added,
and rebuilt at the same 38 pages. Restoring the reviewed bytes would therefore
have removed two environments an already accepted companion needs, to renew a
review that the workflow renews in any case by running `study-review` again
over the current bytes. The current file is adopted as the study's own, and the
hazard is now written into its header: because the file is shared, an
environment added for one entrypoint re-opens the other two documents'
accepted reviews.

**Five standing advisories cleared while in these files.** They were raised by
`study-review` at iterations 0 and 1, gate nothing, and were repaired because
this stage was open in the files they name.

1. `STU-003`. St Gregory's parable no longer "stands just before this Gospel";
   it "opens the same chapter of Matthew". Two pericopes intervene, as the
   study's own Gospel section says, and the research record never claimed
   adjacency. Gregory's role is unchanged.
2. `STU-004`. The Gradual paragraph no longer contains the sentence saying what
   the study declines to conclude from the Missal's typography. It now states
   the two typographic facts in one sentence — `spíritu` here and in the
   Epistle, `Spíritu` in the votive Mass of the Holy Spirit — and then states
   positively that Basil, Augustine and Cassiodorus read the Word and the
   Spirit out of the psalm's own words.
3. `STU-005`. Theodoret of Cyrus is added to the `son-and-lord-of-david` lane's
   declared authors, which is what the section and `research/interpretations.md`
   2.6 already say of him.
4. `STU-006`, manifest half. Rupert of Deutz and William Durandus are added to
   the `son-and-lord-of-david` lane, and John Chrysostom and Thomas Aquinas to
   the `just-judge-merciful-hearer` lane. Every added name is developed in the
   section that now declares it; no declared name is undeveloped, and no prose
   was added to justify a declaration.
5. `STU-007`. Ps 118:135 is located by something a reader can count: "Two
   verses before the antiphon's opening verse 137, in the strophe the antiphon
   passes over between verses 124 and 137". The strophe, the verse number and
   the verb the Offertory reuses are unchanged; only the false offset is gone.

**The dossier sheet.** The Scriptural Date and Location appendix has not fitted
one page since iteration 1, and the Gospel's two tiers were falling either side
of the turn — its summary and narrated-event rows on the first page, its
explanatory row on the second. The sheet now turns between dossiers instead of
inside one: five dossiers stand whole on the first page, the Gospel and the
Epistle whole on the second, with the table's header repeated. Nothing in the
dossiers' content, order or evidence changed.

**Word count.** The three sentence repairs add six substantive words. Measured
by converting the same six argumentative components through Pandoc's LaTeX AST
with headings and the map, comparison and dossier tables removed, this
iteration's implementation of that description counts 13,639 words on the
pre-repair bytes and 13,645 now. It does not reproduce the 13,106 the
iteration-1 record states by the same description, so the two figures are not
comparable and the difference is in the implementations, not in the text: what
is established is that the repair is six words, and the study's extent is
unchanged.

**Files touched.** `sections/10-each-element.tex`,
`sections/20-whole-heart-one-body.tex`, `sections/30-son-and-lord-of-david.tex`,
`sections/80-date-location.tex`, `format.tex`, `proper-components.toml`,
`generation-metadata.tex` and this record. No research record was edited, no
evidence was changed, and no claim was weakened to make anything pass. The
`Derive-synthesis`, `Derive-homily` and `Build artifacts` sections below
describe bytes this iteration supersedes; the stages that own them rewrite
them when they run again.

**Reported upstream, not repaired here.** `STU-006` also asks that
`research/interpretations.md` section 3 record Thomas Aquinas among the
`just-judge-merciful-hearer` reading's witnesses, with his locus *Super
Philippenses* c. 4 on 4:6 and the source role `research/scope.md` 3.7 already
gives him — doctrine on prayer, not exegesis of Daniel. That file belongs to
the research owner and this stage did not touch it, so the manifest and the
prose now agree while the interpretation audit still does not. The cold
reviewer can route it.

## Author proof and checks at iteration 2

`make doc DOC=liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost PROVIDER=claude`
settles in two passes. Built again from a removed auxiliary file, it reproduced
its warm bytes exactly, so the proof is a cold fixed point. The final log has no
error, no `LaTeX Warning`, no package warning, no overfull or underfull box, no
undefined reference and no rerun request.

The settled proof is
`build/claude/liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost.pdf`,
SHA-256 `92511e9c1ddc21bf09c4a5c2d57172771b9732fd0a8a8accb3c707a82f4ae877`, at
the revision timestamp `2026-09-19T00:45:00Z`. It is **38 physical pages**,
inside the contract's 20–50, letter size, Palatino (TeX Gyre Pagella) at 11
points on 15-point leading; all seven font resources are embedded, subsetted
and Unicode-mapped, and the two Latin Modern Mono faces serve the colophon's
record paths. Text extraction is complete and faithful — 18,923 words, no
replacement character. It supersedes the iteration-1 proof, SHA-256
`1895c260216d888caf566fb85cc245cf236fcf620156dd24b2bcbf53bc2fa985`, which
remains beneath that iteration's own directory.

Checks run and passing at these bytes:
`tools/check-proper-components --provider claude --document … --phase artifacts
--edition research`; `python3 scripts/_proper_study.py check … --date
2026-09-20 --phase content --edition research --require-presentation`; every
`check-content-preflight` check the study gate names — references-used,
identifiers-resolve, bindings-valid, restricted-not-reproduced,
relation-coverage, unquoted-not-quoted, structural-meta-labels, house-voice,
the three chronology checks, and provenance-matches-run against this run's own
header; `check-generation-metadata`; and `check-web-edition`. A trial
`tools/web-edition` run converts the leaf without loss and carries the ten
`proper-<element-key>` anchors.

All 38 pages were rendered and both contact sheets read, with the two dossier
pages and the three repaired pages inspected individually. There is no blank
page, no heading-only page, no clipping, collision or missing text; the
least-filled pages remain the title page and the section-end pages, each of
which ends a reading or an element. The proof, its log, auxiliary file,
extracted text and their digests are kept beneath this run's
`author-study-0002` artifact directory, with the page rasters in a replaceable
child of their own. This is an author proof inspection, not the independent
visual evaluation, and not the study review: the workflow obtains a fresh
independent review of these bytes, which is what the finding requires.

## The iteration-3 repair

Two blocking findings reached this stage from the independent visual review,
`VIS-001` and `VIS-002`. Both are defects of the running matter, both were
invisible to every mechanical gate, and both are repaired in the study's own
sources. Two advisories came with them and are answered below.

**`VIS-001`: the two halves of the head overprinted.** On physical page 20 the
left head, `Seventeenth Sunday after Pentecost`, and the right head, the full
title of the second reading, overlapped by 0.12 in, measured between the right
edge of the left string and the left edge of the right one in the settled
bytes of the iteration-2 proof; page 26 was the same defect a hair short of
collision, its two strings separated by 6 pt. The cause is in `fancyhdr`:
it laps each head string out of a `\parbox` the full width of the head, so
the two boxes occupy the same space and a long right string prints straight
over the left one. Nothing overflows any box, and the log is therefore silent.

The repair has two parts, because the mechanism and the content are two faults.

*The mechanism.* `format.tex` now cuts the right head to what remains of the
head width after the fixed left string and a 1.5 em gutter, measured at use
with `\settowidth`. The gutter is white space and not glue, so no setting of
the two strings can close it. A string too long for the remaining box wraps
inside that box instead of reaching the left string, and the second line
trips `fancyhdr`'s `\headheight` warning, which the log carries and a log
inspection catches. The silent failure is now a loud one.

*The content.* A wrapped head is legible but ugly, so the three interpretive
sections, whose reader-first titles run to 67, 74 and 71 characters and are
the only titles too wide for the box, declare short running forms:
`The Whole Heart and the One Body`, `David's Son and David's Lord`, and
`"Thou Art Just, O Lord"`. Each is set by `\runninghead` immediately before
its `\section`, and the heading and the contents keep the full title. The
declaration must replace the section's own mark rather than follow it:
`\rightmark` takes the **first** mark on a page, not the last, so a
`\markright` written after the heading is beaten by the heading's own mark on
the one page where it matters, the page the heading opens. That is why the
first attempt at this repair, which did write `\markright` after the heading,
left pages 20 and 26 exactly as they were.

**`VIS-002`: the References carried the Appendix's head.** `\section*` sets no
mark, so the mark of the preceding `\section{Appendix: Scope and
Qualifications}` stood over pages 36 and 37, which carry nothing but the
bibliography. The heading now sets its own mark, through `\runninghead`, and
those pages are headed `References`, as the concise companion's already were.

Two constraints decide the form, and each rules out the obvious alternative.
The heading must stay starred: `check-content-preflight` finds the References
section by the literal `\section*{References}`, and an ordinary `\section` —
which would set the mark by itself, sections being unnumbered here and the
unstarred form therefore typesetting the identical heading and contents line —
made `references-used` and `unquoted-not-quoted` both report that the leaf
prints no References section. That route was tried and reverted. The mark must
also be set through `\runninghead` rather than by the bare `\markright` the
concise companion writes, because the web converter's macro whitelist does not
carry `\markright` and the canonical study is this leaf's only web edition;
the converter refused the leaf outright while the bare form stood.

**The advisories.** `VIS-003`, the Introit row of the opening map, is
repaired: the row's second column now prints the concise map's shorter
`verse 1` in place of `verse Ps 118:1`. Its gutter to the third column goes
from 6 pt to 33 pt, which is wider than any other row of the same table, and
the two columns no longer read as one run of text. `VIS-004`, the ink fill of
pages 13 and 19, is **not** acted on, and the finding's own reasoning is why:
every repair it proposes moves the pagination of all 38 pages, and with it the
physical-marker evidence this run has settled, for a reader whom the finding
states is not misled. Pagination is unchanged by everything above — the folio
of every page of the study is what it was at iteration 2.

**A constraint this repair discovered.** The web converter does not scan the
leaf's preamble includes, but it does carry their `\newcommand` definitions
into the document it hands pandoc, and it expands every `\runninghead` of the
body there. What may stand in that macro's body is therefore decided by
pandoc, not by LaTeX. `\markright` is safe there — pandoc knows the command
and drops it, which is right, since a running head carries no reader-facing
text in a web edition. A `\newif` boolean is not: the first form of this
repair put `\global\tptshortheadtrue` in `\runninghead` and the conversion
failed on `unexpected \tptshortheadtrue`. The boolean was replaced by an
`\ifx` against a `\let`-made sentinel, and that test now lives in
`\sectionmark`, which LaTeX alone calls and pandoc never expands. The header
of `format.tex` records the constraint for the next author.

## Author proof and checks at iteration 3

`make doc DOC=liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost PROVIDER=claude`
settles in two passes. Two independent builds from a removed PDF, log and
auxiliary file produced identical bytes, so the proof is a cold fixed point.
The final log has no error, no `LaTeX Warning`, no package warning — the
`fancyhdr` `\headheight` warning that the new width discipline raises while a
head is too long is absent, which is the mechanical evidence that no head
wraps — no overfull or underfull box, no undefined reference and no rerun
request.

The settled proof is
`build/claude/liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost.pdf`,
SHA-256 `3fb87bf39141f9d5670add1fb1012f83196b6df398887c5f8435fc035fdee822`, at
the revision timestamp `2026-09-19T03:20:00Z`. It is **38 physical pages**,
inside the contract's 20–50, letter size, Palatino (TeX Gyre Pagella) at 11
points on 15-point leading; all seven font resources are embedded, subsetted
and Unicode-mapped. Text extraction is complete and faithful — 18,889 words,
no replacement character. That is 31 fewer than the 18,920 the same extraction
reports for the iteration-2 proof, and a word-frequency diff of the two
extractions accounts for every one of them: the three full interpretation
titles that stood in the head of one page each, the two `Appendix: Scope and
Qualifications` heads that became `References`, the Introit's `verse Ps 118:1`
that became `verse 1`, and the revision timestamp. Nothing else differs. No
substantive word was added or removed and no section of the study was
rewritten. It supersedes the iteration-2 proof, SHA-256
`92511e9c1ddc21bf09c4a5c2d57172771b9732fd0a8a8accb3c707a82f4ae877`, which
remains beneath that iteration's own directory.

The head geometry is measured rather than asserted. Every one of the 38 pages
carries a single-line head; the narrowest gutter between the left and the
right string anywhere in the study is 0.92 in, on page 9, and pages 20 and 26
now stand at 2.35 in and 2.63 in. Pages 36 and 37 are headed `References`, and
no page is headed with a section it does not contain.

Checks run and passing at these bytes:
`tools/check-proper-components --provider claude --document … --phase artifacts
--edition research`; `python3 scripts/_proper_study.py check … --date
2026-09-20 --phase content --edition research --require-presentation`; every
`check-content-preflight` check the study gate names — references-used,
identifiers-resolve, bindings-valid, restricted-not-reproduced,
relation-coverage, unquoted-not-quoted, structural-meta-labels, house-voice,
the three chronology checks, and provenance-matches-run against this run's own
header; `check-generation-metadata`; and `check-web-edition`. A trial
`tools/web-edition` run converts the leaf without loss and carries the ten
`proper-<element-key>` anchors, with References now a top-level heading of its
own.

All 38 pages were rendered and both contact sheets read, with pages 3, 20, 26,
36 and 38 inspected individually. There is no blank page, no heading-only
page, no clipping, collision or missing text. The terminal colophon page
carries neither head nor folio, which is the shared
`\TriptychRightsNotice`'s own `\thispagestyle{empty}` and not a defect of this
leaf; it was the same at iteration 2. Both companions were rebuilt against the
changed shared `format.tex` and are unchanged in extent, 12 and 5 physical
pages, with clean logs; the concise study's fixed opening still places the
inventory and overview on page 1, the dossier on page 2 and the themes on
pages 3–4. The proof, its log, auxiliary file, contents file, extracted text
and their digests are kept beneath this run's `author-study-0003` artifact
directory, with the page rasters in a replaceable child of their own. This is
an author proof inspection; the shared-timestamp three-document build and the
independent visual review remain the workflow's to obtain.


## The iteration-4 repair

One blocking finding reached this stage from the independent study review,
`STU-009`, and it is a reading error in the study's own prose. Three standing
advisories came with it; two are cleared here and the third is not this
stage's to clear.

**`STU-009`: the direction of Chrysostom's reciprocity was reversed.** The
first reading printed *In Mt.* hom. 71 — "But wherefore 'like unto this?'
Because this makes the way for that, and by it is again established" — and
then glossed it "Love of neighbour opens the road to the love of God, and the
love of God is in turn confirmed by it", which gives both of the sentence's
clauses to the love of neighbour. The elided subject of "is again established"
is the same "this", the second commandment, so what the second establishes is
not the first: the second is established by the first in its turn. The
subsection's closing comparison then called this "mutual dependence" while
naming one direction twice, "the second preparing and confirming the first",
and the homily derived from this study had already been corrected the other
way, so the two documents contradicted each other on the same clause.

The passage was re-read for this repair, whole, in the same tracked CCEL text
of NPNF1 10 that the source binding
`passage.john-chrysostom.homiliae-in-matthaeum.ccel-web-2026-09-17.homily-71`
records, and the homily settles the direction from its own proofs. The four
scriptural texts Chrysostom sets beside the sentence alternate: Jn 3:20 ("every
one that doeth evil hateth the light") and 1 Tim 6:10 ("the love of money is
the root of all evils; which while some coveted after they have erred from the
faith") run from the failure of charity to the loss of God, while Ps 53:1 ("The
fool hath said in his heart, There is no God … They are corrupt, and become
abominable in their ways") and Jn 14:15 ("He that loveth me, will keep my
commandment") run from God to the neighbour; and the conclusion holds both ends
at once — "If therefore to love God is to love one's neighbor … but to love
one's neighbor worketh a keeping of the commandments, with reason doth He say,
'On these hang all the law and the prophets.'" The gloss now reads that both
clauses speak of the second commandment, that the love of neighbour opens the
road to the love of God and the love of God in its turn re-establishes the love
of neighbour, and prints the four alternating proofs and that conclusion. The
closing comparison now says "mutual dependence in both directions: the second
commandment makes the way for the first, and the first establishes the second
again", and the Epistle subsection's remark that Chrysostom's "bind ourselves
together with one another and unto God" could gloss "like to this" now says
that the clause names both directions at once.

The repair rests on the English at the registered locus and on nothing else.
The source binding records that homily as read in translation and not collated
with the Greek, and that is still true: the Greek of PG 58.661 was not read
here and no claim in the study depends on it. No research record was edited.
`research/interpretations.md` §1.2 and `research/scope.md` §4.3 already name
Chrysostom's mechanism "mutual establishment" and "mutual dependence" without
glossing its direction, so the audit record needed nothing, and the study now
agrees with `sections/homily/10-homily.tex`, which states the reciprocity in
the same two directions.

**`STU-008`, advisory, cleared.** The scope appendix disclosed the delivery of
every witness it names except Bellarmine, whose entry read "Bellarmine was read
only in O'Sullivan's abridged English of 1866" and so could be taken for a
reading of the 1866 printing. `research/source-bindings.toml` binds those
passages to a tracked web transcription of the translation. The Reception
paragraph now adds "and that in a tracked web transcription of the translation
(ecatholic2000.com), not on the 1866 printing"; the References entry carries
that transcription's locator; and the limits recorded above say the same. The
ten Bellarmine citations are unchanged.

**`STU-010`, advisory, cleared.** In the second reading the Postcommunion was
the one element carried by a bare assertion — "The Postcommunion's
*Sanctificationibus tuis* names a holiness that is God's own and given in the
sacrament" — with no witness and no textual fact, in a reading that works every
other element through one or both. No witness in the evidence base reads
*sanctificationes* of the Word or the Spirit, and inventing one to fill the
place is exactly what this stage may not do. The reading now says plainly, as
it already does of the Secret, that the prayer adds nothing distinctive to it:
its address is to the *omnípotens Deus* with no distinction of Persons; what it
asks is the healing the first and the third readings develop; and its only
Trinitarian words are the conclusion shared with the Collect and the Secret,
printed here merely as *Per Dóminum nostrum* and completed by RG 115 a.
`sections/50-comparison.tex`, which had listed the Postcommunion's
*sanctificationes* among the three orations this reading hears as confession,
is brought into line and now records the disclaimer instead.

**Reported upstream, not repaired here.** `STU-006` still asks that
`research/interpretations.md` section 3 record Thomas Aquinas among the
`just-judge-merciful-hearer` reading's witnesses, with his locus *Super
Philippenses* c. 4 on 4:6 and the source role `research/scope.md` 3.7 gives
him, and name him in the 3.3 Offertory row and the 3.4 moral sense. The
manifest half was repaired at iteration 2; the audit half is in a research
record this stage does not edit, and it is unchanged. The cold reviewer can
route it.

**Word count.** Measured by the same plain `pdftotext` extraction the
iteration-3 entry used, the settled proof carries 19,187 words against that
proof's 18,889, a net gain of 298. A word-level diff of the two extractions
accounts for all of it: 296 words of the four repairs above, two more because
the extraction breaks the References URL across a line into two tokens, and the
running heads and folios of pages 15–18, 24 and 35–37, which shift with the
repagination and net to nothing. Nothing else was added or removed, and no
section was rewritten.

Measured instead as substantive words — the six argumentative components
converted through Pandoc's LaTeX AST with headings and the map, comparison and
dossier tables removed, which is the description the header of this record
gives — this iteration's implementation counts 12,491 on the pre-repair bytes
and 12,761 now, a gain of 270. As at iteration 2, the absolute figure does not
reproduce the 13,106 the iteration-1 record states by the same description, so
the two are not comparable and the difference is in the implementations rather
than in the text; what this measurement establishes is the size of the repair.
The 270 agrees exactly with the 270 words the four repairs add inside those
components when counted in the source, the remaining 26 of the 296 falling in
the scope appendix and the References, which the substantive count excludes.
The study's extent is unchanged at 38 physical pages, and the headline
statement above — that the total stands above the profile's 6,000–10,000-word
planning range, which the profile states is a range and not a quota — still
holds on either measure.

**Files touched.** `sections/20-whole-heart-one-body.tex`,
`sections/30-son-and-lord-of-david.tex`, `sections/50-comparison.tex`,
`sections/90-apparatus.tex`, `generation-metadata.tex` and this record. No
research record was edited, no evidence was changed, and no claim was weakened
to make anything pass. The `Derive-synthesis`, `Derive-homily` and `Build
artifacts` sections below describe bytes this iteration supersedes; the stages
that own them rewrite them when they run again.

## Author proof and checks at iteration 4

`make doc DOC=liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost PROVIDER=claude`
settles in two passes. Two independent builds from a removed PDF, log and
auxiliary file produced identical bytes, so the proof is a cold fixed point.
The final log has no error, no `LaTeX Warning`, no package warning — the
`fancyhdr` `\headheight` warning that the width discipline raises while a head
is too long is absent, which is the mechanical evidence that no head wraps — no
overfull or underfull box, no undefined reference and no rerun request.

The settled proof is
`build/claude/liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost.pdf`,
SHA-256 `7993908cec4fc289b07bb6ea2c230ad6b456696bc97dd4f7482e81c0bd0d5327`, at
the revision timestamp `2026-09-19T04:10:00Z`. It is **38 physical pages**,
inside the contract's 20–50, letter size, Palatino (TeX Gyre Pagella) at 11
points on 15-point leading; all seven font resources are embedded, subsetted
and Unicode-mapped. Text extraction is complete and faithful, with no
replacement character. It supersedes the iteration-3 proof, SHA-256
`3fb87bf39141f9d5670add1fb1012f83196b6df398887c5f8435fc035fdee822`, which
remains beneath that iteration's own directory.

The head geometry is measured rather than asserted, because the repair's length
moved four subsection heads onto different pages. Thirty-six of the 38 pages
carry a running head — the title page and the terminal colophon page carry none
— and every one of the thirty-six is a single line, with no second line
anywhere in the head band. The narrowest gutter between the left and the right
string is 0.92 in, on page 9, the same page and the same figure as at iteration
3; no gutter is zero or negative, so no two head strings touch. Pages 36 and 37
are headed `References`, and no page is headed with a section it does not
contain.

Checks run and passing at these bytes, seventeen in all:
`tools/check-proper-components --provider claude --document … --phase artifacts
--edition research`; `python3 scripts/_proper_study.py check … --date
2026-09-20 --phase content --edition research --require-presentation`; every
`check-content-preflight` check the study gate names — references-used,
identifiers-resolve, bindings-valid, restricted-not-reproduced,
relation-coverage, unquoted-not-quoted, structural-meta-labels, house-voice,
the three chronology checks, and provenance-matches-run against this run's own
header; `check-generation-metadata`; and `check-web-edition`. A trial
`tools/web-edition` run converts the leaf without loss, carries the ten
`proper-<element-key>` anchors and keeps References a top-level heading; the
References entry's new locator converts as a link like the others.

All 38 pages were rendered and both contact sheets read, with pages 15, 24, 37
and 38 inspected individually — the three that carry repaired prose and the
terminal page. There is no blank page, no heading-only page, no clipping,
collision or missing text. Page 15 ends short because the subsection that
follows it begins on page 16; the terminal colophon page carries neither head
nor folio, which is the shared `\TriptychRightsNotice`'s own
`\thispagestyle{empty}` and not a defect of this leaf. Both companions were
rebuilt against the changed shared `generation-metadata.tex` and build cleanly
at their unchanged extents, 12 and 5 physical pages; they are the derivation
stages' to rewrite against this study, and nothing here anticipates that work.
The proof, its log, auxiliary file, contents file, extracted text and their
digests are kept beneath this run's `author-study-0004` artifact directory,
with the page rasters in a replaceable child of their own. This is an author
proof inspection; the shared-timestamp three-document build and the independent
visual review remain the workflow's to obtain.

## The iteration-5 repair

One blocking finding reached this stage from the independent study review,
`STU-011`, a wrong psalm locus in the first reading. Two standing advisories
came with it; one is cleared here and the other is not this stage's to clear.

**`STU-011`: the psalm cited was not the psalm quoted.** The first reading
prints the four scriptural texts Chrysostom sets beside "thou shalt love thy
neighbour as thyself" in *In Mt.* hom. 71, and attached `(Ps~53:1)` to the
third of them, "The fool hath said in his heart, There is no God … They are
corrupt, and become abominable in their ways". Those words are not Ps 53's in
either numbering. Read in the library's own tracked editions, the Clementine
Vulgate gives Ps 13:1 as *Dixit insipiens in corde suo: Non est Deus. Corrupti
sunt, et abominabiles facti sunt in studiis suis*, and the Douay–Rheims
(Challoner) renders that verse in the very words the study quotes; Ps 52:1–2,
the psalm the Hebrew numbers 53, has instead *abominabiles facti sunt in
iniquitatibus*, "become abominable in iniquities"; and Ps 53 in the Missal's
own Vulgate numbering is *Deus, in nomine tuo salvum me fac*, which has nothing
to do with the sentence. The citation now reads `Ps~13:1; Heb.\ 14:1`, the
Missal's numbering with the Hebrew beside it, as `sections/05-appointed-texts.tex`
says the study cites psalms and as the 1962 profile requires. A sweep of every
psalm number printed in the nine components of `main.tex` finds Pss 32, 75,
101, 109 and 118 and no other: every one is the Missal's number, and after this
repair no bare Hebrew-numbered psalm citation stands in the study.

**A correction to the finding's own premise, reported for the cold reviewer.**
`STU-011` states that the New Advent text of Homily 71 "prints the quotation
without a verse reference of its own, so the locus is the study's, not the
translator's". That is not so of the text this leaf is bound to. The tracked
CCEL transcription of NPNF1 10, the same artifact the source binding
`passage.john-chrysostom.homiliae-in-matthaeum.ccel-web-2026-09-17.homily-71`
records, carries a numbered note `[2636]` on that very quotation, and the note
reads `Ps. liii. 1` — the translator's own reference, in the Hebrew numbering
the series uses. The wrong number was therefore inherited, not invented, though
the study is what printed it bare and in the wrong system. Because a reader who
checks the study against that edition would otherwise meet an unexplained
disagreement, the References entry for the homily now states the divergence as
a fact about the edition: that its note reads "Ps. liii. 1" while the words its
own text prints are those of Ps 13:1 (Heb. 14:1), with the two psalms' Latin
set side by side. Nothing in the reading's argument turns on any of this; the
paragraph's account of Chrysostom's alternating proofs is unchanged.

**`STU-012`, advisory, cleared.** The second reading's Postcommunion paragraph
ended "The reading records the prayer and claims nothing from it", a sentence
about what the guide had declined to infer rather than about the prayer. It is
deleted. The paragraph keeps its opening statement that the Postcommunion adds
nothing distinctive to this reading and the three grounds already given for it,
which is what the advisory asked. A sweep of the nine components for the same
habit finds no other instance: the three remaining uses of "declines" all have
a Father, not the guide, as their subject.

**`STU-006`, advisory, not cleared, and why.** The advisory asks that
`research/interpretations.md` section 3 record Thomas Aquinas among the
just-judge-merciful-hearer reading's witnesses, in its 3.3 Offertory row and in
its 3.4 moral sense, so that the audit record, the manifest and the section
agree. The defect is real and the evidence behind it is sound: `research/scope.md`
§3.7 holds the locus, the Dessain 1857 vol. 2 p. 398 page image read, and the
exact source role — Aquinas uses Dan 9:18 as doctrine on prayer and does not
expound Daniel — and `proper-components.toml` and
`sections/40-just-judge-merciful-hearer.tex` already agree with each other.
What is missing is in a file this stage does not own.
`workflows/fragments/proper-study/research.md` gives
`research/interpretations.md` to the research stage to write, the author-study
fragment gives it to this stage only to read as the evidence map, and
`research/review-dependencies.toml` records that the engine seals the leaf's
research records. Repairing it here would be a silent revision of a reviewed
upstream document, which the workflow contract forbids, so it is left and
reported. The iteration-4 entry reached the same conclusion; this is the second
report of it, and it needs the research owner, not another study pass.

**Word count.** Measured by the same plain `pdftotext` extraction the
iteration-3 and iteration-4 entries used, the settled proof carries 19,242
words against that proof's 19,187, a net gain of 55. A multiset diff of the two
extractions accounts for all of it and leaves nothing over: the References note
adds 60 words as extracted; the deleted sentence removes 10; the corrected
citation turns one token into three, adding 2; and three words break across
lines where they did not before — *misericórdiam*, *Postcommunion* and
*disagreements* — adding 3. The remaining differences are running heads,
folios and table cells that the layout extraction emits in a different order on
the pages whose line breaking moved, and they net to zero.

Measured instead as substantive words — the six argumentative components
converted through Pandoc's LaTeX AST with headings and tables removed, which is
the description the header of this record gives — this iteration's
implementation counts 13,006 on the pre-repair bytes and 12,998 now, a loss of
8: the citation's +2 in the first reading and the deleted sentence's −10 in the
second. As at iterations 2 and 4, the absolute figure does not reproduce the
13,106 the iteration-1 record states by the same description, so the two are
not comparable and the difference is in the implementations rather than in the
text; what this measurement establishes is the size of the repair. The
References note falls in the scope appendix and References, which the
substantive count excludes, which is why the two measures move in opposite
directions. The study's extent is unchanged at 38 physical pages, and the
headline statement above — that the total stands above the profile's
6,000–10,000-word planning range, which the profile states is a range and not a
quota — still holds on either measure.

**Files touched.** `sections/20-whole-heart-one-body.tex`,
`sections/30-son-and-lord-of-david.tex`, `sections/90-apparatus.tex`,
`generation-metadata.tex` and this record. No research record but this one was
edited, no evidence was changed, and no claim was weakened to make anything
pass. The `Derive-synthesis`, `Derive-homily` and `Build artifacts` sections
below describe bytes this iteration supersedes; the stages that own them
rewrite them when they run again.


## Author proof and checks at iteration 5

`make doc DOC=liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost PROVIDER=claude`
settles in two passes. Two independent builds from a removed PDF, log and
auxiliary file produced identical bytes, so the proof is a cold fixed point.
The final log has no error, no `LaTeX Warning`, no package warning — the
`fancyhdr` `\headheight` warning that the width discipline raises while a head
is too long is absent, which is the mechanical evidence that no head wraps — no
overfull or underfull box, no undefined reference and no rerun request.

The settled proof is
`build/claude/liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost.pdf`,
SHA-256 `4903f3c930fdf66e7ecf135b08b5731ec7165f1f815b0751807328787c847367`, at
the revision timestamp `2026-09-19T05:00:00Z`. It is **38 physical pages**,
inside the contract's 20–50, letter size, Palatino (TeX Gyre Pagella) at 11
points on 15-point leading. It supersedes the iteration-4 proof, SHA-256
`7993908cec4fc289b07bb6ea2c230ad6b456696bc97dd4f7482e81c0bd0d5327`, which
remains beneath that iteration's own directory.

The repair did not repaginate. The contents file and the auxiliary file are
byte-identical to iteration 4's — SHA-256
`4274428cbe0909d605fbb4b80de5f17d1ab066e01df1a6e0a85afb6b59ce3c3c` and
`424bc0ef72e2d0ac85f563b68d162d8215fd8194b71d44336471adebd423eeb9` — so no
heading, no float and no cross-reference moved, and the page numbers the study
review cites still name the passages it read. The three touched passages stay
on the pages the findings gave them: the Chrysostom paragraph on page 15, the
Postcommunion paragraph on page 24, and the Chrysostom References entry on
page 37.

Checks run and passing at these bytes, seventeen in all:
`tools/check-proper-components --provider claude --document … --phase artifacts
--edition research`; `python3 scripts/_proper_study.py check … --date
2026-09-20 --phase content --edition research --require-presentation`; every
`check-content-preflight` check the study gate names — references-used,
identifiers-resolve, bindings-valid, restricted-not-reproduced,
relation-coverage, unquoted-not-quoted, structural-meta-labels, house-voice,
the three chronology checks, and provenance-matches-run against this run's own
header; `check-generation-metadata`; and `check-web-edition`. A trial
`tools/web-edition` run converts the leaf without loss. `house-voice` passing
is the mechanical half of the `STU-012` repair; the References note added for
`STU-011` states facts about an edition and takes neither the guide nor its
apparatus as its subject.

All 38 pages were rendered and both contact sheets read, with pages 15, 24, 37
and 38 inspected individually — the three that carry changed prose and the
terminal page. There is no blank page, no heading-only page, no clipping,
collision or missing text, and every running head is a single line. Both
companions were rebuilt against the changed shared `generation-metadata.tex`
and build cleanly at their unchanged extents, 12 and 5 physical pages; they are
the derivation stages' to rewrite against this study, and nothing here
anticipates that work. The proof, its log, auxiliary file, contents file,
extracted text and their digests are kept beneath this run's
`author-study-0005` artifact directory, with the page rasters in a replaceable
child of their own. This is an author proof inspection; the shared-timestamp
three-document build and the independent visual review remain the workflow's to
obtain.


## The iteration-6 repair

One blocking finding reached this stage from the independent study review,
`STU-013`, and it is against this leaf's own audit record rather than against
any reader-facing prose. Two standing advisories came with it and both are
cleared here; the older `STU-006` is not among them and remains where the
iteration-5 entry left it.

**`STU-013`: the record claimed a repair that was not made.** The author-study
`\AIModelContribution` declaration in `generation-metadata.tex` closed its
iteration-5 clause by reporting "two standing advisories" cleared: the second
reading's remark about the Postcommunion removed, and "the third reading's use
of Aquinas on Dan 9:18 recorded in the interpretation audit, whose witnesses,
element table and moral sense now agree with the manifest and the section". The
second half of that is false in each of its three assertions, and this stage
checked every one of them before rewriting the clause.
`research/interpretations.md` names Thomas Aquinas nowhere in section 3: not
among the just-judge-merciful-hearer reading's witnesses in §3.2, not in the
§3.3 element table's Offertory row, which still reads "Jerome on 9:5–23;
Augustine *De pecc. mer.* II sect. 13; Rupert, Durandus (chant)", not in the
§3.4 moral sense, and not in that lane's row of "The three readings in brief",
which still lists "Augustine; Jerome; Cassiodorus; Hilary; Robert Bellarmine;
with Rupert and Durandus for the chants". The file's own header note records
revisions through the fourth research reentry and none at iteration 5, and the
file is byte-identical to its last committed state. So the audit does not
record Aquinas, and it does not agree with `proper-components.toml`, which
declares him for that lane, or with
`sections/40-just-judge-merciful-hearer.tex`, which develops him there at
length.

Only one of the two advisories iteration 5 was handed was in fact cleared. The
iteration-5 clause now says so: it reports `STU-012` cleared, and the other
advisory left uncleared and reported to its owner, with the reason —
`research/interpretations.md` is the research stage's file, and repairing it
from author-study would be the silent revision of a reviewed upstream document
that the workflow contract forbids. That is what the "`STU-006`, advisory, not
cleared, and why" entry above states, and the generation record now agrees with
it instead of contradicting it. Nothing of this reaches a reader: the
contribution declarations render only the revision timestamp. What is repaired
is the tracked audit record itself, which `guidance/editorial.md` ("Audit
records and generation metadata") makes the complete tracked account of what
produced the document.

The correction is to the record, not to the claim. This stage did not make the
iteration-5 sentence true by editing `research/interpretations.md`, for exactly
the reason the earlier entry gives; `STU-006` stands open against its research
owner, and no record of this leaf now states that it has been done.

**`STU-014`, advisory, cleared.** Ps 109 was the one psalm the study cited that
never carried its modern number, against the convention the head of
`sections/05-appointed-texts.tex` states ("Psalms are cited in the Missal's
numbering, with the Hebrew numbering in parentheses") and against the 1962
profile. The note after the Gospel now reads "Ps 109:1 (Heb. 110:1) in verse
44". The conversion was read in the repository's own tracked concordance, the
artifact `psalm-numbering-ee3c7757` of the Douay–Rheims Challoner edition the
study quotes, whose row for Vulgate Ps 109 gives Hebrew and English Ps 110 with
an offset of none, marked uniform through the psalm — the same table already
cited for Pss 32, 75, 101 and 118 in `propers/verified.md`. The later bare uses
in `sections/10-each-element.tex`, `sections/30-son-and-lord-of-david.tex` and
`sections/50-comparison.tex` stand, as the other psalms' later bare uses do.
After this repair every psalm the study cites carries its Hebrew number at
first use: Pss 13, 32, 52, 75, 101, 109 and 118, and no other psalm number is
printed in the nine components.

**`STU-015`, advisory, cleared.** The second reading's Postcommunion paragraph
ended "which RG 115~a completes", the only occurrence of that abbreviation in
the study's reader-facing argument and one the body nowhere expands. It now
reads "which the general rubrics complete (no. 115 a)", the form
`sections/05-appointed-texts.tex` already uses at the Secret ("the conclusion
said is the full form of the general rubrics (no. 115 a)"), so the same rubric
is cited one way throughout the body. The fact is unchanged and unaffected:
`propers/verified.md` §8 records that the typical edition prints this
conclusion only as far as *in unitáte* and that Rubricae generales n. 115 a,
read on the page image at printed p. XIX, gives the full form. The abbreviation
survives only in the terminal appendix and its concise counterpart, where the
References on the following page expand it, which is what the advisory allowed.

**Word count.** Measured as the iteration-5 entry measured it, by `pdftotext
-layout` over the settled proof, the study carries 19,247 words against that
proof's 19,242, a net gain of 5. A multiset diff of the two extractions
accounts for every one of them and leaves nothing over: the `STU-014` repair
adds two tokens, `(Heb.` and `110:1)`; the `STU-015` repair turns four tokens
(`RG`, `115`, `a`, `completes.`) into seven (`the`, `general`, `rubrics`,
`complete`, `(no.`, `115`, `a).`), a gain of three; and the revision timestamp
is one token exchanged for another. Nothing else in the extraction moved.

Measured instead as substantive words — the six argumentative components
through Pandoc's LaTeX AST with headings and tables removed, the description
this record's header gives — this iteration's implementation counts 12,767 on
the pre-repair bytes and 12,770 now, a gain of 3, all of it in
`sections/30-son-and-lord-of-david.tex`. The `STU-014` repair falls in
`sections/05-appointed-texts.tex`, which that measure excludes, which is why
the two measures differ by two. As at iterations 2, 4 and 5 the absolute figure
does not reproduce the 13,106 the iteration-1 record states by the same
description, nor the 12,998 of iteration 5, so only the delta is comparable:
the implementations differ, the text does not.

**Files touched.** `generation-metadata.tex` (the timestamp and the
author-study contribution), `sections/05-appointed-texts.tex`,
`sections/30-son-and-lord-of-david.tex`, and this record. No research evidence
was changed. `research/interpretations.md` is byte-identical to how this
dispatch found it.


## Author proof and checks at iteration 6

`make doc DOC=liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost PROVIDER=claude`
settles in two passes. Two independent builds from a removed PDF, log and
auxiliary file produced identical bytes, so the proof is a cold fixed point.
The final log has no error, no `LaTeX Warning`, no package warning — the
`fancyhdr` `\headheight` warning that the width discipline raises while a head
is too long is absent, which is the mechanical evidence that no head wraps — no
overfull or underfull box, no undefined reference and no rerun request.

The settled proof is
`build/claude/liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost.pdf`,
SHA-256 `9953a1fb142c938c160cf6b59fbc35430e12fc5e2f1120e0a05f27526bb061ad`, at
the revision timestamp `2026-09-19T05:45:00Z`, which the PDF's own `ModDate`
carries. It is **38 physical pages**, inside the contract's 20–50, letter size,
Palatino (TeX Gyre Pagella) at 11 points on 15-point leading. It supersedes the
iteration-5 proof, SHA-256
`4903f3c930fdf66e7ecf135b08b5731ec7165f1f815b0751807328787c847367`, which
remains beneath that iteration's own directory.

The extent and the pagination are unchanged. The contents file and the
auxiliary file are byte-identical to those of iterations 4 and 5 — SHA-256
`4274428cbe0909d605fbb4b80de5f17d1ab066e01df1a6e0a85afb6b59ce3c3c` and
`424bc0ef72e2d0ac85f563b68d162d8215fd8194b71d44336471adebd423eeb9` — so no
heading, no float and no cross-reference moved, and the page numbers the study
review cites still name the passages it read. Four pages differ in their
extracted text, and only four: page 6 and page 24 carry the two repaired
clauses, page 38 the new timestamp, and page 25 receives one line. That line is
the consequence of the `STU-015` repair, which is three words longer than what
it replaced and so lengthens its paragraph by one line: "such Sunday. What
remains firm is the Gospel's second half …" now opens page 25 instead of
closing page 24. It is a reflow within one paragraph across a break that was
already there, not a repagination: the heading "The four senses of this
reading" and everything after it stand where they stood, and both pages were
inspected.

Checks run and passing at these bytes, seventeen in all, with the invocations
and their output kept beside the proof: `tools/check-proper-components
--provider claude --document … --phase artifacts --edition research`; `python3
scripts/_proper_study.py check … --date 2026-09-20 --phase content --edition
research --require-presentation`; every `check-content-preflight` check the
study gate names — references-used, identifiers-resolve, bindings-valid,
restricted-not-reproduced, relation-coverage, unquoted-not-quoted,
structural-meta-labels, house-voice, the three chronology checks, and
provenance-matches-run against this run's own header; `check-generation-metadata`;
and `check-web-edition`. A trial `tools/web-edition` run converts the leaf
without loss, and both repaired clauses survive the conversion intact.

All 38 pages were rendered and both contact sheets read, with pages 6, 24, 25
and 38 inspected individually — the three that carry changed text and the one
that receives the moved line. There is no blank page, no heading-only page, no
clipping, collision or missing text, and every running head is a single line.
Both companions were rebuilt against the changed shared
`generation-metadata.tex` and build cleanly at their unchanged extents, 12 and
5 physical pages; they are the derivation stages' to rewrite against this
study, and nothing here anticipates that work. The proof, its log, auxiliary
file, contents file, extracted text, the check log and their digests are kept
beneath this run's `author-study-0006` artifact directory, with the page
rasters in a replaceable child of their own. This is an author proof
inspection; the shared-timestamp three-document build and the independent
visual review remain the workflow's to obtain.


## The iteration-7 repair

One blocking finding reached this stage from the independent study review,
`STU-016`, against the second reading's gloss on Augustine at the Alleluia in
`sections/30-son-and-lord-of-david.tex`. One advisory came with it, the
standing `STU-006`, which is the research owner's and is untouched.

**`STU-016`: a gloss that dropped the whole of Augustine's distinction.** The
paragraph read: "In the same place he makes a distinction that belongs to this
reading. Christ and the Church are one, *sed Verbum et caro non utrumque unum;
Pater et Verbum utrumque unum*: the Word and the flesh are not one thing, while
the Father and the Word are one." Read plainly, the English half of that denies
the unity of the Incarnation, and it stood in the one reading whose subject is
that Christ is David's son according to the flesh and David's Lord according to
his eternal birth.

The Latin was read again at the locus, in the registered tracked text this leaf
already binds: artifact
`augustine.enarrationes-in-psalmos.latin-migne-corpus-corporum-wikisource-web-2026-09-05.wikisource-part-11-latin-text`,
SHA-256 `8b9dafef805536c0d4551fc427a6b7060fc1655326b0d1e14507b317dfcf711f`
recomputed over the tracked file, which holds Migne's Latin of Psalms CI–CX and
both sermones on Ps 101. Augustine writes, at s. 1, 2: "Jam ergo audiamus quid
oret caput et corpus, sponsus et sponsa, Christus et Ecclesia, utrumque unus:
sed Verbum et caro non utrumque unum; Pater et Verbum utrumque unum; Christus
et Ecclesia utrumque unus, unus quidam vir perfectus in forma plenitudinis
suae", and then quotes Eph 4:13. The antithesis is carried entirely by the
gender of the pronoun: three unions are set side by side and only the middle
one is denied. Christ and the Church are *unus*, masculine — one man. The
Father and the Word are *unum*, neuter — one in substance. The Word and the
flesh are not *unum* in that sense; they are one person, which is why in the
same breath the head can be called *unus* with his body. The study quoted only
the two neuter members, so the *sed* had nothing to turn on, and rendered the
first of them without the qualification the neuter carries.

The repair does both of the things the finding allowed rather than one. The
quotation is restored to Augustine's whole sentence as far as *unus quidam vir
perfectus*, so that the *unus*/*unum* contrast is on the page — the same clause
the first reading already quotes at `sections/20-whole-heart-one-body.tex` — and
the English states the contrast explicitly, since English cannot carry it by
gender: masculine and neuter are named, "one in substance" and "not one
substance" replace the bare "one" and "not one thing", and the personal unity
the Word and the flesh do have is said in the same sentence that denies the
substantial one. The paragraph then says what the distinction is for in this
reading: the one Christ is David's son in the flesh he took and David's Lord in
the substance he has of the Father. No sentence of the study now states without
qualification that the Word and the flesh are not one. The locus is unchanged,
*Enarrationes in Psalmos* 101, s. 1, 2, and no research record was altered to
make the old sentence pass.

**`STU-006`, advisory, not cleared, and why.** It reached this stage again
under `ADVISORY_FINDINGS`. It is unchanged in substance and its owner is
unchanged: `research/interpretations.md` §3 is the research stage's file, and
recording Aquinas there from author-study would be the silent revision of a
reviewed upstream document that the workflow contract forbids. The finding's own
`required_result` says the same. `research/interpretations.md` is byte-identical
to how this dispatch found it, and no record of this leaf states that the repair
has been made. The `STU-016` finding's `required_result` also asks that
`research/interpretations.md` §2.3 carry the clause this reading uses; that half
of it belongs to the same research owner for the same reason, and the §2.3
Alleluia row is likewise untouched. What this stage owns is the study's prose,
and that is repaired.

**Word count.** Measured as the iteration-6 entry measured it, by `pdftotext
-layout` over the settled proof, the study carries 19,357 words against that
proof's 19,247, a net gain of 110. A multiset diff of the two extractions
accounts for it: 121 tokens added and 11 removed, the removals being the
revision timestamp, the eight words of the replaced gloss (`makes`, `belongs`,
`this`, `reading.`, `one,`, `unum:`, `while`, `to`), and the two words `four`
and `senses` that leave a running head as the moved subsection takes its own
head to the next page.

Measured as substantive words — the six argumentative components through
Pandoc's LaTeX AST with headings and tables removed, the leaf's inline commands
declared so that their arguments are counted — this iteration's implementation
counts 13,807 on the pre-repair bytes and 13,918 now, a gain of 111, all of it
in `sections/30-son-and-lord-of-david.tex`; with the content of the `\latin{}`
quotations removed, 12,986 and 13,081, a gain of 95. The header's figures are
restated at these numbers, and the discontinuity from the 13,106 and 12,185 it
carried through iteration 6 is stated there: the implementations differ, and
what changed in the text is the 111 words this repair adds.

**Files touched.** `generation-metadata.tex` (the timestamp and the
author-study contribution), `sections/30-son-and-lord-of-david.tex`, and this
record. No research evidence was changed and no claim was weakened to make
anything pass.


## Author proof and checks at iteration 7

`make doc DOC=liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost PROVIDER=claude`
settles in two passes. Two independent builds, each begun after removing the
PDF, log, auxiliary and contents files, produced an identical PDF, auxiliary
file, contents file and extracted text, so the proof is a cold fixed point.
The final log has no error, no `LaTeX Warning`, no package warning
— the `fancyhdr` `\headheight` warning that the width discipline raises while a
head is too long is absent, which is the mechanical evidence that no head wraps
— no overfull or underfull box, no undefined reference and no rerun request.

The settled proof is
`build/claude/liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost.pdf`,
SHA-256 `a3309c3634f5fa55fcd632c31819b5870854459c1c31054215a4496c58bde3df`, at
the revision timestamp `2026-09-19T06:20:00Z`, which the PDF's own `ModDate`
carries. It is **38 physical pages**, inside the contract's 20–50, letter size,
Palatino (TeX Gyre Pagella) at 11 points on 15-point leading. It supersedes the
iteration-6 proof, SHA-256
`9953a1fb142c938c160cf6b59fbc35430e12fc5e2f1120e0a05f27526bb061ad`, which
remains beneath that iteration's own directory.

The extent is unchanged at 38 pages and one heading moves. The contents file is
no longer byte-identical to iterations 4 through 6: its single changed line is
"The difficulties this confession must carry", which stood at page 24 and now
stands at page 25, because the repaired paragraph is seven printed lines longer
— ten lines before, seventeen now — and pushes that subsection past the break.
Four pages differ in their extracted
text and only four: pages 23 and 24 carry the repaired paragraph, page 25
receives the heading and the text that already followed it, and page 38 the new
timestamp. Nothing before page 23 or after page 25 moved, and the rest of the
auxiliary file's page assignments are unchanged. A cold reviewer holding the
iteration-6 page numbers should read "page 24" for that one subsection as page
25.

Checks run and passing at these bytes, seventeen in all, with the invocations
and their output kept beside the proof: `tools/check-proper-components
--provider claude --document … --phase artifacts --edition research`; `python3
scripts/_proper_study.py check … --date 2026-09-20 --phase content --edition
research --require-presentation`; every `check-content-preflight` check the
study gate names — references-used, identifiers-resolve, bindings-valid,
restricted-not-reproduced, relation-coverage, unquoted-not-quoted,
structural-meta-labels, house-voice, the three chronology checks, and
provenance-matches-run against this run's own header; `check-generation-metadata`;
and `check-web-edition`. A trial `tools/web-edition` run converts the leaf
without loss, and the repaired paragraph survives the conversion intact, Latin
and gloss together.

All 38 pages were rendered and both contact sheets read, with pages 23, 24, 25
and 38 inspected individually — the three that carry changed text and the one
that receives the moved heading. There is no blank page, no heading-only page,
no clipping, collision or missing text, and every running head is a single
line. Page 24 now ends short of the text block, carrying 41 body lines where a
full page of this setting carries 42, because the subsection that follows it
could not be set there; that is the ordinary behaviour of the section guard and
not a defect. Both companions were rebuilt against the changed shared
`generation-metadata.tex` and build cleanly at their unchanged extents, 12 and
5 physical pages; they are the derivation stages' to rewrite against this
study, and nothing here anticipates that work. The proof, its log, auxiliary
file, contents file, extracted text, the check log and their digests are kept
beneath this run's `author-study-0007` artifact directory, with the page
rasters in a replaceable child of their own. This is an author proof
inspection; the shared-timestamp three-document build and the independent
visual review remain the workflow's to obtain.


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

Observations 1, 2 and 3 above were cleared at iteration 2 by the study's own
owner, and their present state is recorded in the next section.

## The concise iteration-2 re-derivation

No blocking finding reached this stage. The run re-entered the study owner
after the artifact gate found the study's accepted review stale, and every
document derived from the study is re-derived when the study is repaired and
re-reviewed; so the companion was read again, whole, against the expansive
study as the author-study iteration-2 pass and its fresh cold review left it.

Four upstream changes were checked against the derived prose.

1. `sections/30-son-and-lord-of-david.tex` now states the Missal's printing of
   the Gradual versicle as facts and names the witnesses, in place of the
   sentence about what the study declined to conclude from the page
   (`STU-004`). The concise commentary's closing clause on the same paragraph
   still carried the older summary form, "the Trinitarian sense of the verse is
   the Fathers' reading of it", and now carries the study's own: "Basil,
   Augustine and Cassiodorus read the Word and the Spirit out of the psalm's
   own words". The three named are the three whom the concise paragraph has
   just quoted reading the verse's own terms; Irenaeus uses it for the rule of
   faith, Aquinas by appropriation and Bellarmine beside the literal sense, and
   none of them is now covered by the sentence.
2. `sections/20-whole-heart-one-body.tex` now places Gregory's parable as the
   one that opens the same chapter of Matthew. The concise copy was repaired at
   iteration 1 for `SYN-003` and already read that way, so the two agree and the
   third upstream observation above is closed.
3. `sections/10-each-element.tex` now locates Ps 118:135 from the antiphon's own
   verse 137 (`STU-007`). The companion does not reprint that verse anywhere,
   and its account of the Introit — verse 137 from the strophe *Sade* joined to
   the first half of verse 124 from *Ain*, with the rest of 124 unsung — is
   unaffected.
4. `sections/80-date-location.tex` now turns the study's terminal dossier
   between dossiers rather than inside one, so the study prints the seven
   dossiers across two pages. The companion's page-2 sheet is a separate,
   compressed component under the profile's one-page rule, and neither it nor
   its dates, relation labels, alternatives or unresolved states change; the
   `format.tex` header records the difference between the two uses. The first
   and second upstream observations above are closed with it: the study's
   record no longer claims a one-page appendix, and the component counts there
   now read nine research and six synthesis components.

The manifest's lane records gained five declared authors at the same pass —
Theodoret of Cyrus, Rupert of Deutz and William Durandus for the second
reading, John Chrysostom and Thomas Aquinas for the third. Nothing in the
companion's own declarations changes, and the witnesses are already used here
where the study uses them: Theodoret at Eph 4:1–6 and again on the three
relations at 4:6, Rupert and Durandus at the Offertory and at the Gospel's
second half, Chrysostom on the lowliness that is the basis of all virtue, and
Aquinas on the confidence that prayer takes from God's mercy.

Two standing advisories against this stage's own files were cleared while in
them. `SYN-007`: the themes section announced "the word ``one''" and then
counted two sites that do not carry *unus* — the Collect reads *te solum Deum*
and the Gospel has no *unus* at all. The habit is now stated for what it is,
the oneness of God, with the Epistle's sevenfold *unus* the only count of a
word, the Collect's *te solum Deum* given as asking that he alone be followed,
and the Gospel's clause left as the identification it always was. `SYN-008`:
"The Offertory is the one element where a disagreement touches the praying
subject himself" claimed a uniqueness the same page refutes, since Augustine
and Cassiodorus divide over whose voice the Alleluia is eight lines above; the
sentence now opens "At the Offertory the disagreement touches the praying
subject himself." Both are editorial slips in derived prose, and neither
touched a source, a locus or a qualification.

**Substantive word count: 4,617 words** (4,241 with the content of the
`\latin{}` quotations removed), over the same two argumentative components,
the themes section and the commentary, counted through Pandoc's LaTeX AST with
comments, headings and page markers removed and the leaf's `\latin` and `\work`
arguments unwrapped, then counted as whitespace-separated plain-text words.
This round's script returns 4,616 (4,241) on the iteration-1 text, which is
exactly what iteration 1 recorded, so the two rounds are directly comparable
and the net gain of this round is one word. The same script gives the study's
six argumentative components 13,645 (12,828) as they now stand and 13,639 on
the text before the study's own iteration-2 repair, matching the six words that
repair reports adding; the companion is therefore a little over a third of the
study's argument, selected and re-integrated. The figure 13,106 recorded for
the study in the author-study section above comes from that stage's own script
and is not comparable with these, exactly as the concise counts of iterations 0
and 1 were not comparable with each other.

Four source files changed at this iteration: `sections/concise/04-themes.tex`,
`sections/concise/10-commentary.tex`, `generation-metadata.tex` for the
revision timestamp and this stage's contribution note, and this record. No
research record, no study component, `format.tex` and `proper-components.toml`
were touched.

## Author proof and checks for the concise companion at iteration 2

`make doc DOC=liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost-synthesis PROVIDER=claude`
settles in two passes and reproduces the same PDF bytes exactly from a removed
auxiliary file. The final log carries no overfull or underfull box, no warning,
no undefined reference and no rerun request. The PDF has 12 physical pages,
inside the 10–12-page requirement; all nine font resources are embedded,
subsetted and Unicode-mapped; the document info carries the title, the subject
and the tracked ModDate with no build-derived CreationDate; and the extracted
text of all twelve pages carries no replacement character.

The settled auxiliary file is byte-identical with iteration 1's, so no fixed
position moved: inventory and overview markers and the four sense markers on
physical page 1, chronology start and end on page 2, themes start on page 3 and
end on page 4, commentary start on page 5.

`tools/check-proper-components --provider claude --document … --phase artifacts
--edition synthesis` passes, as do `python3 scripts/_proper_study.py check …
--phase content --edition synthesis --require-presentation` and every
`check-content-preflight` check the synthesis gate names for this edition:
references-used (24 entries, every one used), identifiers-resolve,
bindings-valid (71 bindings), restricted-not-reproduced (4 restricted, none
reproduced), relation-coverage, unquoted-not-quoted, structural-meta-labels,
house-voice, the three chronology checks and provenance-matches-run against
this run's own header.

The settled proof is
`build/claude/liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost-synthesis.pdf`,
SHA-256 `f8ed7b84cafc0ab7cb481d77578225572d2a48ca00bbf1ebdd7ca87a186baf43`, at
the revision timestamp `2026-09-19T01:30:00Z`; its log is
`deea66d2b48df3728240aa5a4a69e75d37064fe0b56f974eaa56a27bda6b746e`, its
auxiliary file `e2b03c30c57490b09cd3bc26227ace328d7a8d5434998e9c61caf119094028ed`
and its extracted text
`42972fde632a5ae588a628f67f8700a6a0436ce96d84641b78e5d0514cec35a1`. Copies of
all four, with their digests, are kept beneath this stage's own artifact
directory in the run, with the page rasters, thumbnails and contact sheet in a
child of their own. The other two documents were rebuilt at the same shared
timestamp and are unchanged in extent: the expansive study at 38 pages, SHA-256
`9811ae13b5db505b5a75b3cea86dcf2de307408f7033b32513d920cac1743e15`, and the
homily at 5 pages, SHA-256
`57ece8ccdab03ebd61a9fc5a0acbccfc6cfc9af7cb2a3bdb702df8d1aa63933a`.

The author read the contact sheet of all twelve pages and the individual
rasters of the two pages the repairs touched, pages 4 and 8, and of the final
page, and read the extracted text of all twelve. The proof shows no clipping,
collision, missing text, blank page or heading-only page; the map and the four
overview rows rule to the same measure on page 1; the dossier stands whole on
page 2; the themes section fills pages 3 and 4 and ends there; and the revision
timestamp and the rights colophon share the last page with the end of the
References. This is an author proof inspection, not the independent visual
evaluation, which follows the shared-timestamp three-document build.

## The concise iteration-3 re-derivation

Re-derived 19 September 2026 in `proper-study` v3, run `1e02dc05f2df9940`,
seeded at commit `72616eb9cc25c7ea7cc061c0e82efffc8b5ea882`, at iteration 3.
No blocking finding reached this stage: `PRIOR_FINDINGS`, `CARRIED_FINDINGS`
and `ADVISORY_FINDINGS` were all empty, so no `finding_dispositions` are
reported. The stage ran again because the study review at iteration 2 sent the
run back into `author-study`, which repaired the expansive study through five
further rounds (iterations 3 to 7) before its cold review passed; every
document derived from the study is re-derived when the study is repaired.

The study's own records did not move. `propers/verified.md`,
`research/scope.md`, `research/interpretations.md`, `research/context.md`,
`research/chronology.toml`, `research/chronology-annotations.tex` and
`research/source-bindings.toml` carry the same digests at iteration 7 that they
carried at iteration 2, so nothing this companion rests on was re-evidenced.
What changed is the study's prose, and four of those changes reach the derived
argument.

1. **Chrysostom on ``like to this''** (`sections/20-whole-heart-one-body.tex`,
   the study's `STU-009`). The study had given both clauses of ``Because this
   makes the way for that, and by it is again established'' to the love of
   neighbour; re-read at the registered locus, both clauses speak of the
   *second* commandment, and the study's closing comparison now reads ``mutual
   dependence in both directions''. The companion had quoted the sentence
   without glossing it and had summarized the mechanism as ``mutual
   establishment''. The commentary now carries the study's gloss — the love of
   neighbour opens the road to the love of God, and the love of God in its turn
   re-establishes the love of neighbour — and the summary reads ``mutual
   dependence in both directions''.
2. **The Postcommunion in the second reading**
   (`sections/30-son-and-lord-of-david.tex` and `sections/50-comparison.tex`,
   the study's `STU-010` and `STU-012`). The study withdrew the bare assertion
   that the prayer's *sanctificationes* name a holiness God's own and given in
   the sacrament, and its comparison now says outright that the Postcommunion
   gives that reading nothing of its own. The companion still listed the
   Postcommunion as the third of the three orations that reading hears as
   confession, which the accepted study now contradicts. The commentary now
   names two of the three prayers as its confession and states the disclaimer
   with the study's own three grounds.
3. **Augustine's three unions at the Alleluia**
   (`sections/30-son-and-lord-of-david.tex`, the study's `STU-016`). The study
   restored the masculine member of Augustine's sentence and states in English
   what the gender of his pronoun carries, because that distinction is what the
   second reading needs. The companion's Alleluia paragraph never carried the
   defective gloss, so nothing there was false; it now carries the distinction
   itself, compressed to one sentence, and the conclusion the study draws from
   it.
4. **Ps 109 given its Hebrew number** (`sections/05-appointed-texts.tex`, the
   study's `STU-014`). The study's convention, which the 1962 profile requires,
   is the Missal's numbering with the modern number in parentheses at first
   use. The companion's first use of Ps 109 is in the themes section and was
   bare; it now reads Ps 109:1 (Heb. 110:1).

Three further study repairs of these rounds do not reach the companion and were
checked rather than copied: the running-head geometry and the short running
forms of `format.tex` (`VIS-001`, `VIS-002`), which this document inherits and
which its own heads already satisfy; the citation of the general rubrics in
longhand at the second reading's Postcommunion (`STU-015`), a passage the
companion does not reproduce; and the References note on the NPNF1 10 editor's
``Ps. liii. 1'' (`STU-011`), which belongs to a quotation the companion does not
print.

The six advisories the cold review of iteration 2 left standing against this
document (`SYN-009` to `SYN-014`) were not forwarded in this packet and are owed
no disposition, and all six are cleared while in these files.

- `SYN-009`: the scope note's text-control sentence now carries the study's own
  bound, every Latin form **of the ten proper elements**; the reception
  paragraph discloses that Bellarmine's O'Sullivan English was read in a tracked
  web transcription and not on the 1866 printing, and that some Latin was read
  in web deliveries of the standard editions (augustinus.it, monumenta.ch, the
  Corpus Thomisticum) or in optical text layers of printings (Rupert, Durandus,
  Guéranger, Irenaeus, Trent); the References entry for Augustine's
  *Enarrationes* divides the Migne text from the two loci read at augustinus.it,
  and the Bellarmine entry names the transcription.
- `SYN-010`: the Offertory row's ``Its grounds'' is gone; the place and hearers
  in the Location column are now stated to be the article's grounds for the
  traditional position, so nothing supplies a place to the critical theory the
  preceding clause says carries none.
- `SYN-011`: the Gospel row gives Jerome only what the article gives him and
  assigns the departure from Jerusalem to the article itself.
- `SYN-012`: the themes section names the change Guéranger's report depends on,
  the moving of the Luke 14 Gospel eight days earlier and the present Gospel's
  taking its place, instead of pointing back to the variant practice Durandus
  records.
- `SYN-013`: the commentary no longer lets Chrysostom's account of the lawyer's
  motive stand alone; Jerome's reason, that every commandment of God is great so
  that any answer could be attacked, stands beside it, and the study's sixth
  narrow disagreement survives compression.
- `SYN-014`: the Alleluia row of the page-one map carries its Latin incipit,
  *Domine, exaudi*, as the other chants and orations do and as the study's map
  has it.

No new evidence-dependent claim was added. Every sentence added here states what
the accepted study states at the same loci, and no research record, no study
component, `format.tex`, `proper-components.toml` and `web-edition.toml` were
touched. No upstream defect was found in this pass, and none is reported for the
cold reviewer.

**The additions were paid for in the same components.** The opening four pages
are fixed by the presentation contract and the finished PDF must stay inside
10–12 physical pages; the iteration-2 document held 12 with almost no slack, and
the additions above first carried it to 14. Rather than drop them, the derived
prose was tightened by about the same amount, in places where the compression
costs no attribution, no locus, no disagreement and no qualification: Augustine's
threefold ``whole'' is named rather than quoted a second time at *De doctrina*
I.22.20–21; Jerome's answer to the reading that applied Ps 109 to Abraham, the
footstool clause of Chrysostom's counter-question, Chrysostom's image of the fire
and the wet timber, the second of Bellarmine's two sentences on the Gradual
versicle, Hilary's extension of *iustus es, domine* into a rule for affliction,
and Durandus's promise of exaltation in paradise are dropped; Theodoret on
lowliness, Augustine on Daniel's own sins, the Trent *antidotum* clause, and the
scope note's paragraph on the relation to the expansive study are shortened; and
the echo of Aquinas's beatitude in the closing subsection, which the Gradual
subsection already states with its locus, is removed. Every witness the
iteration-2 document named is still named, at the same loci, and all six of the
study's narrow disagreements are still here.

**Substantive word count: 4,585 words** (4,218 with the content of the
`\latin{}` quotations removed), over the two argumentative components, the
themes section and the commentary, counted through Pandoc's LaTeX AST with
comments, headings and page markers removed and the leaf's `\latin` and `\work`
arguments unwrapped, then counted as whitespace-separated plain-text words. The
same script gives the study's six argumentative components 14,024 (13,187) as
they now stand, so the companion remains a little under a third of the study's
argument, selected and re-integrated. As at every earlier round, this round's
implementation of that description does not reproduce the absolute figures of
the rounds before it — iteration 2 recorded 4,617 (4,241) from its own script —
so the absolute is comparable only within this round. The measure that is
directly comparable across the two rounds is the retained extraction of the two
settled PDFs by the same `pdftotext -layout`: 7,409 words at iteration 2 and
7,436 now, a net gain of 27, a multiset diff accounting for 234 tokens added and
207 removed with nothing over. That near-cancellation is why the document holds
at twelve pages.

Six source files changed at this iteration: `sections/concise/01-inventory.tex`,
`sections/concise/03-date-location.tex`, `sections/concise/04-themes.tex`,
`sections/concise/10-commentary.tex`, `sections/concise/90-apparatus.tex`, and
`generation-metadata.tex` for the shared revision timestamp and this stage's
contribution note, now covering iterations 0, 1, 2 and 3; this record is the
seventh.

## Author proof and checks for the concise companion at iteration 3

`make doc DOC=liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost-synthesis PROVIDER=claude`
settles in two passes, and a cold build begun after removing the PDF, log and
auxiliary file reproduced all three byte for byte, so the proof is a fixed
point. The final log carries no overfull or underfull box, no error, no LaTeX
or package warning, no undefined reference and no rerun request. The PDF has 12
physical pages, inside the 10–12-page requirement; all nine font resources are
embedded, subsetted and Unicode-mapped; the document info carries the title, the
subject and the tracked ModDate (`2026-09-19T07:10:00Z`) with no build-derived
CreationDate; and the extracted text of all twelve pages carries no replacement
character.

The settled auxiliary file is byte-identical with those of iterations 1 and 2,
so no fixed position moved: the inventory and overview markers and the four
sense markers stand on physical page 1, chronology start and end on page 2,
themes start on page 3 and end on page 4, and commentary start on page 5.

`tools/check-proper-components --provider claude --document … --phase artifacts
--edition synthesis` passes, and so do the same check for the research and
homily editions, `python3 scripts/_proper_study.py check … --phase content
--edition synthesis --require-presentation`, `tools/check-generation-metadata`,
`tools/check-web-edition`, and every `check-content-preflight` check the
synthesis gate names for this edition: references-used (24 entries, every one
used in the body), identifiers-resolve, bindings-valid (71 bindings),
restricted-not-reproduced (71 bound sources, 4 restricted, none reproduced),
relation-coverage, unquoted-not-quoted, structural-meta-labels, house-voice, the
three chronology checks, and provenance-matches-run against this run's own
header.

The settled proof is
`build/claude/liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost-synthesis.pdf`,
SHA-256 `fb8b658208658f24c0980e36b04441a88ef25ac0c68aa39d66feceb5329aa5b0`; its
log is `c78d03f3ae18685ff9b5d53aad5e8e996deb8d3a76f21a3ff07300f01d210d7d`, its
auxiliary file `e2b03c30c57490b09cd3bc26227ace328d7a8d5434998e9c61caf119094028ed`
and its extracted text
`fde6a7529c784d8661cd0d1aaba093624682eb4328be03ba0f3cf90acb8df6f4`. Copies of
all four, with their digests in `proof-hashes.txt`, are kept beneath this
stage's own artifact directory in the run, with the page rasters, thumbnails and
contact sheet in a child of their own, because the raster helper replaces its
destination. The other two documents were rebuilt at the same shared timestamp
and are unchanged in extent: the expansive study at 38 pages, SHA-256
`4d6f0aa5b447ce84aafaa5870b55dd720c0c7947f913cf524150ee99c21454f0`, and the
homily at 5 pages, SHA-256
`c6b93ca11ad58c0337e291202d30434d39c09778a329072e665bbf554ea573de`; both logs
are clean.

The author read the contact sheet of all twelve pages, the individual rasters of
pages 1, 2, 8 and 12, and the extracted text of all twelve. The proof shows no
clipping, collision, missing text, blank page or heading-only page; the map and
the four overview rows rule to the same measure on page 1, with the Alleluia row
now carrying its incipit in the same column as the rest; the dossier stands
whole on page 2; the themes section fills pages 3 and 4 and ends there; and the
revision timestamp and the rights colophon share the last page with the end of
the References. This is an author proof inspection, not the independent visual
evaluation, which follows the shared-timestamp three-document build.

## The concise iteration-4 repair

Repaired 19 September 2026 in `proper-study` v3, run `1e02dc05f2df9940`,
seeded at commit `72616eb9cc25c7ea7cc061c0e82efffc8b5ea882`, at iteration 4.
One blocking finding was forwarded, `SYN-015`, and it is repaired.
`CARRIED_FINDINGS` was empty. Four advisories came with it under
`ADVISORY_FINDINGS`; they gate nothing and are owed no disposition, and all
four are cleared while in these files.

**`SYN-015` (blocking, repaired).** The themes section opened its account of the
Introit with "in two half-verses of the long alphabetical psalm on God's law".
The antiphon is not two half-verses. The collation at marginal no. 1602 records
its construction as "Verse 137 entire, then the first half of v. 124 only; the
second half (*et iustificationes tuas doce me*) is not sung", and the expansive
study says the same ("Its antiphon joins two verses from different strophes",
`sections/10-each-element.tex`). The sentence was also contradicted by the
clause that immediately followed it in the same paragraph, which already
distinguished verse 137 from the first half of verse 124, so the paragraph did
not agree with itself. It now reads "in one whole verse of the long alphabetical
psalm on God's law and in the first half of another", which is what the
collation and the study give; the following clause is unchanged except that
"the words that complete verse 124" now reads "the words that complete it",
since the verse has just been named. No evidence was re-derived: the repair
states what `propers/verified.md` and the accepted study already state.

The four advisories:

- `SYN-016`: the Hilary and Augustine disagreement at the Introit. The expansive
  study frames it with two clauses the compression had dropped — that Hilary
  wrote "before the controversy with the Pelagians" and that "Augustine's
  account is the one on which the priority of grace rests"
  (`sections/40-just-judge-merciful-hearer.tex`), which are the two controls
  `research/scope.md` §4.11 places on this pair. The advisory asks for one of
  them; the historical one is carried, so the commentary now reads "Hilary,
  writing before the controversy with the Pelagians, says *ex nobis autem
  initium est, ut illa perficiat*, where Augustine gives the whole of it to
  God". Both witnesses were already kept and Hilary was already not cited for
  Augustine's point, so the scope record's binding instruction was met before
  and is met now with the frame the study gives it.
- `SYN-017`: "Chrysostom reads them instead of the one God and Father" could be
  read as saying that he reads the three phrases in place of the one God and
  Father, which is the reverse of what he does. The word order is changed to
  "Chrysostom instead reads them of the one God and Father", the idiom the study
  uses of the Greek commentators, so that "instead" governs the verb and cannot
  reach the one God and Father. This is the place `research/interpretations.md`
  §2.5 warns must not credit Chrysostom with the distribution among the Persons.
- `SYN-018`: the note under the page-one map read "it has the one oration above
  and admits no optional text", which appeared to deny the three orations the
  map prints directly above it. The rubrical sense intended is in the study
  alone, that the Sunday takes the commemoration of no other feast
  (`sections/00-opening.tex`). The note now says what it means: "it says one set
  of orations and admits no commemoration".
- `SYN-019`: the Gradual's "What it says" cell dropped the first half of the
  respond and left the beatitude resting on the choosing alone. It now reads
  "Blessed the nation whose God is the Lord, the people he chose for his
  inheritance", as the study's own map has it — the half of Ps 32:12 that
  Augustine's *Hoc ama, hoc posside* and Cassiodorus's inheritance won by blood
  are both expounding on page 9.

**The additions were paid for in the same components.** Page one is fixed by the
presentation contract, and the map, the note and the four overview rows must all
stand on it; the finished PDF must also stay inside 10–12 physical pages, and
the iteration-3 document held 12 with the same slack it has held since
iteration 1. The Gradual's restored half-verse took a third line in its cell and
pushed the whole overview table to page 2, and the two additions in the
commentary carried the rights colophon on to a thirteenth page. Two compensating
compressions were made, in places where they cost no attribution, no locus, no
disagreement and no qualification. The Secret's summary in the map, "That the
holy things we do may strip us of past sins and of future ones", now reads "That
the holy things we do strip us of past and future sins" and fits one line; the
themes section states that petition in full, with its *exuant*, two pages later.
And the commentary's clause "and it prints them against their own order in the
psalm", at the head of the Gradual subsection, is dropped: the themes section
already states the inversion in full, with both verse numbers and what it
achieves, on page 4. With those two, page one holds and the document holds at
twelve.

**Substantive word count: 4,588 words** (4,222 with the content of the
`\latin{}` quotations removed), over the two argumentative components, the
themes section and the commentary, counted through Pandoc's LaTeX AST with
comments, headings and page markers removed and the leaf's `\latin` and `\work`
arguments unwrapped, then counted as whitespace-separated plain-text words. The
same script gives the study's six argumentative components 14,024 (13,187),
reproducing iteration 3's figure for the study exactly, so this round's counts
are directly comparable with that round's: the companion moved from 4,585
(4,218) to 4,588 (4,222), and remains a little under a third of the study's
argument. The retained `pdftotext -layout` extractions of the two settled PDFs
agree: 7,436 words at iteration 3 and 7,441 now, a net gain of 5, a multiset
diff accounting for 32 tokens added and 27 removed with nothing over.

No new evidence-dependent claim was added; every sentence changed here states
what the accepted study and the collation state at the same loci. No research
record, no study component, `format.tex`, `proper-components.toml` and
`web-edition.toml` were touched, and no upstream defect was found in this pass,
so none is reported for the cold reviewer. Four source files changed at this
iteration: `sections/concise/01-inventory.tex`,
`sections/concise/04-themes.tex`, `sections/concise/10-commentary.tex`, and
`generation-metadata.tex` for the shared revision timestamp, now
`2026-09-19T08:05:00Z`, and this stage's contribution note, now covering
iterations 0, 1, 2, 3 and 4; this record is the ninth.

## Author proof and checks for the concise companion at iteration 4

`make doc DOC=liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost-synthesis PROVIDER=claude`
settles in two passes, and a cold build begun after removing the PDF, log and
auxiliary file reproduced all three byte for byte, so the proof is a fixed
point. The final log carries no overfull or underfull box, no error, no LaTeX or
package warning, no undefined reference and no rerun request. The PDF has 12
physical pages, inside the 10–12-page requirement; all nine font resources are
embedded, subsetted and Unicode-mapped; the document info carries the title, the
subject and the tracked ModDate (`2026-09-19T08:05:00Z`) with no build-derived
CreationDate; and the extracted text of all twelve pages carries no replacement
character.

The settled auxiliary file is byte-identical with those of iterations 1, 2 and
3, so no fixed position moved: the inventory and overview markers and the four
sense markers stand on physical page 1, chronology start and end on page 2,
themes start on page 3 and end on page 4, and commentary start on page 5.

`tools/check-proper-components --provider claude --document … --phase artifacts
--edition synthesis` passes, and so do the same check for the research and
homily editions, `python3 scripts/_proper_study.py check … --phase content
--edition synthesis --require-presentation`, `tools/check-generation-metadata`,
`tools/check-web-edition`, and every `check-content-preflight` check the
synthesis gate names for this edition: references-used (24 entries, every one
used in the body), identifiers-resolve, bindings-valid (71 bindings),
restricted-not-reproduced (71 bound sources, 4 restricted, none reproduced),
relation-coverage, unquoted-not-quoted, structural-meta-labels, house-voice, the
three chronology checks, and provenance-matches-run against this run's own
header.

The settled proof is
`build/claude/liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost-synthesis.pdf`,
SHA-256 `3043a98c4d0cae5e0447e0b133412d051acde2f22065963b8632ee685dca5520`; its
log is `379c07d78401fdf71cff278f35a1d06a907b11e7bee99a7c84772767e8a6b52a`, its
auxiliary file `e2b03c30c57490b09cd3bc26227ace328d7a8d5434998e9c61caf119094028ed`
and its extracted text
`4fe2813a273f8ddcf5da641c950d41237492a4cf057ed1cdc2abe4781d00ae46`. Copies of
all four, with their digests in `proof-hashes.txt`, are kept beneath this
stage's own artifact directory in the run, with the page rasters, thumbnails and
contact sheet in a child of their own, because the raster helper replaces its
destination. The other two documents were rebuilt at the same shared timestamp
and are unchanged in extent: the expansive study at 38 pages, SHA-256
`c2270bfdc23091a5da5137fe3f09ca78223cbddeb448260fdcf9af9fceaba372`, and the
homily at 5 pages, SHA-256
`6ae7edc4b53c380f3a49b9ba70953577e4b30035fd8c242fdabaec6b46de019d`; both logs
are clean.

The author read the contact sheet of all twelve pages, the individual rasters of
pages 1, 3, 9 and 12, and the extracted text of all twelve. The proof shows no
clipping, collision, missing text, blank page or heading-only page; the map and
the four overview rows rule to the same measure on page 1, with the Gradual's
cell now running to three lines and the Secret's to one; the dossier stands
whole on page 2; the themes section fills pages 3 and 4 and ends there; the
repaired sentence on the Introit stands at the head of the second paragraph of
page 3; and the revision timestamp and the rights colophon share the last page
with the end of the References. This is an author proof inspection, not the
independent visual evaluation, which follows the shared-timestamp
three-document build.

## Derive-homily

Authored 18 September 2026 in `proper-study` v3, run `1e02dc05f2df9940`, seeded
at commit `72616eb9cc25c7ea7cc061c0e82efffc8b5ea882`, at iteration 0,
repaired at iterations 1, 2 and 3 of the same run and seed, and re-derived at
iteration 4 after the two studies were re-authored and reviewed again, as the
iteration-4 entry below records. The
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

## The homily iteration-4 re-derivation

No blocking finding reached this stage and none was carried. The homily was
re-entered because the two documents it derives from moved. The artifact gate
found the expansive study's accepted review stale against its current bytes;
the study was re-authored at its own iteration 2 and passed a fresh cold
review, the concise companion was re-derived at its iteration 2 and passed its
own, and the run then returned here. Of the seven review inputs the homily's
accepted review sealed, exactly one had changed: the shared `format.tex`,
which the study stage adopted with two comment blocks added and no typesetting
instruction altered, so nothing in this document's setting moved.

Both studies were read again as they now stand and the speech was checked
against them clause by clause. None of what the re-authoring changed reaches
this speech. `sections/10-each-element.tex` now locates Ps 118:135 from the
antiphon's own verse 137; `sections/20-whole-heart-one-body.tex` places
Gregory's parable in the same chapter of Matthew without asserting that it
stands immediately before this Gospel; `sections/30-son-and-lord-of-david.tex`
states the Missal's two printings of the Gradual versicle as facts and rests
the Trinitarian reading on Basil, Augustine and Cassiodorus rather than on the
page; `sections/80-date-location.tex` turns its dossier sheet between
dossiers; and `sections/concise/04-themes.tex` and
`sections/concise/10-commentary.tex` carry the same corrections into the
companion. The speech uses Gregory nowhere, the Gradual nowhere, the Alleluia
nowhere, Ps 118:135 nowhere and the chronology nowhere. The two enlarged lane
author lists in `proper-components.toml` add no author the speech attributes.

Each passage the speech attributes was re-read at this iteration in the
tracked source behind it, not taken from the studies' report of it:
Augustine's "no part of our life is to be unoccupied" and the one channel of
the affections in the CCEL text of NPNF1 2 at the paragraph the passage record
`…de-doctrina-christiana.ccel-web-2026-09-17.i-22-20-21` bounds; Chrysostom's
"this makes the way for that, and by it is again established", "not to the
rejection of the Son, but to make the distinction from idols" and "to confess
Him also to be God" in the CCEL text of NPNF1 10 within the lines the passage
record for homily 71 bounds, where the third stands in the sentence "Therefore,
after so many things, He asks these questions, secretly leading them on to
confess Him also to be God"; Augustine's `Respondeamus omnino quod Judaei, sed
non remaneamus ubi Judaei` and the form of God and form of a servant in the
tracked Migne text of the *Enarrationes*, part 11; and Jerome's `Peccata
populi, quia unus e populo est, enumerat ex persona sua` in the tracked
Wikisource text of PL 25 at Dan 9:5. The six appointed elements the speech
quotes — Gospel, Epistle, Collect, Introit, Communion, Postcommunion — were
re-read against `sections/05-appointed-texts.tex` and agree with it word for
word, and the Offertory is still described and not translated.

The spoken body is therefore unchanged. Its file is byte-identical to the one
the cold reviewer read at iteration 3, and so is the homily's auxiliary file:
no line of the speech, no page break and no reference moved. A re-derivation
that finds nothing to change in the speech is the honest outcome when nothing
the speech uses has changed upstream, and it is reported as that rather than
dressed as a revision.

`HOM-001`, the advisory left standing by the iteration-3 review, was cleared
while this stage was in the terminal note. The References cited Augustine's
Latin as "Latin text of Migne, PL 37" and Jerome's as "(Migne, PL 25,
678--681)", either of which a reader could take for a reading of the printed
columns; the leaf's records say otherwise, binding the Augustine to
`artifact.augustine.enarrationes-in-psalmos.latin-migne-corpus-corporum-wikisource-web-2026-09-05.wikisource-part-11-latin-text`
and the Jerome to
`artifact.jerome.commentaria-in-danielem.migne-pl-25-wikisource-1845.latin-text-3fe4ba4f`,
and `research/scope.md` records the second as "tracked Wikisource Latin of
PL 25". The two entries now name their deliveries, the Augustine in the form
the expansive study's own References already use ("Latin text of Migne, PL
36--37 (Wikisource and Corpus Corporum)"), and the route paragraph states the
same thing once in prose. That paragraph's run-in label, which read "English
quoted, and its route" while the paragraph also accounted for Latin, now reads
"Texts quoted, and their route".

Two source files changed at this iteration, `sections/homily/90-note.tex` and
`generation-metadata.tex` for the shared revision timestamp and the
contribution note; this record is the third. The spoken word count stands at
1,429 words, unchanged, counted again by the method recorded above, so the
note's pace estimate of eleven to twelve minutes at 120 to 130 words a minute
is untouched. The presentation values are unchanged at 12.5 points on
17-point leading with 0.6em between paragraphs, and nothing in `format.tex`
was edited here.

The proof of this iteration is
`build/claude/liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost-homily.pdf`,
SHA-256 `65ddd79b4a6d37f96687a14a3f5ae27b7f9b01acacc227dbae896f66585a2c31`, at
the revision timestamp `2026-09-19T02:20:00Z`, five physical pages, letter
size, settling in two passes. Deleting the PDF, the auxiliary file and the log
and building again reproduced those exact bytes. The final log carries no
overfull or underfull box, no warning, no undefined reference and no rerun
request. The six font resources are embedded, subsetted and Unicode-mapped;
the document info carries the title, the subject and the tracked `ModDate`
with no build-derived `CreationDate`. `tools/tpt check-content-preflight`
passes for the homily edition on every check the gate names — references-used
(seven entries, every one used in the body), identifiers-resolve,
bindings-valid (71 bindings), restricted-not-reproduced (four restricted, none
reproduced), relation-coverage, unquoted-not-quoted, structural-meta-labels,
house-voice, the three chronology checks and provenance-matches-run against
this run's own header — as do `tools/check-proper-components --phase artifacts
--edition homily`, `check-generation-metadata` and
`python3 scripts/_proper_study.py check … --phase content --edition homily
--require-presentation`.

The author read the contact sheet and the individual rasters of all five pages
and the extracted text of all five. The speech occupies pages 1 to 3 and ends
at the foot of page 3; the Collect paragraph turns between pages 2 and 3,
leaving two lines at the foot of page 2 as before; the note stands whole on
page 4, three lines longer than it was; and the References, the revision
timestamp and the rights colophon share page 5, the `\Needspace` guard still
holding the seven entries together. No clipping, collision, missing text,
blank page or heading-only page, and no paragraph broken with a single line
stranded. This is an author proof inspection and not the independent visual
evaluation.

The two studies were rebuilt at the same shared timestamp and are unchanged in
extent at 38 and 12 physical pages: SHA-256
`0edcc07c76da6c29affb30dfad7431d166f370e4b450818ea66336276bed2967`
(expansive) and
`689f6e31fa5fe237711ccf3759ba4f24d92be6381aebccb7f015bb238fa0638a`
(concise). Each differs from the proof its cold reviewer read in one line
only, the printed `Last revised (UTC)` colophon, and both auxiliary files are
byte-identical to those proofs', so no reference, page break or table width
moved. The concise study's settled auxiliary file still records inventory and
overview with all four sense markers on physical page 1, chronology on 2,
themes from 3 to 4 and commentary beginning on 5. The homily proof, its log,
auxiliary file, extracted text and their digests are kept beneath this stage's
own artifact directory in the run, with the page rasters in a child of their
own. The `Build artifacts` section below records the earlier build-artifacts
stage, whose three PDFs and shared timestamp this iteration supersedes.

No upstream defect was found while re-deriving, and none was silently
repaired. Nothing outside `sections/homily/90-note.tex`,
`generation-metadata.tex` and this record was edited at this iteration.

## The homily iteration-5 re-derivation

No blocking finding reached this stage and none was carried. One advisory,
`HOM-009`, stood from the iteration-4 review. The homily was re-entered
because the two documents it derives from moved again, and moved much further
this time than last. The independent visual review of the three built
artifacts returned `CHANGES_REQUIRED` with two blocking findings, both against
the running matter of the expansive study and both owned by it; the study was
re-authored through its iterations 3, 4, 5, 6 and 7, passing a fresh cold
review at the last; the concise companion was then re-derived at its
iterations 3 and 4 and passed its own; and the run returned here.

Of the seven review inputs the homily's accepted review sealed, one had
changed. `research/interpretations.md`, `research/scope.md`, `homily.tex`,
`sections/homily/10-homily.tex`, `sections/homily/90-note.tex` and
`src/common/preamble.tex` were all byte-identical to the versions that review
read. The shared `format.tex` was not, moving from
`8679a274a48192f9c17c24eb88ce72f88cdae76183b38e590431e37804822b6a` to
`afe32aae071025c30d42a0f981c4b7a7ee62412aa1872c44ba3ca6bfb261e960`.

What the study did to that file is the repair of its two visual findings: the
right running head is now bounded to what the fixed left string and a gutter
leave of the head width, so an overlong string wraps inside its own box
instead of printing silently over its neighbour, and a section whose title is
too wide declares a short running form through a new leaf-local
`\runninghead`. Neither reaches this document's setting. The homily overrides
`\fancyhead[R]` with the single word *Homily* after it inputs the shared file,
so the new bounded box governs the study and the concise companion and not
this speech; the left head resolves the same string it resolved before; and no
type size, leading, measure, margin or environment the homily uses was
touched. The proof confirms it: the auxiliary file of this build is
byte-identical to the one the iteration-4 proof produced, so not a line, a
page break or a reference moved.

Both studies were then read again as they now stand and the speech was checked
against them clause by clause. Four changes of the study's own argument were
followed into this speech, and none of them reaches it. The direction of
Chrysostom's reciprocity between the two commandments is now stated with both
clauses of his sentence spoken of the second commandment, which is what the
spoken body already said and still says. The psalm locus of the third of his
four alternating proof texts was corrected to Ps 13:1 (Heb. 14:1); the speech
cites none of the four. Augustine's three unions at the Alleluia are now
quoted whole and glossed by the gender of his pronoun; the speech uses the
Alleluia nowhere. And the second reading no longer hears the Postcommunion as
one of its confessions, saying instead that the prayer gives that reading
nothing of its own; the speech takes the Postcommunion as the healing the
first and the third readings develop, and closes on the first reading's own
anagogical distillation, where the `remedia aeterna` look to the one hope of
the calling, so the change confirms the speech's use rather than unsettling
it. The smaller corrections — Gregory's parable placed in Matthew 22, Ps
118:135 located from verse 137, the Introit row's shorter verse reference, the
dossier sheet's turn before the Gospel, the disclosed delivery of Bellarmine's
English — touch texts and witnesses the speech does not use.

Each passage the speech attributes was re-read at this iteration in the
tracked source behind it, and not taken from either study's report of it:
Augustine's "no part of our life is to be unoccupied" and the one channel of
the affections in the CCEL text of NPNF1 2 at the paragraph the passage record
`…de-doctrina-christiana.ccel-web-2026-09-17.i-22-20-21` bounds; Chrysostom's
"this makes the way for that, and by it is again established", "not to the
rejection of the Son, but to make the distinction from idols" and "to confess
Him also to be God" in the CCEL text of NPNF1 10 within the lines the passage
record for homily 71 bounds; Augustine's `sed non remaneamus ubi Judaei` and
the form of God and the form of a servant in the tracked Migne text of the
*Enarrationes*, part 11; and Jerome's `Peccata populi, quia unus e populo est,
enumerat ex persona sua` in the tracked Wikisource text of PL 25 at Dan 9:5.
The six appointed elements the speech quotes — Gospel, Epistle, Collect,
Introit, Communion, Postcommunion — were re-read against
`sections/05-appointed-texts.tex` and agree with it word for word, and the
Offertory is still described and not translated.

The spoken body is therefore unchanged in every word, and its file differs
from the one the cold reviewer read at iteration 4 only in its header comment.
That comment is the clearing of `HOM-009`. It said the file's vertical spaces
marked "the four movements", where the four spaces divide the speech into
five blocks and this record's own iteration-2 and iteration-3 entries number
them that way, placing the Collect paragraph in the fourth movement and the
Postcommunion sentence in the fifth. The comment now counts five and names
each, so a reader navigating the file by movement number meets the same count
the audit uses.

One line of the terminal note changed. The note named the second reviewed
reading *David's son and David's Lord*, where the section's title is *David's
Son and David's Lord: The One God Confessed in His Word and Spirit* and the
note gives the first and the third readings their titles whole. The short form
was tolerable while it was only a shortening; it is not now, because the study
has declared exactly that string as the section's running form, distinct from
its title, so the note was printing a running head as though it were a title.
The note now gives all three readings their whole titles.

The spoken word count stands at 1,429 words, unchanged, counted again by the
method recorded above, so the note's pace estimate of eleven to twelve minutes
at 120 to 130 words a minute and just under thirteen at 110 is untouched. No
delivery was timed and none is claimed; the prose was read through in full for
sense and ease of speech, silently. The presentation values are unchanged at
12.5 points on 17-point leading with 0.6em between paragraphs, and nothing in
`format.tex` was edited here — the study owns that file, and an edit to it
from this stage would reopen two accepted reviews.

The proof of this iteration is
`build/claude/liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost-homily.pdf`,
SHA-256 `923fb4936d107d3dec13fc6cf1b7a9197aed5dbb1ef19ae20cc5bb8f2d2fb289`, at
the revision timestamp `2026-09-19T08:10:00Z`, five physical pages, letter
size, settling in two passes. Deleting the PDF, the auxiliary file and the log
and building again reproduced those exact bytes. The final log carries no
overfull or underfull box, no warning, no undefined reference and no rerun
request. The six font resources are embedded, subsetted and Unicode-mapped;
the document info carries the title, the subject and the tracked `ModDate`
with no build-derived `CreationDate`. `tools/tpt check-content-preflight`
passes for the homily edition on every check the gate names — references-used
(seven entries, every one used in the body), identifiers-resolve,
bindings-valid (71 bindings), restricted-not-reproduced (four restricted, none
reproduced), relation-coverage, unquoted-not-quoted, structural-meta-labels,
house-voice, the three chronology checks and provenance-matches-run against
this run's own header — as do `tools/check-proper-components --phase artifacts
--edition homily`, `check-generation-metadata` and
`python3 scripts/_proper_study.py check … --phase content --edition homily
--require-presentation`.

The author read the contact sheet and the individual rasters of all five pages
and the extracted text of all five. The speech occupies pages 1 to 3 and ends
at the foot of page 3; the Collect paragraph turns between pages 2 and 3,
leaving two lines at the foot of page 2 as before; the running head reads
"Seventeenth Sunday after Pentecost" on the left and "Homily" on the right,
with the two well clear of each other on every page that carries them; the
note stands whole on page 4 and is unchanged in extent, the second reading's
restored title absorbed inside the fourteen lines its paragraph already
occupied; and the References,
the revision timestamp and the rights colophon share page 5, which carries no
head and no folio because the shared colophon sets that page empty, as it does
on the last page of all three documents. No clipping, collision, missing text,
blank page or heading-only page, and no paragraph broken with a single line
stranded. This is an author proof inspection and not the independent visual
evaluation.

The two studies were rebuilt at the same shared timestamp and are unchanged in
extent at 38 and 12 physical pages: SHA-256
`a5705241a178bc453e6a93c23f9f6e9201faac8630361470830e51b839dc05d5`
(expansive) and
`126bf160fb5de7e936399c24396d8bc93b46126e736e5f2d0b0a348591959dd7`
(concise). Both differ from the proofs the visual review read, because the
study and the companion were re-authored between that review and this stage;
each is the build of its own accepted sources at the current shared
timestamp. The concise study's settled auxiliary file still records inventory
and overview with all four sense markers on physical page 1, chronology on 2,
themes from 3 to 4 and commentary beginning on 5. The homily proof, its log,
auxiliary file, extracted text and their digests are kept beneath this stage's
own artifact directory in the run, with the page rasters in a child of their
own.

No upstream defect was found while re-deriving, and none was silently
repaired. Nothing outside `sections/homily/10-homily.tex`,
`sections/homily/90-note.tex`, `generation-metadata.tex` and this record was
edited at this iteration.

## Build artifacts

The three documents were built in order with
`make doc DOC=liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost PROVIDER=claude`
and the same target for the `-synthesis` and `-homily` ids. Each settles in
exactly two passes, and each was then rebuilt from a removed auxiliary file and
reproduced its warm bytes exactly, so the three PDFs recorded here are a cold
fixed point rather than an artefact of a seeded auxiliary file. The Makefile's
declared-input assertion, `check-generation-metadata` and
`tools/check-proper-components --phase artifacts` for all three editions pass,
as does
`python3 scripts/_proper_study.py check … --phase artifacts --require-presentation`
against the recorded snapshot. No source file was edited at this stage: no
layout repair was required, and the shared revision timestamp
`2026-09-19T00:05:00Z` therefore stands unchanged, with no content seal
refreshed.

The settled outputs, beneath the provider build root at
`build/claude/liturgy/roman-rite/1962/propers/temporal/`:

- `57-seventeenth-after-pentecost.pdf`, the expansive study, **38 physical
  pages** (the contract's 20–50), SHA-256
  `717a83e990ee864d1422058218254fa5039ce4bb367174570d8efbb1c19070c9`.
- `57-seventeenth-after-pentecost-synthesis.pdf`, the concise study, **12
  physical pages** (the contract's 10–12), SHA-256
  `8ac6eeda33cbf71d74f168aeeab7d0b3bbdee86f2d9db1ea51af6a132983abcd`.
- `57-seventeenth-after-pentecost-homily.pdf`, the homily, **5 physical
  pages**, SHA-256
  `9381b74ae96790703b8463854329fb60cb3d36bd16118f67399396aab704103e`.

All three are letter-size PDF 1.7 with no encryption, no form, no JavaScript
and no embedded file; each carries its own title and subject and the tracked
`ModDate` derived from the shared revision timestamp, with no build-clock
`CreationDate` and no trailer id. Ghostscript renders every page of all three
without a single diagnostic. Every font resource is embedded, subsetted and
Unicode-mapped: seven in the study, nine in the concise work and six in the
homily, all TeX Gyre Pagella faces with Latin Modern Mono for the colophon's
record paths. The study and the concise study carry a bookmark outline; the
homily carries none, as the accepted three-document set of this Sunday in the
other provider's tree also does.

The three final logs are clean: no error, no `LaTeX Warning`, no package
warning, no overfull or underfull box, and no rerun request in any of them.
Text extraction is complete and faithful for all three, with no replacement
character and no dropped run: 18,916 extracted words in the study, 7,408 in the
concise work and 2,299 in the homily, the last including the terminal note and
References around the 1,429-word spoken body. The Latin sets and extracts
correctly, `æ` and the acutes included; the four occurrences of *quǽsumus*,
*sǽcula* and *pharisǽi* extract as the ae-ligature followed by a combining
acute, which is the canonically equivalent decomposition of the glyph the page
prints and not a substitution. Page density was read for every page of all
three: no blank page, no heading-only page, and the least-filled pages are the
study's title page and the six section-end pages, each of which ends a reading
or an element.

The concise opening's physical-page evidence is settled in
`57-seventeenth-after-pentecost-synthesis.aux` and records absolute pages, not
a printed counter: `triptych:concise:inventory:start`/`:end` and
`triptych:concise:overview:start`/`:end` with all four sense markers on
physical page 1, `triptych:concise:chronology:start`/`:end` on 2,
`triptych:concise:themes:start` on 3 with `:end` on 4, and
`triptych:concise:commentary:start` on 5.

`python3 scripts/_proper_study.py snapshot` recorded the exact bytes in
`research/artifacts.json`: the three PDFs, the study's and the concise study's
auxiliary files and logs as pagination evidence, and 25 render inputs. The
bounded page rasters were prepared with `tools/tpt pdf-review` into this
stage's own raster child in the run directory — 38, 12 and 5 page images with
matching thumbnails and four contact sheets, the run record naming the same
three PDF digests. The PDFs, logs, auxiliary files, extracted text, the study's
contents file and their digests are kept beside the rasters, outside that
child.

Compared with the proofs their cold reviewers read, the homily PDF is
byte-identical, and all three auxiliary files are byte-identical, so no
reference, no page break and no table width moved. The study and the concise
study differ from their reviewed proofs in one line only — the printed
`Last revised (UTC)` colophon, which the homily stage's shared timestamp
update moved — 19 differing bytes in the study and 554 in the concise work,
with the extracted text identical on every other line.

Seal state at the close of this stage, honestly reported rather than
refreshed. The research, synthesis and homily seals are intact: every one of
the 2,054 files sealed by the accepted research review, the 14 sealed by the
concise review and the 7 sealed by the homily review still hashes as sealed.
The study seal is stale at exactly one file, `format.tex`, which the concise
stage extended after the study review had passed in order to add the
`concisemaptable` and `conciseoverview` environments its fixed first page
needs. That the extension changed nothing in the study is checkable and
checked: the study PDF built under the current `format.tex` differs from the
proof built under the sealed one only in the colophon timestamp line, its
auxiliary file is byte-identical, and neither environment is invoked outside
`sections/concise/`. This stage neither repaired that nor restamped it; the
artifact gate owns the disposition.

Remaining limitations. No page of any of the three has been read by an
independent visual reviewer; the reading recorded above is a build-side
inspection of extracted text, page density and contact sheets, not the cold
visual evaluation. Nothing is installed: no PDF has been copied beneath `pdf/`,
and no web edition has been generated or converted. The study's auxiliary file
carries one longtable chunk counter whose value depends on whether the build
started from a seeded auxiliary file; the PDF is identical either way, and the
snapshot records the cold, reproducible state.

## Build artifacts at iteration 1

The artifact gate failed the first build's snapshot on `STALE-STUDY-REVIEW`,
the expansive study's seal being stale at `format.tex`. That was repaired
upstream — the study was re-authored at its iteration 2 and independently
reviewed again, and the concise companion and the homily were re-derived and
reviewed against it — so this stage rebuilds all three documents from the
bytes those four reviews now hold.

Each was built with
`make doc DOC=<id> PROVIDER=claude` for the bare id and for the `-synthesis`
and `-homily` ids. Every build settles in exactly two passes. The three
documents were built first from a fully removed auxiliary set and then again
from the settled auxiliary files, and each pair of runs produced byte-identical
PDFs, auxiliary files and contents file, so the artifacts recorded here are a
fixed point and not the residue of a seeded auxiliary file. The Makefile's
declared-input assertion, `check-generation-metadata` and
`tools/check-proper-components --phase artifacts` for the research, synthesis
and homily editions all pass, as does the leaf content preflight for this run's
own provenance and the artifacts-phase gate command
`python3 scripts/_proper_study.py check … --phase artifacts --require-presentation`
against the recorded snapshot. No source file was edited at this stage: no
layout repair was required, so the shared revision timestamp
`2026-09-19T02:20:00Z` stands as the homily stage left it, no render
finalization metadata was restamped, and no content seal was refreshed.

The settled outputs, beneath the provider build root at
`build/claude/liturgy/roman-rite/1962/propers/temporal/`:

- `57-seventeenth-after-pentecost.pdf`, the expansive study, **38 physical
  pages** (the contract's 20–50), SHA-256
  `0edcc07c76da6c29affb30dfad7431d166f370e4b450818ea66336276bed2967`.
- `57-seventeenth-after-pentecost-synthesis.pdf`, the concise study, **12
  physical pages** (the contract's 10–12), SHA-256
  `689f6e31fa5fe237711ccf3759ba4f24d92be6381aebccb7f015bb238fa0638a`.
- `57-seventeenth-after-pentecost-homily.pdf`, the homily, **5 physical
  pages**, SHA-256
  `65ddd79b4a6d37f96687a14a3f5ae27b7f9b01acacc227dbae896f66585a2c31`.

All three are letter-size PDF 1.7 with no encryption, no form, no JavaScript,
no embedded file and no embedded image. Each carries its own title and
subject; each carries `ModDate` 2026-09-19T02:20:00Z, derived from the tracked
revision timestamp, with no build-clock `CreationDate` and no trailer id.
Ghostscript renders every page of all three without a single diagnostic. Every
font resource is embedded, subsetted and Unicode-mapped: seven resources in the
study, nine in the concise work and six in the homily, all TeX Gyre Pagella
faces with Latin Modern Mono for the colophon's record paths. The study carries
a bookmark outline of ten top-level entries and eighteen link annotations;
the concise study an outline of four; the homily none, as the
accepted three-document set of this Sunday in the other provider's tree also
has none.

The three final logs are clean: no error, no `LaTeX Warning`, no package or
class warning, no overfull or underfull box, and no rerun request in any of
them. Text extraction is complete and faithful for all three, with no
replacement character and no dropped run: 18,923 extracted words in the study,
7,409 in the concise work and 2,352 in the homily, the last including the
terminal note and References around the 1,429-word spoken body. The Latin sets
and extracts correctly, `æ` and the acutes included; the four occurrences of
*quǽsumus*, *sǽcula*, *pharisǽi* and *pharisǽis* extract as the ae-ligature
followed by a combining acute, which is the canonically equivalent
decomposition of the glyph the page prints and not a substitution. Page density
was read for every page of all three: no blank page and no heading-only page.
The least-filled pages of the study are its title-and-contents page and the
five pages that end a division — the Preface excursus on 13, the four-sense
distillations of the first two readings on 19 and 25, the comparison on 32 and
the References on 38. No page of the concise study falls below forty-two set
lines. In the homily only page 5, the References, is short, the spoken body
running full to the end of page 3 and the note filling page 4.

The concise opening's physical-page evidence is settled in
`57-seventeenth-after-pentecost-synthesis.aux` and records absolute pages
rather than a printed counter, with `\abspage` equal to `\page` at every
marker: `triptych:concise:inventory:start`/`:end` and
`triptych:concise:overview:start`/`:end` with all four sense markers on
physical page 1, `triptych:concise:chronology:start`/`:end` on 2,
`triptych:concise:themes:start` on 3 with `:end` on 4, and
`triptych:concise:commentary:start` on 5.

`python3 scripts/_proper_study.py snapshot` replaced `research/artifacts.json`
before the new visual review: the three PDFs, the study's and the concise
study's auxiliary files and logs as pagination evidence, and 25 render inputs.
The bounded page rasters were prepared with `tools/tpt pdf-review` into this
stage's own raster child in the run directory — 38, 12 and 5 page images with
matching thumbnails and four contact sheets, the run record naming the same
three PDF digests. The PDFs, logs, auxiliary files, extracted text, the study's
contents file and their digests are kept beside the rasters, outside that
child, so the helper's wholesale replacement of its output directory cannot
take them.

Compared with the proofs their cold reviewers read at the reviewing iterations
— `author-study` 2, `derive-synthesis` 2 and `derive-homily` 4 — the homily PDF
is byte-identical, and all three auxiliary files are byte-identical, so no
reference, no page break and no table width moved. The study and the concise
study differ from their reviewed proofs in one printed line only, the
`Last revised (UTC)` colophon, which the homily stage's later shared timestamp
update moved: 542 differing bytes in the study and 6 in the concise work, both
files unchanged in length, with the extracted text identical on every other
line.

Seal state at the close of this stage. All four content seals are current
against the bytes that now build: the research seal over its 2,054 files, the
study seal over its 19, the concise seal over its 14 and the homily seal over
its 7 each hash exactly as the accepted review recorded them, and the recorded
review results themselves still hash as the run recorded them. The
`format.tex` staleness that failed the gate at iteration 0 is gone, repaired at
its owner rather than restamped here. Nothing at this stage refreshed a seal or
described an old approval as current.

Remaining limitations. No page of any of the three has been read by an
independent visual reviewer; the reading recorded above is a build-side
inspection of extracted text, page density and contact sheets, not the cold
visual evaluation. Nothing is installed: no PDF has been copied beneath `pdf/`,
and no web edition has been generated or converted. The study's auxiliary file
showed no variance between the cold and the seeded build this round, and is
identical to the one its cold reviewer's proof settled.

## Build artifacts at iteration 2

The independent visual review returned the run to the study after the
iteration-1 build. The expansive study was re-authored through its iterations
3 to 7, the concise companion through its iterations 3 and 4, and the homily
re-derived at its iteration 5, each passing a fresh cold review; the research
records were untouched. This stage rebuilds all three documents from the bytes
those four accepted reviews now hold.

Each was built with `make doc DOC=<id> PROVIDER=claude` for the bare id and
for the `-synthesis` and `-homily` ids. Every build settles in exactly two
passes. All three were built first from a fully removed auxiliary set — the
build directory's `.aux`, `.toc`, `.fls`, `.log`, `.pdf` and the metadata
stamps deleted — and then again from the settled auxiliary files, and each pair
of runs produced byte-identical PDFs, auxiliary files and contents file, so
the artifacts recorded here are a fixed point and not the residue of a seeded
auxiliary file. The Makefile's declared-input assertion and
`check-generation-metadata` pass for all three, as do
`tools/check-proper-components --phase artifacts` for the research, synthesis
and homily editions, the leaf content preflight over its twelve checks, the
separate `provenance-matches-run` check against this run's own header, and the
artifacts-phase gate command
`python3 scripts/_proper_study.py check … --date 2026-09-20 --phase artifacts
--require-presentation` against the recorded snapshot. No source file was
edited at this stage: no layout repair was required, so the shared revision
timestamp `2026-09-19T08:10:00Z` stands as the homily stage left it, no render
finalization metadata was restamped, and no content seal was refreshed.

The settled outputs, beneath the provider build root at
`build/claude/liturgy/roman-rite/1962/propers/temporal/`:

- `57-seventeenth-after-pentecost.pdf`, the expansive study, **38 physical
  pages** (the contract's 20–50), SHA-256
  `a5705241a178bc453e6a93c23f9f6e9201faac8630361470830e51b839dc05d5`.
- `57-seventeenth-after-pentecost-synthesis.pdf`, the concise study, **12
  physical pages** (the contract's 10–12), SHA-256
  `126bf160fb5de7e936399c24396d8bc93b46126e736e5f2d0b0a348591959dd7`.
- `57-seventeenth-after-pentecost-homily.pdf`, the homily, **5 physical
  pages**, SHA-256
  `923fb4936d107d3dec13fc6cf1b7a9197aed5dbb1ef19ae20cc5bb8f2d2fb289`.

All three are letter-size PDF 1.7 with no encryption, no form, no JavaScript,
no embedded file and no embedded image. Each carries its own title and
subject; each carries `ModDate` `D:20260919081000Z`, derived from the tracked
revision timestamp, with no build-clock `CreationDate` and no trailer id.
Ghostscript renders every page of all three without a single diagnostic. Every
font resource is embedded, subsetted and Unicode-mapped: seven resources in the
study, nine in the concise work and six in the homily, all TeX Gyre Pagella
faces with Latin Modern Mono for the colophon's record paths. The study carries
a bookmark outline of ten top-level entries and twenty link annotations on four
pages — ten on the contents page and the rest in the References; the concise
study an outline of four and one link annotation; the homily no outline and one
link annotation, as the accepted three-document set of this Sunday in the other
provider's tree also has none.

The three final logs are clean: no error, no `LaTeX Warning`, no package or
class warning, no overfull or underfull box, no missing character, no font
warning and no rerun request in any of them; the only occurrences of the word
are the `rerunfilecheck` package's own banner lines. In particular the bounded
right running head the study adopted at its iteration 3 raises no warning,
which is the signal that no head string overruns its box. Text extraction is
complete and faithful for all three, with no replacement character, no control
character and no dropped run: 19,357 extracted words in the study, 7,441 in the
concise work and 2,361 in the homily, the last including the terminal note and
References around the 1,429-word spoken body. The Latin sets and extracts
correctly, `æ` and the acutes included; the four occurrences of *quǽsumus*,
*sǽcula*, *pharisǽi* and *pharisǽis* extract as the ae-ligature followed by a
combining acute, which is the canonically equivalent decomposition of the glyph
the page prints and not a substitution. Page density was read for every page of
all three: no blank page and no heading-only page. The least-filled pages of the
study are its title-and-contents page and the five pages that end a division —
the Preface excursus on 13, the four-sense distillation of the first reading on
19, the comparison on 32, the Scriptural Date and Location sheet on 34 and the
References and colophon on 38. No page of the concise study falls below
forty-two set lines. In the homily only page 5, the References, is short, the
spoken body running to the end of page 3 and the note filling page 4. The last
page of each document carries neither running head nor folio, which is the
universal preamble's own terminal colophon setting `\thispagestyle{empty}` to
recover the footer area, not a defect of this leaf.

The concise opening's physical-page evidence is settled in
`57-seventeenth-after-pentecost-synthesis.aux` and records absolute pages
rather than a printed counter, with `\abspage` equal to `\page` at every
marker: `triptych:concise:inventory:start`/`:end` and
`triptych:concise:overview:start`/`:end` with all four sense markers on
physical page 1, `triptych:concise:chronology:start`/`:end` on 2,
`triptych:concise:themes:start` on 3 with `:end` on 4, and
`triptych:concise:commentary:start` on 5.

`python3 scripts/_proper_study.py snapshot` replaced `research/artifacts.json`
before the new visual review: the three PDFs, the study's and the concise
study's auxiliary files and logs as pagination evidence, and 25 render inputs.
The bounded page rasters were prepared with `tools/tpt pdf-review` into this
stage's own raster child in the run directory — 38, 12 and 5 page images with
matching thumbnails and four contact sheets, the run record naming the same
three PDF digests. The PDFs, logs, auxiliary files, extracted text, the study's
contents file and their digests are kept beside the rasters, outside that
child, so the helper's wholesale replacement of its output directory cannot
take them.

Compared with the proofs their cold reviewers read at the reviewing iterations
— `author-study` 7, `derive-synthesis` 4 and `derive-homily` 5 — the homily PDF
is byte-identical, and all three auxiliary files are byte-identical, so no
reference, no page break and no table width moved. The study and the concise
study differ from their reviewed proofs in one printed line only, the
`Last revised (UTC)` colophon, which the later shared timestamp moved from
`2026-09-19T06:20:00Z` in the study's proof and `2026-09-19T08:05:00Z` in the
concise proof to the common `2026-09-19T08:10:00Z`: two differing characters in
each extracted text and nothing else on any other line.

Seal state at the close of this stage. All four content seals are current
against the bytes that now build: the research seal over its 2,054 files and 12
chronology computation inputs, the study seal over its 19, the concise seal over
its 14 and the homily seal over its 7 each hash exactly as the accepted review
recorded them, with no mismatch, and all 79 recorded stage results still hash as
the run recorded them. `generation-metadata.tex` is not among the sealed bytes
of any of the three document reviews — its provenance is sealed as a structured
record instead — which is why the homily stage's later timestamp does not stale
the study's or the concise study's review. Nothing at this stage refreshed a
seal or described an old approval as current.

Remaining limitations. No page of any of the three has been read by an
independent visual reviewer since the re-authoring; the reading recorded above
is a build-side inspection of extracted text, page density and contact sheets,
not the cold visual evaluation. Nothing is installed: no PDF has been copied
beneath `pdf/`, and no web edition has been generated or converted.

## Generate-web, iteration 0 — 19 September 2026

The canonical study was converted with the exact compiled-packet command:

```sh
tools/tpt web-edition --provider claude --output build/web liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost
```

It succeeded on its first invocation, with `tools/web-edition` SHA-256
`d945021413b26de9a8b2e1c961caed9035c742a3802ccf9339001c28ba215d7b` and
`scripts/web-shim.tex` SHA-256
`679ff8592e5e8ae1a9755aed9b856710e7fcc49adca32050a54896a723022b22`. The
converter appended the provider and the document to `--output` and wrote
`build/web/claude/liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost.md`
directly, so nothing was moved or relocated. The generated file is 115,834
bytes, SHA-256
`45132c6a78f9c7000d84cd966fb8803de848e6cefa826456457133de0222eb95`, and was
not edited after generation. No accepted TeX and no shared tooling was
changed at this stage.

All of the converter's own audits pass: the schema-2 anchor audit over the
source labels and the site-rendered targets, the undefined-command audit, the
paragraph and severed-run audits over the leaf's files as they stand, and the
table count. `tools/tpt check-web-edition --provider claude --document
liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost`
validates the per-leaf declaration: one eligible leaf, no blocking construct.

Independent reading of the generated Markdown against the nine section files
confirms the whole argument survives. The ten `\section` and `\section*`
headings of the source become the ten level-two headings of the Markdown and
its forty-five `\subsection` headings become forty-five level-three headings,
fifty-five in all beneath the title, with none added and none lost. All three
interpretive lanes are present under their own headings, each ending in its own
four-sense block, and each of the twelve senses is named — literal,
allegorical, moral, anagogical — in all three. Every one of the twenty source
`\label` commands has a target: nineteen as heading anchors and
`sec:references`, whose starred heading carries no anchor of its own, as an
explicit span. The ten appointed-text anchors `proper-introit` through
`proper-postcommunion` match the manifest's `element_keys` exactly, one each
and no others. The ten `latinproper` and ten `englishwitness` environments all
render as quoted blocks with their witness lines and verse superscripts intact;
all three tables — the opening map, the four-column comparison and the
seven-dossier Scriptural Date and Location sheet with both tiers of each
dossier — carry every row, the `\chronodate` and `\chronologyannotation` macros
expanded to their computed dates; and all thirty-six References entries and all
six source URLs are present, the seventh link being the colophon's own. A
head-and-tail probe of all 190 prose blocks of the nine section files found no
block missing from the Markdown.

The reader-facing terminal matter is complete and nothing behind it leaked: the
revision display reads `Last revised (UTC): 2026-09-19T08:10:00Z` and the
rights colophon follows it, while the model identity, effort, agent and
contribution history of `generation-metadata.tex` appear nowhere in the output,
as `guidance/web-editions.md` requires. This leaf uses no footnotes, endnotes
or edition conditionals, so none could be dropped. No render-relevant source
changed at this stage, so the recorded revision time stands unaltered.

`python3 scripts/_proper_study.py snapshot-web --provider claude --document
liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost`
recorded the generated bytes in `research/web-artifact.json`, whose digest
matches the Markdown that now stands. That receipt records conversion
identity, not approval: no independent web review has read these bytes. Only
the canonical study was converted; `build/web/claude/.../temporal/` holds that
one file and no synthesis or homily web leaf. Nothing was installed beneath
`web/`, and no release record or catalog was created or edited.

## Install-publication, iteration 0 — 19 September 2026

All three accepted PDFs were installed with the normal Make recipes and their
declared dependencies and checks, one document at a time and with nothing
suppressed — no `-o`, no `-t`, no touched timestamp, and no edit to an accepted
source or to `\AIDocumentRevisionTimestamp` to avoid a rebuild:

```sh
make install-doc DOC=liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost PROVIDER=claude
make install-doc DOC=liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost-synthesis PROVIDER=claude
make install-doc DOC=liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost-homily PROVIDER=claude
```

Before installing, the artifact snapshot was confirmed current: `python3
scripts/_proper_study.py check --provider claude --document <leaf> --date
2026-09-20 --phase artifacts --require-presentation` exits 0, so
`research/artifacts.json` still described the built bytes exactly as the visual
review sealed them.

Make retypeset the concise study and the homily (the canonical study it found
up to date and did not rebuild). Both rebuilds produced byte-identical PDFs, so
the rebuild is acceptable under the stage contract. Each installed PDF and each
build PDF hashes to the value the four accepted reviews recorded:

| Output | Pages | Bytes | SHA-256 (build and installed) |
| --- | ---: | ---: | --- |
| `57-seventeenth-after-pentecost.pdf` | 38 | 303,195 | `a5705241a178bc453e6a93c23f9f6e9201faac8630361470830e51b839dc05d5` |
| `57-seventeenth-after-pentecost-synthesis.pdf` | 12 | 241,258 | `126bf160fb5de7e936399c24396d8bc93b46126e736e5f2d0b0a348591959dd7` |
| `57-seventeenth-after-pentecost-homily.pdf` | 5 | 149,581 | `923fb4936d107d3dec13fc6cf1b7a9197aed5dbb1ef19ae20cc5bb8f2d2fb289` |

No hash differs from its accepted value, so no artifact defect is reported
upstream and no review boundary is reopened.

### A build-graph defect the retypeset exposed

The retypeset was not caused by any change to a render source. Every one of the
25 `render_inputs` is unchanged, both sealed `.aux` files are byte-identical,
and the canonical study's `.log` is byte-identical. What moved was
`evaluations/blocking-findings-v1.toml`, written at 04:29:36 by the web review
recording its standing findings. `REGISTER_PROPER_DERIVED_SOURCES` in the
Makefile globs `*.toml` anywhere beneath the leaf, so an evaluation record that
no document renders from is a prerequisite of the `-synthesis` and `-homily`
PDFs. `REGISTER_DOCUMENT_SOURCES`, which governs the canonical study, globs
only render extensions and is unaffected — which is exactly why two of the three
PDFs rebuilt and one did not.

The only byte-level consequence was the concise study's `.log`, whose pdfTeX
banner records the wall clock: line 1 read `19 SEP 2026 03:32` before and
`19 SEP 2026 04:33` after, and the two logs are identical on every other line,
both clean. That file is a sealed member of `pagination_evidence`, so the
reviewed visual seal and `research/artifacts.json` both ceased to match a build
that had changed nothing a reader or a reviewer could see. The reviewed log,
retained by this run at
`build/tpt-runs/1e02dc05f2df9940/artifacts/build-artifacts-0002/57-seventeenth-after-pentecost-synthesis.log`
and hashing to the recorded
`8622156d7f5376a23ef9b6614563c0a16e8fc61dfc076547673aae2b8789be27`, was restored
over it, and the post-install log was kept in this stage's scratch area rather
than discarded. No receipt was rewritten to absorb the difference: the snapshot
in `research/artifacts.json` is untouched and still holds the digests the visual
review sealed. Since a `.log` banner can never survive a retypeset, any future
run whose evaluation stage writes into the leaf between the artifact build and
installation will meet the same thing; the durable fix belongs in the Makefile's
derived-source glob, not in this leaf.

### Installed web edition, records and wiring

`build/web/claude/.../57-seventeenth-after-pentecost.md` was copied to
`web/claude/.../57-seventeenth-after-pentecost.md` byte for byte — 115,834
bytes, SHA-256
`45132c6a78f9c7000d84cd966fb8803de848e6cefa826456457133de0222eb95`, `cmp` clean
against the reviewed conversion — and staged, so `git ls-files --error-unmatch`
proves it tracked. No synthesis or homily web leaf exists; the canonical study
remains the sole web authority.

Three release records were created with `make add-publication ID=<id>
CATALOG=library/traditional-latin-mass.md PROVIDER=claude STATUS=alpha`, one per
PDF. No record existed beforehand, so none was overwritten. Each names schema
version 1, its own exact output id, the 1962 catalog
`library/traditional-latin-mass.md`, status `alpha`, and the standing
authorization `perpetual-public-repository-2026`.

The existing row 57 of `library/traditional-latin-mass.md` had its Claude cell
changed from `Planned` to the three PDFs and the canonical web page, in the
output-label order the schema-2 manifest declares — `canonical_label` Full PDF,
`synthesis_label` Synthesis PDF, `homily_label` Homily PDF, then Read. The
ChatGPT cell, every other row and every other cycle are untouched, and no
companion row was created. One canonical publication marker was added,
`claude:liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost`:
`release/public-alpha.json` names `gpt` as primary provider, so the
primary-provider rule requires the provider prefix here, and the unprefixed gpt
marker above it is left alone.

`tools/tpt document-library structure` regenerated the deterministic catalogue
projection. A key-by-key comparison confines every change to work 94: the gpt
edition survives byte-for-byte and moved to index 1, a claude edition was added
carrying the study, both companions under `also`, the web page, the twelve
contribution records the source already held, and this run's `produced`
identity; the three aggregate counts moved by one document, three issues and 38
pages. No other work of the 142 differs.

The release refresh was scoped, per the repository's scoped-refresh rule, to the
three reader-facing paths this stage actually changed: `make
refresh-release-bindings ADOPT=1 ONLY="library/traditional-latin-mass.md
web/claude/.../57-seventeenth-after-pentecost.md
src/web/data/structure/documents/corpus.json"`. Five changes — the new web
edition adopted, the catalogue page and the projection re-recorded, and the
rights table and its digest rewritten. Nothing a sibling production holds
uncommitted was adopted.

### Publication-gate evidence

All five terminal checks were run in this working tree and all five exit 0:
`_proper_study.py check --phase publication --require-presentation` (installed
and build byte identity for all three, exact release ids and owning catalog, one
catalog row linking all three PDFs and the canonical web page, exactly one
canonical marker, the web receipt and the installed web edition both matching
the reviewed conversion, the Markdown tracked, no companion web authority, and
`check-web-edition`); `make check-release-bindings` (0 stale bindings);
`tools/tpt public-alpha check --provider claude --document <leaf>` (scoped
policy valid, 221 publications, global source, release and authorization records
valid); `tools/tpt document-library check` with `document-library structure
--check` (projection current); and `make check-web-editions-current` (tracked
web editions match current sources).

These are this stage's own runs of the gate commands, not an acceptance. The
terminal program gate decides acceptance, and nothing here has been committed.

## House-voice audit and review fixes, 24 September 2026 (outside the workflow)

On 2026-09-24 the maintainer decided to audit every proper leaf of both
providers for the house-voice defect and to repair what the audit finds, with
independent review afterwards. The audit's rewrites are recorded in commits
`bd223d6a9` and `b3c384e4d`. This pass fixes the independent review's findings
on them and, because the leaf is now reopened, applies the three-document
profile's *Liturgical commentators* rule (D11) and its lectionary- and
sacramentary-list rule (D12), which were not applied when this leaf was first
reviewed.

**Review findings.**
- Cassiodorus is an ecclesiastical writer in `author-standing-v1.toml`, not a
  Father. So "Neither Father yields to the other" now reads "The two are not
  reconciled", and the Alleluia setting's "The Fathers divide" now reads "The
  psalm's two principal witnesses divide".
- The comparison and the concise commentary say of Trent's chapter that it
  "has no place in the second reading, which hears …".
- The readings "differ in emphasis more than in what they identify".
- The opening now gives each reading "four senses of its own".
- These were rewritten again: the settings' introduction and closing
  subsection, with "as these settings show" deleted, and the concise themes'
  closing.

**D11: liturgical commentators.** Rupert of Deutz and William Durandus
expounded an office of this Sunday whose Gospel was Luke 14.
`research/scope.md` § 2.4 records their elements.
- Removed from the reader-facing prose:
  - their other Gospel, and the Gospel's move in the year;
  - the Offertory's older verses and the reasons for its choice (Fromage,
    Tommasi, Durandus on Michaelmas);
  - Rupert's and Durandus's reading of the Offertory's answer;
  - the subsection "The medieval office of humility, and its other Gospel",
    with Rupert's banquet mercy in the reading's anagogical sense;
  - "Rupert and Durandus" in the comparison;
  - Rupert in the concise overview, commentary, scope note and References;
  - Rupert and the continuation in the concise References.
- What stays:
  - Durandus's gloss on the Introit's *rectum iudicium*, the judgment *quo Deus
    exaltat humiles, et superbos deprimit*. It is now beside Bellarmine in the
    third reading, with the difference between them.
  - Durandus's reading of this Gospel's second half, at his own locus
    (*Rationale* VI.135). The Sunday on which he read it is not narrated.
- The expansive scope appendix keeps its one permitted clause, reworded:
  "William Durandus, whose office of this Sunday had another Gospel, is cited
  for the Introit and, where his books read it, for this Gospel." The Luke
  14:9–11 locus leaves both Douay entries.

**D12: list history.** The concise themes lose the formulary's early-list
history: the Old Gelasian placing of the Collect and its *corde*, the earliest
graduals, and the Frankish Gelasians and Supplement. They also lose
"reached the day by different roads", "the chants that have stood at this
Sunday longest" and "the texts gathered around them were not written for them".
The expansive study carries all of it in `10-each-element.tex` and
`40-just-judge-merciful-hearer.tex`. The concise scope note now points to the
expansive study for the sacramentary and chant witnesses, and the Wilson and
Hesbert entries leave the concise References. The homily carried none of this.

**Holding page 4.** The concise themes still fill physical pages 3 and 4. The
space freed there is filled from observations the expansive study already
makes:
- Ps 118:135's *illumina*;
- the Collect's *sectari*;
- the Epistle's *Fratres*, doxology and verse 7;
- the Alleluia psalm's turn to Sion;
- the Offertory's 9:7 and 9:18;
- the Communion psalm's v. 10;
- the Preface's *unus es Deus*.

**Homily count.** The spoken body is 1,416 words. The note says 1,416, and that
is correct. The mentions of 1,429 earlier in this record predate the
restyling commit `6caf8946d` of 21 September. That commit shortened the Creed,
Offertory and Communion sentences, and the spoken body went from 1,429 words
to 1,416, counted the same way. Those mentions are corrected here and not
rewritten. The homily note's route sentence now has the antiphon, not the
homily, as its subject. No word of the spoken body changed.

**Checks.** All three editions were built with `make doc` and installed with
`make install-doc`. The installed bytes equal the build, and the settled-aux
component and metadata checks pass.

| Edition | Pages | SHA-256 |
| --- | --- | --- |
| Study | 31 | `5c90ed75d4b8231f4b2b5461576d8f9df7a9ebbc6432fe2bc986f94810459b12` |
| Concise study | 10 | `c73b383a66b1617ebb7ceed9bb05d4b1d5add0f3ed47da12085694ed7346ffef` |
| Homily | 3 | `324fe5e6e63b4fcaf71e2729da1437328639b0cd6749980dbdfd04f087dcba64` |

- Every changed page was inspected at 70 dpi. The concise themes still end on
  page 4, and the commentary opens page 5.
- `check-content-preflight` passes on all four editions. references-used now
  counts 63 entries and structural-meta-labels 87 headings, because Rupert,
  the continuation's concise entry, the Wilson/Hesbert concise entry and one
  heading were removed.
- The web edition is regenerated and `make check-web-editions-current` passes.
- The receipts are re-snapshotted, and `_proper_study.py check` passes in
  content, artifacts and publication with `--require-presentation
  --require-format`.
