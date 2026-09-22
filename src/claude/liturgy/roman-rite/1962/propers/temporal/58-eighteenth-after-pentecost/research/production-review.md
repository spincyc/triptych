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
