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
   this Mass does not read.
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
