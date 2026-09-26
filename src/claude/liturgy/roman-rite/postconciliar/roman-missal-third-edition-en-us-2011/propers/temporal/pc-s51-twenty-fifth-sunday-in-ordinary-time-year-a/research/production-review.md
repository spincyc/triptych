# Production and review record

## Author-study

Authored 19 September 2026 in `proper-study` v4, run `472e2eb20876b22a`, seeded
at commit `02bae3f417048707bf5f76a9ef50b3236bf60701`, at iteration 0. The
canonical study is *The Twenty-fifth Sunday in Ordinary Time, Year A*, formula
`PC-S51-A`: the Week XXV formulary of the *Roman Missal*, Third Edition, for the
dioceses of the United States, with Lectionary no. 133, for the occurrence of
20 September 2026. No blocking, carried or advisory finding was forwarded to
the stage at iteration 0. The study review of that iteration returned two
blocking findings and five advisories, and iteration 1, recorded below,
answers them. The study review of iteration 1 returned one blocking finding and
one advisory, and iteration 2, recorded below it, answers those. Where this
entry describes the study it describes the study as it stands after
iteration 2.

### What the study contains

An opening on the parable's complaint and question, with the standing notice
on the study English where Scripture first appears and an eleven-row map of the
appointed elements (the two Communion antiphons as alternatives); the appointed
Scripture in the Douay–Rheims (Challoner), every partial verse marked with the
words the Mass does not read set in brackets, the adapted Alleluia verse given
only by its basis in Acts 16:14, and the Entrance Antiphon and three orations by
Latin incipit and description, each saying in its own place that no English is
printed; an element-by-element section giving each text its literary, textual
and liturgical setting; three interpretations of the whole formulary, each
carrying all eleven element keys, naming its strongest difficulty and closing
with its own four senses; a comparison; a terminal Scriptural Date and Location
sheet on the generated chronology projection, which is the reviewed home of the
chronology the concise page 2 will reprint; the Liturgical Resolution and Scope
appendices; and References. One `\label{proper-<element-key>}` stands at each
of the eleven appointed texts.

The three interpretations are those of `research/interpretations.md`, under its
lane keys:

- `economy`, *One Wage across the Ages*. Witnesses developed: Gregory (*Hom. in
  Evang.* 19.1, 4; 14.4), Augustine (*Sermo* 87.5–6, 9; *Tract. in Ioh.*
  47.4–5), Jerome (*In Matt.* III, PL 26, 141, as reporter of the scheme; *In
  Isaiam* XV, PL 24, 553–555), Aquinas (*Super Matt.* c. 20 lect. 1), Bede
  (*Retractatio in Actus* 16), Bellarmine (Ps 144:9).
- `conversion`, *Seek the Lord While He May Be Found*. Witnesses developed:
  Chrysostom (*Hom. in Matt.* 64.3–4; *Hom. in Phil.* 3–4), Jerome (*In Matt.*
  III, col. 141; *In Isaiam* XV, col. 553), Augustine (*Sermo* 87.1, 7–11;
  *Enarr. in Ps.* 144.11), Gregory (*Hom.* 19.2–3, 6; 14.4), Aquinas (*Super
  Matt.*; *Super Isaiam* c. 55; *Super Phil.* c. 1 lect. 3), Bellarmine
  (Ps 144:8), with Hilary (Ps 118, Aleph 11) once.
- `gift`, *Because I Am Good*. Witnesses developed: Augustine (*Sermo* 87.4, 6;
  *Enarr. in Ps.* 144.11, 21–22; 118 s. 4.2; *De praed. sanct.* 20.41; *Tract.*
  47.2), Gregory (*Hom.* 19.4; 14.1–5), Jerome (*In Matt.* III, cols. 141–142;
  *In Isaiam* XV, col. 555), Aquinas (*Super Matt.* p. 262; *Super Isaiam*;
  *Super Phil.*; *Super Ioannem* c. 10 lect. 4), Hilary (Ps 144.14; Ps 118,
  Aleph 12), Bellarmine (Ps 144:17; Ps 118:5, 8). Chrysostom is quoted for the
  half of the claim he shares and for his own reading of Acts 16:14, and is
  not declared an author of this lane, as the research record requires.

Differences carried where the research records them: what Augustine and
Chrysostom each say of Acts 16:14, reported in their own words beside the step
the difference qualifies, with no position on lateness attributed to Augustine
from *Sermo* 87 and neither author presented as answering the other;
Chrysostom against Gregory and Aquinas on the excuse "No man hath hired us";
Augustine, Chrysostom, Jerome and Aquinas on how "the last shall be first"
stands to the parable, given once in the element section and recalled in the
comparison; the differing divisions of the hours and identifications of the
eleventh-hour workers; Gregory, Jerome and Chrysostom on the murmuring; and the
three glosses of "in truth". No witness is credited with a reading of this Mass.
Every connection between a Missal text or the second reading and the parable is
made in the study's own voice, and each interpretation says which of its
element placements rest on no commentator.

The research review's standing advisories were observed in the prose. No order
of priority among the witnesses and no claim that one wrote independently of
another is made (RES-017). *Praenotanda* 106 is paraphrased and not quoted in
English (RES-018). RES-019 concerns an audit sentence and nothing in the study.

### Counts and the proof at iteration 0

The figures in this subsection are those of the first submission and are kept
as its record. The current figures are under iteration 2 below.

**Substantive word count: 13,452 words** (12,858 with the content of the
`\latin{}` spans removed). The count converts the six argumentative components,
opening, element-by-element setting, the three interpretations and the
comparison, through Pandoc's LaTeX reader to plain text with the leaf's inline
commands declared first, removes headings and the map and comparison tables, and
counts whitespace-separated words. It excludes the appointed-text component, the
Scriptural Date and Location sheet, both appendices and the References. The
total stands above the 6,000–10,000-word planning range: three interpretations
that each carry eleven elements and four senses account for 9,447 words of it
and the element settings for 2,426. Two passes of cutting during composition
removed restatement between the opening, the map, the appointed-text notes and
the element section.

The author proof is `build/claude/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s51-twenty-fifth-sunday-in-ordinary-time-year-a.pdf`:
37 physical pages, inside the 20–50-page requirement, SHA-256
`142f9f184885c3e5c80787113aca42b471a31d4b9368641618426f770fa78a02`, built with
`make doc` at revision timestamp 2026-09-19T15:12:54Z. The settled log carries
no overfull or underfull box, no undefined reference and no LaTeX warning; every
font is embedded; the metadata gate passed; and
`tools/check-proper-components --phase artifacts --edition research` passed. All
37 pages were inspected on contact sheets of the settled proof, and the title
page, the map, an appointed-text page, the close of the first interpretation,
the comparison table, the dossier sheet, the branch table and the last page at
full size during composition. Three layout defects found on the way were
repaired before this proof: a five-line spill page at the end of the first
interpretation, a heading parted from its text at the foot of a page (headings
now move with `nobottomtitles*`), and a rights colophon forced onto a page of
its own. Subsection marks were silenced so that the right running head names the
section alone. The thirteen study-preflight checks, run by hand with this run's
header, all exit 0, and a trial conversion through `tools/web-edition` into
scratch space produced all eleven appointed-text anchors. This is author
verification; the shared-timestamp three-document build and the independent
visual review remain to be done.

### Source limits

Those of `research/scope.md`, restated to the reader in the scope appendix. The
points that shaped the prose: what is reported of Aquinas on Matthew from
pp. 258–261 is paraphrased and only p. 262 is quoted; Augustine's *Enarr.*
144.21–22 rests on the augustinus.it delivery alone, and nothing is any longer
reported from 144.3–5; Bellarmine is quoted from O'Sullivan's abridged English;
Gregory's Latin is quoted in short phrases; the Ambrosian occurrence of the
Prayer after Communion is a lead and is not mentioned; no biblical date is
printed outside the generated Date cells, and the dossier prose names later
critical positions without figures.

### Iteration 1: repair of the study review's findings

Revised 19 September 2026 in the same run, against study-review iteration 0.

| Finding | Severity | Outcome | What was done |
| --- | --- | --- | --- |
| STU-001 | blocking | repaired | In the third interpretation ("Asking for what is commanded" and "The contract that remains") and in the comparison (table cell and paragraph), Chrysostom's two sentences on Acts 16:14 are now quoted whole from *Hom. in Acta* 35 and Augustine's from *De praed. sanct.* 20.41, and the difference is stated in their own terms: Chrysostom speaks of hearts that are willing and gives the opening to God and the attending to Lydia, and does not say where the willingness comes from; Augustine counts the beginning of faith a gift and says she was called so that she might believe. "Objection", "dissent", "denies that the willingness God opens is itself given", "the witnesses part" and "no witness read here settles between him and Augustine" are gone, as is the second interpretation's "where it meets Augustine". The second difficulty is now one of evidence: the step rests on Augustine's argument and on no agreement between the two. No statement of the Church's teaching on the beginning of faith was added, since none is bound. Chrysostom's agreement with the controlling claim (64.4) stays. The manifest comment on the third lane was reworded to match. |
| STU-002 | blocking | repaired | (a) Jerome is credited only with the coin as the king's figure and the wage as the king's image and likeness; that the likeness is Christ is marked as the study's identification. (b) Jerome, Augustine and Gregory are credited with the ages of a life, and Augustine alone (*Sermo* 87.9) with the householder who goes out as Christ. (c) Gregory's point stands in his tense: the fathers have already passed, after their delay, to the joys of the kingdom. (d) The third interpretation's anagogical sense and its body paragraph on the wage say that Augustine speaks of the psalm and Gregory of the shepherd's pasture and that setting them beside the coin is the study's; the comparison's Paul row credits Aquinas and Chrysostom only with what they say of the letter. The same rule was applied to four other parentheticals met on the way: Bede in the first interpretation's allegorical sense and in the comparison, Jerome in its moral sense, Augustine beside Gregory in the third interpretation's allegorical sense (Augustine says the sheep acknowledge their price and find the body and blood on the altar, not that the shepherd feeds them with it), and Jerome beside Aquinas in the comparison's Isaiah row. |
| STU-003 | advisory | cleared | The first interpretation's difficulty now says what Chrysostom applies his rule to, the murmuring and the excuse "No man hath hired us", quotes the second application, and sets his "He called all, as far as lay in Him, from the first" against Gregory's and Aquinas's reading of the excuse as the Gentiles' true plea. The inference that the rule tells against giving the hours an epoch was dropped. The comparison follows. |
| STU-004 | advisory | cleared | The study opens on the parable. One identifying sentence names the Sunday, the Missal and Lectionary no. 133; the date, colour, omitted memorial and Preface rule stand only in the resolution appendix. |
| STU-005 | advisory | cleared | Jerome's sentence is quoted with its ground, "Qui enim fecerit eam, vivet in ea", placed at the householder's "Take what is thine", and taken up in "The contract that remains" beside Augustine and Aquinas. |
| STU-006 | advisory | cleared | The tractate's heading (John 10:14–21) and the sections read; Jerome as carrying the second sentence of 20:16 without comment, in the element section and the scope appendix; Aquinas's division of the hours by paraphrase; Gregory 19.4 in its own sense; Jerome's envy as directed at the Gentiles. |
| STU-007 | advisory | cleared | Both texts are said to concern Philippi, and Acts 16:14 is named as what narrates; "for ever" lost its quotation marks; the three psalm contacts carry the study's dual numbering; the *Ordo*'s titles are said to mark the two correlated readings, with the second reading's own title noted; Paul is given no hour in the third interpretation, and the first interpretation's moral sense no longer calls him a labourer called early. |

Evidence read at this iteration, beyond what the research rows quote. Each
locus is inside a bound source; none of it changes a research record.

- Chrysostom, *Hom. in Acta* 35 and *Hom. in Matt.* 64.3–4, re-read in the
  tracked NPNF text: the two sentences on Lydia, the rule stated about the
  murmuring, and its second application to "No man hath hired us".
- Jerome on Matthew, PL 26, col. 142, re-read on the page image of the retained
  facsimile: "Iudaeus in Lege non gratia, sed opere salvatur. Qui enim fecerit
  eam, vivet in ea" stands under the lemma of vv. 14–15, and the second
  sentence of v. 16 is carried in the lemma and repeated as the parable's end
  with no comment of its own. The second clause was compared with Leviticus
  18:5 and Romans 10:5 in the tracked Douay–Rheims and Clementine texts, whose
  wording at Romans 10:5 it follows.
- Aquinas on Matthew: two sentences of the pages the research record calls
  OCR-only were read on the page image of the retained facsimile (its fourth
  page) as well as in the text layer, his division of the sixth and ninth hours
  at David and his reference of "No man hath hired us" to the Gentile people,
  excused because they had not the prophets. Both are reported by paraphrase,
  as the record directs for those pages, and the scope appendix says so.
- Gregory, *Hom.* 19.3–4, and Augustine, *Sermo* 87.9–10 and *Tract.* 47 (the
  heading, sections 1, 2 and 5 whole and the opening lines of 3 and 4), re-read
  in the tracked texts.

**Substantive word count: 14,249 words** (13,648 with the content of the
`\latin{}` spans removed), by the method stated above: opening 974, element
settings 2,478, the three interpretations 3,310, 3,049 and 3,875, comparison 563
(its table excluded). The repairs added about 800 words, most of them in the
first interpretation's difficulty and the third interpretation's two repaired
passages, where quoting each author whole took more room than characterizing
him.

The author proof is the same build path as before: 39 physical pages, inside
the 20–50-page requirement, SHA-256
`bc75cba2a2bcb43fc14b845a5b39dc567ee365e475c6d11ba4bb51df62391ec3`, built with
`make doc` at revision timestamp 2026-09-19T15:58:43Z; a second build from
unchanged sources reproduced the same bytes. The settled log carries no
overfull or underfull box, no undefined reference and no LaTeX warning; all
eight fonts are embedded; the metadata gate passed;
`tools/check-proper-components --phase artifacts --edition research` passed; and
the thirteen study-preflight checks, run by hand with this run's header, all
exit 0. A trial conversion through `tools/web-edition` into scratch space again
produced all eleven appointed-text anchors. All 39 pages were inspected on
contact sheets of the settled proof, and pages 2, 23, 30, 31, 38 and 39 at full
size. The first drafts of the repairs produced a two-line spill page at the end
of the second interpretation, a comparison table broken before its last row, a
three-line spill page after the comparison and a rights colophon alone on a
final page; all four were removed by tightening the new prose, and none stands
in this proof. The first and third interpretations now end about a third of the
way down a page, before the forced break that opens the next section. This is
author verification; the shared-timestamp three-document build and the
independent visual review remain to be done.

### Iteration 2: repair of the second study review's finding

Revised 19 September 2026 in the same run, against study-review iteration 1.
Only `sections/40-because-i-am-good.tex`, `generation-metadata.tex` and this
record changed.

| Finding | Severity | Outcome | What was done |
| --- | --- | --- | --- |
| STU-008 | blocking | repaired | The six sentences of the third interpretation that had the study as subject or possessor were recast, and no parenthesis removed under STU-002 was restored. "The wage is the giver" now ends its sentence at "each of his own text and neither of the parable". "The contract that remains" now reads "The step rests on Augustine's argument and on no agreement between the two". The allegorical sense states the identifications with no name attached (the householder's goodness is the goodness of Christ, the good shepherd; the likeness given to each labourer alike is Christ) and gives each author as the subject of what he says: Gregory, Aquinas and Augustine of the shepherd of John 10 and his sheep and not of the parable, and Jerome of the coin, with the limit that he does not name Christ there. The anagogical sense states that the one denarius is God giving himself, gives Jerome what he says of the coin, and says that Augustine and Gregory speak each of his own text and neither of the parable. After the repair no sentence of the section names the study. |
| STU-009 | advisory | cleared | The model contribution no longer gives the packet's declared effort as the effort the stage ran at. Its qualifier field now records the packet-declared effort (high) and the host's dispatch effort (xhigh) as two separate qualifiers, as this run's intervention record states them for every author stage, in the `key=value` form the metadata gate accepts; sampling configuration stays named as unexposed. |

Evidence read at this iteration. Jerome on Matthew, PL 26, col. 142, was
re-read on the page image of the retained facsimile for the limit the
allegorical sense now states: under the lemma "Nonne ex denario convenisti
mecum?" the comment runs "Denarius figuram regis habet. Recepisti ergo mercedem
quam tibi promiseram, hoc est, imaginem et similitudinem meam: quid quaeris
amplius", and it does not name Christ. No research record was changed.

**Substantive word count: 14,223 words** (13,622 with the content of the
`\latin{}` spans removed), by the method stated above: opening 974, element
settings 2,478, the three interpretations 3,310, 3,049 and 3,849, comparison 563
(its table excluded). The repair removed 26 words, all in the third
interpretation.

The author proof is the same build path as before: 39 physical pages, inside
the 20–50-page requirement, SHA-256
`1fe5f568d193ab167ce5cb50c0eba25b21fbe59987860938e7365d3c4e5ea6b1`, built with
`make doc` at revision timestamp 2026-09-19T16:26:46Z; a second build from
unchanged sources reproduced the same bytes. The settled log carries no
overfull or underfull box, no undefined reference and no LaTeX warning; all
eight fonts are embedded; the metadata gate passed;
`tools/check-proper-components --phase artifacts --edition research` passed; and
the thirteen study-preflight checks, run by hand with this run's header, all
exit 0. The house-voice screen does not know the word "study" as a name for the
work, so the section and the five other argumentative components were also
searched for it directly: none of them names the study. A trial conversion
through `tools/web-edition` into scratch space again produced all eleven
appointed-text anchors. Page by page, the extracted text of this proof differs
from the iteration-1 proof only on pages 25 to 30, the third interpretation
from "The wage is the giver" to its end, and on page 39, where the revision
timestamp stands. All 39 pages were inspected on contact sheets of the settled
proof, and pages 25 to 30 and 39 at full size. The pagination is unchanged: the
third interpretation still ends about a third of the way down page 30, before
the forced break that opens the comparison, and the rights colophon shares the
last page with the References and the timestamp. This is author verification;
the shared-timestamp three-document build and the independent visual review
remain to be done.

### For the cold reviewer, about the research records

These were met while authoring. None was repaired here, because the research
records are the research stage's.

1. `research/interpretations.md` enters Gregory, *Hom.* 19.6, in the
   `conversion` author table, while its standing limits say nothing rests on the
   second sentence of Matthew 20:16. Gregory draws the two cautions of 19.6
   expressly from that sentence. The study reports them as drawn from a sentence
   this Mass does not read. (Resolved in `interpretations.md` on 2026-09-25.)
2. The research record describes Aquinas on Matthew pp. 258–261 as read in OCR
   only. The retained facsimile bound for p. 262 contains those pages as images.
   The study keeps to paraphrase for them, as the record directs.
3. The owner's summary of the Collect gives the petition as coming to eternal
   life and does not give the verb of the Latin. The study therefore says
   nothing about whether the prayer speaks of meriting, which the third
   interpretation would otherwise want to discuss.
4. Met at iteration 1. `research/interpretations.md`, Reading 3, says that
   Chrysostom "disputes" Augustine's second step, speaks of "Chrysostom's
   objection" and of "the one real dispute among the authors read … whether
   the willingness God opens is itself his gift", and says "This leaf does not
   adjudicate it". *Hom. in Acta* 35 addresses no such claim and says nothing
   of where the willingness comes from. The study no longer follows that
   wording; it keeps what the record rightly requires, that the difference
   between the two readings of Acts 16:14 appear beside the step it qualifies.
   (The record was brought into line with the study on 2026-09-25.)
5. Met at iteration 1. The standing limits of `research/interpretations.md`
   and the scope record say that Chrysostom, Jerome, Gregory and Aquinas
   expound the second sentence of Matthew 20:16. On the page (PL 26, 142)
   Jerome carries it in his lemma and repeats it without a comment of its own.
   The study now says so.
6. Met at iteration 1. The scope row for Chrysostom on Matthew does not record
   his second application of the rule on parables, to "No man hath hired us"
   (64.3, inside the bound locus), and the row for Aquinas on Matthew does not
   record his division of the hours or his reading of that excuse. The study
   reports all three from the bound sources, as listed under iteration 1.

## Derive-synthesis

Authored 19 September 2026 in `proper-study` v4, run `472e2eb20876b22a`, seeded
at commit `02bae3f417048707bf5f76a9ef50b3236bf60701`, at iteration 0. No
blocking, carried or advisory finding was forwarded to the stage. The concise
companion is *The Twenty-fifth Sunday in Ordinary Time, Year A: A Concise Study
of the Proper in the Roman Missal, Third Edition*, built from `synthesis.tex`
and derived from the expansive study as its third review accepted it. No
research record, no component of the study and `format.tex` were edited; the
presentation environments the first page needs were already defined there. In
`proper-components.toml` one comment line above the concise components was
brought up to date and no declaration changed.

### What was written

- `synthesis.tex`, the concise entrypoint: a compact title block naming the
  Sunday, the Missal and Lectionary no. 133, with no cover and no contents page
  before the fixed opening.
- `concise-inventory` (`sections/concise/01-inventory.tex`): the map of the
  eleven appointed elements in the order of the Mass, the two Communion
  antiphons in rows of their own marked first and second option, and beneath it
  a note that they are alternatives and the standing notice that the Scripture
  printed is the Douay–Rheims (Challoner) and not the Lectionary's approved
  English.
- `concise-overview` (`sections/concise/02-overview.tex`): exactly four rows,
  Literal, Allegorical, Moral and Anagogical. Every parenthetical name stands
  beside what that author says of his own passage, and the two sentences that
  come from the psalm and from John 10 say so.
- `concise-date-location` (`sections/concise/03-date-location.tex`): the
  Scriptural Date and Location sheet. It imports the generated chronology
  annotations once and carries one `\chronodate` cell for each of the seven
  dossiers, in the study's canonical order; the dates, relation labels,
  disputed alternatives and the unresolved narrated-event state of the Gospel
  are the study's own, unchanged. The Location cells and the explanatory rows
  are compressed so that the sheet stands whole on one physical page.
- `concise-themes` (`sections/concise/04-themes.tex`): *The Propers: Themes and
  Movement*, two pages that open on a thesis and follow the formulary from the
  Entrance Antiphon's promise to the Prayer after Communion, with the two books
  and the three relations the liturgical books state, and close by introducing
  the three interpretations.
- `concise-commentary` (`sections/concise/10-commentary.tex`): *The Propers:
  Detailed Commentary*, seven cross-proper questions and a closing comparison:
  the five hours as ages of the world or of a life; how far the pardon reaches
  and how long it waits (Isaiah and the psalm); the murmur and what the
  householder's reply decides; "So shall the last be first"; what the wage is
  (with the second reading); whose work the coming is (the Alleluia verse, the
  first Communion antiphon and the Collect); the shepherd and the prayers at
  the altar; and where the four senses of the three interpretations part.
- `concise-apparatus` (`sections/concise/90-apparatus.tex`): the scope note and
  the References for the sources this companion uses.

### What compression kept and what it set aside

All three controlling claims are stated in the themes section and developed in
the commentary, with each interpretation's strongest difficulty beside it: the
ages of the world as a received allegory and not the parable's plain sense;
the second interpretation's answer to delay as true and drawn from outside the
story, with the murmurers left little to do; and the contract that remains for
the third. The differences the study carries are kept where the argument turns
on them: what Augustine and Chrysostom each say of Acts 16:14, in their own
words, beside the step the difference qualifies, with no position on lateness
given to Augustine and neither presented as answering the other; Chrysostom
against Gregory and Aquinas on "No man hath hired us"; Augustine, Chrysostom
and Jerome on how "the last shall be first" stands to the parable, with
Aquinas recording the first two; Gregory, Jerome and Chrysostom on the
murmuring; Jerome as reporter of the ages of the world and holder of the ages
of a life; and the differing starting points of Gregory and Augustine. The
first two interpretations are called complementary and the third different in
kind, as the study calls them.

Set aside, and still in the expansive study: Hilary's and Bellarmine's glosses
of "in truth" beside Augustine's; Bellarmine's different emphasis at Psalm
118:5 and his reading of "sweet to all"; Aquinas's division of the hours at
David and the fuller list of who the eleventh-hour workers are; Gregory's
caution from the closing saying and everything he draws from the second
sentence of Matthew 20:16; Augustine on John 10:16 and at *Tract.* 47.2;
Aquinas on the manner of conversion and its parallel with the Collect's two
loves; Jerome's father who runs to meet the returning son; the comparison with
the elder son; Augustine's calculation and Gregory's thief before Peter on why
the last are paid first; Chrysostom's reading of Philippians 1:21 through
Galatians 2:20; Bede's seller of purple; and Schuster with the psalm contacts
of the Entrance Antiphon. The References were cut to match: Schuster, the
*Antiphonary*, the *Notitiae* list and the loci no longer used are absent, and
the entries for Hilary, Bellarmine, Gregory and Augustine's tractate name only
the loci the companion uses.

No evidence-dependent claim was added. Every quotation is a whole or an
unbroken part of a quotation the study prints, and the loci are the study's.
Where the study gives one joint locus for several sentences of Jerome and the
companion keeps only some of them (the ranking by faith, the wish that another
receive nothing), the column range the References give, PL 26, 140–142 or
141–142, is printed and no narrower column is claimed.

### Counts

**Substantive word count: 4,536 words** (4,335 with the content of the
`\latin{}` spans removed): themes 1,139 and commentary 3,397. The count
converts the two argumentative components through Pandoc's LaTeX reader to its
document tree with comments stripped and the leaf's inline commands declared
first, removes headings and tables, writes plain text and counts
whitespace-separated words; it excludes the map, the overview rows, the
dossier sheet, the scope note and the References. The same script gives the
study's four components that contain no table the figures this record states
for them to within four words each (2,478, 3,306, 3,045 and 3,845); it does
not drop the study's two custom table environments, so its totals for the
opening and the comparison are not comparable with those above. Against the
study's 14,223 words the companion is a little under a third of the argument.
The whole PDF extracts to 7,396 words with `pdftotext -layout`.

### Author proof and checks

`make doc` for the `-synthesis` output settles with no overfull or underfull
box, no LaTeX or pdfTeX warning, no undefined reference and no rerun request.
The proof is
`build/claude/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s51-twenty-fifth-sunday-in-ordinary-time-year-a-synthesis.pdf`:
12 physical pages, inside the 10–12-page requirement, letter size, SHA-256
`313e39578ee672cec42a347189142d9de99f2f37929917b24ced1e9be2fd5a7f`, at revision
timestamp 2026-09-19T17:31:30Z; removing the PDF and building again from
unchanged sources reproduced the same bytes. All seven font resources (TeX Gyre
Pagella and Latin Modern Mono) are embedded, subsetted and Unicode-mapped, and
the document information carries the title, the subject and the tracked
modification date.

The settled auxiliary file (SHA-256
`1ec0ec3d5e4c5de9e0bc17565f08d0cff7b6b897873a36ab33c9545b0a06ee64`) records the
physical pages the presentation contract fixes: inventory start and end,
overview start and end and the four sense markers on page 1; chronology start
and end on page 2; themes start on page 3 and end on page 4; commentary start
on page 5. `tools/check-proper-components --phase artifacts --edition
synthesis` passes, and so do `python3 scripts/_proper_study.py check … --phase
content --edition synthesis --require-presentation`, the twelve
`check-content-preflight` checks the synthesis gate names, run by hand with
this run's header, and `tools/check-generation-metadata` against the rendered
PDF. The house-voice screen does not know "study" or "companion" as names for
the work, so the four body components were also searched for both words
directly: neither names the work there.

The proof, its auxiliary file, log and extracted text, the build, preflight,
artifact and metadata logs and the counting script are kept with their digests
under `build/tpt-runs/472e2eb20876b22a/artifacts/derive-synthesis-0000/proof/`,
and the page rasters and contact sheet made with `tools/tpt pdf-review` in the
dedicated child `rasters/`. All twelve pages were inspected on the contact
sheet of the final proof. Pages 1, 2, 4, 10, 11 and 12 were read at full size
during composition and page 1 again on the final proof; one sentence of the
Gospel dossier was reordered after the last full-size reading of page 2, and
that page was checked again on its thumbnail, its extracted text and the
settled markers. The extracted text of pages 3 to 10 was read through. The map and the four rows stand together on
page 1 and rule to the same measure; the dossier stands whole on page 2 with
about a line to spare; the themes section fills pages 3 and 4; the scope note
begins on page 10 and the References on page 11; and the revision timestamp
and the rights colophon share page 12 with the end of the References. Page 5
ends about three lines short, where the second question's heading moves to the
next page with its text. On the way to twelve pages the first drafts ran to
nineteen: a four-senses table by interpretation was replaced by the closing
prose comparison, Latin was dropped wherever the English beside it carried the
point, and the material listed above was set aside.

The shared generation record carries a second contribution for this stage and
the revision timestamp above. The expansive study was rebuilt at that
timestamp: 39 pages, SHA-256
`fa9be4ca35112f0ca3bf568da81431879913bd952849b8226009c4ab4740697b`, its
extracted text identical to the accepted iteration-2 proof except for the
timestamp line, and its artifacts check passes. This is author verification;
the shared-timestamp three-document build and the independent visual review
remain to be done.

### For the cold reviewer, about upstream records

1. The manifest names `research/interpretations.md` and `research/scope.md` as
   references of the concise components. Those records still carry the
   sentences the study review's standing observation lists (Chrysostom said to
   dispute or object to Augustine's second step; Jerome among those who expound
   the second sentence of Matthew 20:16; Chrysostom's rule said to tell against
   the ages of the world). The companion follows the accepted study at each of
   these points and not the records, and states no order of priority or
   independence among the witnesses (RES-017). Nothing was repaired, because
   the records are the research stage's.
2. No other upstream defect was met while deriving. The study's three
   interpretations, element settings and comparison answered every question
   the concise argument put to them.

## Derive-homily

Authored 19 September 2026 in `proper-study` v4, run `472e2eb20876b22a`, seeded
at commit `02bae3f417048707bf5f76a9ef50b3236bf60701`, at iteration 0. No
blocking, carried or advisory finding was forwarded to the stage. The homily is
*The Twenty-fifth Sunday in Ordinary Time, Year A: The Wage and the Giver*,
built from `homily.tex` for an adult parish assembly and derived from the two
studies as their reviews accepted them. No research record, no component of
either study and `format.tex` were edited; the homily's type is set inside
`homily.tex`. In `proper-components.toml` the comment line above the homily
components was brought up to date and no declaration changed.

### What was written

- `homily.tex`, the entrypoint: a compact title block naming the Missal,
  Lectionary no. 133 and the date; the spoken body in one group at 13pt on
  18pt leading, unjustified, with a paragraph space and a wider space between
  movements; a page break; the terminal note; the shared generation record
  and the rights colophon.
- `homily-body` (`sections/homily/10-homily.tex`): the speech, in six
  movements with no headings: the line at evening and the complaint, with the
  question what the first-hired have lost; the householder's answer as payment
  and gift, the psalm's two words, and the evil eye; the first reading as the
  reason, its contrast of thoughts said of pardon; what the denarius is, why
  it cannot be divided, and Paul; the two kinds of hearer; and the prayers of
  the Mass, the second line at Communion, and one response for the week.
- `homily-note` (`sections/homily/90-note.tex`): audience and occasion,
  spoken length and arithmetical pace, relation to the reviewed
  interpretations, the route of each quoted or reported text, exact loci, and
  References for the nine sources the homily uses.

### The argument and its relation to the reviewed interpretations

The homily preaches the third interpretation (`gift`, *Because I Am Good*)
joined to the second (`conversion`, *Seek the Lord While He May Be Found*).
The studies call the first two interpretations complementary and the third
different in kind, and record that all three take the householder as God, the
denarius as eternal life and the first reading's contrast of thoughts as a
statement about mercy; the combination stands on that ground. From `gift`:
Augustine's payment and gift (*Sermo* 87.4) and the equal wage with unequal
brightness (87.6); Aquinas on grief at goodness (*Super Matt.*, p. 262) and on
mercy against requital (*Super Isaiam* c. 55); Jerome on the wish that another
receive nothing and on the coin as the king's image (PL 26, col. 142);
Augustine on calling in truth and God giving himself (*Enarr.* 144.22). From
`conversion`: Chrysostom's two kinds of hearer (*Hom. in Matt.* 64.4) and
Augustine against delay (87.8).

One difference bears on the argument and is kept in the speech. For Chrysostom
no one murmurs in the kingdom and the complaint is a device of the story
(64.3); the `gift` interpretation makes the murmur the point. The speech quotes
Chrysostom's sentence and applies the murmur to its hearers now and not to the
saved. The qualification that the saints differ in brightness while equal in
living for ever is spoken beside the claim that the wage cannot be divided.
The contract with the first-hired is kept ("Justice to the one, a gift to the
other").

Each Father is credited only with what he says of his own passage. Four
connections are spoken in the preacher's voice with no name attached, as the
study draws them from the wording of the texts: the psalm's two words as the
householder's two dealings; Paul adding hours where the murmurers reckon
theirs; the keeping and the arriving both inside the Collect's prayer; and
those who come to Communion hired at different hours and given the same food,
the pledge of the one wage. "The first reading was chosen to stand beside this
Gospel" paraphrases *Praenotanda* 106 and claims no more design than the
Lectionary states.

Left to the studies: the `economy` interpretation; the saying on first and
last, on which Augustine, Chrysostom and Jerome differ; the Alleluia verse,
with what Augustine and Chrysostom each say of Acts 16:14; the Prayer over the
Offerings; both Communion antiphons; Hilary, Gregory, Bede and Bellarmine. The
speech uses the Gospel, the first reading, the psalm, the second reading, the
Entrance Antiphon, the Collect, Communion and the Prayer after Communion.

### Texts, rights and what the speech does not assert

Scripture is spoken in the Douay–Rheims (Challoner) at Mt 20:12, 13–14, 15;
Isa 55:7–8; Ps 144:8, 17, 18; Phil 1:21, 23, 24, and the speech names the Douay
Bible just before it first quotes it, because the assembly has heard the
Lectionary's approved English, which is reproduced nowhere. The Entrance
Antiphon, the Collect and the Prayer after Communion are described after the
study's descriptions and are not quoted; nothing is said of the verb of the
Collect's petition, as the study says nothing of it. Because another chant may
lawfully replace the Entrance Antiphon, the speech says what "the antiphon the
Missal sets at its entrance" says and does not say that the assembly sang it.
Augustine's *Sermo* 87 and Chrysostom are quoted in the NPNF English the study
prints; Jerome, Aquinas and Augustine's *Enarratio* are reported without
quotation marks in English that renders the Latin the study prints. The speech
contains no anecdote, no first-person experience, no clerical identity, no
recited prayer and no stage direction, and it ends as preaching.

### Evidence re-read at this stage

Every sentence quoted or reported was read again in its witness; none of it
changes a research record.

- Douay–Rheims: Mt 19:27 and 20:1–16, Isa 55:6–9, Ps 144:8–9 and 17–18 and
  Phil 1:20–27 in the tracked verse files; every quotation matches.
- Augustine, *Sermo* 87.4, 6, 8 and 10–11, and Chrysostom, *Hom. in Matt.*
  64.3–4, in the tracked NPNF texts; every quotation matches, and the two
  reported sentences (the saints' brightness, 87.6; the eleventh hour promised
  and the seventh not, 87.8) follow the English closely.
- Jerome, PL 26, col. 142, on the page image of the retained facsimile:
  "Denarius figuram regis habet. Recepisti ergo mercedem quam tibi promiseram,
  hoc est, imaginem et similitudinem meam: quid quaeris amplius; et non tam
  ipse plus accipere, quam alium nihil accipere desideras". Both sentences
  stand in col. 142, which the note cites.
- Aquinas on Matthew, p. 262 of the retained Venice facsimile, on the page
  image: "sed nequam est proprie qui de bonitate dolet". Aquinas on Isaiah,
  p. 556 of the retained Parma facsimile, on the page image: "Vos impii, ego
  pius; vos ultionem cogitatis, ego misericordiam".
- Augustine, *Enarr. in Ps.* 144.22: the augustinus.it page was fetched again
  over verified TLS into scratch space; it has the byte count and SHA-256 the
  scope record gives for the research stage's delivery, and reads "quanto
  beatior eris, cum seipsum tibi dederit? … Ergo qui Deum ipsum … praeponit
  his omnibus rebus quas accepit, ipse invocat Deum in veritate". It remains
  the sentence's only witness here, and the note says so. Nothing was
  registered or retained.

### Spoken length, pace and rehearsal

**Spoken word count: 1,482 words.** The count converts `10-homily.tex` through
Pandoc's LaTeX reader to plain text and counts whitespace-separated words; a
count of the uncommented source lines, with its two ties opened, gives the
same figure. At 130 words a
minute that is about 11.4 minutes, at 125 about 11.9, at 120 just over 12.3.
These are arithmetic on the word count. No speaker has delivered the text and no
delivery was timed.

The prose was read through in full, silently and not aloud, for sense,
sentence length and ease of speech. What the rehearsal changed: a first draft
of 1,764 words was cut to 1,482 by removing the title the *Ordo* sets over the
Gospel, the Alleluia verse, Aquinas's bailiff and king and a separate paragraph
on the psalm, whose two words moved beside the householder's answer; the one
sentence over fifty words (Chrysostom's two kinds of hearer) and the Collect
sentence were each split in two; "requital" is glossed at once as "paying
back", "denarius" as the coin agreed for the day and the Douay's "penny"; no
sentence needs an ellipsis to be read, and Isaiah 55:7–8 is read whole. The
longest sentences that remain are Isaiah 55:7, of 36 words, and two of the
speech's own, of 33; the mean is under fifteen words.

### Author proof and checks

`make doc` for the `-homily` output settles with no overfull or underfull box,
no LaTeX or pdfTeX warning, no undefined reference and no rerun request. The
proof is
`build/claude/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s51-twenty-fifth-sunday-in-ordinary-time-year-a-homily.pdf`:
6 physical pages, letter size, SHA-256
`99a0877432a268bd56b92c4cfe45011d059a00ab42498113def2f376457bd70f`, at revision
timestamp 2026-09-19T18:27:31Z; removing the PDF and building again from
unchanged sources reproduced the same bytes. All seven font resources (TeX Gyre
Pagella and Latin Modern Mono) are embedded, subsetted and Unicode-mapped, and
the document information carries the title, the subject and the tracked
modification date. `tools/check-proper-components --phase artifacts --edition
homily` passes, as do `python3 scripts/_proper_study.py check … --phase content
--edition homily --require-presentation`, the twelve `check-content-preflight`
checks the homily gate names and `provenance-matches-run`, run by hand with
this run's header, and `tools/check-generation-metadata` against the rendered
PDF.

All six pages were inspected on a contact sheet of the final proof and each
of them at reading size. The speech fills pages 1 to 3 and about half of page 4;
the note stands whole on page 5; the References, the revision timestamp and
the rights colophon share page 6. Two ties keep the last words of the first
quotation together, so that no paragraph of the speech ends on a single
word. At 12.5pt on 18pt the speech left its fourth
page well under half full and the note ran over onto the References page; at
13pt with a slightly wider paragraph space, and with the note shortened, each
part stands on its own pages. The note fills page 5 to its last line, so a
later addition to it will carry over.

The shared generation record carries a third contribution for this stage and
the revision timestamp above. The expansive study and the concise study were
rebuilt at that timestamp: 39 pages, SHA-256
`fd3a4d13f7bb980bbe3bb6025dac194997add5bf40a9f53eb4bced31af81dcb8`, and 12
pages, SHA-256
`09275d9d8d97c81068c262dc7cab16f24744ce9f1b0f1af9bce8fd39e2cfa96f`; the extracted
text of each is identical to its preceding proof except for the timestamp
line, and the artifacts check passes for both. The evidence scopes of the
study review and the concise review, recomputed with `python3
scripts/_proper_study.py seal`, are what those reviews sealed: the same files
with the same digests, the same component contract and the same generation
provenance. This is author verification; the shared-timestamp three-document
build and the independent visual review remain to be done.

### Limits that remain

The Scripture spoken is the Douay–Rheims and differs in wording from what the
assembly hears. The approved English of the Missal was read in no witness, so
the three Missal texts are spoken of only as the study describes their Latin.
Augustine's sentence on Psalm 144:18 has an electronic text as its only
witness. Whether the United States Lectionary admits another Alleluia verse was
not determined, and the speech does not use the verse.

### For the cold reviewer, about upstream records

1. The manifest names `research/interpretations.md` and `research/scope.md` as
   references of the homily components. Those records still carry the
   sentences the study review's standing observation lists (Chrysostom said to
   dispute or object to Augustine's second step, among them). The homily does
   not use Acts 16:14 or that step, and follows the accepted study wherever it
   and the records differ. Nothing was repaired, because the records are the
   research stage's.
2. The studies cite Jerome's sentence on the wish that another receive
   nothing at PL 26, 141–142. On the page image it stands in col. 142, directly
   after the sentence on the coin. The homily's note cites col. 142; the
   studies' wider range is not wrong.
3. No other upstream defect was met while deriving.

## Build-artifacts

Completed 19 September 2026 in `proper-study` v4, run `472e2eb20876b22a`, seeded
at commit `02bae3f417048707bf5f76a9ef50b3236bf60701`, at iteration 0. No
blocking, carried or advisory finding was forwarded to the stage.

### What was built, and what was not changed

The author proofs of all three outputs, with their auxiliary files, logs and
metadata stamps, were moved out of the build tree, and each output was then
built from nothing with `make doc DOC=<output-id> PROVIDER=claude`: the bare
document ID, `-synthesis` and `-homily`. Each build settled in two passes and
passed the Makefile's declared-input and metadata verification. No layout
repair was needed and none was made. No render-relevant source, accepted prose,
evidence record, component declaration, `format.tex` or generation declaration
was edited by this stage, so the shared generation record stands as the homily
stage left it, at revision timestamp 2026-09-19T18:27:31Z with its three
contributions; a stage that changes no render source adds none. The only
tracked files this stage wrote are this entry and the snapshot receipt
`research/artifacts.json`.

| Output | Pages | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| research | 39 | 330921 | `fd3a4d13f7bb980bbe3bb6025dac194997add5bf40a9f53eb4bced31af81dcb8` |
| synthesis | 12 | 216677 | `09275d9d8d97c81068c262dc7cab16f24744ce9f1b0f1af9bce8fd39e2cfa96f` |
| homily | 6 | 179884 | `99a0877432a268bd56b92c4cfe45011d059a00ab42498113def2f376457bd70f` |

The PDFs stand at the mirrored `build/claude/` paths of the three output IDs.
All three reproduce, byte for byte, the proofs the derive-homily entry records
at the same timestamp, and the concise auxiliary file reproduces the digest the
derive-synthesis entry records
(`1ec0ec3d5e4c5de9e0bc17565f08d0cff7b6b897873a36ab33c9545b0a06ee64`). The study
is inside the 20–50-page requirement and the concise study inside the
10–12-page requirement.

### Logs, structure, fonts and extraction

- **Logs.** The three settled logs carry no fatal error, no LaTeX, package or
  pdfTeX warning, no undefined reference or citation, no overfull or underfull
  box, no missing character, no font substitution and no rerun request. The
  first pass of the study and of the concise study carries the ordinary notice
  that labels may have changed, which the second pass clears; it stands in the
  build transcript and not in the settled log.
- **Physical pages of the concise opening.** The settled auxiliary file records,
  by `\abspage`: inventory start and end, overview start and end and the four
  sense markers on page 1; chronology start and end on page 2; themes start on
  page 3 and end on page 4; commentary start on page 5. The printed folio equals
  the physical page at every marker, so no counter reset stands in for a page.
  `tools/check-proper-components --phase artifacts` passes for each edition and
  for the leaf as a whole.
- **Structure.** `pdfinfo`, `pdffonts` and `pdftotext -layout` exited 0 for
  every PDF, and Ghostscript parsing with `-q -dNOPAUSE -dBATCH
  -sDEVICE=nullpage -dPDFSTOPONERROR` exited 0 with no diagnostic on each. Every
  page of every PDF is letter size; each file is PDF 1.7, unencrypted and
  untagged, carries its title and subject, a modification date equal to the
  tracked revision, no creation date and no trailer ID, and contains no raster
  image. qpdf, mutool and pypdf are not installed here, so no check by them is
  claimed.
- **Fonts.** The study has eight font resources and the concise study and the
  homily seven each: TeX Gyre Pagella in regular, bold and italic, and Latin
  Modern Mono. Every one is Type 1, embedded, subsetted and Unicode-mapped.
- **Extraction.** Each extracted text was read through in full. The three have
  39, 12 and 6 nonempty pages and 20,923, 7,396 and 2,585 words; none contains a
  replacement character or an unresolved `??`; each shows the revision
  timestamp exactly once; and none shows a workflow digest, run ID, seed commit,
  model identity or machine path. Reading order is intact in the map, the
  four-senses rows, both dossier sheets, the comparison table, the branch table
  and the References. Verse-numbered Scripture blocks extract with a blank line
  after their first line, and one paragraph of the study with a one-space
  indent; both are effects of the layout extractor on raised verse numbers and
  hanging quotation marks, and nothing is displaced on the page.
- **Size.** About 8.3, 17.6 and 29.3 KiB a page; all three are below the 1 MiB
  and 75 KiB-a-page review triggers.

### Snapshot, gate check and rasters

`python3 scripts/_proper_study.py snapshot --provider claude --document
<canonical-id>` wrote `research/artifacts.json`: the three PDF digests above, 26
render inputs (the leaf's TeX sources, its component manifest and the shared
preamble) and four pagination-evidence files, the settled log and auxiliary
file of the study and of the concise study. Every recorded digest was
recomputed independently and matches. `python3 scripts/_proper_study.py check
--provider claude --document <canonical-id> --date 2026-09-20 --phase artifacts
--require-presentation`, the artifact gate's own command, then exited 0, as did
`tools/check-generation-metadata` against each rendered PDF. The four accepted
content seals (research, study, synthesis and homily reviews) were recomputed
with `scripts/_proper_study.py seal`, before and after this entry was written,
and each equals the evidence scope its accepted review recorded. Nothing was
rebuilt after the snapshot.

`tools/tpt pdf-review --output
build/tpt-runs/472e2eb20876b22a/artifacts/build-artifacts-0000/rasters` with the
three PDFs exited 0 and wrote 57 page rasters, 57 thumbnails and four contact
sheets, with a receipt that binds them to the three PDF digests above. That
directory holds only the helper's output. The sibling `proof/` directory holds
exact copies of the three PDFs, their settled logs and auxiliary files, the
study's contents file, the three build transcripts, the PDF-information, font,
Ghostscript and extraction outputs, the marker lines, the check outputs, a copy
of the snapshot and a `SHA256SUMS` over all of it.

The four contact sheets, pages 1 and 2 of the concise study, page 1 of the
homily and page 39 of the study were opened to confirm that the build is whole:
no page is blank, clipped or overprinted, the concise map and four rows stand
together on page 1, the dossier stands whole on page 2, and each final page
carries the References' end, the timestamp and the rights colophon together.
That is a build check and not the visual review. No page-by-page visual
acceptance is claimed, and no PDF was installed.

### For the visual reviewer

No semantic defect was met while reading the extracted texts. The points below
are matters of presentation that the build cannot settle and this stage did not
alter, since every one lies in a source that a content review has sealed.

1. Study pages 18, 30 and 34 end short before a forced break: the first
   interpretation ends about two fifths of the way down page 18, the third
   about a third of the way down page 30, and the dossier's continuation fills
   about a third of page 34 before the Liturgical Resolution appendix opens on
   a fresh page, as the profile requires of that appendix.
2. The homily's speech ends about half way down page 4, before the forced break
   to the note, and its final page is under half full.
3. On page 1 of the homily the two ties that keep "and the heats" together
   leave the line before them visibly short in the unjustified setting.
4. On page 2 of the concise study two Date cells run to the edge of the
   measure ("c. A.D. 40–42;" and "A.D. 61; A.D."). The log reports no overfull
   box there.
5. The running head names the section that begins on a page, so a page that
   opens with the tail of the preceding section carries the next section's name
   (study pages 4, 8, 36 and 38; concise pages 10 and 11). The final page of
   each document carries no running head and no folio, which is the shared
   colophon's behaviour and not this leaf's.
6. The two URLs in the References break across lines inside the address.

### Limits that remain

Those of the three preceding entries and of `research/scope.md` stand
unchanged. Structural checking rests on Poppler and Ghostscript alone. The
snapshot records bytes and declared inputs and is not a claim of review.

## Generate-web

Completed 19 September 2026 in `proper-study` v4, run `472e2eb20876b22a`, seeded
at commit `02bae3f417048707bf5f76a9ef50b3236bf60701`, at iteration 0. No
blocking, carried or advisory finding was forwarded to the stage.

### What was converted

Only the canonical study was converted, with `tools/tpt web-edition --provider
claude --output build/web <canonical-id>`; no synthesis or homily web leaf was
made. The declaration `web-edition.toml` (eligible, no blocking construct)
passes `tools/tpt check-web-edition --document <canonical-id>`. No leaf source,
component declaration, `format.tex` or generation record was edited, so the
shared generation record stands at revision timestamp 2026-09-19T18:27:31Z and
the built PDFs and `research/artifacts.json` are untouched.

### A conversion defect found and repaired

The first conversion exited 0 but silently dropped words. In the appointed text
of the Alleluia verse the study quotes Acts 16:14 with its unappointed first
half in brackets, `\notread{And a certain woman named Lydia, a seller of
purple, of the city of Thyatira, one that worshipped God, did hear:}`, at the
start of an `englishwitness` block whose opening ends in `\nopagebreak`. Pandoc
expands `\notread` before `\nopagebreak` looks ahead, takes the bracket for that
command's optional argument and discards it; TeX sets it, and the PDF shows it.
The whole clause was missing from the web edition. No existing audit covered
it.

The defect lay in the converter, not in the source, and was repaired there.
`tools/web-edition` now hands pandoc every command whose replacement text opens
with `[` behind an empty group, which sets nothing and ends the lookahead. A
new audit refuses any conversion in which the words of such a call do not
arrive. Two regression tests were added to
`tools/tests/test_web_edition_conversion.py`: a conversion test, which fails
against the previous converter, and an audit test. The known-deletions
paragraph of `guidance/web-editions.md` records the case. The converter's two
test modules (85 tests) and `tests/tools/web-edition.test` pass. Every leaf of
both providers was converted before and after the change. The outputs are
byte-identical and the failure sets identical, except for this leaf. Here the
only change is the restored clause. This leaf is the only one in the corpus
whose macros open with a bracket.

### What the edition contains

The generated file has 550 lines, 121,097 bytes and SHA-256
`2bd7f5908e264581a4e66b209dc825266d43b51c688d4887ddea77ff4cd3586d`. It has
the title as its only first-level heading, followed by the PDF subject and the
title-page lines. It then carries the opening with its map table, the eleven
appointed elements under their `proper-<key>` anchors, the element-by-element
settings, and the three interpretations as separate second-level sections, each
closing with its own Literal, Allegorical, Moral and Anagogical senses. The
comparison table, the Scriptural Date and Location table, both appendices and
the References with their two links follow. It ends with the revision timestamp
and the rights colophon. It carries no model identity, effort or run detail.

The extracted text of the built study PDF (SHA-256 `fd3a4d13…81dcb8`, recorded
above) was compared word by word with the Markdown after the repair. Every
difference falls in the table of contents, which the converter omits because
the headings replace it; the running heads; the table headers that the PDF
repeats on continuation pages; the title and subject that the converter prints
at the head; hyphenation in narrow table cells; and the order in which the
extractor reads table cells. No word of the study's text is missing.

### For the web reviewer

1. Each four-senses label ("Literal.") is set as plain text followed by a line
   break, not in bold. This is how the converter writes a `description` list,
   and the tracked 1962 claude edition shows the same thing.
2. In the Scriptural Date and Location table each full-width note stands in
   the row's first cell, padded with empty cells. `guidance/web-editions.md`
   declares this the deliberate handling of a `\multicolumn` span.
3. The PDF's table of contents does not appear.

### Snapshot

`python3 scripts/_proper_study.py snapshot-web --provider claude --document
<canonical-id>` wrote `research/web-artifact.json`, which binds the generated
path to the digest above. That receipt records conversion identity, not
approval. Nothing was installed under `web/`, and no release record or catalog
was edited.

## Install-publication

Completed 19 September 2026 in `proper-study` v4, run `472e2eb20876b22a`, seeded
at commit `02bae3f417048707bf5f76a9ef50b3236bf60701`, at iteration 0. No
blocking, carried or advisory finding was forwarded to the stage.

### Reviews completed before installation

The run's own retained results record these review and gate outcomes; nothing
below is inferred from an author's account.

| Stage and iteration | Result | Findings |
| --- | --- | --- |
| research-review 0 | CHANGES_REQUIRED | 5 blocking, 7 advisory |
| research-review 1 | CHANGES_REQUIRED | 1 blocking, 3 advisory |
| research-review 2 | PASS | 3 advisory |
| study-review 0 | CHANGES_REQUIRED | 2 blocking, 5 advisory |
| study-review 1 | CHANGES_REQUIRED | 1 blocking, 1 advisory |
| study-review 2 | PASS | none |
| synthesis-review 0 | PASS | 3 advisory |
| homily-review 0 | PASS | 2 advisory |
| artifact-gates 0 | PASS | none |
| visual-review 0 | PASS | 1 advisory (VIS-001) |
| web-review 0 | PASS | 2 advisory (WEB-001, WEB-002), 3 observations |

Before anything was installed, each accepted seal was recomputed with
`scripts/_proper_study.py seal`: research (review contract `proper-study-v3`),
study, synthesis, homily, visual and web. Each equals the evidence scope that
its accepted result records, so no reviewed source, artifact or conversion has
moved since its review.

### PDFs

Before installation `python3 scripts/_proper_study.py check --provider claude
--document <canonical-id> --date 2026-09-20 --phase artifacts
--require-presentation` exited 0. So `research/artifacts.json` still described
the built bytes, their 26 render inputs and four pagination-evidence files
exactly as the visual review sealed them. The three PDFs were then installed
one at a time with the normal recipe, its declared dependencies and checks, and
nothing suppressed: no `-o`, no `-t`, no touched timestamp, and no edit to an
accepted source or to the revision timestamp.

```sh
make install-doc DOC=<canonical-id> PROVIDER=claude
make install-doc DOC=<canonical-id>-synthesis PROVIDER=claude
make install-doc DOC=<canonical-id>-homily PROVIDER=claude
```

Make found all three build PDFs current and retypeset none of them. It ran the
source check and the generation-metadata verification each install depends on,
and then copied the bytes. The standing-findings file
`evaluations/blocking-findings-v1.toml` changed after the build, and it did not
make the two derived PDFs stale. The derived-source rule in the Makefile now
prunes `evaluations/`, which settles the defect an earlier production reported.
The build PDFs, logs and auxiliary files keep their build-stage modification
times, and the artifact check above still exits 0 after installation.

| Output | Pages | Bytes | SHA-256 (accepted, build and installed) |
| --- | ---: | ---: | --- |
| research | 39 | 330921 | `fd3a4d13f7bb980bbe3bb6025dac194997add5bf40a9f53eb4bced31af81dcb8` |
| synthesis | 12 | 216677 | `09275d9d8d97c81068c262dc7cab16f24744ce9f1b0f1af9bce8fd39e2cfa96f` |
| homily | 6 | 179884 | `99a0877432a268bd56b92c4cfe45011d059a00ab42498113def2f376457bd70f` |

Each installed file at `pdf/claude/<output-id>.pdf` and each build file hashes
to the value the visual review sealed. No hash differs, so no artifact defect
is reported and no review boundary is reopened.

### Web edition

The reviewed conversion `build/web/claude/<canonical-id>.md` was copied byte for
byte to `web/claude/<canonical-id>.md`: 121,097 bytes, SHA-256
`2bd7f5908e264581a4e66b209dc825266d43b51c688d4887ddea77ff4cd3586d`, equal to
`research/web-artifact.json` and to the web review's seal, and `cmp` clean. The
file was staged, so `git ls-files --error-unmatch` proves it is tracked. Only
this one file was installed, not the provider-wide `install-web-editions`
target. No synthesis or homily web leaf exists, and the canonical study remains
the sole web authority.

### Release records and catalog

No release record for these outputs existed, so none was overwritten. Three
were created with `make add-publication ID=<output-id>
CATALOG=library/novus-ordo-liturgy.md PROVIDER=claude STATUS=alpha`, one for
each PDF. Each names schema version 1, its own exact output ID, the
postconciliar catalog `library/novus-ordo-liturgy.md`, status `alpha` and the
standing authorization `perpetual-public-repository-2026`.

In `library/novus-ordo-liturgy.md` the existing row for the Twenty-fifth Sunday
in Ordinary Time is the only row changed, and in it only the Year A cell. The
Claude links were appended after the ChatGPT edition's four links, in the order
of the manifest's output labels: Research PDF, Synthesis PDF, Homily PDF and
then the web page. The cell already holds another provider's links, so they are
labelled `Claude Research PDF`, `Claude Synthesis PDF`, `Claude Homily PDF` and
`Read Claude`, which follow the provider-qualified form of the page's other
shared cycle cells. The ChatGPT links and labels, the B and C cells and every
other row are untouched, and no companion row was added. The one canonical
marker added is `claude:<canonical-id>`. `release/public-alpha.json` names
`gpt` as primary provider, so the primary-provider rule requires the provider
prefix. The unprefixed marker for the ChatGPT edition is left as it was.

### Derived catalogue, release bindings and source inventory

`tools/tpt document-library structure` regenerated
`src/web/data/structure/documents/corpus.json`. The only change is a Claude
edition added to this work, carrying the study, its two companions, the web
page, the three contribution records of the generation record and this run's
`produced` identity. With it the aggregate counts moved from 195 to 196
documents, 221 to 224 issues and 6,258 to 6,297 pages, and the model and
provider tallies each rose by one. The ChatGPT edition of the work is
unchanged. The tool kept the recorded extent of one uninstalled edition that is
not built in this working tree, rather than dropping it.

The release refresh was limited, under the scoped-refresh rule, to the three
reader-facing paths this stage changed: `make refresh-release-bindings ADOPT=1
ONLY="library/novus-ordo-liturgy.md
src/web/data/structure/documents/corpus.json web/claude/<canonical-id>.md"`.
It made five changes: the new web edition adopted, the catalog page and the
projection re-recorded, and the rights table and its digest rewritten.
`make check-release-bindings` had named exactly those three paths beforehand,
so no concurrent or unrelated change was adopted.

`make check-publication-inventories` refused the tree as it stood. The Claude
publication inventory did not list this leaf, its source-bearing files or the
Week XXV owner's `propers/verified.md`. It also held superseded digests for the
edition registry's `README.md`, `formula-dispositions.md` and
`occurrences-2026.md`, which this production's research checkpoint had changed.
`tools/source-inventory refresh` rewrote the inventory from the current tree,
and nothing else moved: 53 to 54 publications and 1,248 to 1,285 source-bearing
files. The new publication entered the classification review as `unresolved`.
Its categories were then set from the leaf's own 87 bindings and the sources
its References name, and applied with `tools/source-inventory classify`:

- `scripture`: the Douay–Rheims and Clementine Vulgate verse texts, and the
  Nova Vulgata;
- `liturgical`: the Missale Romanum 2002, its rubrics, calendar and norms, the
  2008 variation list, the Ordo lectionum Missae, the Lectionary, the General
  Instruction, the Antiphonary, and the Ambrosian Missal as a lead;
- `patristic`: Chrysostom, Augustine, Gregory, Jerome, Hilary and Bede;
- `scholastic`: Aquinas and Bellarmine;
- `historical-primary`: the Migne, CSEL, Venice and Liège printed volumes read
  in facsimile;
- `institutional-current`: the USCCB 2026 liturgical calendar, its daily
  readings for 20 September 2026 and its NABRE introduction to the Psalms;
- `secondary`: Schuster and the Catholic Encyclopedia;
- `finding-aid`: the postconciliar propers index and the calendar tools that
  `research/context.md` uses only as finding aids;
- `repository-internal`: the shared chronology corpus and the generated
  chronology records.

Two categories that neighbouring leaves carry are deliberately absent. The
records use no code of canon law and no conciliar, papal or doctrinal
magisterial text: the liturgical law this leaf does use — the General
Instruction, the universal norms for the liturgical year and the general Roman
calendar, and the 2008 variation list — is printed in the Missal itself and is
recorded under `liturgical`. No classical, prayer-devotional, archival or
dataset source occurs either. The inventory records this entry's own digest, so
it was refreshed after the entry was written.

### Publication-gate evidence

Each terminal check was run in this working tree after the work above, and
each exits 0:

- `python3 scripts/_proper_study.py check --provider claude --document
  <canonical-id> --date 2026-09-20 --phase publication --require-presentation`.
  It covers build and installed byte identity for all three outputs, the exact
  release IDs and owning catalog, one catalog row linking all three PDFs and
  the canonical web page, exactly one canonical marker, the web receipt and the
  installed edition against the reviewed conversion, the Markdown tracked, no
  companion web authority, and `check-web-edition`.
- `make check-release-bindings`: 0 stale bindings.
- `tools/tpt public-alpha check --provider claude --document <canonical-id>`:
  scoped policy valid for the three outputs; global source, release and
  authorization records valid for 224 publications.
- `tools/tpt document-library check --provider claude --document
  <canonical-id>`, which confirmed all three titles against the built PDFs,
  and `tools/tpt document-library structure --check`.
- `make check-web-editions-current`: tracked web editions match current
  sources.
- `make check-publication-inventories`, which includes `check-source-graph`.

These are this stage's own runs of the gate commands and not an acceptance.
The terminal program gate decides acceptance, and nothing has been committed.

### An upstream defect reported, not repaired here

`make check-sources` fails in this tree, and not on anything this stage wrote.
`tools/source-reader structure --check` reports that the tracked browser
projection `src/web/data/structure/sources` has drifted from the source
records. Regenerating it into a scratch directory shows thirteen differences,
and every one of them belongs to a source record this production's research
stage registered: the General Instruction's 2011 edition, the Missale Romanum
2002, the 2010 ICEL Antiphonary, the Ordo lectionum Missae 1981, Hilary in CSEL
22, Migne PL 24, 26, 37 and 92, the Venice Aquinas, the USCCB daily readings and
its 2026 liturgical calendar, and the projection index. The research checkpoint
commit added seventeen such records and did not regenerate the projection.

The defect is the research owner's and is reported rather than absorbed. This
stage repaired wiring only, and the browser projection is neither this leaf's
publication wiring nor a member of the terminal publication gate, whose checks
all pass. It does gate deployment: `make check-deployment-sources` fails until
`tools/source-reader structure` is run and the result is committed, with the
release bindings then refreshed for exactly those projection paths.

### Limits that remain

Those of the earlier entries, of `research/scope.md` and of the standing
advisories stand unchanged. The public-alpha check is scoped to this leaf's
three outputs and is not a deployment verification. The Claude publication
inventory records the current digest of every source-bearing file in the leaf,
the standing-findings file among them. A later write into the leaf, such as an
archive of this run, makes that inventory stale until it is refreshed again.

## Postconciliar chronology consumer repair — 21 September 2026

This is a subsequent authoring and repair record, not a new workflow acceptance.
Earlier review dispositions, build hashes, page counts and installation records
above describe their historical bytes, not the current chronology or format
revision. In particular, the earlier statement that critical positions appear
without figures is superseded by the current dossier and scope. No engine-owned
result or archive was changed.

The terminal and concise dossiers now distinguish Isaiah's traditional
ministry attribution from composition, and from the separately attributed
critical late-exilic prophecy horizon. The tentative collection of Isaiah
1–35 does not date chapter 55 or the whole book. Matthew's NABRE position is
the open post-A.D. 70 boundary, probably at least a decade later, not a bounded
date in the 80s. Traditional alternatives retain their unequal warrants.
Writing place, first readership and narrative setting remain distinct,
including the qualifications on Matthew, John, Acts and Philippians. Psalter
bounds do not supply precise individual dates or a date of final assembly.
The composed Entrance remains distinct from Scripture, but the official ICEL
Antiphonary's express identification of Psalm 36[37]:39–40 now enters the
scriptural inventory as `identified-basis`, not as an adaptation.

`research/scope.md` records the retained witnesses actually inspected and the
limits of those checks. Both apparatus components, used references, source
bindings and review-dependency explanations have been reconciled with that
scope. There are 94 valid publication bindings and eight scriptural elements
with 18 chronology assertions. No shared corpus addition was required, and no
generated chronology annotation was hand-edited by this repair.

All three canonical Make builds exited 0: **31 research, 10 synthesis and
4 homily pages**. The concise dossier initially overflowed physical page 2;
prose compression retained its substantive qualifications without reducing
type, and the final component artifact check passes. No padding was added to
restore an earlier page count. The final log screen found no warning,
undefined-reference or overfull/underfull-box diagnostic; the word “Rerun”
occurred only in the `rerunfilecheck` package description. Removing one
trailing space in the research apparatus and rebuilding exited 0. A later
visual reflow removed forced breaks without changing the source argument; the
current hashes are recorded in the final repair report.

The following scoped checks exited 0: `bindings-valid`,
`chronology-record-current`, `chronology-annotations-current`,
`chronology-claims-supported`, `references-used`, `house-voice`,
`restricted-not-reproduced`, `structural-meta-labels`, and
`check-proper-components --phase artifacts`. The critical-profile query for
Matthew 20:1 returned `composition-only` and `post-A.D. 70 date`.
`source-library validate` exited 0. `make check-sources` exited 2 on the
out-of-scope installed GPT 1962 synthesis PDF's subject mismatch with its
current source; this repair did not update that publication.

The external-evidence dependency audit found no missing external source owner
among the observed opens, but this provider's trace reused in-process caches
and is not a fresh exhaustive cold trace. The opened leaf-local
`proper-components.toml` was absent from the research seal; this is reported
to the coordinating tooling owner, not treated as a complete seal pass.

Review rasters and contact sheets were generated under
`build/pc-consumer-chronology-review-20260921/`. The concise dossier's physical
page 2 and the three outputs' contact sheets were opened. This does not
establish full-size page-by-page inspection, final-page acceptance or a
no-padding verdict. Diagnostic logs are under `.scratch/propers-format/`.

Independent research, content and visual acceptance remain outstanding.
Generation metadata was not refreshed with an invented model identity or
review event; finalization belongs to the coordinator. No installed PDF or web
edition, release inventory, Git index, commit or push was changed by this
consumer repair.

## House-voice audit, review fixes and re-check, 24 September 2026 (outside the workflow)

On 2026-09-24 the maintainer decided to audit every proper leaf of both
providers for the house-voice defect of `guidance/editorial.md` and to repair
what the audit finds, with independent review afterwards. That decision is the
provider authority for the three passes below and for nothing else.

**Audit (`6baabe283`).** A full read of the three documents found sentences
that took the study, its pages or its own interpretations as grammatical
subject, or narrated the study's attribution discipline. There were eighteen:
sixteen in the expansive study and two in the concise commentary. Each was
rewritten with a text, a witness or a fact as subject:
- the opening's roadmap;
- the settings' introduction and the note on Augustine's tractate 47;
- the cross-references between the interpretations;
- the three statements of where the Missal's texts take their places;
- Paul's place as the editor's;
- the third interpretation's second step and its difficulties;
- the comparison's "made on" and "belongs beside".

The homily needed no change.

**Review fixes (`abe9e50a0`).**
- F18: in four places the Missal's texts "take their places … by their own
  wording; the placing is the editor's, not a commentator's".
- F4: the opening reads "What each interpretation's witnesses say of their own
  passages supplies it", and four senses of its own close each.
- F19: "The second difficulty is one of evidence, and it concerns the furthest
  step alone" is restored.
- "as has been seen" is deleted.
- The settings' introduction and "The three interpretations below" are
  rewritten.
- Under the compiler-intent addendum, two clauses are deleted with their points
  kept: "The Missal's own texts were not written for this Gospel", and "no
  connection claims that the formulary was composed to make it" in both scope
  appendices.

**Re-check fix (this pass).** The first interpretation's "The Missal's own
texts, prayed with the readings of all three years, serve this Gospel …" had
lost its "here". It now reads "In this interpretation the Missal's own texts …
serve this Gospel …", so the placing stays the editor's and does not read as a
property of the texts.

**Checks.**
- In each pass all three editions were built with `make doc` and installed
  with `make install-doc`, and the settled-aux component and metadata checks
  pass.
- Pages are unchanged at 31, 10 and 4.
- Word diffs against the parent's builds show only the listed changes and the
  timestamp, and the changed pages were inspected at 70 dpi.
- `check-content-preflight` output is byte-identical before and after on all
  four editions.
- The web edition is regenerated, and `make check-web-editions-current` passes.
- The receipts are re-snapshotted, and `_proper_study.py check` passes in
  content, artifacts and publication with `--require-presentation
  --require-format`.
