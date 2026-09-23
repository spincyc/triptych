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
