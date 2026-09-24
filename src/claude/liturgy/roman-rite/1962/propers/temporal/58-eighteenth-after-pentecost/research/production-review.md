# Production and review record

## Author-study

Authored 22 September 2026 in `proper-study` v6, run `71b6f89518984232`, seeded
at commit `fa5355745b5e973584f047a7f59a20ad22676d64`, at iteration 0, after the
research review of the same run passed at its iteration 4 with four standing
advisories (RES-024 to RES-027) and two observations. The canonical study is
*The Eighteenth Sunday after Pentecost*, the Mass *Dominica decima octava post
Pentecosten*, II classis, of the 1962 *Missale Romanum*, pp. 410–411,
nos. 1669–1678, in the universal calendar, for the occurrence of 27 September
2026.

The expansive study has an opening on the Sunday's three questions with a
ten-row map of the appointed elements; the complete appointed Latin of all ten
elements with the public-domain English of each where one carries it
(Douay–Rheims Challoner for Scripture at the canonical verses, the 1861
Cummiskey hand missal for the three orations), a description and no English
for the Introit antiphon and the Offertory, and a note at every place where the
Missal's wording leaves the Douay; an element-by-element section giving each
text its literary, textual, transmission and liturgical setting; three readings
of the whole formulary, each carrying all ten element keys and closing with its
own four senses; a comparison of the three; a terminal Scriptural Date and
Location appendix on the generated chronology projection; the scope appendix;
and References.

The three readings are those recorded in `research/interpretations.md`:

- `peace-of-the-house` — the peace of a city still being built, from *Da
  pacem* to the courts of the Lord. Carried by Augustine (*En. in Ps.* 121, 2,
  12–13; 101, s. 1, 16–18; 95, 1, 9–10), Hilary (*Tract. in Ps.* 121, 1–5,
  13–14) and Chrysostom (*Hom. in 1 Cor.* 2; *Expos. in Ps.* 121), with
  Cassiodorus on all three psalms, Theodoret and the PG 27 expositions on
  Ps 101, Bellarmine and Schuster on Ps 121, and Hilary on the Gospel as the
  *Catena aurea* reports him.
- `authority-on-earth` — the Son of man's power on earth to forgive, and the
  altar of the covenant. Carried by Chrysostom (*Hom. in Mt.* 29; *Hom. in
  Heb.* 16), Augustine (*De cons. evang.* II.25.57), Aquinas (*Super Mt.* c. 9
  at v. 6, *per viam administrationis, non auctoritatis*) and Bl. Schuster (at
  v. 8, his three senses in his own order), with Jerome (PL 26, cols. 54–55),
  Theodoret, the PG 27 expositions and Bellarmine at Ps 95:8, a Lapide on
  Ex 24:4–8, the continuation of *The Liturgical Year* (pp. 403, 405, 406–409),
  and Rupert and Durandus for the chants of their Mass and for Mt 9 at their
  Nineteenth Sunday.
- `nothing-of-our-own` — thanks at both ends and a man who was carried.
  Carried by Chrysostom (*Hom. in 1 Cor.* 2, 1–7; *Hom. in Mt.* 29), Augustine
  (*En. in Ps.* 95, 9; 101, s. 1, 16), Jerome (PL 26, cols. 54–55) and Aquinas
  (*Super Mt.* c. 9; *Super I Cor.* c. 1 lect. 1), with Theodoret, Theophylact
  and Ambrosiaster at 1 Cor 1:4–8, Cassiodorus at Ps 95:8, Berno and Schuster on
  the Collect, and Hilary on the Gospel as the *Catena* reports him.

The manifest opts into `authority_contract = "authority-standing-v1"` and names
each lane's carrying authors, all Fathers, Doctors or the Blessed in
`src/sources/inventories/author-standing-v1.toml`. Cassiodorus and Theodoret,
whom the registry records as ecclesiastical writers, support the readings and
carry none, and the study does not call either a Father.

Material disagreements are carried where the research records them: the Latin
readers of Ps 121 (Augustine, Hilary, Cassiodorus) against Chrysostom and
Theodoret, with Bellarmine and Schuster holding both in order; the three Latin
senses of *virtus* and of the towers at Ps 121:7; Augustine's lemma
*Jucundatus sum in his qui dixerunt mihi* against the Missal's; Chrysostom,
Jerome, Augustine and Aquinas on *civitatem suam*; Jerome against Chrysostom on
whose faith Christ saw, with Aquinas declining to choose; the division at
1 Cor 1:8 between accusation and promise; the contrite heart against the
priests' sacrifice at Ps 95:8; and, at Mt 9:8, the absence of any Father's
ministerial reading beside Aquinas at v. 6, Schuster's third sense, the
continuation, Rupert and Durandus on another Mass, and Honorius and Sicard,
who read the chants of the return from exile. No witness is credited with a
reading of the whole 1962 Mass except Schuster and the continuation, and the
commentators whose Mass had another Gospel are cited only for the elements
their Mass shares with this one, with that Gospel stated where they are used.
The age of the Gospel–Offertory pairing is asserted in neither direction.

**Substantive word count: 14,125 words** (13,049 with the content of the
`\latin{}` quotations removed). The count takes the six argumentative
components — opening, element-by-element setting, the three readings and the
comparison — removes comments, headings, labels and the map and comparison
tables, strips control words and braces, and counts whitespace-separated tokens
that carry a letter or digit. It excludes the appointed-text component, the
Scriptural Date and Location appendix, the scope appendix and References. The
total stands above the profile's 6,000–10,000-word planning range, which the
profile states is a range and not a quota: three readings that each carry all
ten appointed elements, report the principal witnesses' own reasoning with
their loci and preserve the disagreements above, and close with four senses
account for 9,576 words of it, and the element-by-element settings, which carry
the textual, transmission and liturgical facts the readings then use, for 3,032
more. The finished PDF is 32 physical pages, inside the 20–50-page requirement.

### Standing research advisories and observations

The four standing advisories are addressed to `research/scope.md`,
`research/interpretations.md` and `research/source-bindings.toml`, which this
stage does not edit. The study's prose follows what each asks without
repeating the defect:

- RES-024: Schuster is not called the one registered witness who reads Mt 9:8
  of the ministry. His senses of the verse are given in his own order, the
  crowd's judgement, the hypostatic "still deeper meaning", and then "Further",
  the symbolical and prophetic communication to the apostles and their
  successors; and the continuation's application of the verse's closing words
  to the Church's power (vol. XI, p. 405) is reported as its own, read on the
  tracked facsimile's text layer at PDF pp. 414–430 for this stage.
- RES-025: the continuation is not dated to 1909 as a composition; the study
  cites the 1909 English printing it read.
- RES-026: Chrysostom and Theodoret are named at Ps 121; the study nowhere
  calls them "the Greek Fathers".
- RES-027: none of the five slips it names is carried into the study; the study
  does not cite the Würzburg gospel list's *Ebd. IIII*, the numbering of the
  Exodus 32 lesson, Theophylact's holdings or Honorius's Alleluia.

The observation on Theophylact's standing is respected by using him only
beside Chrysostom, Theodoret and the Latin readers of 1 Cor 1:4–8 and never as
a carrying author.

### Verification performed at this stage

Quotations were checked against the witnesses the research reached, and where
a tracked text of a delivery the research quoted exists, the tracked text is
quoted:

- Augustine's *Enarrationes* English is quoted from the tracked CCEL NPNF1-8
  text (Ps XCVI §§ 1, 9–10; Ps CII §§ 16–18; Ps CXXII §§ 2, 12–13), which keeps
  the translation's own second person, and not from the New Advent wording
  `research/scope.md` quotes.
- Chrysostom's *Hom. in Mt.* 29 and Augustine's *De cons. evang.* II.25.57 are
  quoted from the tracked CCEL NPNF1-10 and NPNF1-6 texts.
- Chrysostom's *Hom. in 1 Cor.* 2 and *Hom. in Heb.* 16 were re-fetched from
  New Advent into this stage's scratch area; both responses matched the SHA-256
  values `research/scope.md` § 6.3 records, and every sentence quoted was read
  there. The sentence of *Hom. in 1 Cor.* 2 § 1 that a favour "is not a debt nor
  a requital nor a payment", and the sentence of § 5 on the remission of sins
  as "the Gift from above", stand in the section range the research read but
  are not quoted in its records; the study quotes them from that delivery.
- The Douay–Rheims and the Cummiskey English are quoted from the tracked
  verse-text artifacts and the tracked `temporal-orations-en` payload, lines
  164–166.
- Cassiodorus's Latin was checked in the tracked Corpus Corporum files for
  Pss 95 and 121; Bellarmine's English in the tracked O'Sullivan
  transcription; Schuster's in the tracked 1927 optical layer at lines
  10470–10710; the continuation's in the tracked facsimile's text layer.
  Aquinas's *Super Mt.* c. 9 was spot-checked in the tracked Venice 1745
  optical layer, where the sentence *quia portabatur, praecepit ut portaret*,
  which the research read on the page images but did not quote, also stands.
- The Catholic Encyclopedia articles behind the dossier's explanatory rows were
  read in their tracked article texts; the dossier names no article author,
  because the tracked texts carry none.

The Latin of Jerome, Hilary, Rupert, Durandus, Honorius, Sicard, Berno and the
Catena, and the Greek of Chrysostom on Ps 121, Theodoret and the PG 27
expositions, are taken from the research records, which read them on page
images; this stage did not reopen those images.

### Research points reported for the cold reviewer

- The Offertory's English: `research/scope.md` § 10.11 forbids an English
  Offertory. The study prints none; it gives a description of the antiphon and
  quotes the Douay only at the cited verses, labelled as those verses. The
  continuation prints a nineteenth-century English of the antiphon (vol. XI,
  p. 407), which the study does not use.

### Author proof and checks

`make doc DOC=liturgy/roman-rite/1962/propers/temporal/58-eighteenth-after-pentecost
PROVIDER=claude` settles with a clean log: no undefined reference, no rerun
request, no overfull or underfull box. The PDF has 32 physical pages, Latin
Modern fonts only, all embedded, and PDF title and subject from the entrypoint.
The study-preflight checks pass for the research edition: the component
contract with presentation and format required, references-used,
identifiers-resolve, bindings-valid, restricted-not-reproduced,
relation-coverage, unquoted-not-quoted, structural-meta-labels, house-voice,
the three chronology checks, and provenance-matches-run; so do
`check-proper-components --phase artifacts --edition research`,
`check-generation-metadata`, `check-web-edition` and a trial canonical web
conversion. Every page was inspected on rasters prepared by `tools/tpt
pdf-review`; two forced page breaks in the dossier were revised so that the
appendix opens on a fresh page and turns between dossiers, not inside one.
This is author verification; the shared-timestamp three-document build and
independent visual review remain to be done.

## Author-study, iteration 1

Revised 22 September 2026 in the same run, at author-study iteration 1, after
study review iteration 0 returned five blocking findings. STU-001 went to
research, which re-entered and passed research review at its iteration 6;
STU-002 to STU-005 were carried to this stage. The iteration-0 entry above is
kept as the record of that pass; where it describes Hilary on the Gospel "as the
*Catena aurea* reports him", Rabanus, or Rupert and Durandus in the second
reading, this entry supersedes it.

### Carried findings

- **STU-002.** The comparison's "genuine conflict" paragraph is replaced. The
  three readings now use the Gospel's city compatibly: the first allegorically
  with Hilary, who names no town (*In Matth.* VIII.4, PL 9, cols. 959–960); the
  second as the literal place of a verifiable sign; the third not at all.
  Aquinas's lecture is cited for holding the harmony and the allegory together.
  The real disagreements are set inside the readings that carry them:
  Chrysostom against Jerome on the town (second), Jerome and Ambrose against
  Chrysostom on whose faith (third), the Greek against the Latin readers of
  Ps 121 (first). Augustine is described accurately in the comparison, the
  element-by-element Gospel paragraph and the second reading: reconciling
  Matthew with Mark, he takes "his own city" first as Nazareth, places the
  healing at Capernaum and offers two explanations. The second reading's title
  and three sentences that named Capernaum as the place no longer decide the
  town.
- **STU-003.** Chrysostom's "not only the beginnings must be good, but the end
  also" and "there is need of many labors to be able to come unto the end" are
  attributed to 1 Cor 1:7 (*Hom. in 1 Cor.* 2, § 6), in the third reading's
  answer to quietism. His reading of v. 8 is given only as covert accusation
  (§ 7). The New Advent delivery was re-fetched for this stage; its SHA-256,
  `66bffe29…4b5858`, matches `research/scope.md` § 6.3, and §§ 6 and 7 were read
  there. The sentence is withdrawn from the second reading.
- **STU-004.** The second reading's anagogical sense now develops the command to
  go home: Hilary's order of the cure ending in the way into paradise given back
  to believers (VIII.7), Ambrose's true home lost by fraud (*Exp. in Lc.* V.14)
  and Aquinas's house of eternity. The third reading's anagogical sense is its
  own: the end given as the beginning was, through 1 Cor 1:8 (the confirming is
  Christ's on either reading), Hilary on what the many receive at v. 8
  (VIII.8), and the Postcommunion's *perficias* with God as its subject. 1 Cor
  1:8 and *perficias* are anchors of the third reading only; the distinction
  between completion and perfection is dropped.
- **STU-005, partly repaired.** The Introit's explanatory row now says that the
  record answers its two loci separately: at Ecclus 36:18 a preferred interval
  and an alternate approximate year for the composition of Ecclesiasticus, both
  from the *Catholic Encyclopedia*'s "Ecclesiasticus" (1909) under the
  traditional Catholic profile, and at Ps 121:1 the Psalter boundary given with
  the Gradual. The scope appendix's Chronology paragraph says the Introit has
  two separate answers. **The record's labels are not printed.** Printed with
  their era, both were refused by `check-content-preflight --check
  chronology-claims-supported`: its supported set is built only from each
  element's `publication_claims` and declared profile comparisons, the Introit's
  `publication_claims` is empty because the element is nonuniform, and a
  comparison that does not hold at every locus of an element is itself refused
  (`guidance/scripture-chronology.md` § 14.1). No route in the current tooling
  lets a locus-specific date for a nonuniform element reach dossier prose. That
  is a question for the maintainer about the chronology contract, reported
  here for the cold reviewer; this stage cannot edit the checker or the
  guidance.

### Revision to the re-entered research

The study now follows the research as re-entered for STU-001 and RES-028:

- Hilary on the Gospel is cited from his *Commentarius in Matthaeum* at PL 9 and
  no longer through Aquinas: the city (§ 4, with the Maurist *Deo civitas*), the
  paralytic as the nations, brought by angels and pardoned Adam's first
  transgression (§ 5), the return home as the way into paradise (§ 7), and v. 8
  as fitting praise for a power and a way given to men (§ 8). The Catena's
  *ut fiant filii Dei* and its splice of *quae lex laxare non poterat* are gone.
- The Catena's "Rabanus" is withdrawn from the second reading's moral sense and
  replaced by Bede, *In Lucam* II on Lk 5:24.
- Ambrose, *Exp. in Lc.* V.11–15, enters the second reading (V.13 as the one
  Father's warrant for the ministerial step, glossing the scribes' question;
  V.14; V.15 beside Chrysostom on the crowd's fear) and the third (V.11 with
  Jerome on whose faith). The research's negative sentence about V.14 (RES-031)
  is not repeated.
- Under the profile's *Liturgical commentators* rule, the readings and the
  element-by-element section no longer mention the commentators' other Gospels
  or Sundays; Rupert and Durandus are withdrawn from the second reading, and
  the scope appendix carries the one permitted clause. The second reading's
  paragraph on the pairing's history keeps only the 1862 and 1962 books.
- Advisories STU-006, STU-007, STU-009, STU-010 (in part), STU-012 and STU-013
  were cleared while in those files.

The manifest's lane authors now add Ambrose and Bede to the second reading and
Ambrose to the third, and drop Rupert and Durandus from the second. Carrying
authors are unchanged.

**Substantive word count: 14,967 words** (13,809 without the `\latin{}`
quotations), by the method of the iteration-0 entry and excluding the opening's
map table; the three readings account for 10,220. The finished PDF is 33
physical pages.

### Author proof and checks

`make doc` settles with 33 pages; `check-proper-components --phase artifacts
--edition research`, `check-generation-metadata` and every
`check-content-preflight` check for the research edition pass, including
provenance-matches-run against this run. The rights colophon was kept off a
page of its own by merging two pairs of References entries and dropping the
Catena entry, which the study no longer quotes or relies on. This remains author
verification; the shared-timestamp three-document build and independent visual
review are still to be done.

## Author-study, iteration 2

Revised 22–23 September 2026 in the same run, at author-study iteration 2,
after study review iteration 1 returned one blocking finding, STU-014, on the
comparison. The entries above are kept as the record of the earlier passes;
where the iteration-1 entry describes the third reading's anagogical sense as
resting on Hilary at v. 8, this entry supersedes it.

### Blocking finding

- **STU-014.** Hilary on Mt 9:8 is kept in the third reading, and the
  comparison now says so. Its shared-ground paragraph no longer says that none
  of the readings sets the crowd's praise against Chrysostom's reading. It says
  that none takes a sense of the Church's ministry from a Father's reading of
  that verse. It names all four places where the second reading takes the
  ministerial sense: Ambrose, *Exp. in Lc.* V.13, glossing the scribes'
  question; Aquinas at v. 6; Schuster's third sense of v. 8; and the
  continuation, with its keys and Penance. It also says that the readings hear
  the verse differently: the first does not use it, the second reports
  Chrysostom first, and the third draws on Hilary. The disagreements paragraph
  now opens "Most of the real disagreements", and a new paragraph adds the one
  that runs between two readings. Chrysostom, with Ambrose at V.15, hears an
  inadequate confession. Hilary hears fitting honour for a power and a way
  given through Christ's word to the many who receive them. The second reading
  reports both and draws its own sense of the verse from Schuster. The third
  takes Hilary's side, so that its Gospel closes, as its Epistle opens, with
  God glorified for what men have been given. The sentence "No witness sets one
  reading's use of a text against another's" is removed. The Postcommunion
  clause keeps "all three" and now says how each reading hears
  *perficias*. For the first reading, the sentence on the prayers now says that
  the Postcommunion still asks to be made worthy: the courts are entered and
  the city is still ahead. The table's Gospel row for the third reading adds
  Hilary. In the third reading's Gospel subsection, Hilary's *conclusa sunt
  omnia suo ordine* and his contrast between the praise of one man and the
  praise of many (PL 9, col. 962, text layer `db389fea`, re-read for this stage)
  are added. The sentence "The last of those gifts is given as the first was"
  is replaced: the power and the way are given now, through the word, and the
  resurrection and the return to heaven are where the way ends.

### Standing advisories cleared

- STU-010: the element-by-element section opens with the books its elements
  come from. The second sentence of the second reading's pairing paragraph is
  dropped.
- STU-011: the Gradual's Sextuplex placings are given only as the database's
  report.
- STU-015: Hilary's plea is given in his own form, that all be of one mind,
  exercising the same charity (*Tract. in Ps.* 121, 5). Zingerle refers it to
  1 Cor 1:10, and the schisms clause is attributed to Paul's verse. *Pax enim
  ecclesiae …* is cited to § 14. Both were checked in the registered CSEL 22
  optical layer, re-fetched for this stage with its SHA-256 matching
  `research/scope.md` (`6b39d974…14a7fa`). The page images were not reopened.
- STU-016: Augustine argues from Luke's *homo* beside Matthew's *fili*.
- STU-017: Honorius's reading of the Gospel's city (IV.86) is dropped from the
  second reading. The scope appendix no longer says that the commentators are
  cited for what they say of this Gospel at another Sunday.
- STU-018: Hilary's way home is kept only in the second reading's anagogical
  sense, which develops it with Ambrose and Aquinas. The third reading's
  anagogical sense now rests on 1 Cor 1:8 and the Postcommunion.
- STU-019: the Introit's commentators are no longer counted. "The Mass whose
  Epistle begins *Gratias ago*" replaces the Epistle-as-beginning phrasing. The
  objection's four words are described as the chants' words. The references
  are narrowed to Rupert XII.18 (col. 326), Durandus VI.135, Honorius IV.84–85
  (cols. 722–723) and Sicard VIII.18. The column locations are from the
  tracked layers' chapter headings.

### For the reviewer

`research/interpretations.md` § 4.3 still says that all three readings treat
*qui dedit potestatem talem hominibus* alike and that none turns on it. That
was true of the research's own readings. It is not true of the study since the
iteration-1 revision gave the third reading Hilary at v. 8. The same section
lists the Chrysostom–Hilary disagreement among the real ones, and the study now
follows that list. This stage does not edit research records. The drift is
reported for routing.

**Substantive word count: about 15,300 words** (about 14,100 without the
`\latin{}` quotations; the three readings about 10,300). This was counted by a
re-implementation of the iteration-0 method, excluding the map and comparison
tables, and exact agreement with the earlier count is not claimed. The finished
PDF is 34 physical pages. The comparison now runs onto a short page before the
Scriptural Date and Location appendix, which starts a new page.

### Author proof and checks

`make doc` settles at 34 pages. These all pass: `check-proper-components
--phase artifacts --edition research`, `check-generation-metadata`,
`check-web-edition`, and every `check-content-preflight` check for the research
edition, including provenance-matches-run against this run. This is still
author verification. The shared-timestamp three-document build and the
independent visual review remain to be done.

## Author-study, iteration 3

Revised 23 September 2026 in the same run, at author-study iteration 3. Study
review iteration 2 returned one blocking finding, STU-020, and routed it to
research: `research/interpretations.md` no longer recorded the readings the
study gives. Research re-entered at its iteration 7 and revised only that
record. Research review passed at its iteration 7. This stage reruns as a
dependent of that repair and was forwarded no blocking finding. The entries
above are kept as the record of the earlier passes. Where the iteration-2 entry
says that Chrysostom, "with Ambrose at V.15", hears an inadequate confession,
this entry supersedes it.

### The study against the revised record

The study was read against the revised record on every point STU-020 named. On
v. 8, the first reading does not use the verse. The second reports Chrysostom
first and Hilary after, takes its own sense of the verse from Schuster, and
cites Hilary only to show that the men of the verse receive forgiveness and do
not minister it. The third takes Hilary's side. In the anagogical senses, the
second reading rests on Hilary VIII.7, Ambrose V.14 and Aquinas's *domum
aeternitatis*, and 1 Cor 1:8 and *perficias* anchor the third reading only.
Chrysostom's "not only the beginnings must be good, but the end also" and "need
of many labors" stand on 1 Cor 1:7 (§ 6). His reading of v. 8 is covert
accusation (§ 7). The record now agrees with the study on all of these points,
and none of that prose was changed.

In one place the revised record now contradicts the study. Record § 4.3 says
that Ambrose at V.15 "may not be reported as judging the crowd 'in the same
way' as Chrysostom". The study said exactly that in two places, which the
standing study-review advisory STU-021 had named. Both places are repaired.

### Standing advisories cleared

- STU-021: in the second reading ("What the crowd said") and in the comparison,
  Ambrose now judges the fear more severely than Chrysostom. At V.15 those who
  watch the man rise are unbelievers, *Spectant surgentem increduli*, who
  *divini operis miracula malunt timere quam credere*. Had they believed they
  would have loved, and *quia non diligebant, calumniabantur*. The second
  reading says that Chrysostom's crowd glorify God and fall short, while
  Ambrose's fearers are the calumniators. The comparison says that his
  judgement is negative, as Chrysostom's is, but his own. The wording was
  checked in the tracked transcription `ambrose-luke5-raw.txt`, whose SHA-256
  `fde2303a…6330ac52` was re-computed for this stage, at the line carrying
  §§ 13–17.
- STU-022: the Gradual paragraph now says what `research/scope.md` § 2.3
  reports of the database's day 823. *Laetatus sum* is the Gradual in four of
  the six books (Rheinau, Mont-Blandin, Corbie, Senlis). The Offertory and
  Communion stand in the same four, and the Introit in three of them.

The research-review advisories RES-031 to RES-036 are addressed to research
records, which this stage does not edit. The study does not repeat the defect
any of them names. RES-034 records that three loci the study quotes are
carried by no research record: the continuation's pp. 395 and 408–409, and
Aquinas's *quia portabatur, praecepit ut portaret*. Research review read all
three and found them accurate. The iteration-0 entry above discloses the
Aquinas sentence as this stage's own check.

**Substantive word count: about 15,400 words** (about 14,200 without the
`\latin{}` quotations; the three readings about 10,300). The count follows the
iteration-2 method, excluding the map and comparison tables. As at iteration 2,
exact agreement with the iteration-0 count is not claimed. The finished PDF is
34 physical pages. As before, the comparison ends on a short page before the
Scriptural Date and Location appendix, which starts a new page.

### Author proof and checks

`make doc` settles at 34 pages. The log has no undefined reference, rerun
request, or overfull or underfull box. These all pass: `check-proper-components
--phase artifacts --edition research`, `check-generation-metadata`,
`check-web-edition`, and every `check-content-preflight` check for the research
edition, including provenance-matches-run against this run. Every page was
inspected on the contact sheets prepared by `tools/pdf-review`. The pages that
carry the changes (9, 18, 28 and 29) and the final page, which holds the
revision timestamp and colophon, were also inspected at full size. This is
still author verification. The shared-timestamp three-document build and the independent
visual review remain to be done.

## Derive-synthesis

Authored 23 September 2026 in `proper-study` v6, run `71b6f89518984232`, seeded
at commit `fa5355745b5e973584f047a7f59a20ad22676d64`, at derive-synthesis
iteration 0, after study review passed at its iteration 3. The concise
companion is *The Eighteenth Sunday after Pentecost: A Concise Study of the
Proper in the 1962 Roman Missal*, built from `synthesis.tex` and derived from
the accepted expansive study of this same leaf. No research record and no
component of the study was edited for it. The manifest changed only in two
comments, which had described the concise components as still to be written.

The six synthesis components were written at this stage:

- `concise-inventory` (`sections/concise/01-inventory.tex`): the map of the ten
  appointed elements in the order of the Mass, with a rubrical note that the
  Mass is of the second class, has one oration of each kind, no optional element
  and no commemoration (so Saints Cosmas and Damian give way), and takes the
  Trinity Preface by rubric.
- `concise-overview` (`sections/concise/02-overview.tex`): exactly four overview
  rows, drawn from the three readings' own senses and from
  `research/interpretations.md` § 4.4. They orient the reader and do not replace
  each reading's own four senses.
- `concise-date-location` (`sections/concise/03-date-location.tex`): the
  Scriptural Date and Location sheet. It imports the generated chronology
  annotations once and carries one `\chronodate` cell for each of the seven
  appointed Scriptures, in the study's canonical order. The dates, relation
  labels, disputed alternatives and unresolved states are the study's own,
  unchanged. The explanatory rows are compressed from the study's appendix so
  that the sheet occupies one physical page.
- `concise-themes` (`sections/concise/04-themes.tex`): *The Propers: Themes and
  Movement*, two pages. It opens with a direct thesis and follows the formulary
  from *Da pacem* to *perficias*, with the transmission facts the study reports.
  It then names three habits of the whole (the house; the visible given for the
  invisible; nothing self-made) and the three readings and how they relate.
- `concise-commentary` (`sections/concise/10-commentary.tex`): *The Propers:
  Detailed Commentary*, six cross-proper questions, each drawing on several
  elements and setting the readings' answers beside one another. Which house
  and which city (Introit, Gradual, Alleluia, Communion, the Gospel's city).
  What peace is and what threatens it (Gradual versicle, Epistle). Power on
  earth (Gospel). Whose faith, and who was carried (Gospel, Alleluia, Collect).
  "Such power to men", the one disagreement between two readings (Gospel,
  v. 8). The altar, the exchange and the courts (Offertory, Secret, Communion).
  Where the Mass sends its people (Gospel, Epistle v. 8, Postcommunion).
- `concise-apparatus` (`sections/concise/90-apparatus.tex`): the scope note and
  the References for the sources this companion actually uses.

Every reading's controlling claim is preserved. So are the shared ground the
study's comparison states and the one disagreement that runs between two
readings: Chrysostom's inadequate confession, with Ambrose's severer judgement
kept as his own, against Hilary's fitting honour at Mt 9:8. The second reading
takes its sense of that verse from Schuster, and the third takes Hilary's side.
The four places of the ministerial sense are named: Ambrose's gloss on the
scribes' question (V.13), Aquinas at v. 6, Schuster's third sense of v. 8, and
the continuation with the keys and Penance. The statement that no Father read
here takes v. 8 of the ministry stands. The disagreements inside single readings are all kept:

- Chrysostom against Jerome on the town, with the town left undecided;
- Jerome and Ambrose against Chrysostom on whose faith, with Aquinas declining;
- the Greek against the Latin readers of Ps 121, with Bellarmine and Schuster
  holding both in order;
- the three senses of *virtus* and the towers at Ps 121:7;
- Augustine's lemma against the Missal's;
- Jerome's *forsan* against Aquinas on why the sins came first;
- accusation against promise at 1 Cor 1:8.

The Communion's two identifications of the *hostiae* at Ps 95:8, the contrite
heart and the Church's sacrifice offered by its priests, are kept as compatible
emphases that Bellarmine and the continuation hold together, not as a
disagreement (corrected at iteration 1; iteration 0 had listed them here as one).

The compression set aside the study's liturgical commentators on the Introit
(Rupert, Durandus, Honorius, Sicard) and on the chants of the return from
exile, St Anthony of Padua, Theophylact, Augustine's Donatist setting, the
first reading's objection that the chants were chosen word by word, and the
Frankish lectionaries' other placements. Nothing in the concise argument turns
on them, and the study carries each. Every quotation printed is one the
reviewed study prints, at the same locus. This was checked mechanically: each
quoted English and Latin span of the concise components was searched in the
study's components. The only spans the search did not find verbatim were the
Missal's own Latin, which the study prints with accents, and one heading.

**Substantive word count: 6,218 words** (5,595 with the content of the
`\latin{}` quotations removed). The count covers the two argumentative
components: the themes section, 1,585 (1,475), and the commentary, 4,633
(4,120). It strips comments, headings, zref labels and control words, then
counts whitespace-separated tokens that carry a letter or digit. It excludes
the map, the overview rows, the dossier sheet, the scope note and the
References. The finished PDF is 12 physical pages, inside the 10–12-page
requirement.

The shared generation record now carries a contribution for this stage and the
revision timestamp `2026-09-23T14:30:00Z`. The expansive study was rebuilt at
that timestamp and is unchanged at 34 pages with a clean log.

### Upstream observations reported for the cold reviewer

- `research/interpretations.md` § 4.4, the Anagogical note for the page-1
  overview, groups Aquinas under "the way back to paradise" (standing advisory
  RES-035). The overview keeps each witness's own word: paradise for Hilary and
  Ambrose, the house of eternity for Aquinas.
- `research/interpretations.md` § 2.4 Literal still places the healing "At
  Capernaum" (standing advisory STU-023). The concise study follows the
  reviewed study and leaves the town undecided.
- No missing argument or source was found. The study, its dossier appendix and
  the research records answered every point the concise prose needed.

### Author proof and checks

`make doc DOC=liturgy/roman-rite/1962/propers/temporal/58-eighteenth-after-pentecost-synthesis PROVIDER=claude`
settles with no overfull or underfull box, no undefined reference, no LaTeX
warning and no rerun request. The PDF has 12 pages, letter size, Latin Modern
Roman and Mono only, all embedded and subsetted. The document info carries the
entrypoint's title and subject.

The settled auxiliary file records the physical pages that the presentation
contract fixes:

- the inventory and overview markers, and all four sense markers, on page 1;
- chronology start and end on page 2;
- themes start on page 3 and themes end on page 4;
- commentary start on page 5.

These all pass: `tools/check-proper-components --phase artifacts --edition
synthesis`; `scripts/_proper_study.py check --phase content --edition synthesis
--require-presentation --require-format`; every `check-content-preflight` check
the synthesis gate names (references-used, identifiers-resolve, bindings-valid,
restricted-not-reproduced, relation-coverage, unquoted-not-quoted,
structural-meta-labels, house-voice, the three chronology checks, and
provenance-matches-run against this run); and `check-generation-metadata`.

The settled proof is
`build/claude/liturgy/roman-rite/1962/propers/temporal/58-eighteenth-after-pentecost-synthesis.pdf`,
SHA-256 `08cd1bae08f752b1c17d799194280e25967679a0d4a5923e4d318e4c4de6d403`, at
the revision timestamp `2026-09-23T14:30:00Z`. Its auxiliary file is SHA-256
`462a8f9e960cdda5fdf5b065a768e40e967e02010a8442e00b75d1e6b21f8528`. The
expansive study rebuilt at the same timestamp is SHA-256
`c7af8fe21fe2005cf81a9897e8c2870202c800acd699bf96b0394e7bf4d3f248`. Copies of
both PDFs are kept beneath this stage's own artifact directory in the run, with
the synthesis auxiliary file, log, extracted text, checks, and their digests.
The page rasters are in a child directory of their own.

The author read the contact sheet of all twelve pages and the individual
rasters of pages 1, 2, 4 and 12. Layout revision removed a spill of the
Anagogical row onto page 2, which had also pushed the whole document to 13
pages. It also filled the second thematic page, which had been about a fifth
empty. The proof shows no clipping, collision, missing text, blank page or
heading-only page. The map and the four overview rows rule to the same measure
on page 1. The dossier stands whole on page 2. The themes section fills pages 3
and 4. The revision timestamp and the rights colophon share the last page with
the end of the References. This is an author proof inspection, not the
independent visual evaluation, which follows the shared-timestamp
three-document build.

### Iteration 1: repair of the synthesis review

Revised 23 September 2026 at derive-synthesis iteration 1, after synthesis
review returned three blocking findings and four advisories. Only the concise
components, the shared generation record and this entry changed. No research
record, study component or manifest entry was edited.

- SYN-001 (`sections/concise/10-commentary.tex`, the Communion paragraph): the
  framing sentence and the two "On that reading ... rests" clauses said the
  witnesses divide over the *hostiae* and that the division runs between the
  second and third readings. The paragraph now presents the two
  identifications as compatible. The third reading hears the offering of the
  heart (Augustine, Cassiodorus), the second the priests' sacrifice (Theodoret,
  the expositions under Athanasius's name), and neither denies the other.
  Bellarmine gives both and the continuation holds both together. The
  witnesses and quotations are unchanged. Mt 9:8 remains the only place where
  two readings follow contrary judgements, as the Themes and the fifth
  commentary heading state.
- SYN-002 (the same file, "Where the Mass sends its people"): the gloss *sine
  crimine* as *sine peccato mortali* is now Aquinas's alone. Ambrosiaster and
  Cornelius a Lapide are kept as readers of a promise of perseverance, in the
  study's own attribution.
- SYN-003 (`sections/concise/03-date-location.tex`, the Gospel's explanatory
  row): the critical span is restored in the study's words, "from shortly
  before the fall of Jerusalem to well into the second century", without
  numerals. The chronology sheet still begins and ends on physical page 2.

The standing advisories were cleared in the same files. SYN-004: four
sentences that narrated the discipline were recast with the witness or the text
as subject. They covered the continuation's reading of the Epistle, the Epistle
join at Mt 9:8 (now the third reading's hearing of Hilary's crowd), the order
of the study's report (dropped), and the keys and Penance. SYN-005: the Themes
now say that in the Missal the Sunday's Mass follows those of the September
Ember Days. SYN-006: the Collect paragraph opens with the study's framing, "The
Collect says outright what the Epistle implies", so that Berno and Schuster no
longer stand under a Collect-Gospel claim. SYN-007: the scope note now says
that the dossier's Date cells, relation labels, alternatives and unresolved
states are the generated record's, as in the study, and that the map and the
dossier's explanatory rows condense the study's.

**Substantive word count at iteration 1: 6,193 words** (5,570 with the content
of the `\latin{}` quotations removed): the themes section 1,585 (1,475) and the
commentary 4,608 (4,095). This is the same stated rule, recounted with this
iteration's tokeniser. That tokeniser gives 6,195 (5,572) for the iteration-0
text, so the repair shortened the argument by two words. The iteration-0 figure
of 6,218 came from a tokeniser that treats some control-word arguments
differently.

The shared generation record carries the iteration-1 repair in this stage's
contribution and the revision timestamp `2026-09-23T14:53:00Z`. The expansive
study was rebuilt at that timestamp and is unchanged at 34 pages with a clean
log.

`make doc DOC=liturgy/roman-rite/1962/propers/temporal/58-eighteenth-after-pentecost-synthesis PROVIDER=claude`
settles with no overfull or underfull box, no undefined reference, no LaTeX
warning and no rerun request. The PDF has 12 physical pages. The settled
auxiliary file places the inventory, overview and four sense markers on page 1,
chronology start and end on page 2, themes start on page 3 and end on page 4,
and commentary start on page 5. The checks named in the iteration-0 entry all
pass again: the component artifacts check, the content check with presentation
and format, every synthesis `check-content-preflight` check including
provenance-matches-run against this run, and `check-generation-metadata`.

The settled proof is SHA-256
`c55f9eff3bf44abdbbae874df2a118073f608236cadc505ff67a0a8e3135ecc1`. Its
auxiliary file is SHA-256
`462a8f9e960cdda5fdf5b065a768e40e967e02010a8442e00b75d1e6b21f8528`, unchanged,
because no marker moved. The expansive study rebuilt at the same timestamp is
SHA-256 `bcdf6c6b73a7b312fa9f823801c75136379270408226aac1e106674780248b96`.
Copies, with the log, the extracted text, the checks and their digests, are
kept beneath this iteration's own artifact directory in the run. The page
rasters are in a child directory of their own. The author read the contact
sheet of all twelve pages and the rasters of pages 2 and 10. The dossier stands
whole on page 2 with room below it, and the revised Communion and *sine
crimine* passages set cleanly on page 10. This is an author proof inspection,
not the independent visual evaluation.

## Derive-homily

Authored 23 September 2026 in `proper-study` v6, run `71b6f89518984232`, seeded
at commit `fa5355745b5e973584f047a7f59a20ad22676d64`, at derive-homily
iteration 0, after the synthesis review passed. The homily is *The Eighteenth
Sunday after Pentecost: The Man Who Was Carried*, built from `homily.tex`,
addressed to an adult parish assembly for the occurrence of 27 September 2026,
and derived from the two accepted studies of this same leaf. No research
record and no component of either study was edited for it. The manifest
changed only in one comment, which had described the homily components as
still to be written.

The entrypoint imports `common/preamble`, `common/propers-format` and
`common/propers-homily` in that order, then the leaf's `format.tex`, and uses
the shared full-width `\propertitle`. The `properhomily` environment encloses
only the literal import of the spoken component; the terminal note follows the
environment's closing page break. No font, geometry, title or column setting
is overridden locally.

The two homily components the manifest declares were written at this stage:

- `homily-body` (`sections/homily/10-homily.tex`): the spoken text, continuous
  preaching with no heading, no direction to a preacher and no citation inside
  the speech, in six movements. It opens on the paralytic who never speaks. It
  hears the Collect's *sine te* and the Epistle's thanks for gifts given, with
  Chrysostom on grace as no debt and no payment, and the parties that the
  verses after the lesson reveal. It keeps the open disagreement over whose
  faith Christ saw (Jerome and Ambrose against Chrysostom) and rests on what
  both sides grant. It takes the power "on earth" to forgive from Mt 9:6, with
  Chrysostom's unseen proved by the seen and Aquinas's ministry beneath
  Christ's authority, and applies it to the sacrament of Penance. It sets
  Chrysostom's and Hilary's judgements of the crowd at Mt 9:8 side by side. It
  hears the Communion's command with Augustine's contrite heart and the
  Postcommunion's thanks and plea. It answers quietism from the Gospel's own
  commands and Aquinas's *quia portabatur, praecepit ut portaret*. It ends with
  three practicable responses (confession, carrying another, thanks for what
  one is proudest of) and the hope of 1 Cor 1:8, where Chrysostom's warning
  and Aquinas's promise are both named.
- `homily-note` (`sections/homily/90-note.tex`): the terminal note and the
  References, read aloud by nobody: audience and occasion, spoken word count
  and pace, relation to the three reviewed readings, the route by which each
  quoted text reaches the page, and the exact loci.

The argument follows the third reviewed reading, `nothing-of-our-own`, as
`research/interpretations.md` § 4.5 recommends. It takes from
`authority-on-earth` only the Gospel's power on earth (Mt 9:6), and it takes
the Communion as the entry into the courts, not the first reading's city;
`peace-of-the-house` is not otherwise used. The homily stays within § 4.5's
bounds:

- no Father is given a ministerial reading of Mt 9:8;
- the ministry of forgiveness is spoken as Aquinas's at v. 6, and its
  application to Penance is the homily's own;
- the crowd's praise as thanks for a gift is named as Hilary's, with
  Chrysostom's different judgement beside it, and its join to the Epistle is
  editorial;
- no liturgical commentator is cited, and nothing is said of the Offertory's
  age or pairing;
- the Chrysostom sentence on 1 Cor 1:7 is not used, and his reading of 1:8 is
  given as a warning.

The Gospel, the Epistle, the Collect, the Communion and the Postcommunion carry
the argument. The Introit, the Gradual, the Alleluia, the Offertory and the
Secret are left to the studies. The manifest's complete element keys on both
homily components are the component checker's coverage declaration and are
unchanged.

No English of a liturgical text was composed. The Collect and the
Postcommunion are quoted from the 1861 Cummiskey translation, re-read in the
tracked orations table (`post-pentecosten-18`, pp. 444–445). Scripture is the
Douay–Rheims at the canonical verses, and 1 Cor 1:4, 5, 8, 10 were re-read in
the tracked verse table. *Sine te* is glossed as the studies gloss it, and no
prayer is recited at the end. The following were re-read at this stage in the
tracked sources:

- Chrysostom on Matthew, homily 29, in the tracked CCEL text of NPNF1 10
  within the registered segment (lines 18438–18793);
- Augustine on Ps 95, 9, in the tracked CCEL text of NPNF1 8 (line 48061);
- Ambrose, *Exp. in Lc.* V.11, in the tracked Wikisource transcription;
- Hilary, *In Matth.* VIII.8, in the tracked PL 9 optical text;
- Aquinas on Matthew, c. 9, in the tracked Venice 1745 optical text, lines
  16493–16496 (*per viam administrationis, non auctoritatis*) and 16508–16511
  (*quia portabatur, praecepit ut portaret*).

Three sources are reported as the reviewed study prints them and were not
re-read here:

- Chrysostom on First Corinthians, homily 2, whose New Advent delivery is
  unregistered;
- Jerome on Mt 9:1–2, whose PL 26 scan has no text layer;
- Aquinas on First Corinthians, whose Corpus Thomisticum artifact is not held
  locally.

No anecdote, personal experience, clerical identity, miraculous story or
attributed quotation was manufactured.

**Spoken word count: 1,448 words.** The count is taken over
`sections/homily/10-homily.tex` alone. Comments are removed, `\latin{}`
contents kept and every other macro dropped, and the remainder is counted as
whitespace-separated words carrying a letter. At an unhurried preaching pace
of 120 to 130 words a minute that is 11.1 to 12.1 minutes, within the
profile's approximately 10–12 minutes. The figure is arithmetic on the word
count and not a timed delivery: nobody has spoken these words and no
rehearsal was audible. The prose was read through in full, silently, for
sense, sentence length and ease of speech. That reading changed one sentence
that called the Collect "the one prayer said before the Epistle".

### Upstream observations reported for the homily's cold reviewer

- Standing advisory RES-034 remains true. The homily's Aquinas sentence *quia
  portabatur, praecepit ut portaret* is in the accepted study but in no
  research record. It was confirmed at this stage in the tracked Venice optical
  text, lines 16508–16511.
- Chrysostom's *Homilies on First Corinthians* 2, which both studies and this
  homily quote, rests on an unregistered New Advent delivery
  (`research/scope.md` § 6.3 register). The library's registered route to that
  text was deliberately not used. The homily's two quotations were not re-read
  here.
- No other missing argument or source was found, and nothing upstream was
  edited.

### Author proof and checks

The shared generation record now carries a contribution for this stage and the
revision timestamp `2026-09-23T15:16:00Z`. The expansive study and the concise
study were rebuilt at that timestamp. They are unchanged at 34 and 12 physical
pages, with clean logs. The concise study's settled auxiliary file is
byte-identical to the one the synthesis stage recorded (SHA-256
`462a8f9e960cdda5fdf5b065a768e40e967e02010a8442e00b75d1e6b21f8528`), so its
presentation markers have not moved.

`make doc DOC=liturgy/roman-rite/1962/propers/temporal/58-eighteenth-after-pentecost-homily PROVIDER=claude`
settles with no overfull or underfull box, no undefined reference, no LaTeX
warning and no rerun request. The PDF has 3 physical pages, letter size, Latin
Modern Roman and Mono only, all embedded, subsetted and Unicode-mapped. The
document info carries the entrypoint's title and subject and the tracked
`ModDate`. Deleting the PDF, the auxiliary file and the log and building again
reproduced the same bytes.

These all pass:

- `python3 scripts/_proper_study.py check --phase content --edition homily
  --require-presentation --require-format`;
- every `check-content-preflight` check the homily gate names: references-used
  (nine entries, every one used), identifiers-resolve, bindings-valid,
  restricted-not-reproduced, relation-coverage, unquoted-not-quoted,
  structural-meta-labels, house-voice, the three chronology checks, and
  provenance-matches-run against this run;
- `tools/check-proper-components --phase artifacts --edition homily`;
- `check-generation-metadata`.

The settled proof is
`build/claude/liturgy/roman-rite/1962/propers/temporal/58-eighteenth-after-pentecost-homily.pdf`,
SHA-256 `40de55df12b6823dd85549af759f5ff38e86e5727ded405fd1140a7c625af4bc`.
Its auxiliary file is SHA-256
`96da8bd61cc21463cd3eda0260cb058d26e765e456536a181a79f8efa1798486`. The
expansive and concise studies rebuilt at the same timestamp are SHA-256
`aaaec463874d813efd9e205a64fbccf351f983a3be51621e95f118b8aa2e5fcb` and
`c44638b77c6b25f9473b665fb85a6a50d1a7938860f4b28e77a7d91cd60d75ff`.

The author read the individual rasters and the extracted text of all three
pages:

- The speech occupies pages 1 and 2 in two balanced Latin Modern columns under
  the full-width title, and ends about four-fifths of the way down page 2. Its five
  wider spaces mark the six movements.
- The running head reads "Eighteenth Sunday after Pentecost" and "Homily" on
  page 2.
- The note, the References, the revision timestamp and the rights colophon
  share page 3.

A first layout put the colophon alone on a fourth page. The note was shortened
by trimming the quotations repeated in its loci paragraph and compressing two
sentences, and nothing was set smaller. The proof shows no clipping,
collision, missing text, blank page or heading-only page. This is an author
proof inspection, not the independent visual evaluation.

### Iteration 1: repair of the homily review

Revised 23 September 2026 at derive-homily iteration 1, after the homily review
returned one blocking finding and six advisories. The changes are in the two
homily components, the shared generation record and this entry. No research
record, study component, concise component or manifest entry was edited.

- HOM-001 (`sections/homily/10-homily.tex`, the Communion movement): the
  sentence "The one gift that is not borrowed is the humble admission that we
  need everything" is withdrawn. It answered the homily's own question by
  making humility the one present we bring that God did not give. That
  contradicts the Collect's *sine te*, which the homily expounds, and it
  departs from the study, which says the Communion's *hostiae* are "not
  something the worshipper owns and hands over". A new paragraph follows the
  two Augustine quotations and is set apart from them. It uses the study's
  formulation: the sacrifice the verse asks for is not something we own and
  hand over; it is the one present that claims nothing as its own and costs
  nothing but pride. It then quotes Paul's question to the same Corinthians,
  "What hast thou that thou hast not received?" (1 Cor 4:7, which the study
  quotes after Schuster on the Collect, re-read here in the tracked Douay
  verse table). It says that our confession and our humble heart are God's
  gifts too, which we bring back to him and which he is pleased to call a
  present. The rest of the speech was then read against the same rule, and two
  more sentences were changed. Of the paralytic's faith the speech now says
  that "if he had any, that too was given him". Of the penitent it says that
  he brings only his sins and his sorrow for them, "and the sorrow too is
  God's gift". No act that pleases God (faith, sorrow, confession or
  humility) is now presented as something not given. The note says that these
  statements apply the Collect and 1 Cor 4:7, are the homily's own, and are
  not Augustine's gloss.

The standing advisories were cleared in the same files:

- HOM-002: the penitent now brings "nothing to pay with: only his sins and
  his sorrow for them". The week's first response says the same: "go to
  confession, with your sins and your sorrow for them, and nothing to pay
  with".
- HOM-003: Hilary's gift is now given "to men, to all of us who receive
  them, through his word". A hearer cannot take it as the power of those who
  absolve.
- HOM-004: "The Gospel ends with commands" now reads "Christ's last words to
  the man are commands". Aquinas's triad is complete, and its third answer,
  *quia ire non poterat, dixit, Et ambula*, was read in the tracked Venice
  optical text at lines 16508–16511. It is added to the note's loci.
- HOM-005: the opening's "this whole Mass is gathered around him" now reads
  "the rest of this Mass can be heard around him".
- HOM-006: the note says that three disagreements are spoken. It names the
  third: Chrysostom against Aquinas, with Ambrosiaster and Cornelius a Lapide,
  on whether 1 Cor 1:8 accuses or promises.
- HOM-007: the note's route sentence names each author with his work. Ambrose
  on Luke, and Hilary and Aquinas on Matthew, were re-read; Jerome on Matthew
  and Aquinas on First Corinthians are reported as the study reads them.

To keep the speech near its length, three settled sentences that the repairs
did not need were removed. They are the opening's "Saint Matthew gives us not
one word of his", the Corinthian party names after 1:10, and "That deserves a
moment's honesty". Two clauses were shortened. The note's loci and
References follow the Scripture now spoken: 1 Cor 1:4–10 and 4:7, no longer
1:12. The note was tightened in wording only, so that the note, the
References, the timestamp and the colophon share the third page again.

**Spoken word count at iteration 1: 1,519 words**, by the same rule as at
iteration 0, which recounts the iteration-0 text as 1,448. At 120 to 130 words
a minute that is 11.7 to 12.7 minutes. This is at the upper edge of the
profile's approximately 10–12 minutes, and slightly beyond it at the slower
rate. The figure is arithmetic on the word count and not a timed delivery:
nobody has spoken these words, and no rehearsal was audible. The revised prose
was read through in full again, silently, for sense and for the line on grace
from the Collect to the close.

#### Upstream observation reported for the homily's cold reviewer

- The expansive study's `sections/40-nothing-of-our-own.tex` (the quietism
  subsection) has the same gap that HOM-004 found in the homily. It announces
  Aquinas's three disabilities and gives two of his answers. The third answer
  is in no research record. The homily's third answer was taken from the
  tracked Venice text and not from the study. Neither the study nor the
  research was edited.

#### Author proof and checks

The shared generation record carries the iteration-1 repair in this stage's
contribution and the revision timestamp `2026-09-23T15:35:00Z`. The expansive
and concise studies were rebuilt at that timestamp. They are unchanged at 34
and 12 physical pages, with clean logs. The concise study's settled auxiliary
file is still SHA-256
`462a8f9e960cdda5fdf5b065a768e40e967e02010a8442e00b75d1e6b21f8528`.

`make doc DOC=liturgy/roman-rite/1962/propers/temporal/58-eighteenth-after-pentecost-homily PROVIDER=claude`
settles with no overfull or underfull box, no undefined reference, no LaTeX
warning and no rerun request. The PDF has 3 physical pages, letter size, Latin
Modern Roman and Mono only, all embedded, subsetted and Unicode-mapped.
Deleting the PDF, the auxiliary file and the log and building again
reproduced the same bytes. The component content check with presentation and
format passes. So does every homily `check-content-preflight` check,
including references-used and provenance-matches-run against this run, and
so do the component artifacts check and `check-generation-metadata`.

The settled proof is SHA-256
`62a1014c221118c3f432069eecba1147615d723dcfebb25b062d5e52eb2d4bb7`. Its
auxiliary file is SHA-256
`96da8bd61cc21463cd3eda0260cb058d26e765e456536a181a79f8efa1798486`. The
expansive and concise studies rebuilt at the same timestamp are SHA-256
`5dd437b0355d8fb1d20896f6e0a4d4dd31eeba738e2fa8f91adf4c990560821b` and
`ea145b8e60cc2c651bf78f417cdfbcef68ea91582a76bbd334f56e7f05a3a161`.

The author read the rasters of all three pages:

- The speech fills pages 1 and 2 in two balanced columns under the full-width
  title. It ends near the foot of page 2, and its five wider spaces mark the
  six movements.
- The note, the References, the revision timestamp and the rights colophon
  share page 3.

A first layout of this revision put the timestamp and colophon on a fourth
page. The note's wording was tightened, and nothing was set smaller. The
proof shows no clipping, collision, missing text, blank page or heading-only
page. This is an author proof inspection, not the independent visual
evaluation.

## Build-artifacts

Iteration 0 of the build stage for run `71b6f89518984232` at commit
`fa5355745b5e973584f047a7f59a20ad22676d64`. No source file was edited at this
stage: no layout repair was needed, so no content seal is affected and the
shared generation record keeps its revision timestamp `2026-09-23T15:35:00Z`,
which all three PDFs display.

### Builds

The three earlier proofs, with their auxiliary, log, recorder and metadata
stamps, were deleted, and each output was built fresh with
`make doc DOC=<id> PROVIDER=claude` for the bare document, `-synthesis` and
`-homily`. Each build settled through the Makefile's fixed-point passes and
passed generation-metadata validation, and the two companions passed the
component manifest check. The fresh builds reproduced the author proofs byte
for byte.

| Output | Physical pages | PDF SHA-256 |
| --- | --- | --- |
| `build/claude/liturgy/roman-rite/1962/propers/temporal/58-eighteenth-after-pentecost.pdf` | 34 | `5dd437b0355d8fb1d20896f6e0a4d4dd31eeba738e2fa8f91adf4c990560821b` |
| `build/claude/liturgy/roman-rite/1962/propers/temporal/58-eighteenth-after-pentecost-synthesis.pdf` | 12 | `ea145b8e60cc2c651bf78f417cdfbcef68ea91582a76bbd334f56e7f05a3a161` |
| `build/claude/liturgy/roman-rite/1962/propers/temporal/58-eighteenth-after-pentecost-homily.pdf` | 3 | `62a1014c221118c3f432069eecba1147615d723dcfebb25b062d5e52eb2d4bb7` |

The expansive study falls within 20–50 pages and the concise study within
10–12. The concise study's settled auxiliary file is SHA-256
`462a8f9e960cdda5fdf5b065a768e40e967e02010a8442e00b75d1e6b21f8528`; its
log is `616a78dadf49c70bb927251b323c6bc76e4dec6ecc07db2efbbbfd0cd4397afc`.
The expansive study's auxiliary file and log are
`1b4b9eb18cf6af9a247303aca3d045c27557527c738fd92013fc24265ac66328` and
`34d4e74d2bb62ad16c2f6f4a41f1a6019058041559abb25a66755d48c81e081e`.

### Log, font, structure and extraction checks

- **Logs.** None of the three logs has a TeX error, an undefined or
  multiply defined reference, an overfull or underfull box, a LaTeX or
  package warning, or a rerun request. The only line matching "warning" is
  the `rerunfilecheck` package banner.
- **Fonts.** Every font is Latin Modern (Roman, Roman Caps or Mono), Type 1,
  embedded, subsetted and Unicode-mapped. Nothing was substituted.
- **Structure.** All three are unencrypted letter-size PDF 1.7 files from
  pdfTeX 1.40.29. Their titles and subjects name the Missal and the Sunday.
  Poppler's `pdfinfo`, `pdffonts` and `pdftotext` read them without a parse
  error. No stricter PDF validator (qpdf or pypdf) was installed, so none was
  run.
- **Extraction.** Text extracts from every page, with no `??` marker and no
  replacement character. The extracted word counts, apparatus included, are
  22,123 for the study, 9,461 for the concise study and 2,438 for the homily.
- **Concise opening.** The settled `zref` evidence places the inventory,
  the overview and the four sense rows (literal, allegorical, moral,
  anagogical) on physical page 1. It places the chronology on page 2, the
  themes from page 3 to page 4, and the start of the commentary on page 5.
  The extracted text agrees. Page 1 carries the map and exactly the four
  sense rows. Page 2 is headed only "Scriptural Date and Location". Pages 3
  and 4 carry "The Propers: Themes and Movement". Page 5 opens "The Propers:
  Detailed Commentary".
- **Gates run ahead.** Both `tools/check-proper-components --phase artifacts`
  and `scripts/_proper_study.py check --phase artifacts --require-presentation
  --require-format` pass against the snapshot below. The second check
  includes `check-generation-metadata` on each PDF.

### Snapshot and rasters

`python3 scripts/_proper_study.py snapshot` wrote `research/artifacts.json`
from the final builds. It records the three PDF hashes above, 27 render
inputs, and the pagination evidence for the two studies (their auxiliary files
and logs). Bounded rasters and contact sheets for all 49 pages came from
`tools/tpt pdf-review` and are in the run's `build-artifacts-0000/rasters`
child. The logs, auxiliary files, extracted text and check output are kept
beside that child, outside it.

### Remaining limitations for the visual reviewer

The build worker only glanced at the contact sheets to decide whether a layout
repair was needed. That glance is not the visual review. Two pages of the
expansive study are short because they end a section that the next heading
starts on a fresh page:

- page 22 (about 280 words) ends the second reading's four senses;
- page 29 (about 150 words) ends "The Three Readings Compared" before the
  Scriptural Date and Location appendix.

These are ordinary section ends, not warnings, and they were left alone
because any repair would be a source edit that reopens reviewed content. The
visual reviewer should judge whether either is a sparse spill.

## Reviews completed after the artifact build

These are the engine's own recorded results for run `71b6f89518984232`, as
the run holds them; no acceptance is claimed beyond them.

- **Artifact gates, iteration 0 — PASS.** `_proper_study.py check --phase
  artifacts --require-presentation --require-format` exited 0 against the
  snapshot in `research/artifacts.json`.
- **Visual review, iteration 0 — PASS.** Every page of the three sealed PDFs
  was inspected: 34 pages of the study, 12 of the concise study and 3 of the
  homily. Two findings were accepted, VIS-001 (the sparse closing page 29 of
  the study) and VIS-002 (the comparison table carrying one row onto page 28).
  Three were advisory: VIS-003 (the dossier note sitting close to its top
  rule), VIS-004 (two abutting comparison-table headers) and VIS-005 (unequal
  movement breaks in the homily). One observation records that the shared
  dossier-table measurements differ from those the 1962 profile states.
- **Generate-web, iteration 0 — PASS.** The canonical study alone was
  converted. `research/web-artifact.json` records the conversion at SHA-256
  `12acf5ccdbe373e848bf5fc5657e7e45387ab6316f5284e6f2622cd706ace915`.
- **Web review, iteration 0 — PASS.** It found one advisory, WEB-001: the
  converter drops the second and third `\propertitle` fields, the Latin title
  and the Missal line, from the web title block. Both strings recur in the H1
  and the opening, so no fact is lost. It also made one observation, on how
  the full-width dossier rows linearize.

## Install-publication, iteration 0 — 23 September 2026

### Installed PDFs

The snapshot was confirmed current before anything was installed.
`_proper_study.py check --phase artifacts --require-presentation
--require-format` exited 0, and each build PDF, both sealed `.aux` files and
both sealed `.log` files hashed to the values in `research/artifacts.json`. The
three PDFs were then installed with the normal recipe, one at a time. Nothing
was suppressed: no `-o`, no `-t`, no timestamp change and no source edit.

```sh
make install-doc DOC=liturgy/roman-rite/1962/propers/temporal/58-eighteenth-after-pentecost PROVIDER=claude
make install-doc DOC=liturgy/roman-rite/1962/propers/temporal/58-eighteenth-after-pentecost-synthesis PROVIDER=claude
make install-doc DOC=liturgy/roman-rite/1962/propers/temporal/58-eighteenth-after-pentecost-homily PROVIDER=claude
```

A dry run showed beforehand, and the real runs confirmed, that Make found all
three PDFs current. It ran the metadata source check and
`check-generation-metadata` on each, then copied the bytes. Nothing was
retypeset, and the sealed `.aux` and `.log` files are unchanged. The build
PDF and the installed PDF each hash to the value that the build, the artifact
gates and the visual review recorded:

| Output | Pages | Bytes | SHA-256 (build and installed) |
| --- | ---: | ---: | --- |
| `58-eighteenth-after-pentecost.pdf` | 34 | 568,330 | `5dd437b0355d8fb1d20896f6e0a4d4dd31eeba738e2fa8f91adf4c990560821b` |
| `58-eighteenth-after-pentecost-synthesis.pdf` | 12 | 477,461 | `ea145b8e60cc2c651bf78f417cdfbcef68ea91582a76bbd334f56e7f05a3a161` |
| `58-eighteenth-after-pentecost-homily.pdf` | 3 | 275,620 | `62a1014c221118c3f432069eecba1147615d723dcfebb25b062d5e52eb2d4bb7` |

No hash differs, so no artifact defect is reported and no review boundary is
reopened.

### Web edition, release records and wiring

The reviewed conversion `build/web/claude/.../58-eighteenth-after-pentecost.md`
was copied byte for byte to `web/claude/.../58-eighteenth-after-pentecost.md`:
132,138 bytes, SHA-256
`12acf5ccdbe373e848bf5fc5657e7e45387ab6316f5284e6f2622cd706ace915`, with a
clean `cmp`. It was staged, so `git ls-files --error-unmatch` finds it. No
synthesis or homily web leaf exists; the canonical study remains the only web
authority.

`make add-publication ID=<id> CATALOG=library/traditional-latin-mass.md
PROVIDER=claude STATUS=alpha` created one release record per PDF under
`release/publications/claude/`. No record existed beforehand. Each record has
schema version 1, its own output id, the 1962 catalog, status `alpha` and the
standing authorization `perpetual-public-repository-2026`.

In `library/traditional-latin-mass.md`, the Claude cell of the existing row 58
changed from `Planned` to Full PDF, Synthesis PDF, Homily PDF and Read. That is
the order of the schema-2 manifest's `canonical_label`, `synthesis_label` and
`homily_label`, followed by the canonical web page. The ChatGPT cell, every
other row and every other page are untouched, and no companion row was added.
`release/public-alpha.json` names `gpt` as primary provider, so the one new
canonical marker carries the provider prefix:
`claude:liturgy/roman-rite/1962/propers/temporal/58-eighteenth-after-pentecost`.

### Catalogue, release bindings and source inventory

`make document-catalogue` regenerated `src/web/data/structure/documents/corpus.json`.
Every change belongs to this leaf. A new work carries the study, the two
companions under `also`, the web page, the three contribution records the
leaf's generation metadata declares and this run's `produced` identity. The
counts moved by one work, one document, three issues and 34 pages. The
provider, section and model tallies moved with the new work, and
`claude-opus-5-5[1m]` gained its model entry. A comparison against the
committed projection, work by work, finds no other work added, removed or
changed.

The release refresh followed the repository's scoped rule. `make
refresh-release-bindings ADOPT=1 ONLY="library/traditional-latin-mass.md
web/claude/.../58-eighteenth-after-pentecost.md
src/web/data/structure/documents/corpus.json"` made five changes: it adopted
the new web edition, re-recorded the catalogue page and the projection, and
rewrote the rights table and its digest. Sixteen bindings stay stale because
this stage did not write them: `scripts/_proper_components.py`,
`src/web/data/structure/sources/index.json` and fourteen new source-edition
projections, all committed earlier on this branch. They are the bindings the
maintainer's release-rebind approval of 2026-09-23 covers, and
`PROJECT-WORK.md` records that approval for application at `publication-gates`,
with its own note. This stage did not adopt them.

`tools/tpt source-inventory refresh
src/sources/inventories/claude-publications-v1.toml --review
src/sources/inventories/claude-classification-review-v1.toml --audited-on
2026-09-23` added this publication and its source-bearing files to the Claude
publication inventory. The leaf's classification row was then replaced from
its placeholder by an audit of the 83 source ids in
`research/source-bindings.toml` and of the witnesses its research records name
without a binding. That audit gave these categories:

- scripture: the Clementine Vulgate, Douay–Rheims and the CATSS LXX morphology;
- liturgical: the 1962 typical edition, its 1862 Pustet and Benziger printings,
  the 1861 Cummiskey English, and the Gelasian, Gregorian and Veronense
  sacramentaries;
- patristic: Ambrose, Athanasius, Augustine, Bede, Cassiodorus, Chrysostom,
  Hilary, Jerome and Theodoret;
- scholastic: Aquinas, Bellarmine, Cornelius a Lapide, Rabanus Maurus,
  Theophylact, Anthony of Padua, and the medieval commentators on the Mass:
  Berno, Bernold, Durandus, Honorius, Rupert and Sicard;
- historical-primary: the Migne volumes and their facsimiles;
- institutional-current: the FSSP and ICRSP ordos for 2026 and the USCCB
  introduction to the Psalms;
- secondary: Guéranger, Schuster, the *Catholic Encyclopedia*, and Morin and
  Wilmart in the *Revue bénédictine*;
- finding-aid: the gregorien.info chant database.

No magisterial, prayer-devotional or repository-internal source occurs in the
leaf's records, so none of those categories was assigned.
`tools/tpt source-inventory classify` then applied the row. The tool's own
functions recomputed both snapshots.

### Publication-gate commands run by this stage

These are this stage's own runs of the terminal gate commands. They are not an
acceptance, and nothing has been committed.

- `_proper_study.py check --phase publication --require-presentation
  --require-format` exits 0.
- `tools/tpt public-alpha check --provider claude --document <leaf>` exits 0:
  the scoped policy is valid for the three outputs, and the global source,
  release and authorization records are valid.
- `tools/tpt document-library check` with `document-library structure --check`
  exits 0, and the projection is current.
- `make check-web-editions-current` exits 0.
- `make check-release-bindings` exits nonzero. It reports only the sixteen
  bindings named above, none of which this stage wrote. All three of this
  stage's paths are bound exactly.

## First revision, 23 September 2026 (outside the workflow)

### What this revision is, and why it was made directly

This is the leaf's first revision after publication. It discharges the three
revision obligations the maintainer recorded on 23 September 2026 in
`src/sources/inventories/research-staleness-v1.toml`: HOM-010 for the homily,
STU-005 for the dossier date, and RES-032 for Chrysologus. It changes nothing
else. The workflow has no mode for revising an accepted leaf. `proper-study`
seeds a new production and runs every review again, and it is meant for new
and substantially revised guides. Three bounded corrections are neither. So
the revision was made directly, under the profile's rules. It follows the
precedent of the Seventeenth Sunday's dated dossier correction
(`57-seventeenth-after-pentecost/research/chronology-revision-2026-09-21.md`,
commit `6caf8946d`). That precedent edited under the profile, recorded the
revision in the leaf's own research records, and claimed no workflow
acceptance for it.

The archived run `71b6f89518984232` under `evaluations/proper-study-results/`
is unchanged, and so is `evaluations/blocking-findings-v1.toml`. Only an
evaluation writes that file, and it still lists HOM-010, STU-005 and RES-032
as the run left them. The generation provenance still names the run, and the
new contribution record says that the provenance identifies the historical
production, not acceptance of this revision. The revision timestamp,
`2026-09-24T03:02:51Z`, is UTC; the revision was made on 23 September local
time.

### HOM-010: the Eucharist and the Paschal mystery in the preacher's own voice

`sections/homily/10-homily.tex`, the fifth movement's last paragraph. Two
sentences were taken out: "So the sacrifice this verse asks for is not
something we own and hand over", and the clause "we bring them back to him".
Three sentences were written in the preacher's own voice. The first hears the
assembly's own approach to Communion in the Communion's "come into his
courts": "We carry them into his courts when we come up to this altar". The
second and third say what the Postcommunion's "what we have received" is:
"the holy sacrifice that last prayer thanks him for", "Christ himself, his
Body given up on the Cross and his Blood poured out for the forgiveness of
sins, the Lord who died and rose again". The words "what we have received"
are the 1861 Cummiskey English already quoted in the movement. None of this is
credited to a Father. It is the Church's faith, and it agrees with the second
reading, which joins the altar to the blood shed "for the remission of sins".
The optional fourth-movement sentence that HOM-010 offered was not added. The
fifth movement's "Blood poured out for the forgiveness of sins" already
grounds the forgiveness in the Passion, and the speech was at the top of its
length.

**Spoken word count after HOM-010: 1,562 words**, up from 1,519 (the second
pass below trims the speech to 1,438). The count uses the rule
recorded at iteration 0, which reproduces both earlier figures: 1,448 for
iteration 0 and 1,519 for iteration 1. At 120 to 130 words a minute that is
12.0 to 13.0 minutes, a little beyond the profile's approximately 10–12 at the
slower rate. The figure is arithmetic and not a timed delivery. The whole
revised speech was read through silently for sense and for the join from the
fifth movement into the sixth. The homily note's "Length and pace" carries
the new figure. Its "Relation to the reviewed readings" paragraph was not
extended: an added clause pushed the rights colophon onto a fourth page, so
the relation of the new sentences is recorded here instead, as the profile's
"terminal note or audit" allows.

### STU-005: the Introit's per-passage dates

`sections/80-date-location.tex` (expansive) and
`sections/concise/03-date-location.tex` (concise), in the Introit's
`\dossierprose` row. The statement that the record answers the two loci
separately was replaced by the dates, in the per-passage form of
`guidance/scripture-chronology.md` § 14.1:
`Ecclus~36:18: B.C.~190--170 or c.~B.C.~280` and
`Ps~121:1: before c.~165~B.C.`. Each carries its relation (composition), its
profile and its source in the same sentence. The Date cell is unchanged and
still prints the generated annotation.

The dates are the generated concise displays of the claims in
`research/chronology.toml`, printed by the wiring's own projection:

    cd scripts && python3 -c 'import _proper_chronology as w; d = w.dossier("liturgy/roman-rite/1962/propers/temporal/58-eighteenth-after-pentecost", provider="claude"); [print(",".join(r.locus for r in c.reaches), c.disposition, c.profile, c.label, "=>", w.concise_display_label(c)) for e in d.elements if e.key == "introit" for c in e.claims]'

That prints `Ecclus.36.18 preferred catholic-traditional-v1 between 190 and 170
B.C. => B.C. 190–170`, `Ecclus.36.18 alternate catholic-traditional-v1 about
280 B.C. => c. B.C. 280` and `Ps.121.1 preferred catholic-critical-v1 before
the Maccabean period, around 165 B.C.; … => Before c. 165 B.C.`. The raw labels
agree with `tools/tpt scripture-chronology query Ecclus.36.18` and `… Ps.121.1`.
`tools/tpt proper-chronology record --check` and `annotations --check` both
still pass, so the record and the annotation file are current and were not
rewritten. `check-content-preflight --check chronology-claims-supported`
reports 3 per-passage dates in each study, each the record's answer for the
passage it names. As a negative test, the concise row was altered on a scratch
copy to `c. B.C. 290` and to a psalm label carrying the Ecclesiasticus
interval. The checker refused both, naming the record's answers at
Ecclus.36.18 as `['B.C. 190–170', 'c. B.C. 280']`, and the file was restored
byte for byte.

### RES-032: Peter Chrysologus, Sermo 50

The research record now carries the sermon. In `research/scope.md`: the
revision note at the head; in § 3.5 the Rabanus v. 2 bullet, the Catena's
other lemmata, a new Chrysologus entry and the "No Father … reported only by
another" bullet; § 4.2; § 6.3; and § 10 item 1. In
`research/interpretations.md`: § 3.2 and the `gospel` bullet of § 3.3. In
`research/source-bindings.toml`: the PL 107 facsimile binding's context, and
six new bindings. Those are the Sermo 50 passage, the PL 52 leaves n171 and
n172, the Maximus Homilia CVIII passage, and the PL 57 leaves n254 and n255.
Every page image was hashed and matched before it was read. The places quoted
were read on the images: col. 339C, cols. 341A–B and col. 342B in PL 52, and
the admonition and col. 504 in PL 57. The sequel that the record had called
untraced, the text Rabanus prints under *(Joan. Chrysost.)* at PL 107,
col. 871, is identified as Sermo 50. The Catena's "Ioannes episcopus" lemma
was not re-read. Its recorded opening words answer to Bede's sentence at the
head of that same compilation, which is not in Sermo 50, so the review's
identification of the lemma with the sermon is recorded as the review's
finding.

In the expansive study, `sections/40-nothing-of-our-own.tex` gains one
paragraph after St Ambrose in "The man who was carried". It says that the
sermon takes the bearers' side and reads the man's silence against him. It
quotes *Audit veniam …*, *fidei alienae suffragio* and *Deum non quaerere …
quod per solam gratiam conferebat* from PL 52, col. 341. It states that Migne
prints the text both as Chrysologus's Sermo 50 and as Maximus of Turin's
Homilia CVIII, and that its author is disputed. It gives the Breviary's use on
this Sunday only as Maximus's editor reports it. The main clause *offerentium
fidem non respicit*, whose reading is unsettled, is not quoted. The References
gain one entry, and the scope appendix gains one clause on how the sermon was
read. D11 does not reach the sermon, because it preaches this formulary's
Gospel. `proper-components.toml` adds "Peter Chrysologus" to the third lane's
`authors` but not to `carrying_authors`, because the ascription is disputed.
The concise study and the homily do not use him. The concise study may
introduce no source-dependent claim of its own, and the homily's account of
whose faith Christ saw needs no further witness.

### Substantive word counts and rendered pages

By the homily rule, the third reading grows by 177 words, the scope appendix
and References by 27, and the expansive dossier falls by 6. The concise
dossier falls by 1.

| Output | Pages | Bytes | SHA-256 (build and installed) |
| --- | ---: | ---: | --- |
| `58-eighteenth-after-pentecost.pdf` | 34 | 569,432 | `72bd8bdc19439c860eae6d3ca0575d0c70377ebe9fccf347e8fb76916b7f4e2c` |
| `58-eighteenth-after-pentecost-synthesis.pdf` | 12 | 477,495 | `30b61281ed3af6e1e9c7f6b6faf9f824c943b9fbe3cb3832193d2b6a8aed5859` |
| `58-eighteenth-after-pentecost-homily.pdf` | 3 | 275,779 | `89bd3573383b01a1437e85c90a2f9b9dd2a0509eed9770218e8db537a19a195b` |

These were the bytes of the first pass. The second pass below supersedes them.

The web edition is `web/claude/…/58-eighteenth-after-pentecost.md`: 133,869
bytes, SHA-256
`a18360d8d60b13309c0821015f98a7e25f53d5e0fdc71b6f7466cf68b560f8aa`. It is
byte-identical to the fresh conversion, and its diff against the previous
edition is exactly the four changed passages and the timestamp.

The new paragraph moves the study's comparison table from a break after six
rows to a break after three, with the header repeated. It also fills the
formerly sparse page 29 to about two fifths. These are the pages of accepted
findings VIS-002 and VIS-001. The scope clause and the Reference entry were
shortened until the rights colophon stood again on page 34 rather than alone
on page 35. The concise page 2 still holds the whole dossier, and the homily
still ends on page 3. Every changed page was inspected on rasters from
`tools/tpt pdf-review`: study pp. 24–25, 27–30 and 32–34, concise p. 2, and
homily pp. 2–3. The logs of all three builds show no overfull or underfull
box, no undefined reference and no rerun warning, and every font is embedded.

### Checks run

- `make doc`, then `make install-doc`, for all three outputs. The installed
  bytes equal the build.
- `_proper_study.py check --phase content`, `artifacts` and `publication` with
  `--require-presentation --require-format` exit 0. So does `content` with
  `--require-authority`.
- `check-proper-components --phase artifacts` exits 0: it checks the concise
  physical-page markers.
- `check-generation-metadata` exits 0 on each PDF.
- `check-content-preflight` exits 0 on `leaf`, `research`, `synthesis` and
  `homily`, with 89 bindings valid.
- `make check-web-editions-current` exits 0, as does `check-web-edition`.
- `public-alpha check --provider claude --document <leaf>` exits 0.
- `source-library validate` exits 0, and `make check-source-reader` reports
  the projection current.

The two build receipts, `research/artifacts.json` and
`research/web-artifact.json`, were rewritten by `_proper_study.py snapshot`
and `snapshot-web`. They record these bytes and approve nothing. The
`.log` hashes in `artifacts.json` include this checkout's path, so another
checkout will report the snapshot as differing until it rebuilds, as the
original receipt already did here.

### What this revision still needs

The acceptance of run `71b6f89518984232` does not cover these bytes. Still
needed are an independent content review of the changed research and of the
three documents, a visual review of the changed pages, and a web review.
Three shared derived files are stale and belong to the coordinator: the
document catalogue `src/web/data/structure/documents/corpus.json`, where this
leaf's entry gains the new contribution and timestamp; the release binding of
the web edition; and the Claude publication inventory, which is stale for ten
of this leaf's files. The revision obligations in the research-staleness
ledger and the deliverable requirement `eighteenth-sunday-introit-dated` are
the coordinator's to clear. The standing findings are disposed of in the
second pass below.

### Second pass: the run's standing findings resolved

On the maintainer's request that every known open issue be resolved, the same
revision took up the findings standing in `evaluations/blocking-findings-v1.toml`.
That file is left as the evaluations wrote it. Each finding was read in full, and
each cited source layer was re-read here before the text moved. One line per
finding follows.

| Finding | Disposition | Where, and what changed or why |
| --- | --- | --- |
| HOM-008 | Fixed | Homily, third movement. Before: "Once laid down, says Chrysostom, he ``gives himself up to the power of the healer.''", set before the first word. After, following the word of forgiveness: "He came to be healed and is forgiven instead; he might have complained, Chrysostom says, but he says nothing, and ``gives himself up to the power of the healer.''" Re-read in the tracked CCEL NPNF1-10 text (`adb8f1c9`), Hom. 29 § 2, where the sentence answers "One thing I came to have healed, and amendest Thou another?" after the scribes' murmur. |
| HOM-009 | Fixed | Homily, same movement. Before: "Whatever faith he had brought him exactly as far as he was carried, and if he had any, that too was given him." After: "Whatever faith he had, it brought him only as far as he was carried; and if he had any, that too was given him." |
| HOM-011 (accepted; its condition, re-entry of the study, is met) | Fixed | `sections/40-nothing-of-our-own.tex`, "Not quietism": the triad is completed with *quia ire non poterat, dixit, Et ambula*, "because he could not walk, he said, Walk". Read in the Venice 1745 optical layer (`10aa155e`), physical lines 16507–16512; homily review read the page image, PDF p. 140. Recorded in `research/scope.md` § 3.5 and `research/interpretations.md` § 3.4. |
| RES-031 | Fixed | In four places: interpretations § 2.2; scope § 3.5 (V.14 bullet); scope § 10 item 1 (the Aquinas bullet); and the scope header's fifth re-entry. Ambrose, *Exp. in Lc.* V.14, was re-read in the tracked transcription (`fde2303a`). It has the body as the bed washed nightly with tears (Ps 6:7), *lectus doloris, in quo anima nostra gravi conscientiae aegra cruciatu jacebat*, the bed of rest, and the return to paradise. "Is not penitential" and "Aquinas's …, not Ambrose's" are withdrawn. The fence stays: *per contritionem … per satisfactionem … in domum aeternitatis, vel in conscientiam propriam* is Aquinas's and no Father's. |
| RES-033 | Fixed | In three places: interpretations, "Two further boundaries"; scope § 2.7; scope § 10 item 16. Each now says four of the five name this Communion, and that Sicard names the Offertory and Communion together only by their sense. `commentary-work-index formulary --calendar roman-1962 --mass pentecost-18` lists communion among Sicard's unnamed elements. His *Mitrale* VIII.18 layer (`ea9fd813`, lines 29685–29728) reads *in offerenda et communione invitat et monet populum revertentem, ad instar Moysi, altaria erigere et hostias immolare*. |
| RES-034 | Fixed | The continuation's vol. XI (`95ba98e2`) was read on its rendered pages. Pp. 408–409 (PDF pp. 429–430), *other victims, that is ourselves*, are recorded in scope § 3.11 and in interpretations § 2.3 (communion) and § 2.4 (Moral), under the continuator's name. P. 395 (PDF p. 416), the sentence before the Collect, is recorded in scope §§ 3.9 and 3.11 and interpretations § 3.2. Aquinas's *quia portabatur, praecepit ut portaret* is recorded in scope § 3.5 and interpretations § 3.4. PDF pp. 416, 429 and 430 are added to the § 6.3 register row, and `vol-xi-p-395` to the binding's loci. |
| RES-035 | Fixed | Interpretations § 4.4, the anagogical note. Before: "the way back to paradise (the second, with Hilary, Ambrose and Aquinas)". After: "the way back to paradise (Hilary, Ambrose) and to the house of eternity (Aquinas), in the second". The concise overview already kept them apart. |
| RES-036 | Fixed | Interpretations § 3.2, Chrysostom on 1 Cor 1:8. New Advent's `220102.htm` was re-fetched, and its SHA-256 matched the recorded `66bffe29…5858`. § 7 reads "Here he seems to court them, but the saying is free from all flattery; for he knows also how to press them home … But he is also covertly accusing them". "This covert accusation is Chrysostom's whole reading of v. 8" is withdrawn, and § 7 is given as it stands. |
| STU-023 | Fixed | Interpretations, three changes. § 2.4 Literal: "At Capernaum" became "In his own city (Capernaum for Chrysostom, Nazareth for Jerome; § 4.3 leaves the town undecided)". § 1.2: "the one checked witness" became "the one Father", with Aquinas added. § 1.3: Aquinas is added as the second allegorical witness. His *scilicet in civitatem gentium, quae sibi datae sunt* is at Venice layer lines 16345–16346. |
| STU-024 | Fixed | `sections/10-each-element.tex`. In the Offertory, Schuster's regret over the lost verses and the a Lapide and Chrysostom-on-Hebrews paragraph are removed, leaving one clause: "and the covenant blood of the chapter it cites is taken up in the second reading". In the Secret, Schuster's sentence on the exchange became "What the exchange is, the second reading takes up." The a Lapide reading, the exchange and Schuster's regret now each have one home, in the second reading. |
| SYN-008 (not in the coordinator's list; leaf-local and open) | Fixed | `sections/concise/04-themes.tex`: "confesses in its single prayer" became "confesses in its Collect", and "the Mass's only oration" became "the Mass's only collect". |
| VIS-003 | Fixed | `sections/80-date-location.tex`: a `\medskip` after the introductory sentence. Study p. 30 inspected; the line no longer sits on the rule. The shared table style is untouched. |
| VIS-004 | Fixed | `sections/50-comparison.tex`: the header "Power on earth to forgive" became "Power to forgive". Pp. 27–28 inspected; each header now has clear space before the next. The shared table style is untouched. |
| VIS-005 | Fixed | `sections/homily/10-homily.tex` opens with multicol's `\raggedcolumns`, so each column's foot takes a `\vfil` instead of stretching the movement breaks. Homily pp. 1–2 inspected; the five breaks are one height, and the log has no underfull or overfull box. The shared homily environment is untouched. |
| VIS-001, VIS-002 (accepted; conditional on reopening) | No longer arise | P. 29 now carries 23 lines of the comparison's close rather than about eight. The comparison table breaks after three rows with its header repeated, so no single row stands alone. |
| Research-review observation: the scope header undercounts the re-entries | Fixed | `research/scope.md` header now records research iteration 7 (`c2c54133a`), which revised `research/interpretations.md` alone for STU-020. Of the other three observations, the web edition's squeezed dossier rows were resolved upstream (commit `0df032e15` sets each dossier note as a paragraph beneath its row); the shared dossier measurements belong to records this leaf does not own and are left to their owners. The first observation, that the index lists Chrysologus only at Luke 22, no longer holds: its Matthew 9 row names his *Sermones* (commit `3cc830e86`), and `discover --passage "Mt 9:1" --max-results 0` reports his held fragment, Sermo 50, at Mt 9:1–7 (rechecked in the third pass, which corrected an earlier line here that called the row missing). |
| WEB-001 | Already resolved | Converter commit `0df032e15` restored the title fields; the current web edition carries all four title lines. |

**Homily length.** The profile asks for approximately 10–12 minutes at an
unhurried pace and names no rate. The leaf's note uses 120 to 130 words a
minute. The speech is now **1,438 words**, 11.1 to 12.0 minutes at those rates,
within the range at both. It was 1,562 after HOM-010. The cuts are in the
homily's own wording, except that Chrysostom's second question, "Whence is it
that you are puffed up?", is no longer quoted; no quotation's wording was
altered. They are:
- the Collect's "the prayer said just before the Epistle";
- in the Chrysostom-on-Corinthians paragraph, that second question, with two
  sentences compressed;
- "perhaps even my faithfulness in coming here week after week";
- "The first costs nothing to say; nobody can check it. The second anyone can
  check at once.";
- a sentence of the Aquinas authority paragraph, compressed;
- "greater than all men";
- "The bed that carried him, he now carries.";
- "Do not leave your sins to your feelings".

HOM-010's sentences are unchanged. The note carries the new figure. The count
rule is the one recorded at iteration 0.

**Maximus of Turin.** `src/sources/inventories/author-standing-v1.toml` gains
one row for him, standing `father`. It rests on three sources read here: the
*Catholic Encyclopedia*'s "St. Maximus of Turin" (vol. 10, 1911); its "Fathers
of the Church", in the sentence that also grounds Chrysologus; and the Roman
Martyrology in the English of the 1914 Roman edition (Baltimore, 1916), whose
25 June entry reads "At Turin, the birthday of St. Maximus, bishop and
confessor, most celebrated for his learning and sanctity". `commentary-work-index
standing` passes with 31 persons, and `tools.tests.test_author_standing` passes.

**Word counts of this pass, by the homily rule.**
- Element section: −96.
- Third reading: +15.
- Comparison: −2.
- Concise themes: −1.
- Homily: −124.

**Rendered pages after the second pass.** Printed pages: study 34, concise
study 12, homily 3. The pages whose text or layout moved are study pp. 10–11,
26–28 and 30, concise p. 3, and homily pp. 1–2. Each was inspected on rasters
from `tools/tpt pdf-review`, together with study pp. 29 and 34. The final
hashes are in the commit that installs them and in `research/artifacts.json`.

**Checks after the second pass.** All three outputs were rebuilt with
`make doc` and installed with `make install-doc`; the installed bytes equal
the build.

| Output | Pages | Bytes | SHA-256 (build and installed) |
| --- | ---: | ---: | --- |
| `58-eighteenth-after-pentecost.pdf` | 34 | 569,016 | `c75624211f7b9fb26eeddd385fcec71201f89b10d210f3b801e9bbd510ed55e3` |
| `58-eighteenth-after-pentecost-synthesis.pdf` | 12 | 477,472 | `27b5f2270afcbd079b077d3560b1982338e239edd829e766e6b3e7fe1d90f7ec` |
| `58-eighteenth-after-pentecost-homily.pdf` | 3 | 275,105 | `eba6268e7ddc1160728975b616093fe6caf0e60c675a2ef747246f1b398d71a5` |

The web edition is 133,361 bytes, SHA-256
`e90a3c6362c11e17470b0f03fcfb019359b2227512d29e4c850eb935287af07c`, identical to
the fresh conversion. These exit 0:

- `_proper_study.py check` in phases `content`, `artifacts` and `publication`
  with `--require-presentation --require-format`, and `content` with
  `--require-authority`;
- `check-proper-components --phase artifacts`;
- `check-generation-metadata` on each PDF;
- `check-content-preflight` on all four editions, with 89 bindings and 3
  per-passage dates in each study;
- `proper-chronology record --check` and `annotations --check`;
- `make check-web-editions-current` and `check-web-edition`;
- `public-alpha check --provider claude --document <leaf>`;
- `source-library validate`, `make check-source-reader` and
  `make check-commentator-inventories`.

The logs show no overfull or underfull box, no undefined reference and no
rerun warning.

The same 13 test modules as at the start pass: 492 tests. Two modules were
added this pass. `test_formulary` passes. `test_house_voice` fails three tests
of `TheSpecimenLeaf`, which reads the Fourteenth Sunday leaf. Neither that leaf
nor `tools/` nor `scripts/` differs from base `f5a3be5f4`, so the failure is
inherited, not caused here. Stale for the coordinator, as before: the web
edition's release binding, this leaf's entry in `corpus.json` (two new
contributions and the timestamp), and fourteen of this leaf's files in the
Claude publication inventory.

### Third pass: D12 in the concise study, the index at Matthew 9, portable receipts

**D12.** The three-document profile keeps the history of a formulary's texts in
early lectionary and sacramentary lists out of the concise study and the
homily; the leaf is reopened, so the grandfathering for this paragraph alone no
longer shields it. `sections/concise/04-themes.tex` loses five passages. Each
is carried in the expansive study already:

- the Collect's Old Gelasian and Gregorian placement, carried in
  `sections/10-each-element.tex`, the Collect;
- the Würzburg gospel and epistle lists, with Schuster's *Tertia post natale
  Sancti Cypriani* and the Ember-Saturday vigil and the Ephesians course of the
  neighbouring Sundays, carried in `00-opening.tex` and in `10-each-element.tex`,
  the Epistle and the Gospel;
- the Sextuplex chant witnesses, carried in `10-each-element.tex`, the Gradual
  and the Alleluia;
- "as the Pustet Missal of 1862 already does" at the Communion, carried in
  `05-appointed-texts.tex` and `10-each-element.tex`;
- the Old Gelasian's two Postcommunion placements, carried in
  `10-each-element.tex`, the Postcommunion.

Nothing had to be moved into the expansive study. The freed space holds
textual observations the expansive study already makes, so the themes still
fill physical pages 3 and 4:

- the Introit's *sustinentibus te*;
- the Collect's single petition, and the Mass's other petitions of the same
  kind;
- the Epistle's passives, "is given", "are made rich", "was confirmed";
- the two psalms as songs of the house;
- the Offertory's verbs, all of which have Moses as subject;
- the Secret's indicative and subjunctive;
- the Communion's two commands in order;
- the Postcommunion's thanks before its petition.

The concise scope note no longer names the sacramentary, chant and lectionary
witnesses. It points to the expansive study. The Wilson, Hesbert and Morin
entries leave its References. The homily carried none of this history.
Concise pp. 3–4 were inspected: page 3 is full and page 4 is filled to within
a few lines of its foot, as before. By the homily rule, the themes went from
1,580 words to 1,621.

**The index at Matthew 9.** The second pass wrote that the commentary index had
no Chrysologus row at Mt 9. That was wrong when written. The index's Matthew 9
row names his *Sermones* (commit `3cc830e86`), and `commentary-work-index
discover --passage "Mt 9:1" --max-results 0` reports his held fragment, Sermo 50,
at Mt 9:1–7. The observation line above is corrected. `research/scope.md` § 3.5
now notes that the re-run returns twenty-four rows with Chrysologus among them.

**The shared dossier measurements.** This leaf changes neither file; the
detail is reported to the coordinator. The 1962 profile,
`guidance/liturgy/roman-1962-propers.md` line 301, gives these values. The
shared format, `src/common/propers-format.tex` lines 103–124, sets these:

| Setting | Profile | `dossiertable` | `concisedossiertable` |
| --- | --- | --- | --- |
| Type size | `\footnotesize` | `\footnotesize` | 8.2 on 9.15 pt |
| Columns | 0.14, 0.18, 0.35 and 0.16 `\linewidth` | .12, .15, .29, and .44 `\linewidth` less 6 `\tabcolsep` | the same as `dossiertable` |
| `\arraystretch` | 1.02 | 1.02 | .96 |
| `\LTpre` | 0.15em | .15em | .1em |
| `\LTpost` | 0 | 0 | 0 |
| Explanatory row | 0.92 `\linewidth` | `\linewidth` | `\linewidth` |
| Space after the row | 0.1em | .1em | .1em |

The row widths come from `\dossierprose` and `\dossierevent`, lines 123–124.
The type size, stretch and `\LTpre` of the concise table are set at lines
114–116.

**Receipts.** `research/artifacts.json` was re-recorded in receipt schema 2
(`b41ad8202`), which no longer digests the `.log` files. `research/web-artifact.json`
was re-recorded for the regenerated web edition. The research edition's build
now runs the settled-aux page check (`f23cd5fbc`), and all three editions pass it.

**Checks after the third pass.** All three outputs were built and installed
with `make doc` and `make install-doc`. Each build ran the settled-aux page
check and exits 0. The installed bytes equal the build.

| Output | Pages | Bytes | SHA-256 (build and installed) |
| --- | ---: | ---: | --- |
| `58-eighteenth-after-pentecost.pdf` | 34 | 569,016 | `5fa472e4359a8bc3c8a8923284b182920cf58ef2a1e7dd9e869c42e14d72658c` |
| `58-eighteenth-after-pentecost-synthesis.pdf` | 12 | 459,514 | `b45ea4908cdf3e5e906470ab8bdb92a37f766da31f9b4a3cc1105cd0a7d719b7` |
| `58-eighteenth-after-pentecost-homily.pdf` | 3 | 275,105 | `482c117d47e1a69be0086cf664a85d9d470c5f7d8a4cbc06d08e84042e43165b` |

The web edition is 133,361 bytes, SHA-256
`34b1dc60438a875e366028550c247d1bd079efad9c0a6b2036630759c3c19fb1`. Only its
timestamp changed, because the concise study has no web edition. These exit 0:

- `_proper_study.py check` in phases `content`, `artifacts` and `publication`,
  each with `--require-presentation --require-format --require-authority`;
- the settled-aux page check for each of the three editions;
- `check-generation-metadata` on each PDF;
- `check-content-preflight` on all four editions; the concise study's
  References are now 23 entries, each used;
- both chronology currency checks;
- `make check-web-editions-current` and `check-web-edition`;
- `public-alpha check --provider claude --document <leaf>`;
- `source-library validate`, `make check-source-reader` and
  `make check-commentator-inventories`.

The 15 test modules run in the second pass now all pass: 610 tests, with
`test_house_voice` passing at this base. Stale, as at the base, for the
coordinator:

- the web edition's release binding, one of 12 stale bindings at base and
  after;
- this leaf's entry in `corpus.json`;
- the Claude publication inventory, where 15 of the 59 errors are this leaf's,
  against 14 of 58 at the base.

### Fourth pass: six findings of the independent review

An independent review of the whole revision returned six non-blocking items.
Each is fixed.

| Item | Where | Before → after |
| --- | --- | --- |
| 1 | `sections/homily/10-homily.tex` | "the Gospel that began with a man who contributed nothing" → "the Gospel that began with a man who was carried". The old wording stated Jerome's side as fact against the homily's own "we need not settle their argument", and denied the man any cooperation. The count is unchanged at 1,438 words, 11.1 to 12.0 minutes, so the note stands. |
| 2 | `sections/40-nothing-of-our-own.tex`; `sections/90-apparatus.tex` (References) | "as Maximus of Turin's Homilia CVIII" → "as St Maximus of Turin's Homilia CVIII"; "St Peter Chrysologus or Maximus of Turin" → "St Peter Chrysologus or St Maximus of Turin". Both now carry the honorific the Roman Martyrology gives him (25 June). |
| 3 | `research/interpretations.md` § 3.2; `research/scope.md` § 3.5 and § 4.2 | "A Father and Doctor, preaching this Gospel …" → "The sermon received as Chrysologus's, a Father and Doctor, preaches this Gospel … who wrote it is not decided here". The § 3.5 heading "Direct, a Father and Doctor, ascription disputed: Peter Chrysologus" → "Direct, ascription disputed: the sermon received as Peter Chrysologus's (a Father and Doctor)". In § 4.2, "takes that side in his own words" → "takes that side, its preacher preaching this Gospel". Pronouns that assumed his authorship now read "the preacher" or "the sermon", as Catena Rule 15 hangs the text without deciding who wrote it. |
| 4 | `research/source-bindings.toml`, the Ambrose *Exp. in Lc.* V.10–15 binding | The context's "nothing of contrition or satisfaction, which is Aquinas's tropology and not Ambrose's" is replaced by V.14 as scope § 3.5 gives it: the bed washed nightly with tears (Ps 6:7), *lectus doloris … cruciatu jacebat*, the bed of rest, the return to paradise, and the fence that *per contritionem … per satisfactionem …* is Aquinas's and no Father's. `source-library validate` and `bindings-valid` pass. The fingerprint does not cover the context. |
| 5 | `sections/concise/03-date-location.tex`, Introit row | "that article's dates for the book" → "that article's dates for the book's composition"; "the Psalter's boundary given with the Gradual" → "the Psalter's critical composition boundary, given with the Gradual". Page 2 still holds the whole dossier. |
| 6 | `sections/concise/90-apparatus.tex` | "the early sacramentaries, chant books and lectionaries" → "the early sacramentaries and lectionaries". D12 names only those lists, and the themes keep the Offertory's lost verses. |

**Checks after the fourth pass.** All three outputs were built and installed
through `make install-doc`. Each build ran the settled-aux page check, and the
installed bytes equal the build:

| Output | Pages | SHA-256 |
| --- | ---: | --- |
| study | 34 | `722ab1a620902cd68632e2d70e1ddfff9c72f79720280646d5631ea6f9b6cb06` |
| concise study | 12 | `6b1f018ff83828a0c2e60937696cc30a411212f3cec169702ecfd25e0599f096` |
| homily | 3 | `36d7e29ac4913a16b1428ba3a44b4875a2eb8afbbc064d413534956d2a324b5d` |

The web edition is `7fe2263e011351315a594f0532f3e1e276183966d618249e25b9acc4f180064e`.
These pass:

- `_proper_study.py check` in `content`, `artifacts` and `publication`, with
  all three `--require` flags, the receipts being re-snapshotted in schema 2;
- the settled-aux check for each edition;
- `check-generation-metadata`;
- `check-content-preflight` on four editions;
- both chronology currency checks;
- `make check-web-editions-current` and `check-web-edition`;
- `source-library validate`, `make check-source-reader` and
  `make check-commentator-inventories`;
- the 15 test modules, now 622 tests.

`public-alpha check --provider claude --document <leaf>` fails at this base
with or without these changes. The source edition
`…/the-liturgical-year/1900-english-volume-10.json`, which the authorization
names, no longer exists after `f82f5ecc6` re-dated that edition. That is
another lane's to repair. Stale for the coordinator, as before: this leaf's
web binding (1 of 16 stale), its `corpus.json` entry, and 15 of its files in
the Claude publication inventory.
