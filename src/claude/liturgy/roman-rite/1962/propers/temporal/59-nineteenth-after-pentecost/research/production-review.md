# Production and review record

## Author-study

Authored 30 September 2026 in `proper-study` v7, run `a27462e34ec9c09a`,
seeded at commit `56d8c30f24bd0e42234c88c7d71c801981a9f2f9`, at iteration 0,
and revised at iteration 1 on the first study review's findings (below),
after the research review of the same run passed at its iteration 2 with two
standing advisories (RES-010, RES-011) and one observation. Every agent stage
of the run is a Claude Code harness subagent running as `claude-opus-5-5[1m]`;
the stage declares effort `high`, which the harness does not enforce (run
intervention 0000). The canonical study is *The Nineteenth Sunday after
Pentecost*, the Mass *Dominica decima nona post Pentecosten*, II classis, of
the 1962 *Missale Romanum*, pp. 411–412, nos. 1679–1688, in the universal
calendar, for the occurrence of 4 October 2026.

### What the study contains

- An opening on the Sunday's occurrence (the omission of St Francis, the
  single oration of each kind, green, Gloria, Credo and Trinity Preface, and
  the optional external solemnity of the Holy Rosary under RGMR 358 b and
  360), the formulary's movement and the three questions it raises, with a
  ten-row map of the appointed elements.
- The complete appointed Latin of all ten elements from the 1962 typical
  edition, with the Douay–Rheims (Challoner) at the canonical verses for the
  six scriptural elements and the 1861 Cummiskey English for the Introit
  antiphon and the three orations, and a note at every place where the
  Missal's form leaves the Douay or the 1861 English departs from the Latin.
  No English is composed for the Missal's divergent forms; the Offertory's
  future tenses are described, not rendered.
- An element-by-element section giving each text its literary context,
  textual facts, liturgical place and the reception of the liturgical
  commentators on the shared elements (Honorius and Sicard for the return
  from exile; Schuster and the continuation of *The Liturgical Year* on this
  formulary).
- Three readings of the whole formulary, each carrying all ten element keys
  and closing with its own four senses, recorded in the manifest as the lanes
  `wedding-garment`, `call-to-the-nations` and `feast-that-now-is`.
- A comparison of the three readings.
- A terminal Scriptural Date and Location appendix on the generated
  chronology projection, which is the reviewed home of the chronology the
  concise study's page 2 will print; the scope appendix; and References.

The three readings are those recorded in `research/interpretations.md`:

- `wedding-garment` — the garment the King looks for, the new man put on in
  charity. Carried by Gregory the Great (*Hom. in Ev.* 38, 9–14), Augustine
  (*Sermo* 90, 1–10; *Sermo* 95, 4–7; *En. in Ps.* 77, 2; 104, 1; 118, Aleph
  5; 137, 10) and Jerome (PL 26, cols. 160–161 on Mt 22:11–14; col. 508 on
  Eph 4:24; col. 512 on Eph 4:28), with Aquinas on Ephesians (lect. 7–9) and
  on Matthew (c. 22, summarised), Chrysostom (*Hom. in Eph.* 13–14; *Hom. in
  Mt.* 69; *Expos. in Ps.* 140, described), Hilary (*Tract. in Ps.* 140, 3–4;
  118, Aleph 12; *In Matth.* 22, 7), Irenaeus (IV.36.6), Bellarmine on
  Ps 140:2, Schuster, the PG 27 *Expositiones* on Ps 118:4–5 (described) and
  the continuation of *The Liturgical Year*.
- `call-to-the-nations` — the invitation refused and carried to the highways.
  Carried by Chrysostom (*Hom. in Mt.* 69), Irenaeus (IV.36.5–6) and Hilary
  (*In Matth.* 22, 3–7), with Jerome (PL 26, cols. 159–160), Augustine
  (*Quaest. ev.* I.31; *En. in Ps.* 77, 1–2; 104, 1, 34, 36; 137, 11; 140, 2),
  the PG 27 *Expositiones* on Pss 77:1 and 104:1 (described), Schuster and
  Bellarmine on Ps 104:1, and, as the principal alternative, Gregory
  (*Hom.* 38, 3–6) with Rabanus Maurus's catena setting the two answers side
  by side. Honorius is not cited in this reading (iteration 1).
- `feast-that-now-is` — the feast that now is, the Church at the Lord's Table
  and its evening sacrifice. Carried by Augustine (*Sermo* 90, 1, 4–5, 9;
  *Sermo* 95, 5–7; *En. in Ps.* 140, 2–3; 137, 10; 104, 1), Gregory (*Hom.* 38,
  1, 4, 7, 9, 11, 14), Chrysostom (*Hom. in Mt.* 69; *Expos. in Ps.* 137 and
  140, described), with Bl. Ildefonso Schuster on the Gradual, Secret and
  Postcommunion, Bellarmine on Pss 137:7 and 140:2, Hilary as the different
  answer on Ps 140:2, and Jerome and Aquinas on Eph 4:25–27. Schuster's own
  comment on the Gospel (p. 173) places its banquet in heaven; the reading
  records it beside its claim about the feast, and he is not among the
  lane's carrying authors (iteration 1).

The manifest declares `authority_contract = "authority-standing-v1"` and
names each lane's carrying authors as the author-standing registry names
them: Gregory the Great, Augustine and Jerome; John Chrysostom, Irenaeus of
Lyons and Hilary of Poitiers; Augustine, Gregory the Great and John
Chrysostom. The *Expositiones in Psalmos* printed under St
Athanasius's name have no standing row, carry no reading and are not listed
among any lane's authors. Honorius, Rupert, Sicard, Durandus and Berno are
cited only for the elements their Mass shares with this one, and their other
Gospel appears only in one clause of the scope appendix; after iteration 1,
the readings cite Honorius and Sicard nowhere, and the element-by-element
section cites them for the shared elements alone. Lucien Fromage (the
continuation) supports and carries nothing.

Material disagreements are carried where the research records them: the
garment as baptismal gift (Hilary, Irenaeus) against charity that the
baptized may lack (Gregory, Augustine), with Chrysostom holding both; the
burned city as Jerusalem (Chrysostom; Jerome, one of two) or the persecutors
in eternal fire (Gregory; Hilary); the highways as the nations (Irenaeus,
Hilary, Jerome, Chrysostom), the teachings of the Gentiles (Augustine,
*Quaest. ev.* I.31) or the failure of worldly undertakings (Gregory); the
evening sacrifice as the Passion (Augustine; Bellarmine as a possibility) or
the works of mercy of the last age (Hilary); and the servants as prophets then
apostles (Gregory; Chrysostom, with John and the Son between), prophets and
apostles sent by one God (Irenaeus), or apostles then apostolic men (Hilary).
No Father is credited with a reading of this Mass as a whole, and the
connections between elements are presented as the readings' argument and not
put in any witness's mouth.

### Extent

**Substantive word count at iteration 1: 16,331 words** (15,363 with the
content of the `\latin{}` spans removed; iteration 0 counted 16,528). The
count takes the six argumentative components — opening, element-by-element
section, the three readings and the comparison — removes comments, headings,
labels and the map and comparison tables, strips control words and braces,
and counts whitespace-separated tokens that carry a letter or digit. By
component: opening 1,063; element-by-element 3,206; `wedding-garment` 4,346;
`call-to-the-nations` 3,670; `feast-that-now-is` 3,407; comparison 639. The
count excludes the appointed-text component (2,061 by the same method), the
Scriptural Date and Location appendix (656), and the scope appendix with
References (1,782). The total stands above the profile's 6,000–10,000-word
planning range, which is a range and not a quota: three readings that each
carry all ten elements, report the principal witnesses' own reasoning at their
loci, carry the five disagreements above, and close with four senses account
for 11,423 words of it.

**Author proof at iteration 1: 33 physical pages**, inside the 20–50-page
requirement. `make doc DOC=liturgy/roman-rite/1962/propers/temporal/59-nineteenth-after-pentecost
PROVIDER=claude` built `build/claude/liturgy/roman-rite/1962/propers/temporal/59-nineteenth-after-pentecost.pdf`
in two passes with no undefined reference, overfull or underfull box, or
rerun warning in the settled log; SHA-256
`5896842328dc874d36881ac97ba41119efe2b3903dd6375a9792d0e3f5a85657`, with
generation timestamp `2026-09-30T19:28:15Z` (iteration 0's proof was 33 pages,
`b52d7820…fdc19720`). Every font is an embedded Latin Modern Type 1 subset.
All 33 pages were inspected on rendered rasters. The Scriptural Date and
Location appendix holds its seven dossiers on one page; an intermediate build
of the revised rows spilled the Epistle's explanatory row onto a second page,
and the rows were shortened until the whole sheet stood on one page again.
The scope appendix now runs a few lines onto the page on which References
begins, whose running head is therefore References; the revision timestamp
and rights colophon share the final page with the end of the References.
This is author verification only: the later shared-timestamp three-document
build and the independent visual review remain required, and the proof hash
will change when they rebuild.

### Checks run at this stage

On the final sources: `scripts/_proper_study.py check … --phase content
--edition research --require-presentation --require-format
--require-authority`; every `check-content-preflight` check of the
study-preflight gate (references-used, identifiers-resolve, bindings-valid,
restricted-not-reproduced, relation-coverage, unquoted-not-quoted,
structural-meta-labels, house-voice, chronology-record-current,
chronology-annotations-current, chronology-claims-supported, and
provenance-matches-run against this run's workflow, version, digest, run id
and seed commit); `tools/check-proper-components --provider claude --document
… --phase artifacts --edition research`; `tools/check-generation-metadata`;
and `tools/check-web-edition` for the new `web-edition.toml`. All pass. A
trial conversion by `tools/web-edition` succeeded in a scratch environment
holding the pinned `requirements-public-alpha.txt` (the host's installed
Python Markdown is 3.11 against the pinned 3.10.3, which the tool refuses);
its output is not installed and belongs to the later web stage. At
iteration 1 every one of these checks except the trial web conversion was run
again on the revised sources, and all pass; the web conversion was not
repeated.

### Iteration 1: repair of the study review

The study review of the same run (iteration 0) returned three blocking
findings against the study, and this stage repaired them as follows.

- STU-001. The second reading's paragraph that set Honorius's
  return-from-exile reading of the shared chants beside the Fathers as a
  third answer, and contrasted a homecoming with the mission carried by the
  Alleluia and the Gospel, is removed, and Honorius leaves the
  `call-to-the-nations` lane's `authors`. He is cited only in the
  element-by-element section, for what he says of the Introit, Collect,
  Epistle, Gradual, Offertory and Communion.
- STU-002. The Gospel's dossier now gives the writing's tradition as the
  Catholic Encyclopedia reports Eusebius (Matthew wrote in Hebrew when he left
  Palestine), in the Location cell and the explanatory row, and states that
  c. A.D. 50 is Durand's date for the lost Aramaic original, quoting his
  sentence on the unknown date of the Greek rendering. The Epistle's dossier
  places the writing in the captivity at Caesarea or Rome, quotes Ladeuze's
  "much mooted question", and says that Prat's table sets the letter in the
  Roman captivity. Both come from `composition.gospel-of-matthew` and
  `composition.epistle-to-the-ephesians` in
  `src/sources/chronology/composition.yaml`; no date absent from
  `research/chronology.toml` is printed (the captivities' own years are
  not), and `chronology-claims-supported` accepts the repeated c. A.D. 50
  (a probe with a changed year was refused and reverted). The scope
  appendix's Chronology paragraph says the same. The Date cells are
  unchanged.
- STU-003. The opening credits the present-Church feast to Augustine and
  Gregory, with Chrysostom's address to those who have partaken of the
  mysteries, and states Schuster's contribution as his reading of the
  Gradual, Secret and Postcommunion. The third reading records, beside its
  claim about the feast, Schuster's own comment on the Gospel (the
  predestination of souls to the heavenly banquet, p. 173). Schuster leaves
  the `feast-that-now-is` lane's `carrying_authors` and the comparison's
  Carried by cell; Augustine, Gregory and Chrysostom carry it.

Of the four standing advisories, this stage also cleared what lay in the
files it was repairing: the dossier rows restated with a source or a fact as
subject and the psalms' Location cells given a setting or the title's
attribution (STU-004); Schuster's sentences on the Introit, Collect,
Gradual, Secret and Postcommunion, Augustine's *Enarr.* 140, 2, the
incensation's Latin, and several shorter repeats (Augustine's *Sermo* 90, 5
and *Enarr.* 118, Aleph 5, Hilary's *nos, in quos consummatio*, Augustine's
*Evangelizate*, Schuster on the Alleluia) each printed in full once
(STU-005); the third reading's list of healing language removed (STU-006);
and the Collect said alone, the Offertory's memory of being heard moved to
Ps 137:1, "the Fathers … sharply different" replaced by Augustine and Hilary
named, Gregory's warning paraphrased without quotation marks, and the scope
appendix's clause on the medieval commentators' Mass made true of each
(STU-007). A citation error found on the way is corrected: Schuster's
Postcommunion sentence stands on p. 174 of the 1927 English, not p. 173.

### Verification performed at this stage

Quotations were checked against the tracked texts the research reached:

- Latin of the ten elements against `propers/verified.md`; the Douay–Rheims
  at every quoted verse against the Challoner edition's verse-text files
  (Pss 34:3; 77:1–8, 12–13, 49, 52–54, 67–72; 90:15; 104:1–11, 16–38, 42–45;
  118:1–8; 137:1–8; 138:16; 140:1–5; 1 Par 16:1–2, 7–9; Mt 13:35; 21:23, 43, 45;
  22:1–16; 25:34–35; Rom 13:14; Eph 1:1; 3:1; 4:1, 22–32; 6:20; 1 Tim 1:5; 2:8); the
  Clementine at Pss 77:1, 104:1, 118:1–2, 137:1, 140:1 and Eph 4:1, 22, 30;
  and the 1861 English against the tracked checked payload and the
  `temporal-orations-en` rows, which agree.
- The NPNF and ANF English at the quoted loci: Augustine, *Sermones* 90 and 95
  (NPNF1-6 text), *En. in Ps.* 77, 104, 118, 137 and 140 (NPNF1-8 text);
  Chrysostom, *Hom. in Mt.* 69 (NPNF1-10) and *Hom. in Eph.* 13–14 (NPNF1-13);
  Irenaeus IV.36.5–6 (ANF 1 OCR layer).
- Latin: Gregory, *Hom.* 38 (tracked Wikisource text, CC BY-SA 3.0);
  Augustine, *En. in Ps.* 104, 1, 34–36 (tracked Wikisource text) and
  *Quaest. ev.* I.31 (tracked transcription, which the research collated on the
  PL 35 page image). Hilary on Ps 140 and on Matthew, and Aquinas on Ephesians, were read in the
  tracked PL 9 and 1857 OCR layers, which corroborate the research's page-image
  transcriptions; the study quotes those transcriptions. Hilary on Ps 118 was
  not re-read and is quoted from the research's page-image transcription.
- English: Bellarmine (O'Sullivan text), Schuster (1927 OCR, pp. 171–174) and
  the continuation of *The Liturgical Year* (1883 layer, pp. 425–433).

Not re-read at this stage: the PL 26 page images for Jerome (a remote scan;
the study reproduces the research's page-image transcriptions of cols.
159–161 and 507–512); the PG 27 and PG 55 Greek, which the study describes
from the research's reading and does not quote; Honorius and Sicard, whom the
study paraphrases from the research's reading and does not quote; and Aquinas
on Matthew, summarised from the research's reading of the Venice layer.

Loci used beyond the sentences `research/interpretations.md` quotes, all
within passages `research/scope.md` records as read and all read here in the
tracked texts: Augustine, *Sermo* 95, 5–7 (the invitation by his ministry;
the Bridegroom who quickens whom he calls; "Clothe others, and ye are clothed
yourselves … Christ is naked; and He will give you that wedding garment");
*Sermo* 90, 1 (bearing with the evil within); *En. in Ps.* 140, 3 ("Still we too are figured there … our old
man is crucified with Him"); *En. in Ps.* 104, 1 (the first psalm headed
Alleluia; praise before invocation, in the NPNF English); Gregory, *Hom.* 38,
7, 9 and 11 (tolerating the bad; the warning to those already inside; hatred
and envy weighed); Chrysostom, *Hom. in Mt.* 69 (the apostles first to the
Jews; Acts 13:46; "Hear whence ye were called"); Irenaeus IV.36.6 (the God
who calls the unworthy examines the called); and the continuation, p. 433
(the garments of grace placed at the guests' disposal). The Eph 4:1 opening of
the Epistle's chapter is a textual observation read here in the Douay and
Clementine.

At iteration 1, read again or newly: Schuster's pages 171–174 in the tracked
1927 OCR layer, including the Gospel paragraph on p. 173 (the heavenly
banquet; God calls our souls, but they must be in accord with their calling)
and the Postcommunion on p. 174; the Challoner Douay at Ps 77:68–70,
118:19, 23, 54, 137:1–4 and 140:1–2, 1 Par 15:1–3 and 16:1–2, 7–8, and
Mt 21:17–18, 23 and 26:1–2 in the edition's verse-text files; and the
`composition.gospel-of-matthew`, `composition.epistle-to-the-ephesians` and
Psalter-boundary entries of `src/sources/chronology/composition.yaml`, whose
quoted sentences (Eusebius as reported by the Catholic Encyclopedia; Durand
on the Aramaic original and its Greek rendering; Ladeuze on Caesarea or Rome;
Prat's table; the NABRE introduction on the Maccabean period) are the only
source of the revised dossier rows. The Catholic Encyclopedia articles
themselves were not re-read at this stage.

### Standing research advisories and observation

The two advisories are addressed to `research/interpretations.md` and
`research/scope.md`, which this stage does not edit. The study follows what
each asks without carrying the defect:

- RES-010: the servants are cited clause by clause — prophets then apostles
  for Gregory, with John and the Son between them for Chrysostom, the one God
  who called by the prophets and calls by the apostles for Irenaeus, and the
  apostles then apostolic men for Hilary — in the second reading's text and
  its allegorical sense.
- RES-011: nothing in the study rests on the sentence about the search of
  Sermones 90 and 95; the study quotes the sermons at their loci and says only
  what they say.

The observation on the `commentary-work-index` example transcript concerns a
tool outside this leaf and is not the study's.

### Upstream items reported for the reviewer, not repaired

- `research/source-bindings.toml` binds the Challoner Douay only through its
  psalm-numbering artifact. The study prints the Douay at the canonical verses
  of all six scriptural elements (from the verse-text artifacts of Psalms,
  Matthew and Ephesians) as its scriptural English; those verse-text artifacts
  are not bound in any role, although `research/review-dependencies.toml`
  declares the whole Challoner edition directory. A research-owned binding
  gap.
- The NPNF1-8 artifact is bound at `77.1-2`, `118.4-5`, `137.10-11` and
  `140.2-4`; the study also quotes its English of Augustine on Ps 104, 1 (the
  research quoted that exposition only in Latin, bound through the Wikisource
  part-11 artifact at `104.1-4`). A research-owned locus omission.
- The research's open items remain as it records them (§ 10 of
  `research/scope.md`): the six scriptural elements' Latin provenance rows,
  the stale translation-overlay rows, the duplicated FSSP France work, and the
  chronology corpus's missing traditional attributions for the five psalms and
  narrated-event date for the Gospel.
- After the iteration-1 repairs, `research/interpretations.md` still names
  Bl. Ildefonso Schuster among the carrying authors of `feast-that-now-is`
  (the reading table, § 3.2, § 4.2 and § 5), and § 2.3 and § 2.5 still set
  Honorius in the `call-to-the-nations` reading, § 2.5 as an alternative that
  "would make the formulary a homecoming rather than a mission". The study
  and its manifest now differ from that record on both points, as STU-001
  and STU-003 required; the record itself is research-owned and is not
  edited here. The Schuster Gospel sentence that the study now quotes is
  recorded in `research/scope.md` § 3.6.

### Source limits carried into the study

The Introit antiphon's source, and the source of the Gradual's and
Offertory's *Domine* and of the Offertory's futures, are unidentified; no
Roman or Old Latin psalter or chant manuscript was consulted. Gregory's Latin
is a licensed transcription not collated with PL 76. The Greek psalm
expositions are OCR layers and are described, not quoted. The witnesses not
reached are those the scope appendix names. The formulary's early lectionary
and station history, which Schuster reports, is not used: no claim about the
age of the pairing of these chants with this Gospel is made in either
direction.

## Derive-synthesis

Authored 30 September 2026 in `proper-study` v7, run `a27462e34ec9c09a`,
seeded at commit `56d8c30f24bd0e42234c88c7d71c801981a9f2f9`, at
derive-synthesis iteration 0, after the study review passed at its
iteration 1. The stage declares effort `high`, which the harness does not
enforce (run intervention 0000); the worker is a Claude Code harness subagent
running as `claude-opus-5-5[1m]`. The concise companion is *The Nineteenth
Sunday after Pentecost: A Concise Study of the Proper in the 1962 Roman
Missal*, built from `synthesis.tex` and derived from the accepted expansive
study of this same leaf, for the occurrence of 4 October 2026. No research
record and no study component was edited for it. In the manifest only the
synthesis-only `concise-apparatus` entry changed: its references now name
`propers/verified.md` and `research/interpretations.md` beside
`research/scope.md`, which its scope note cites.

The six synthesis components were written at this stage:

- `concise-inventory` (`sections/concise/01-inventory.tex`): the map of the ten
  appointed elements in the order of the Mass, quoting the 1861 English for the
  three orations as the study's map does, with a rubrical note: second class,
  green, Gloria, Credo and the Trinity Preface; St Francis (third class) gives
  way and the Mass has one oration of each kind; and, as an option, the
  external solemnity of the Holy Rosary under RGMR 358 b and 360, whose votive
  Masses commemorate this Sunday's orations.
- `concise-overview` (`sections/concise/02-overview.tex`): exactly four
  overview rows, drawn from the three readings' own senses and from
  `research/interpretations.md` § 4.4, with each witness named beside the
  clause he states (see STU-008 below).
- `concise-date-location` (`sections/concise/03-date-location.tex`): the
  Scriptural Date and Location sheet. It imports the generated chronology
  annotations once and carries one `\chronodate` cell for each of the seven
  appointed Scriptures, in the study's canonical order. The dates, relation
  labels, disputed alternatives and the Gospel's unresolved narrated-event
  state are the study's, unchanged; the explanatory rows are the study's
  appendix rows, with the antiphon's sentence shortened.
- `concise-themes` (`sections/concise/04-themes.tex`): *The Propers: Themes and
  Movement*, two pages. It opens with a direct thesis (a call, and what those
  who answer it bring), follows the formulary from *Salus populi* to
  *inhaerere mandatis* with the verbal returns the study records
  (*tribulatio*; *expediti*/*expediat*; *quae tua sunt*/*tuis mandatis*;
  *dirigatur*/*dirigantur*; Ps 104:45's justifications and the Communion's;
  *in perpetuum*/*semper*; *oculis tuae maiestatis* and the *Placeat*), the
  Gospel's setting in Mt 21–22, and the Epistle's chapter context. It then
  names calling, hearing and keeping as the formulary's threads and states the
  three readings, their questions and how they relate.
- `concise-commentary` (`sections/concise/10-commentary.tex`): *The Propers:
  Detailed Commentary*, six cross-proper questions, each drawing on several
  elements and setting the readings' answers beside one another. Who was
  invited, and where the call went (Gospel vv. 1–10, Introit psalm, Alleluia,
  Collect). The feast that now is, and the feast to come (Gospel vv. 10–11,
  Secret). What the king looks for (Gospel vv. 11–13, Epistle). Gift or work,
  and the Communion's answer (Gospel, Communion, Postcommunion, Alleluia's
  psalm). The evening sacrifice (Gradual, Offertory, Introit). Many called, few
  chosen (Gospel v. 14, Postcommunion, and each reading's anagogical end).
- `concise-apparatus` (`sections/concise/90-apparatus.tex`): the scope note and
  the References for the sources this companion uses.

Every reading's controlling claim is preserved, and so are the shared ground
and the relation the study's comparison states (the second supplies the
history in which the other two take place). The disagreements are kept where
the study carries them:

- the garment as the Spirit's baptismal gift (Hilary; Irenaeus's works of
  righteousness on which the Spirit rests) against charity that the baptized
  may lack (Gregory, Augustine), with Chrysostom holding both, and the
  Communion's verse as the study's answer (Augustine, Hilary, the PG 27
  *Expositiones*);
- the garment as charity (Gregory, Augustine) beside the garment of the new
  man made of the precepts kept, whose new man is Christ (Jerome; Aquinas in
  two commentaries), stated as compatible and not identical;
- the burned city as Jerusalem (Chrysostom; Jerome, one of two) or the
  persecutors in eternal fire (Gregory; Hilary);
- the highways as the nations (Irenaeus, Hilary, Jerome, Chrysostom), the
  teachings of the Gentiles (Augustine, *Quaest. ev.* I.31) or the failure of
  worldly undertakings (Gregory), with Rabanus Maurus heading Gregory's as the
  moral sense;
- the servants cited clause by clause (Gregory, Chrysostom, Irenaeus, Hilary,
  Jerome), as RES-010 asks;
- the feast named as the Lord's Table and the Scriptures (Augustine), the
  Word and Scripture with no altar named (Gregory), or the mysteries partaken
  (Chrysostom), with none calling the Gospel's feast the Eucharist; Hilary's
  wedding in the resurrection and Schuster's heavenly banquet set beside the
  present-Church reading, which is credited to Augustine and Gregory alone;
- the evening sacrifice as the Passion (Augustine; Bellarmine as a
  possibility) or the works of mercy of the last age (Hilary), with the first
  reading taking Hilary's and the third Augustine's;
- the Offertory's Vulgate past (Augustine; Chrysostom's Greek, which reports
  two versions with the future) against the Missal's future.

The compression set aside the element-by-element section's liturgical
commentators other than Schuster (Honorius and Sicard are not cited, and no
other Mass is mentioned), the continuation of *The Liturgical Year*, the
psalms' titles beyond the dossier, Augustine on Ps 104's order of praise and
invocation, his *Sermo* 95 invitation by his ministry and *Sermo* 90, 9 on the
enemy's death, Jerome's *homo* and *rex*, Jerome and Aquinas on the place
given to the devil, Chrysostom on Eph 4:23–24, Bellarmine on Pss 104:1 and
137:7, and Schuster on the Introit, Collect, Alleluia, Offertory and
Communion beyond the *utinam*. Nothing in the concise argument turns on them,
and the study carries each.

Every quotation printed is one the reviewed study prints. This was checked
mechanically: each quoted English span and each `\latin{}` span of the six
components (215 spans, split at ellipses) was searched in the study's
components, and all were found; two that the first pass did not find had been
recapitalised at the head of a sentence and were restored to the study's form.
No source was read afresh at this stage, and no claim, date or locus absent
from the study was added. The References list only works the concise body
cites; Hilary's tractate on Ps 137 is not cited (STU-010).

**Substantive word count: 6,668 words** (6,146 with the content of the
`\latin{}` spans removed). The count covers the two argumentative components:
the themes section, 1,679 (1,581), and the commentary, 4,989 (4,565). It
strips comments, headings, zref and running-head labels, control words and
braces, and counts whitespace-separated tokens that carry a letter or digit.
It excludes the map (347), the overview rows (307), the dossier sheet (607)
and the scope note with References (1,334), counted the same way.

### Standing findings the concise study meets

The study review left four advisories against the study and one against the
research record that bear on this companion; the stage edits neither owner,
and the concise study does not carry their defects:

- STU-008: the opening's colon construction is not reused. The themes state
  that Gregory and Augustine make the garment charity, that Jerome makes it the
  garment of the new man made of the precepts kept and names the new man
  Christ, and that the reading finds that garment in the Epistle's acts and the
  Communion's wish; the third reading's feast is credited to Augustine and
  Gregory, with Chrysostom's address named as his own. The overview rows name
  each witness beside his own clause.
- STU-009: the Postcommunion is said to name God's healing work, and the
  Eucharistic reading is Schuster's; the Introit's antiphon is said only to
  stand in no verse of the Vulgate; no psalm outside the formulary is cited,
  and the scope note states the numbering convention as the text follows it.
- STU-010: Hilary is not cited for the Offertory's tense.
- STU-011: `research/interpretations.md` still names Schuster a carrying
  author of `feast-that-now-is` and keeps Honorius in `call-to-the-nations`
  (§ 2.3, § 2.5, § 4.2). The concise study follows the reviewed study and
  manifest: Schuster is cited for the Gradual, Secret and Postcommunion with
  his heavenly banquet beside the present-Church claim, and Honorius is not
  cited.

### Upstream observations reported for the cold reviewer

- STU-012 applies to this companion too: it prints the Challoner Douay at
  verses whose verse-text artifacts are bound in no role, and it quotes the
  NPNF1-8 English of *Enarr. in Ps.* 104, 1, whose binding omits that locus.
  Both are research-owned.
- The study review's observation stands for page 2 as for the study's
  appendix: the chronology corpus holds no modern critical claim for Matthew or
  Ephesians, so neither explanatory row carries one.
- No missing argument or source was found. The study, its dossier appendix and
  the research records answered every point the concise prose needed.

### Author proof and checks

`make doc DOC=liturgy/roman-rite/1962/propers/temporal/59-nineteenth-after-pentecost-synthesis PROVIDER=claude`
settles with no overfull or underfull box, no undefined reference, no LaTeX
warning and no rerun request. The PDF has 12 physical pages, letter size,
Latin Modern Roman and Mono only, all embedded Type 1 subsets. The document
info carries the entrypoint's title and subject.

The settled auxiliary file records the physical pages the presentation
contract fixes: the inventory and overview markers and all four sense markers
on page 1; chronology start and end on page 2; themes start on page 3 and end
on page 4; commentary start on page 5.

These all pass on the final sources: `scripts/_proper_study.py check … --phase
content --edition synthesis --require-presentation --require-format
--require-authority` with `--date 2026-10-04`; every `check-content-preflight`
check the synthesis gate names (references-used, identifiers-resolve,
bindings-valid, restricted-not-reproduced, relation-coverage,
unquoted-not-quoted, structural-meta-labels, house-voice, the three chronology
checks, and provenance-matches-run against this run's workflow, version,
digest, run id and seed commit); `tools/check-proper-components --phase
artifacts` for both the synthesis and the research editions; and
`tools/check-generation-metadata`.

The shared generation record carries a contribution for this stage and the
revision timestamp `2026-09-30T20:13:53Z`. The settled concise proof is
`build/claude/liturgy/roman-rite/1962/propers/temporal/59-nineteenth-after-pentecost-synthesis.pdf`,
SHA-256 `62ae7851118ad854bb75dcd29739ec28e5c8e0defb1024c42fcc2072bb6a3ea7`;
its auxiliary file is SHA-256
`e362708b1767b56d21fb519df51a33f58447aa0adbb67bfea2ef2b944d505678` and its
log SHA-256 `a10acc019e3ae9329ae8588b60f89ef0b70b526eba0c0fb3f7504b7273e5a346`.
The expansive study was rebuilt at the same timestamp and is unchanged at 33
pages with a clean log, SHA-256
`b8918eba6b4fab193a426c01402285249f9e34638f3183d56fa7deed46e57b1b`. Copies of
both PDFs, the synthesis auxiliary file, logs, extracted text, font list,
physical-page list, checks and their digests are kept beneath this stage's
artifact directory in the run; the page rasters and contact sheet are in a
child directory of their own.

The author read the contact sheet of all twelve pages and the full rasters of
pages 1, 2 and 12. Layout revision removed a spill of the Moral and Anagogical
rows onto page 2, which had pushed the whole document to 13 pages, by
shortening the map and overview rows; it then filled the second thematic page,
about a third empty, from the study's own setting of the Gospel (Mt 21:23,
43, 45; 22:15), the verses after the Epistle (Eph 4:29–32) and the offering of
the chalice (*Ordo Missae* no. 1032), and trimmed until the section ended on
page 4. The map and the four overview rows rule to the same measure on page 1;
the dossier stands whole on page 2 with room below it; the themes fill pages 3
and 4; the revision timestamp and the rights colophon share the last page with
the References. This is an author proof inspection, not the independent visual
evaluation, which follows the shared-timestamp three-document build.

## Derive-homily

Authored 30 September 2026 in `proper-study` v7, run `a27462e34ec9c09a`,
seeded at commit `56d8c30f24bd0e42234c88c7d71c801981a9f2f9`, at derive-homily
iteration 0, after the synthesis review passed at its iteration 0. The stage
declares effort `high`, which the harness does not enforce (run intervention
0000); the worker is a Claude Code harness subagent running as
`claude-opus-5-5[1m]`. The homily is *The Nineteenth Sunday after Pentecost:
Clothed for the Wedding*, built from `homily.tex`, addressed to an adult parish
assembly for the occurrence of 4 October 2026, and derived from the two
accepted studies of this same leaf. No research record and no component of
either study was edited for it. The neighbouring Claude leaf
`58-eighteenth-after-pentecost` was consulted only for the shape of its homily
files, its word-count rule and the defects its homily reviews recorded; no
claim, locus or quotation was taken from it. The other provider's leaf for this
identity was not opened.

The entrypoint imports `common/preamble`, `common/propers-format` and
`common/propers-homily` in that order, then the leaf's `format.tex`, and uses
the shared full-width `\propertitle`. The `properhomily` environment encloses
only the literal import of the spoken component; the terminal note follows the
environment's closing page break and sets its own running heads with
`\runninghead`. No font, geometry, title or column setting is overridden
locally. In the manifest the two homily components were already declared;
their `references` now also name `propers/verified.md`, which holds the Missal
loci and the route of the 1861 English that the speech and the note use. No
other manifest entry changed.

The two homily components:

- `homily-body` (`sections/homily/10-homily.tex`): the spoken text, continuous
  preaching with no heading, no direction to a preacher and no citation inside
  the speech, in eight movements. It opens on the king's question to the guest
  who says nothing, the one in the parable most like an assembly already
  inside. It tells the call briefly (Mt 22:3, 5, 10), with Chrysostom on the
  excuses that seem reasonable and his "From the highway", and sets the
  Collect's freedom "both in soul and body" beside the excuses. It says what the
  garment is not and what it is: Gregory's "not baptism or faith", Augustine's
  "not the altar" and "in the heart", their shared answer, charity, and
  Gregory's reason, that our Maker had it when he came to the wedding, with his
  friend by faith and no friend by deeds. It hears the Epistle's "Put on the
  new man" with Jerome's garment of the new man and his new man who is Christ,
  the four acts of Eph 4:25–28, Gregory's hands already bound, and the
  Gradual's lifted hands as Hilary reads them (Mt 25:35). It gives Augustine's
  other answer to the same verse, the evening sacrifice of the Passion and its
  morning offering in the Resurrection, and the Bridegroom praying on the Cross
  for his enemies; then, in the preacher's own voice, the altar where the
  sacrifice of the Cross is made present and Christ gives his Body and Blood.
  It asks how guests from the highways could have a garment, and answers from
  the Communion's command and wish with Augustine on *O that* and "God must be
  prayed to grant Himself what He enjoineth", with Hilary's baptismal gift of
  the Spirit beside Gregory's charity, Augustine's "Clothe others" and "Run to
  Him", the Introit's promise to hear, and the Postcommunion. It sets
  Augustine's two feasts, his present feast received worthily, and the wish he
  forbids at the Lord's Table ("O that mine enemy might die!") against the
  Communion's wish; gives Gregory's two questions of hatred and envy and three
  acts for the week (anger settled before sunset, hands that give, the
  Communion's verse prayed each morning); and ends on Gregory's called and
  chosen, his psalm of hope for the imperfect (Ps 138:16), the king's
  "Friend", and Augustine's "He knoweth how to clothe His naked ones".
- `homily-note` (`sections/homily/90-note.tex`): the terminal note and the
  References, read aloud by nobody: audience and occasion, spoken word count
  and pace, relation to the three reviewed readings, the route by which each
  quoted text reaches the page, and the exact loci.

The argument joins the first and third readings, `wedding-garment` and
`feast-that-now-is`, as `research/interpretations.md` § 4.5 recommends, and
takes from `call-to-the-nations` only the story of the call. It keeps § 4.5's
bounds:

- no Father is said to call the wedding feast the Eucharist. Augustine is
  quoted in his own words for the present feast (the Lord's Table, the Feast of
  the Holy Scriptures) and for his denial that the garment is the altar
  (*Sermo* 90, 5); the sentences on the altar are the Church's faith in the
  preacher's voice and are credited to no one;
- the highways are not identified with the nations, and the first invited are
  not named;
- no other Mass, liturgical commentator or compilation fact is mentioned, and
  nothing is said about why these texts stand together;
- the Postcommunion is quoted in the 1861 English without its "these thy
  mysteries" (STU-009), and Schuster's Eucharistic reading of it is not used.

Two disagreements the study keeps are spoken: Augustine against Hilary on the
Gradual's evening sacrifice (the Passion, or the works of mercy), and Hilary's
baptismal gift of the Spirit beside Gregory's and Augustine's charity, with the
point both sides grant. Jerome's join of the new man to the garment is his own
(*In Matth.* III, col. 160). The other joins are the homily's and are credited
to no Father: the Collect beside the excuses; the charity the Bridegroom wore on
the Cross, drawn from Gregory's reason and Augustine's Passion; the Communion's
wish against the wish Augustine forbids; and the Introit's promise beside the
asking. The Gospel, the Epistle, the Gradual, the Collect, the Introit, the
Communion and the Postcommunion carry the argument; the Alleluia, the Offertory
and the Secret are left to the studies. The manifest's complete element keys on
both homily components are the component checker's coverage declaration and
are unchanged.

No English of a liturgical text was composed. The Introit antiphon, the Collect
and the Postcommunion are quoted from the 1861 Cummiskey English in the tracked
checked payload `…pentecost-19-checked-english` (SHA-256 `e13f1baa…`
recomputed). Scripture is the Douay–Rheims at the canonical verses, each quoted
verse matched in the tracked Challoner verse tables (Psalms `578f023d…`,
Matthew `dd0ba183…`, Ephesians `10c79be0…`, digests recomputed). The one text
the speech commends for private prayer is Ps 118:5 in the exact Douay wording,
and the speech ends as preaching, with no recited prayer. Gregory, Jerome and
Hilary are reported in English paraphrase of their Latin; no gloss of theirs is
printed as a translation, and the Gregory transcription's Latin is not quoted.
No anecdote, personal experience, clerical identity, miraculous story or
attributed quotation was manufactured.

### Verification performed at this stage

Every attributed sentence was read again at its locus in the tracked source,
not taken from the studies:

- Augustine, *Sermo* 90 §§ 1, 4, 5 and 9 and *Sermo* 95 § 7, in the tracked
  CCEL text of NPNF1 6 (SHA-256 `ce371798…` recomputed), physical lines
  37787–38198 and 39370–39410;
- Augustine, *Enarr. in Ps.* 118, Aleph 5 (lines 56788–56795) and 140, 3
  (lines 65246–65262), in the tracked CCEL text of NPNF1 8 (`d6841950…`);
- Chrysostom, *Hom. in Mt.* 69, in the tracked CCEL text of NPNF1 10
  (`adb8f1c9…`), lines 39009–39011 (the excuses) and 39176–39180 ("Hear whence
  ye were called. From the highway.");
- Gregory, *Hom. in Ev.* 38 §§ 9–14, in the tracked Wikisource transcription
  (`dc25dd69…`), lines 538–546;
- Jerome, on Mt 22:11–12 and on Eph 4:24: the registered whole-volume PL 26
  scan was fetched again from its source URL, and its 63,426,233 bytes matched
  SHA-256 `0d889bd6…`; col. 160 D was read on a 300-dpi crop of PDF p. 87,
  col. 161 A on PDF p. 88, and col. 508 C on PDF p. 261 at 150 dpi;
- Hilary, *Tract. in Ps.* 140 §§ 3–4 (lines 65848–65921) and *In Matth.* 22, 7
  (lines 82612–82640), in the tracked PL 9 optical text (`db389fea…`); the
  page images were not re-read at this stage.

All 38 quoted spans of the speech were then compared mechanically with those
tracked texts and verse tables, and every one was found. The only differences
are the nested quotation marks, the capital that begins a quotation where the
Douay's "And" (Eph 4:24) or "Wherefore," (Eph 4:25) is left out, and the
Communion's quotation, which joins two verse rows (Ps 118:4–5).

**Spoken word count: 1,453 words.** The count is taken over
`sections/homily/10-homily.tex` alone. Comments are removed, `\latin{}`
contents kept and every other macro dropped, and the remainder is counted as
whitespace-separated words carrying a letter, the rule the Eighteenth Sunday's
homily recorded. The same count taken from the extracted text of the built
PDF's first two pages, without the title block and running heads, is also
1,453. At an unhurried 120 to 130 words a minute that is 11.2 to 12.1 minutes,
within the profile's approximately 10–12; at 110 it would be 13.2. The figure
is arithmetic on the word count and not a timed delivery: nobody has spoken
these words and no rehearsal was audible. The prose was read through in full,
silently, for sense, sentence length (mean 14 words, median 12, longest 32)
and ease of speech. That reading split the longest sentences; recast a
sentence that could be heard as Hilary answering the question of the guests
swept in from the highways, which he answers otherwise; set doing and asking
both under the gift of the garment rather than assigning putting on to our
doing alone; and gave the king's servants back to the sentence that sends them
into the highways.

### Upstream observations reported for the homily's cold reviewer

- STU-012 applies to the homily too: it prints the Challoner Douay at verses
  whose verse-text artifacts are bound in no role. Research-owned.
- STU-009's point is observed and not carried: the Latin Postcommunion names
  only *tua medicinalis operatio*, and the homily's "healing work" follows the
  Latin.
- No missing argument or source was found, and nothing upstream was edited.

### Author proof and checks

The shared generation record carries a contribution for this stage and the
revision timestamp `2026-09-30T20:57:05Z`. The expansive and concise studies
were rebuilt at that timestamp and are unchanged at 33 and 12 physical pages
with clean logs (SHA-256 `27c7d197…b213c` and `448b926a…c1754f`); the concise
study's settled auxiliary file is byte-identical to the one the synthesis stage
recorded (`e362708b1767b56d21fb519df51a33f58447aa0adbb67bfea2ef2b944d505678`),
so its presentation markers have not moved.

`make doc DOC=liturgy/roman-rite/1962/propers/temporal/59-nineteenth-after-pentecost-homily PROVIDER=claude`
settles in two passes with no overfull or underfull box, no undefined
reference, no LaTeX warning and no rerun request. The PDF has 3 physical
pages, letter size, Latin Modern Roman and Mono only, every font an embedded,
subsetted Type 1 with a Unicode map; the document info carries the
entrypoint's title and subject. Deleting the PDF, auxiliary file and log and
building again reproduced the same bytes, SHA-256
`e1dcfb384e9334670e5ea4d015390d7f4685b88b603a907d919312245c9e33c5`. The author
read all three pages on rendered rasters. A first proof ran to four pages, the
fourth holding only the last two References, the timestamp and the colophon;
the note was shortened until the note, the References, the timestamp and the
colophon share page 3. The speech fills page 1 and most of page 2 in two
columns, with the seven movement breaks visible. This is an author proof
inspection, not the independent visual evaluation, which follows the
shared-timestamp three-document build.

These all pass on the final sources:

- `python3 scripts/_proper_study.py check --phase content --edition homily
  --require-presentation --require-format --require-authority` with
  `--date 2026-10-04`;
- every `check-content-preflight` check the homily gate names: references-used
  (eight entries, every one used), identifiers-resolve, bindings-valid,
  restricted-not-reproduced, relation-coverage, unquoted-not-quoted,
  structural-meta-labels, house-voice, the three chronology checks, and
  provenance-matches-run against this run's workflow, version, digest, run id
  and seed commit;
- `tools/check-proper-components --phase artifacts` for the homily, synthesis
  and research editions;
- `tools/check-generation-metadata` for the record and for each of the three
  built PDFs.

## Build-artifacts

Iteration 0 of the build stage of `proper-study` v7, run `a27462e34ec9c09a`,
seeded at commit `56d8c30f24bd0e42234c88c7d71c801981a9f2f9`, after the homily
review passed at its iteration 0. The worker is a Claude Code harness subagent
running as `claude-opus-5-5[1m]`; the stage declares effort `high`, which the
harness does not enforce (run intervention 0000). No source file was edited at
this stage: the logs carry no layout warning and no layout repair was made, so
no content seal is affected, and the shared generation record keeps its
revision timestamp `2026-09-30T20:57:05Z`, which all three PDFs carry as their
modification date. The only files this stage writes in the leaf are
`research/artifacts.json`, written by the snapshot helper, and this entry.

### Builds

The author proofs, with their auxiliary files, logs, recorder files, contents
file and metadata stamps, were deleted, and each output was built fresh with
`make doc DOC=<id> PROVIDER=claude` for the bare document, `-synthesis` and
`-homily`. Each settled in two pdfTeX passes; the first pass's requests to
rerun for changed labels and table widths are answered by the second, whose log
carries none. Each build passed the component-manifest and generation-metadata
validation the Makefile runs. The fresh builds reproduced the derive-homily
stage's proofs byte for byte, and the three auxiliary files are identical to
theirs.

| Output | Physical pages | Bytes | PDF SHA-256 |
| --- | --- | --- | --- |
| `build/claude/liturgy/roman-rite/1962/propers/temporal/59-nineteenth-after-pentecost.pdf` | 33 | 525,153 | `27c7d1979e4dfe30e3525cda062b7d380ae762f957ff58b21e3c473c478b213c` |
| `build/claude/liturgy/roman-rite/1962/propers/temporal/59-nineteenth-after-pentecost-synthesis.pdf` | 12 | 462,746 | `448b926a2a1cee8e44f11b3a5518eaa89cc3a6056f158cb5f4ba7699b8c1754f` |
| `build/claude/liturgy/roman-rite/1962/propers/temporal/59-nineteenth-after-pentecost-homily.pdf` | 3 | 259,524 | `e1dcfb384e9334670e5ea4d015390d7f4685b88b603a907d919312245c9e33c5` |

The expansive study falls within 20–50 pages and the concise study within
10–12. The auxiliary files are SHA-256
`6bb79596ab47b316641188cb77aab4dd136ba593ca11d82d9cbc84e896d9fe9b` (study),
`e362708b1767b56d21fb519df51a33f58447aa0adbb67bfea2ef2b944d505678` (concise)
and `96da8bd61cc21463cd3eda0260cb058d26e765e456536a181a79f8efa1798486`
(homily); the settled logs are
`aa02cef8afdd3fadc61282c57f45788be5fcd20a3704676018e29a5abdb10bf2`,
`1f7c59bca6c7a51b4c0a57625c8628b52c28df324d1c9812c43f62f00cd1c3f5` and
`ad4d221a2bef4d0e3bbea21a3b17fcf008bb43bbcd9cfb8cbb68c93ae3480374`. The
concise auxiliary file and log stay beside the PDFs in `build/` for the gate.

### Log, font, structure and extraction checks

- **Logs.** None of the three settled logs has a TeX error, an undefined or
  multiply defined reference, an overfull or underfull box, a LaTeX or
  package warning, a missing character or font-shape substitution, or a rerun
  request. The only lines matching "warning" or "rerun" are the `infwarerr`
  and `rerunfilecheck` package banners; the lines matching "substituted" are
  `xcolor`'s colour-model information.
- **Fonts.** Every font is Latin Modern (Roman, Roman Caps in the study, and
  Mono), Type 1, embedded, subsetted and Unicode-mapped. Nothing was
  substituted.
- **Structure.** All three are unencrypted PDF 1.7 files from pdfTeX 1.40.29,
  letter size on every page, with no image. Their titles and subjects are the
  entrypoints', naming the Missal and the Sunday. They carry no creation date
  and no trailer ID. Poppler's `pdfinfo`, `pdffonts` and `pdftotext` read them
  with nothing on standard error, and the raster helper rendered every page. No
  stricter PDF validator (qpdf, pypdf or pikepdf) is installed, so none was
  run.
- **Size.** The homily is 84.5 KiB a page, above the 75 KiB review trigger.
  Measured by stream, 227,391 of its 259,524 bytes (87.6 %) are its nine
  embedded Latin Modern font subsets and 21,153 bytes are page content; there
  is no image. The figure is the fixed cost of the house fonts over three
  pages, and nothing was rewritten. The study (15.5 KiB a page) and the
  concise study (37.7 KiB a page) are below the trigger, and all three are
  below 1 MiB.
- **Extraction.** Text extracts from every page, with no `??` marker and no
  replacement character. The extracted word counts, apparatus, running heads
  and page numbers included, are 22,407 for the study, 9,685 for the concise
  study and 2,306 for the homily.
- **Concise opening.** The settled `zref` evidence places the inventory, the
  overview and the four sense rows (literal, allegorical, moral, anagogical)
  on physical page 1, the chronology on page 2, the themes from page 3 to page
  4, and the start of the commentary on page 5. The extracted text agrees: page
  1 carries the ten elements from Introit to Postcommunion and exactly the four
  sense rows; page 2 holds only "Scriptural Date and Location", with the seven
  passages in canonical order (Pss 77, 104, 118, 137, 140; Mt 22; Eph 4); pages
  3 and 4 carry "The Propers: Themes and Movement"; page 5 opens "The Propers:
  Detailed Commentary".
- **Gates run ahead.** `tools/check-proper-components --phase artifacts` for
  the research, synthesis and homily editions,
  `tools/check-generation-metadata` on each of the three PDFs, and, after the
  snapshot, `scripts/_proper_study.py check --phase artifacts
  --require-presentation --require-format --require-authority --date
  2026-10-04` all pass.

### Snapshot and rasters

`python3 scripts/_proper_study.py snapshot` wrote `research/artifacts.json`
(receipt schema 2) from the final builds. It records the three PDF hashes
above, 27 render inputs (the leaf's TeX sources, manifest and chronology
annotations, and `src/common/preamble.tex`, `propers-format.tex` and
`propers-homily.tex`) and, as pagination evidence, the study's and the concise
study's auxiliary files. Bounded rasters and contact sheets of all 48 pages came
from `tools/tpt pdf-review` and are in the run's
`artifacts/build-artifacts-0000/rasters` child. Copies of the three PDFs,
auxiliary, recorder, contents and log files, the extracted text, the font and
info listings and the check output are kept beside that child, outside it, with
their digests.

### Remaining limitations for the visual reviewer

The build worker looked at the contact sheets, the thumbnail of study page 3
and the full rasters of study pages 7 and 8 only to decide whether a layout
repair was needed. That is
not the visual review, and no page has been inspected for it. Nothing found
called for a repair; any repair would be a source edit that reopens reviewed
content. For the reviewer to judge:

- The shared format's right-hand running head takes the first section mark
  on the page. Where a section begins below the top of a page, the head names
  it over the end of the section before: study page 8 (the Appointed Texts'
  Postcommunion under "Each Element in Its Setting"), pages 18, 23 and 28 (each
  reading's four senses under the next reading's or the comparison's title),
  and page 32 (the end of the scope appendix under "References", which the
  author-study entry above records).
- Short pages at section ends: study page 1 (title and contents, the lower
  half empty), page 3 (the map ends about seven-eighths down, before the
  Appointed Texts begin a fresh page), page 7 (the Postcommunion block moves
  whole to page 8, leaving the foot of the page empty), and the final pages of
  the study (33) and the concise study (12), which carry the end of the
  References, the revision timestamp and the rights colophon.
- The homily's note, References, timestamp and colophon fill page 3; its
  speech occupies page 1 and page 2.

## Reviews and gates recorded by the engine

These are the engine's own recorded results for run `a27462e34ec9c09a`, as the
run holds them when installation begins. No acceptance is claimed beyond them;
the terminal publication gates have not yet run. Each result's SHA-256 is the
hash the engine recorded for that result.

| Stage, iteration | Result | Findings and observations | Result SHA-256 |
| --- | --- | --- | --- |
| research-review 0 | CHANGES_REQUIRED | blocking RES-001 to RES-004; advisory RES-005 to RES-007 | `530d7337173681acd7644b04e2fa36bf048100325a54d93cc722787f6f87fa70` |
| research-review 1 | CHANGES_REQUIRED | blocking RES-008; advisory RES-009 | `505e484be54eee4ac62c06a362bce638022fbb4d2b86c5f0b2545e6399b3583b` |
| research-review 2 | PASS | advisory RES-010, RES-011; one observation | `0b8a2cf6599ffb90bc64d1af705d9d5c9b3564d4a9d7a88e10383cd962df716d` |
| study-review 0 | CHANGES_REQUIRED | blocking STU-001 to STU-003; advisory STU-004 to STU-007; one observation | `d43b5540f56d3ddb51006bb017ea75d809dbbfef5035bc89dcf073c764754bfa` |
| study-review 1 | PASS | advisory STU-008 to STU-012; two observations | `86c641bb440a946faf545b9f4c2020ef811ee1c3df16148c1e2b1dcf7887878d` |
| synthesis-review 0 | PASS | advisory SYN-001 to SYN-003; one observation | `6f3d6358ef9ab958e3ad5199357a485fb43dd9a8d2b7c26d73cb8950af47e173` |
| homily-review 0 | PASS | advisory HOM-001 to HOM-003; one observation | `73a466212a349c6eea41fbb5026234eeeab8bf6397d09d3da46e2be1d4854efe` |
| artifact-gates 0 | PASS | none | `97af5c9c6c70bfc4459030f6b4c4d3ef1c5d44f458a9759ff4ab5fcbb5607d3c` |
| visual-review 0 | PASS | advisory VIS-001, VIS-002; one observation | `2a50ceafe601b1213ec339cfcf345c57c625761ab5621a3b82994994adf85ab5` |
| generate-web 0 | PASS | worker stage | `4d9b2bc045672aca9203a8f2c380bf7c2589684c0a14232fa9e290b612f34f16` |
| web-review 0 | PASS | none | `861205d0d0dce2b343e527634737e3dd768338c47daef0acc01b72b5813032c7` |

The four stages after the artifact build, in brief:

- **Artifact gates, iteration 0.** `_proper_study.py check --phase artifacts
  --require-presentation --require-format --require-authority --date
  2026-10-04` exited 0 against the snapshot in `research/artifacts.json`.
- **Visual review, iteration 0.** Every page of the three sealed PDFs was
  inspected: 33 pages of the study, 12 of the concise study and 3 of the
  homily. VIS-001 is the homily's page turn between "St" and "Hilary" at the
  foot of page 1, with none of the spoken body's "St" honorifics tied; VIS-002
  is the two studies setting their References subdivisions at different
  heading levels. The observation records that the homily's 84.5 KiB a page is
  the fixed cost of its embedded font subsets.
- **Generate-web, iteration 0.** The canonical study alone was converted, under
  the pinned Markdown 3.10.3 in a scratch environment because the host carries
  3.11. `research/web-artifact.json` records the conversion at SHA-256
  `a8b494c540f2cf7e4a8a63f2a0c27db0e64bf6b34b4890dc13f1bfd58430ee2d`.
- **Web review, iteration 0.** No finding and no observation. The reviewer
  reproduced the conversion byte for byte and compared it word by word with
  the reviewed 33-page PDF.

## Install-publication, iteration 0 — 30 September 2026

The worker is a Claude Code harness subagent running as `claude-opus-5-5[1m]`;
the packet declares effort `high`, which the harness does not enforce (run
intervention 0000). No reviewed source, generation timestamp or receipt was
changed at this stage.

### Installed PDFs

The snapshot was confirmed current before anything was installed.
`_proper_study.py check --phase artifacts --require-presentation
--require-format --require-authority --date 2026-10-04` exited 0, and all 32
hashes in `research/artifacts.json` (three PDFs, 27 render inputs and two
pagination `.aux` files) matched the files on disk. A dry run of each install
target showed metadata checks and a copy, with no typesetting. The three PDFs
were then installed with the normal recipe, one at a time; nothing was
suppressed: no `-o`, no `-t`, no timestamp change and no source edit.

```sh
make install-doc DOC=liturgy/roman-rite/1962/propers/temporal/59-nineteenth-after-pentecost PROVIDER=claude
make install-doc DOC=liturgy/roman-rite/1962/propers/temporal/59-nineteenth-after-pentecost-synthesis PROVIDER=claude
make install-doc DOC=liturgy/roman-rite/1962/propers/temporal/59-nineteenth-after-pentecost-homily PROVIDER=claude
```

Each run validated the generation metadata and copied the bytes. Nothing was
retypeset: the build PDFs keep their build-stage times, and the three `.aux`
and three `.log` files still hash to the values the build-artifacts entry
above records. The build PDF and the installed PDF each hash to the value that
the build, the artifact gates and the visual review recorded:

| Output | Pages | Bytes | SHA-256 (build and installed) |
| --- | ---: | ---: | --- |
| `59-nineteenth-after-pentecost.pdf` | 33 | 525,153 | `27c7d1979e4dfe30e3525cda062b7d380ae762f957ff58b21e3c473c478b213c` |
| `59-nineteenth-after-pentecost-synthesis.pdf` | 12 | 462,746 | `448b926a2a1cee8e44f11b3a5518eaa89cc3a6056f158cb5f4ba7699b8c1754f` |
| `59-nineteenth-after-pentecost-homily.pdf` | 3 | 259,524 | `e1dcfb384e9334670e5ea4d015390d7f4685b88b603a907d919312245c9e33c5` |

No hash differs, so no artifact defect is reported and no review boundary is
reopened.

### Web edition, release records and wiring

The reviewed conversion
`build/web/claude/liturgy/roman-rite/1962/propers/temporal/59-nineteenth-after-pentecost.md`
was installed byte for byte at
`web/claude/liturgy/roman-rite/1962/propers/temporal/59-nineteenth-after-pentecost.md`:
132,440 bytes, SHA-256
`a8b494c540f2cf7e4a8a63f2a0c27db0e64bf6b34b4890dc13f1bfd58430ee2d`, the value
`research/web-artifact.json` records, with a clean `cmp`. It is staged, so
`git ls-files --error-unmatch` finds it. No synthesis or homily web edition
exists; the canonical study is the only web authority.

`make add-publication ID=<id> CATALOG=library/traditional-latin-mass.md
PROVIDER=claude STATUS=alpha` created one release record per PDF under
`release/publications/claude/liturgy/roman-rite/1962/propers/temporal/`. No
Claude record existed beforehand. Each has schema version 1, its own output
id, the 1962 catalog, status `alpha` and the standing authorization
`perpetual-public-repository-2026`.

In `library/traditional-latin-mass.md`, the Claude cell of the existing row 59
changed from `Planned` to Full PDF, Synthesis PDF, Homily PDF and Read. That is
the order of the schema-2 manifest's `canonical_label`, `synthesis_label` and
`homily_label`, followed by the canonical web page. The ChatGPT cell, every
other row and every other catalog page are untouched, and no companion row was
added. `release/public-alpha.json` names `gpt` as the primary provider, so the
one new canonical marker carries the provider prefix,
`claude:liturgy/roman-rite/1962/propers/temporal/59-nineteenth-after-pentecost`,
beside the ChatGPT edition's unprefixed marker for the same identity.

### Catalogue, release bindings and source inventory

`make document-catalogue` regenerated
`src/web/data/structure/documents/corpus.json`. Every change belongs to this
leaf. The existing work for this identity gains the Claude edition: the study,
the concise study and the homily under `also`, the web page, the three
contribution records the leaf's generation metadata declares, and this run's
`produced` identity. Documents moved from 202 to 203, issues from 238 to 241
and pages from 6,447 to 6,480; the Claude provider tally moved from 57 to 58
and `claude-opus-5-5[1m]` from 85 to 86 documents. The work count stays 147,
because the identity's work already existed.

Before this stage wrote anything, `make check-release-bindings` reported no
stale binding. After its writes it reported exactly three, all this stage's:
`library/traditional-latin-mass.md`, the catalogue projection, and the new web
edition as unrecorded. The refresh followed the repository's scoped rule:
`make refresh-release-bindings ADOPT=1 ONLY="library/traditional-latin-mass.md
web/claude/liturgy/roman-rite/1962/propers/temporal/59-nineteenth-after-pentecost.md
src/web/data/structure/documents/corpus.json"` made five changes. It adopted
the web edition, re-recorded the catalog page and the projection, and rewrote
the rights table and its digest. `make check-release-bindings` then reported
no stale binding. Nothing outside those three paths was re-recorded.

`make check-sources` then showed the source library's reader projection
stale, and only for this production's own addition: research iteration 2 of
this run registered *Patrologia Latina* 35 (work, edition and remote scan) to
read Augustine's *Quaestiones evangeliorum* on a page image, and the projection
under `src/web/data/structure/sources/` had not been regenerated. `make
source-projection` wrote one new edition file,
`editions/jacques-paul-migne/patrologia-latina-volume-35/1845-1845-paris.json`,
and updated `index.json`: one work, one edition and two artifacts more, all
public domain, and the facet counts that follow from them. No other projection
file changed. `make check-release-bindings` then reported exactly those two
paths, and a second scoped refresh, `make refresh-release-bindings ADOPT=1
ONLY="src/web/data/structure/sources/index.json
src/web/data/structure/sources/editions/jacques-paul-migne/patrologia-latina-volume-35/1845-1845-paris.json"`,
adopted the new file, re-recorded the index and rewrote the rights table and
its digest again: four changes, after which no binding is stale.

`tools/tpt source-inventory refresh
src/sources/inventories/claude-publications-v1.toml --review
src/sources/inventories/claude-classification-review-v1.toml --audited-on
2026-09-30` added this publication (57 to 58) and its 34 source-bearing files
(1,497 to 1,531) to the Claude publication inventory. The leaf's
classification row was then replaced from its placeholder by an audit of the
55 bindings in `research/source-bindings.toml`, the witness register and
negative results in `research/scope.md`, the dated witnesses in
`research/context.md` and the declarations in `research/review-dependencies.toml`:

- scripture: the Clementine Vulgate verse texts and chapters, and the
  Douay–Rheims with its psalm-numbering concordance;
- liturgical: the 1962 typical edition with its Order of Mass and Preface
  passages, the 1862 Pustet printing and the 1861 Cummiskey English;
- patristic: Irenaeus, Hilary, Jerome, Chrysostom, Augustine, Gregory, the
  *Expositiones in Psalmos* printed under Athanasius's name, and Cassiodorus
  as a lead;
- scholastic: Aquinas, Bellarmine, Rabanus Maurus, and the medieval
  commentators on the Mass: Berno, Honorius, Rupert, Sicard and Durandus;
- historical-primary: the Migne volumes and their facsimiles, CSEL 22, and the
  1745 and 1857 Aquinas printings;
- institutional-current: the FSSP France and ICRSP France ordos for 2026 and
  the USCCB introduction to the Psalms;
- secondary: Schuster, the continuation of *The Liturgical Year*, and the
  *Catholic Encyclopedia*;
- finding-aid: the calendar and rubric computations `research/context.md`
  adopts as finding aids only, the commentary and containment joins behind the
  lead dispositions, and the text layers used to locate page-image readings;
- repository-internal: the facsimile-rights inventory, the Latin provenance
  ledger, the translations overlay, the author-standing inventory and the
  chronology corpus, each declared in `research/review-dependencies.toml` and
  relied on for a stated conclusion.

No canon-law, magisterial, classical, prayer-devotional, archival or dataset
source occurs in the leaf's records, so none of those categories was
assigned. The review's `audited_on` became 2026-09-30, and the tool's own
render function recomputed both of its snapshots; `tools/tpt source-inventory
classify` then applied the row and `check` reports the inventory valid. The
inventory records this file's hash, so the refresh and `classify` were run
again after this entry was written. The provider-neutral inventory and the
family-migration ledger, which pins only that inventory, are unchanged.

### Publication-gate commands run by this stage

These are this stage's own runs of the terminal gate commands. They are not an
acceptance, and nothing has been committed.

- `_proper_study.py check --phase publication --require-presentation
  --require-format --require-authority --date 2026-10-04` exits 0.
- `make check-release-bindings` reports no stale binding.
- `tools/tpt public-alpha check --provider claude --document <leaf>` exits 0:
  the scoped policy is valid for the three outputs, and the global source,
  release and authorization records are valid for 241 publications.
- `tools/tpt document-library check --provider claude --document <leaf>` and
  `tools/tpt document-library structure --check` exit 0, and the projection
  is current.
- `make check-publication-inventories` exits 0 for both publication
  inventories.
- `make check-sources` exits 0 after the projection refresh above. It lists
  238 issues with no PDF installed in this workspace, none of them this leaf's
  Claude outputs; those lines are informational and gate nothing.
- `make check-web-editions-current` exits nonzero, for two reasons, neither of
  which this stage wrote. Under the host's Markdown 3.11 the converter's
  site-rendered quotation audit refuses to run against the bound lock of
  3.10.3. Under a scratch environment built from `requirements-public-alpha.txt`
  and `requirements-tools.txt`, it stops at the Claude angelology leaf,
  `theology/angelology`: its `web-edition.toml` of 2026-09-29 declares it
  eligible while its `main.tex` keeps commented-out `\input` lines for planned
  sections, and the converter reports `cannot resolve
  \input{theology/angelology/sections/10-fathers-before-dionysius}`. That leaf
  is unchanged since this run's seed commit and belongs to another production.
  The same comparison replayed in that environment with only that leaf left
  out converted 56 Claude and 72 ChatGPT eligible leaves and found every
  tracked web edition current, this one included.

## Post-acceptance research-record correction, 2026-09-30

On 30 September 2026 the maintainer asked for the correction. For this leaf it
is the four standing advisories of run `a27462e34ec9c09a` that
`evaluations/blocking-findings-v1.toml` assigns to the leaf's research
records: RES-010, RES-011, STU-011 and STU-012. The correction was made outside
the workflow, as one lane of a coordinated repair. Each finding was checked
against the tracked witness it cites before anything changed, and the reviewed
study, concise study and homily were taken as the statement of what is
settled. Five files changed: `research/interpretations.md`,
`research/scope.md`, `research/source-bindings.toml`, this record and the
standing-findings file. No render input changed, so the installed PDFs, the
web edition, `generation-metadata.tex`, `research/artifacts.json` and
`research/web-artifact.json` still describe the accepted build.

### Findings and dispositions

| Finding | Checked against | Disposition | What changed |
| --- | --- | --- | --- |
| RES-010 | Gregory, *Hom.* 38, 3 (tracked Wikisource transcription, line 534: *et prius prophetas, et postmodum apostolos fecit*); Chrysostom, *Hom. in Mt.* 69 (NPNF1-10, lines 39016–39023); Irenaeus IV.36.5 (ANF 1 OCR layer, lines 66435–66479); Hilary, *In Matth.* XXII.4 (PL 9 OCR layer, lines 82594–82599); each digest re-matched | repaired | `interpretations.md` § 2.4, allegorical sense: the servants are prophets and then apostles (Gregory; Chrysostom, with John and the Son between them), sent by the one God who called those of old by the prophets and calls us by the apostles (Irenaeus); for Hilary, the apostles and then apostolic men, their successors. That is the study's own wording in its allegorical sense. §§ 2.2 and 2.6 already gave each identification to its author, and no other sentence of the research records carried the joint clause. |
| RES-011 | NPNF1-6, `ccel-text-ce371798`, digest re-matched; the search replayed with `tools/source-library search` (case-folded literal within each physical line) for the nine stated terms, kept to lines 37787–38310 and 39237–39464 | repaired | `scope.md` § 3.6, Sermo 95 bullet: the replay returns 23 lines. The record now says that no hit identifies the refusing guests or the highways and lists every hit by line, in five kinds: the servants who invite good and bad; the hearers and the guests as invited; the Israelites and Pharaoh's magicians; the Jews in the Stephen and tribute-money passages; and two matches inside other words, *ways* in *always* (line 39261) and *nation* in *explanation* (line 39360), which the finding did not list. *Gentile*, *highway* and *streets* return nothing. The conclusion is unchanged. A dated sentence in the record's opening names the replay's method and claims no `searched` binding. |
| STU-011 | the reviewed study (`sections/40-feast-that-now-is.tex`, `30-call-to-the-nations.tex`, `50-comparison.tex`) and `proper-components.toml`; Schuster, *The Sacramentary* III, tracked 1927 OCR, digest re-matched (Introit p. 171, Collect pp. 171–172, Gradual p. 172, Gospel, Offertory, Secret and Communion p. 173, Postcommunion p. 174) | repaired | `interpretations.md`: the readings table, § 4.2 and § 5 name Augustine, Gregory and Chrysostom as the carrying authors of `feast-that-now-is`. § 3.1 records beside the controlling claim Schuster's reading of this Gospel's banquet as the heavenly one (p. 173), and § 3.2 and § 5 make him a supporting witness, cited on the Introit, Collect, Gradual, Offertory, Secret, Communion and Postcommunion as § 3.3 cites him (second round, REV-B-001). Honorius leaves the introit, collect, epistle and gradual rows of § 2.3, the lifted-hands row of § 4.2 and the `call-to-the-nations` row of § 5. The alternative of § 2.5 is now Gregory's moral reading of the highways, which the study's comparison and § 4.3 already call the second reading's alternative. No sentence of the record credits Honorius with a reading of the formulary; his readings of the shared elements stay unchanged in `scope.md` § 3.12. A dated note in the record's opening lists these changes. |
| STU-012 | the four Challoner verse-text artifacts named below and the NPNF1-8 text, digests re-matched; the documents' text matched against every verse file of the edition; fingerprints from `tools/source-library fingerprint` | repaired | `source-bindings.toml` binds, in role `translation-control` with states cataloged, acquired and inspected, the verse texts of Psalms (`578f023d`), Matthew (`dd0ba183`), Ephesians (`10c79be0`) and 1 Timothy (`1f76a59e`). They are the four books from which the three documents print or quote Douay English. Their loci are the Douay loci the study's References cite in those books, of which the concise study's and the homily's are subsets, and every locus was read. The finding's `study-text` is not a declared binding role; `translation-control` is the role the sibling leaves give these artifacts. `104.1` is added to the NPNF1-8 *Enarrationes* binding, read at Psalm CV § 1, lines 52659–52675, against the quotations in the study and the concise study. A dated header comment in the file records the additions. |

Two facts found in the course of the checks are recorded here and changed
nothing outside the four findings. Hilary's sentence at *In Matth.* XXII.4
does name the prophets, as those whose invitation the apostles recall
(*commonefacere eos quos invitaverant prophetae*), though not as the servants;
RES-010's "He names no prophets" is therefore too strong, and its conclusion
stands. And the study's and the concise study's References cite the Douay also
at 1 Par 15:3; 16:1, 7–8, Rom 13:14 and 1 Tim 1:5. The documents print no Douay English at any of these: the Paralipomenon verses are
summarised beside the Alleluia and in its dossier, Rom 13:14 stands beside
Jerome's Latin, and the words printed at 1 Tim 1:5 are the NPNF English of
Augustine's Sermo 90. The 1 Paralipomenon and Romans artifacts are therefore
not bound; 1 Tim 1:5 is bound with the 1 Timothy artifact, with that fact in
the binding's context.

### Checks run

- `tools/tpt source-library validate` exits 0 (`source-library valid:
  artifact=2910 corpus=5 edition=1050 passage=5199 segment=94 work=936
  bindings=3533`), and `tools/source-library uses` lists this leaf for each of
  the five artifacts whose bindings changed.
- `scripts/_proper_study.py check --provider claude --document
  liturgy/roman-rite/1962/propers/temporal/59-nineteenth-after-pentecost --date
  2026-10-04 --phase research` exits 0.
- `git diff` against the commit before the correction touches only the five
  files named above.

### What review covers these files

The review seals of run `a27462e34ec9c09a` were taken over the research
records as they stood when the run accepted them. They do not cover this
correction's changes to `research/interpretations.md`, `research/scope.md` and
`research/source-bindings.toml`. An independent re-review of the first round
is recorded below; no review of the second round's changes is recorded
here.

### Limits that remain

`src/sources/inventories/claude-publications-v1.toml` records the digest of
every source-bearing file of this leaf. After this correction its entries for
the five changed files are stale, and `tools/tpt source-inventory check`
reports them, until the inventory is refreshed and its classification row
re-applied. That inventory is outside this correction's files. The other
standing findings of the run (HOM-001 to HOM-003, STU-008 to STU-010, SYN-001
to SYN-003, VIS-001 and VIS-002) are not research-owned and are untouched.

### Independent re-review and second round

An independent re-review of the first round, on the same day, returned
CHANGES_REQUIRED with one blocking finding and three advisories, REV-B-001 to
REV-B-004. A second round, again outside the workflow and within the same five
files, checked each against the witness it cites and repaired all four, with
one further correction the reviewer named.

| Finding | Checked against | Disposition | What changed |
| --- | --- | --- | --- |
| REV-B-001 (blocking) | `interpretations.md` § 3.3; `sections/40-feast-that-now-is.tex`; Schuster, tracked 1927 OCR (Introit p. 171, Collect pp. 171–172, Offertory and Communion p. 173) | repaired | The first round called Schuster a supporting witness for the Gradual, Secret and Postcommunion "only", while § 3.3 cites him also on the Introit, Collect, Offertory and Communion and the study on the Introit, Collect and Communion. § 3.1, § 3.2, § 5 and the record's dated note now name every element on which he is cited, and § 3.2 keeps the Gradual, Secret and Postcommunion as the three he reads in the reading's direction. |
| REV-B-002 | NPNF1-8 text, lines 52672–52677; ANF 1 OCR layer, lines 66476–66480 | repaired | Augustine on Psalm CV § 1 ends at line 52675 (*in prophecy?*), and Irenaeus's sentence ends at line 66479. The range is corrected in the NPNF1-8 binding's context, in the STU-012 resolution note and in the table above, and the Irenaeus range in the RES-010 row above. |
| REV-B-003 | `interpretations.md` §§ 2.1 and 2.6 | repaired | The alternative of § 2.5 no longer says that the highways "lead to the nations": the controlling reading is that of Irenaeus, Hilary, Jerome and Chrysostom, for whom the highways are the nations, with Augustine's own form, for whom they are the teachings of the Gentiles out of which believers came to Christ. |
| REV-B-004 | Augustine, *Enarr. in Ps.* 140, 2 (NPNF1-8, lines 65232–65244) | repaired | `interpretations.md` § 4.2, lifted-hands row, `call-to-the-nations` cell: Augustine is credited with the whole Christ's prayer, which goes on while tribulation remains for the Church, even to the end of the world; "a people still on the road" is marked **[S]**, as § 2.3 already marks it. |

The further correction: the paragraph above on the Douay loci the documents
do not print said that only the study's References cite 1 Par and Rom 13:14;
the concise study's References cite them too, and the sentence now says so.
The STU-011 and STU-012 resolution notes in
`evaluations/blocking-findings-v1.toml` were amended to match, and its header
comment records this round.

Open items for the next revision of the reviewed documents, which this
correction may not edit:

- The study's comparison table (`sections/50-comparison.tex`, lifted-hands
  row) credits "The prayer of the whole Church still on its road" to
  Augustine, the credit REV-B-004 removed from the research record.
  *Enarr. in Ps.* 140, 2 says that the whole Christ prays while tribulation
  remains for the Church, to the end of the world; the road is the reading's
  own image.
- The study (`sections/30-call-to-the-nations.tex`, the close of "Two
  difficulties") and the concise study (`sections/concise/10-commentary.tex`,
  the paragraph on Gregory's highways) set Gregory's answer beside that of
  Irenaeus, Hilary, Jerome and Chrysostom, "with Augustine in his own form,
  that the highways lead to the nations": the wording REV-B-003 removed from
  `interpretations.md` § 2.5. The study states each Father's identification
  correctly elsewhere.

## Post-acceptance revision answering every standing finding, 2026-09-30

On 30 September 2026 the maintainer asked that everything still standing
against this leaf be fixed. That was the eleven advisories of run
`a27462e34ec9c09a` that had no disposition (STU-008 to STU-010, SYN-001 to
SYN-003, HOM-001 to HOM-003, VIS-001 and VIS-002), the two rendered
inaccuracies the research-record correction above left open, and the study
review's observation on the page-2 critical horizon. The revision was made
outside the workflow, as one lane of a coordinated repair. Each point was
checked against the witness it cites before anything changed, and repaired in
every document that states it. It changed rendered content, so the run's
visual and content acceptances do not cover these PDFs. Independent content
and visual/web reviews of the first round, and their re-checks of the second,
are recorded under "Independent re-review and second round" below.

### Findings and dispositions

| Finding | Checked against | Disposition | What changed |
| --- | --- | --- | --- |
| STU-008 | Gregory, *Hom.* 38, 9, 11, 14 (tracked Wikisource transcription, digest re-matched); Augustine, *Sermo* 90, 1, 6 (NPNF1-6 tracked text, digest re-matched); Jerome, *In Matth.* III, PL 26 col. 160 D, and *In Eph.* II, col. 508, on page images of the registered PL 26 scan, fetched whole and matched to its digest | repaired | `sections/00-opening.tex`: Gregory and Augustine make the garment charity; Jerome the new man's garment of the Lord's precepts kept, the new man Christ; the reading finds it in the Epistle's acts and the Communion's wish. Augustine and Gregory say the feast is the Church now, the Lord's Table for Augustine and the banquet of the Word for Gregory; Chrysostom addresses its guests. No "carry it:" sentence remains. The third reading's allegorical sense (`40-feast-that-now-is.tex`) now credits each his own term; `interpretations.md` § 3.4 follows. |
| STU-009 | the Postcommunion's Latin (`propers/verified.md`); Schuster, *Sacramentary* III, p. 174 (tracked OCR, line 10890); the Douay psalm-numbering table and verse texts of Pss 34:3, 90:15, 138:16 | repaired | (a) `40-feast-that-now-is.tex`: the Postcommunion names God's work, *tua … medicinalis operatio*, and the reading's opening says God's healing work, which Schuster reads of the Eucharist; `interpretations.md` § 3.1 follows. (b) `10-each-element.tex`: the orations are the Church's composition; the antiphon stands in no verse of the Vulgate, its source unidentified; "no single verse of Scripture" now "of the Vulgate". (c) Ps 34:3 (35:3) and 90:15 (91:15) in `05-appointed-texts.tex`, Ps 138:16 (139:16) in `20-wedding-garment.tex`, and the numbering convention restated so that it is true of the text. |
| STU-010 | Hilary, *Tract. in Ps.* 137, 15, CSEL 22 OCR layer fetched whole and matched to its digest, lines 37995–38030 (lemma *extendisti … fecit*), and, in the second round, the Internet Archive's page images n771–n772 of the same item, which put § 15 on pp. 742–743; Rupert XII.19–20, Durandus VI.136 and Berno's *Libellus* in their tracked layers, digests re-matched | repaired | `90-apparatus.tex` References: Hilary on Ps 137, 15 (CSEL 22, ed. Zingerle, pp. 742–743; the first round printed p. 748, the OCR layer's misreading of p. 743's running head, corrected in the second round, REV-C-001); Rupert, *De divinis officiis* XII.19–20 (PL 170); Durandus, *Rationale* VI.136 (Lyon, 1612); Berno, *Libellus* (PL 142). The scope clause is unchanged; the three commentators' bindings now say they are cited (REV-C-005). |
| SYN-001 | Gregory, *Hom.* 38, 9; Augustine, *Sermo* 90, 5–6 | repaired | `concise/02-overview.tex`: "The garment is charity (Gregory; Augustine), which the Bridegroom himself wore (Gregory)". |
| SYN-002 | the built concise pages 3–4 | repaired | `concise/10-commentary.tex`: the Ordo Missae no. 1037 sentence reduced to a clause on the Offertory; the third reading's prayers named in "Many called, few chosen" without restating the incensing or the *Placeat*; the sentence repeating the themes' "The Mass that began …" removed. |
| SYN-003 | `main.tex` and `synthesis.tex` title fields | repaired | "the expansive study" becomes "the full study" in `concise/04-themes.tex` and the homily note; the concise scope appendix names it as the Full PDF subtitled *The wedding garment, the call to the highways, and the evening sacrifice: a study of the proper in three readings*. |
| HOM-001 | Augustine, *Enarr. in Ps.* 140, 3 (NPNF1-8, digest re-matched) | repaired | "St Augustine hears the Gradual's verse differently". |
| HOM-002 | — | repaired | "Today's Collect". |
| HOM-003 | the Douay psalm-numbering table | repaired | The note's loci and Douay References give Ps 140:2 (141:2), 118:4–5 (119:4–5) and 138:16 (139:16). |
| VIS-001 | the rebuilt homily, on rasters | repaired | All 13 "St <Name>" in the spoken body tied; page 2 now opens "St Hilary of Poitiers". |
| VIS-002 | the rebuilt concise study, on rasters | repaired | Concise References subdivisions at `\subsection*`, the study's level; page 12 still holds References, timestamp and colophon. |
| Open item: Augustine's highways | Augustine, *Quaest. ev.* I.31 (tracked Latin transcription: *viae intelliguntur dogmata Gentium*) | repaired | `30-call-to-the-nations.tex` (close of "Two difficulties") and `concise/10-commentary.tex`: Gregory's answer stands beside that of Irenaeus, Hilary, Jerome and Chrysostom, for whom the highways are the nations, and beside Augustine's own, for whom they are the teachings of the Gentiles. The concise themes' "where the highways lead" now reads "what the highways are". |
| Open item: the road in the comparison | Augustine, *Enarr. in Ps.* 140, 2 (NPNF1-8, lines 65232–65244) | repaired | `50-comparison.tex`, lifted-hands row: "The prayer of a people still on the road: the whole Christ crying to the end of the world (Augustine), in the last age (Hilary)". The concise commentary's sentence now has the second reading take from Augustine the Church that must cry to the end of the world. |
| Study-review observation: critical horizon | `src/sources/chronology/composition.yaml`; the NABRE introductions' passage records; both public introductions read on 2026-09-30 through a web fetch, which returned the cited sentences (no bytes retained or hashed) | repaired | The observation's premise was wrong: the corpus holds `critical.gospel-of-matthew` and `critical.ephesians-later-disciple` under `catholic-critical-v1`. `research/chronology-profile-comparisons.toml` (new) selects both; `tools/tpt proper-chronology record --document … --provider claude --write` and `annotations … --format tex --write` regenerated `research/chronology.toml` (schema 3) and `research/chronology-annotations.tex`, default answers unchanged. The Gospel and Epistle explanatory rows of `80-date-location.tex` and `concise/03-date-location.tex` carry each as the modern critical horizon with its corpus condition; the scope appendices and References follow. Declared in `proper-components.toml` (references of both chronology components), `research/scope.md` §§ 7.1–7.4, a comment in `research/review-dependencies.toml` and two `cataloged` bindings in `research/source-bindings.toml`. |
| The two "carry it" observations (study review; synthesis review) | `guidance/liturgy/propers-three-documents.md` | repaired | Every instance in this leaf is repaired (STU-008, SYN-001, and RES-010 earlier). The first round recorded them open because the criterion they asked for belongs to guidance; the coordinator has since added it to the profile (an opening, overview or summary that names a reading's authors beside its thesis credits each only with the clause he states), and the findings record now marks both repaired. |
| Homily-review observation: `element_keys` of the homily | `guidance/liturgy/propers-three-documents.md`, "Mechanical and judgment gates" | repaired | Answered by the coordinator's profile sentence: a homily component's `element_keys` declare the elements whose research informs the speech, which the checker requires to be all of them, and do not claim the speech recites each. The manifest and checker are unchanged. |
| Research-review observation: `commentary-work-index` example drift | commit `9d0c5b7fa` | repaired | The coordinator recaptured the tool's transcripts from real runs in that commit; all 13 of its examples replay clean. |
| Visual-review observation: homily bytes per page | the rebuilt homily (259,496 bytes over 3 pages, fonts only) | not-a-defect | As the observation itself found, the ratio is the fixed overhead of the embedded Latin Modern subsets; the revised homily keeps the same fonts. |

The derive-synthesis section above says that the corpus holds no modern
critical claim for Matthew or Ephesians. That statement was wrong and is
superseded here. One generated wording changed with the comparisons: the
Gospel's event annotation now reads "Narrated event date unresolved", the
projection's fixed form when a comparison is declared; the corpus state is
still `research-pending`. A probe of `check-content-preflight --check
chronology-claims-supported` with the dossier's dates altered to "after
A.D. 75" and "A.D. 80–105" refused both; the dossiers as written pass.

### Layout repairs

- The opening's new attributions first pushed the map's last row onto page 4;
  the paragraph was tightened until the map stood whole on page 3 again.
- The critical horizon lengthened the study's dossier appendix past one page
  and split the Epistle's dossier. A `\pagebreak` before that dossier keeps it
  whole, as the pc-s52 revision did for its Gospel, and the `\clearpage`
  between the appendix and `sections/90-apparatus.tex` was removed from
  `main.tex`, so the scope appendix follows the Epistle's dossier on page 31
  instead of leaving a sparse page.
- The concise page 2 holds the sheet with room to spare; no repair was needed.

### Artifacts

| Output | Pages | SHA-256 | Bytes |
| --- | --- | --- | --- |
| `build/…/59-nineteenth-after-pentecost.pdf` | 33 | `2f7707347671c95e7ed27fc7cf28c29f9629ab57f9a2f43af40a48abf9f8b8a4` | 528,081 |
| `build/…/59-nineteenth-after-pentecost-synthesis.pdf` | 12 | `cc11da2da51fe051be9989dd3f509fc12d98aecf7dacabdfb42c42109bc1ef32` | 448,015 |
| `build/…/59-nineteenth-after-pentecost-homily.pdf` | 3 | `aaa3c8fe8dcecb86377242b5a3325fe380bd83fce12897ccf080d21b05ff8288` | 259,496 |
| `build/web/…/59-nineteenth-after-pentecost.md` | — | `2ea1fc7a9e069093ee3d331f6e65b5b435f192645b9d107aefb6efa113abe50b` | 134,830 |

`\AIDocumentRevisionTimestamp` is `2026-10-01T01:50:15Z`, and one
`\AIModelContribution` line records this revision. The spoken body is 1,453
words by the rule recorded under Derive-homily, with `~` read as a space.
`research/artifacts.json` and `research/web-artifact.json` were re-recorded
by `scripts/_proper_study.py snapshot` and `snapshot-web`. Nothing was
installed under `pdf/` or `web/`.

### Checks run

- `make doc` for the study, the concise study and the homily: two passes each,
  and the settled logs carry no overfull or underfull box, LaTeX or package
  warning, undefined reference or rerun request. A second build of all three
  was byte-identical. `pdffonts` reports every font embedded; `pdfinfo` gives
  each PDF its title and subject and the revision time.
- The concise aux file places inventory, overview and all four sense markers on
  page 1, chronology on page 2, themes on pages 3–4 and commentary from page 5.
- `tools/tpt pdf-review --output build/tpt-revision-2026-09-30/rasters` over
  the three PDFs; every changed page was inspected (study pp. 2–4, 8, 13, 22,
  23, 27–33; concise pp. 1–5, 9–12; homily pp. 1–3), with both contact sheets
  of the study.
- `tools/tpt web-edition` with Markdown 3.10.3, the version
  `requirements-public-alpha.txt` pins, installed in a temporary environment
  for the run.
- The coordinator's gate list, every preflight and artifact gate the workflow
  ran for this leaf: for each edition `scripts/_proper_study.py check --phase
  content` and `check-content-preflight` (references-used,
  identifiers-resolve, bindings-valid, restricted-not-reproduced,
  relation-coverage, unquoted-not-quoted, structural-meta-labels, house-voice,
  chronology-record-current, chronology-annotations-current,
  chronology-claims-supported, provenance-matches-run); `check --phase
  artifacts`; `proper-chronology record --check` and `annotations --check`;
  and `source-library validate`. All 43 pass.
- `tools/tpt source-library validate` passes; `tools/tpt source-inventory
  check` passes.

### Independent re-review and second round

An independent content review of the revision, on the same day, returned
CHANGES_REQUIRED with one blocking finding and four advisories, REV-C-001 to
REV-C-005; the visual and web review passed. A second round, outside the
workflow and within the same leaf, checked each against its witness and
repaired all five.

| Finding | Checked against | Disposition | What changed |
| --- | --- | --- | --- |
| REV-C-001 (blocking) | the Internet Archive's page images of the CSEL 22 item, leaves n771 (p. 742, where § 15 begins, lemma *extendisti manus tuas: et saluum me fecit dextera tua*) and n772 (p. 743), read on 2026-09-30; the OCR layer re-fetched and matched to its digest | repaired | Hilary, *Tract. in Ps.* 137, 15 is at CSEL 22 pp. 742–743. The p. 748 that the research stage took from the layer, and that the first round repeated and called verified, is the layer's misreading of p. 743's running head; the real p. 748 is in the tractate on Ps 138. Corrected in the study's References, `research/scope.md` § 3.7, the CSEL 22 binding's context, the STU-010 row above and the STU-010 resolution note. The leaves are not registered, and nothing was retained. |
| REV-C-002 | `evaluations/blocking-findings-v1.toml` as the coordinator left it | repaired | The table above now gives all six observations: the critical horizon (repaired by this revision); the two on the "carry it" form, repaired, the leaf's instances by this revision and the missing criterion by the coordinator's sentence in `guidance/liturgy/propers-three-documents.md`; the homily `element_keys` observation, answered by the coordinator's second sentence there; the example drift, recaptured in commit `9d0c5b7fa`, after which all 13 examples replay clean; and the PDF size, `not-a-defect`. The findings record's header now says that this revision answered three of the six, the two on the sentence form first as open, and the coordinator the other three; a sentence for this round follows it. |
| REV-C-003 | the generated Date cells, which now print the declared comparison after the default answer | repaired | In both studies' Gospel dossiers "The last date, c. A.D. 50" now reads "The sixth, c. A.D. 50"; in both Epistle dossiers "The range is Ladeuze's" reads "The first range shown is Ladeuze's". The study's scope appendix no longer says the Date cells come from the record "under its default profile": they carry its default answer for every element and, for the Gospel and the Epistle, a declared comparison under the critical profile. The concise scope note had no such phrase. |
| REV-C-004 | the corpus note of `critical.ephesians-later-disciple` | repaired | "a secretary writing at Paul's (his) direction" now reads "a secretary working at Paul's direction" in both Epistle dossiers. `research/scope.md` § 7.2 no longer quotes the restricted introduction's sentence; it summarises it in the corpus's terms. |
| REV-C-005 | the three bindings and the study's References | repaired | The Rupert, Durandus and Berno binding contexts in `research/source-bindings.toml` now say that the study's References cite them for the scope appendix's clause that the commentators' Mass read another Gospel, and that nothing of theirs is used in a reading. `tools/tpt source-library validate` passes. |

Render inputs changed, so `\AIDocumentRevisionTimestamp` moved to
`2026-10-01T02:29:20Z`, and a second `\AIModelContribution` line records this
round. All three documents were rebuilt with `make doc`: two passes each, with
settled logs carrying no overfull or underfull box, warning, undefined
reference or rerun request. A second build was byte-identical. The concise
markers are unchanged, with inventory, overview and four senses on page 1,
chronology on page 2, themes on pages 3–4 and commentary from page 5. The
changed pages (study pp. 30–33) and concise pp. 1–5 were inspected on rasters
from `tools/tpt pdf-review --output build/tpt-revision-2026-09-30/rasters-r2`.
`snapshot` and `snapshot-web` re-recorded the receipts. The web edition was
regenerated with the full pinned deploy environment (Markdown 3.10.3); the
first round had used a temporary environment carrying only that pin.

| Output | Pages | SHA-256 | Bytes |
| --- | --- | --- | --- |
| study | 33 | `343d68584f0497f286f251744061df8356336a66c084083bd216786b0c071c94` | 528,196 |
| concise study | 12 | `d845791fa6edfc0f30fabadb3695bc129563a60420a17bc2189727ce6a21f30d` | 448,068 |
| homily | 3 | `597e74d7a80ec96a02ddf640bfe429d9dd7190181d463c7ad833590ba653ddd1` | 259,493 |
| web Markdown | — | `4b3697b0cdf149eb27d97cdfac8940be738cffce190ca4c870ec2b3863c461b4` | 134,942 |

After the second round the coordinator's gate list (every preflight and
artifact gate named under "Checks run" above) passes all 43 checks, and
`tools/tpt source-library validate` and `tools/tpt source-inventory check`
pass. No independent review of the second round is recorded here.

### Coordinator's record of the reviews

The coordinator dispatched two fresh reviewers that had not authored the
revision. The content review of the first round returned CHANGES_REQUIRED
with REV-C-001 (blocking: Hilary's CSEL 22 page) and REV-C-002 to REV-C-005;
its re-check of the second round passed, with one advisory, REV-C-006 (this
entry's opening still said no review was recorded), which the coordinator
repaired in the paragraph above. The visual and web review inspected every
page of the three first-round PDFs, regenerated the web edition byte for byte
under the pinned Markdown 3.10.3 and rendered it at 360, 390 and 1280 px; it
passed, and its re-check of the second round pixel-diffed every page against
the first, viewed each changed page at full size, confirmed the concise
page contract, clean logs and embedded fonts, and again reproduced the web
edition byte for byte. Its one advisory (REV-V-001, renumbered REV-V-002)
stands for the owner of `tools/tpt proper-chronology annotations`, not this
leaf: the generated Gospel and Epistle Date cells print the profile key
"catholic-critical-v1" and "composition-only", the generator's standard
comparison label, already published in Claude 57 and GPT 59, which the
profile forbids editing by hand. The reviewed artifacts are the study
`343d68584f0497f286f251744061df8356336a66c084083bd216786b0c071c94` (33 pp.),
the concise study `d845791fa6edfc0f30fabadb3695bc129563a60420a17bc2189727ce6a21f30d`
(12 pp.), the homily `597e74d7a80ec96a02ddf640bfe429d9dd7190181d463c7ad833590ba653ddd1`
(3 pp.) and the web Markdown
`4b3697b0cdf149eb27d97cdfac8940be738cffce190ca4c870ec2b3863c461b4`.

## Contents links and bookmarks rebuild, 2026-10-01

On 1 October 2026 the maintainer reported that the PDFs' hyperlinks did not
jump to their claimed locations, and authorized regenerating every leaf built
with `src/common/propers-format.tex`, both providers. The cause was shared:
`common/preamble` loads hyperref before the format loads titlesec, so hyperref
never defined titlesec's anchor hooks and titlesec replaced them with
`\@gobble`. With `secnumdepth` 0 every section went without an anchor, and
each contents line, PDF bookmark and following `\label` pointed at the last
anchor before it, usually `table.1`. The shared format now defines hyperref's
own hooks after loading titlesec. Its References heading, starred so that `check-content-preflight` can find it, now has `\phantomsection` immediately before it, so the manual contents line, its bookmark and `\label{sec:references}` have an anchor of their own that keeps the heading in view. No word, layout or page
changed: every page is pixel-identical to the previous installation, and only
link destinations and bookmarks differ. The three PDFs were rebuilt with the
normal recipes and installed byte-identical:

| PDF | Pages | SHA-256 |
| --- | ---: | --- |
| Study | 33 | `bbdb436d4910d6bff0f3114cf17901bafa2cdcc833d1b27a6abf8605d224fa3a` |
| Concise study | 12 | `6836b0169fc519297a6beeea89826a5b3cb4e83b6b136b72bc5fdc0ac09611b7` |
| Homily | 3 | `597e74d7a80ec96a02ddf640bfe429d9dd7190181d463c7ad833590ba653ddd1` |

Verified on the installed PDFs: 10 contents links and 14 bookmarks
each land on the page of their heading with the anchor at or above it, and
0 footnote links resolve. The artifacts-phase gate under this leaf's
declared contracts and `check-generation-metadata` pass, and
`research/artifacts.json` is re-recorded. An independent review
confirmed the cause, the definitions' identity with hyperref's, and the links,
bookmarks and pixels of all 27 rebuilt PDFs; its advisory that the References
anchor sat below its heading was answered by moving the anchor before it.
