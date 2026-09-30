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
