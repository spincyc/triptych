# Research scope — Sixteenth Sunday after Pentecost (1962 Roman Rite)

Audit record for the canonical leaf
`liturgy/roman-rite/1962/propers/temporal/56-sixteenth-after-pentecost`.
Written by `research-synthesis` of run `e4aebcbd941b6b1a`
(workflow `proper v25`, commit `b66eb4b44d8e76801a86275b19c3a2e45713b4ab`,
2026-09-05). This file is rewritten at each iteration of this stage, which is
its sole writer; the research lanes were forbidden to touch it and no later
stage may add to it or amend it.

**This is the iteration-2 state, and it integrates a fresh seven-lane join
whole rather than a diff against what stood before.** The join carries **216
findings, all seven lanes `PASS`** — `scripture-context` 45,
`patristic-reception` 34, `liturgical-history` 21, `theological-synthesis` 41,
`source-citation-coverage` 21, `cultural-afterlife` 15, `precedent-search` 39.
The iteration-0 join carried 140 and the iteration-1 brief was written from it;
where a lane has since corrected itself, the correction is carried here and the
superseded statement is named as superseded rather than silently dropped.
`CARRIED_FINDINGS` was empty at this iteration.

**Why the lanes ran again.** The iteration-1 content evaluation raised one
blocking finding whose `repair_target` is `research`: **`CON-REC-002`**
(`reception-sweep`), against §2.1, §2.4, §2.5, §2.7 and §2.8, §3.2, §5.3 and
§5.11 — that the patristic and saintly sweep at the five appointed psalm
passages was not broad, exactly two corpora having been opened at them
(Augustine at all five, Aquinas at the Offertory alone), with no Greek psalm
commentary of any kind. **It is answered.** Three further direct commentators
are now opened at all five psalms at their own works and loci — Cassiodorus's
*Expositio psalmorum* in Latin, Theodoret of Cyrus's *Interpretatio in Psalmos*
in PG 80 (the Greek voice §5.3 recorded as missing), and Bellarmine's 1866
English *Explanatio in Psalmos* — with Jerome's *Epistula* 106 adjudicating the
wording at two of the five and returning bounded negatives at the other three.
§2's rows carry each, `source-citation-coverage` independently confirms the
reachability, rights and evidence state of all three (COV-016 to COV-018,
COV-021), and §5.3 and §5.11 are rewritten to the searched result. No psalm
element of this formulary now rests on one Latin Father.

Two further things this iteration settles that iteration 1 recorded as
unresolved: **Guéranger does reach this Sunday** (§7.1, now closed on a rendered
page image), so a formulary-level commentator on this Mass exists and §5.4 is
rewritten; and the **1955 decree** that reduced this Sunday to one oration was
found and read (§4.6). What remains unresolved is named at §7.

This file is an audit record and is written in an audit's register. Nothing in
it is a sentence the guide may paste. `guidance/editorial.md` keeps method,
evidence classes and caution machinery out of reader-facing prose; the author
inherits the conclusions recorded here and not the register they are recorded
in.

The text control is `propers/verified.md`, which this stage does not restate
and does not amend. The date control is `research/chronology.toml`, which
nothing in this workflow may edit and which **§12** below transcribes.

**Where a lane corrected itself between the two sweeps, the correction is
carried and the superseded statement is named.** The substantive ones are
gathered so a reader can find them: the Clementine's reading at Ps. 101:17
(§2.4); that a commentator's lemma **is** the missal's at the Offertory (§0.6,
§2.7); the four registry and prose-corpus figures (§3.4); the reception discovery
index's count of twenty and not eighteen (§5.10); the distance of Augustine's
`ex alto factus est humilis` from the Gradual's cut (§2.4); the `copios` sweep
returning 23 verses and not 20, and the `tota die` net reaching three of the five
psalms and not two (§2.1, §1.2); Eph. 4:2 rather than 4:1 for `cum omni
humilitate` (§1.2); Guéranger's chapter (§7.1); and this brief's own P6 mechanism
(§9.6).

Evidence classes throughout are those of
`guidance/liturgy/roman-1962-propers.md`, "Evidence and Claim Discipline":
(1) textual observation, (2) documented historical orientation,
(3) documented reception, (4) source-grounded synthesis,
(5) exploratory proposal.

---

## 0. Overlaps reconciled between lanes

Seven lanes swept independently and reached the same witnesses by different
routes. Where they did, the accounts are joined here; where they conflict, the
conflict is preserved in section 7 rather than settled.

### 0.1 Augustine's *Enarrationes in Psalmos*, reached three times over

`patristic-reception`, `theological-synthesis` and `source-citation-coverage`
each opened Augustine on all five appointed psalms, by three different routes,
and the three do not report the same bytes.

| Psalm (Vulg.) | Element | Latin route, `patristic-reception` | Latin route, `theological-synthesis` | English, both, and `source-citation-coverage` |
| --- | --- | --- | --- | --- |
| 85 | Introit | la.wikisource Corpus Corporum / Migne, part 9 (sha256 `9a41f4de…`) | augustinus.it, `esposizione_salmo_104_testo.htm` (sha256 `3909c029…`) | New Advent NPNF 1.8, "Exposition on Psalm 86" (sha256 `4f242c3f…`) |
| 101 | Gradual | same series, part 11 (sha256 `e2181ab7…`) | augustinus.it, `…salmo_122` and `…salmo_123` | New Advent, "Psalm 102" (sha256 `adb31091…`) |
| 97 | Alleluia | same series, part 10 (sha256 `09d04cdd…`) | augustinus.it, `…salmo_118` (sha256 `695aa883…`) | New Advent, "Psalm 98" (sha256 `ac7372de…`) |
| 39 | Offertory | same series, part 4 (sha256 `c92354f5…`) | augustinus.it, `…salmo_054` (sha256 `0de304d7…`) | New Advent, "Psalm 40" (sha256 `3fab0826…`) |
| 70 | Communion | same series, part 7 (sha256 `b4361105…`) | augustinus.it, `…salmo_089` (sermo II only) (sha256 `7fdf9aa5…`) | New Advent, "Psalm 71" (sha256 `e92895c6…`) |

Both Latin routes are web transcriptions of Migne, not critical texts: CSEL /
CCSL 38–40 was opened by neither lane, and Migne's column numbers were not
verified against a facsimile by either. The two lanes' section numbers agree
wherever both cite one, so the locus form that survives the join is
**enarratio + sermo + section**, never a Migne column. The English of all five
is New Advent's revised delivery of the 1888 NPNF translation, whose host
markup `source-citation-coverage` records at `rights_status = "unresolved"`:
short attributed quotation of the public-domain translation only.

`source-citation-coverage` (COV-006) reports the registration state, and it has
moved: Augustine's *Enarrationes* at all five appointed psalms are now
registered on **three** editions — the New Advent English, the Migne/Corpus
Corporum Latin at la.wikisource, and augustinus.it — and every one of those
fifteen artifacts re-fetched byte-identical this run. At iteration 0 the library
registered the edition and held no artifact and no passage at any of the five.
Two citation limits survive the closure and are §0.5's: the New Advent delivery
files these expositions under the Hebrew psalm numbers and prints inline verse
numbers that run one behind the missal at the Gradual and the Offertory, and the
NPNF English is visibly abbreviated by its editors with their own ellipses
inside sections, so the Latin routes are the fuller witness and a quotation must
say which route it comes from.

**And the join's own correction to itself: registering Augustine five times over
does not make him more than one witness.** That is what `CON-REC-002` said and
what §0.7 answers.

### 0.2 Eph. 3:18, where four lanes converge and the tradition divides

`patristic-reception` (PAT-006, PAT-007, PAT-013), `theological-synthesis`
(THE-009), `scripture-context` (SCR-008), `cultural-afterlife` (CUL-004) and
`precedent-search` (PRE-021) all reach the four dimensions. Joined:

- **Chrysostom**, Homily 7 on Ephesians (NPNF 1.13, New Advent
  `230107.htm`, sha256 `e663cc18…`), takes them as the immensity of God's love
  "and how it extends every where", sketched by the visible dimensions of a
  solid body, "pointing as it were to a man". **He does not read them as the
  Cross.** Homilies 6 and 8 were retrieved as boundary witnesses, fixing the
  whole appointed pericope inside Homily 7.
- **Augustine** reads them as the four members of the Cross in **three**
  places, not two. `patristic-reception` found two — *Epistula* 55 (ad
  Ianuarium) 14.25 and *In Iohannis euangelium tractatus* 118.5 — and recorded
  that they differ on two of four assignments and reverse the order of height
  and length. `theological-synthesis` independently found a third, *Sermo* 165.3.3–5.5,
  whose assignments differ again (breadth = the charity that alone works well;
  length = perseverance to the end; height = *sursum cor* and loving God
  *gratis*; depth = the unsearchable judgments of God). **The join is that
  Augustine gives three cross-readings with three different sets of virtues,
  which is a development within one author and must not be printed as one
  fixed patristic reading.**
- **Aquinas**, *Super Epistolam ad Ephesios lectura* cap. 3 lect. 5
  (Corpus Thomisticum ref. 87805, sha256 `9dad10c5…`), holds three readings
  together without choosing: the Dionysian (the dimensions in God
  metaphorically, grounded on Job 11:8–9), the charity reading, and the Cross,
  in which he specifies the hidden depth as **predestination**. Marietti text,
  not Leonine.
- **Scripture context** independently identifies the Job 11:7–9 counterpart
  Aquinas cites for the first reading, and observes that both passages set the
  four measures against a verb of comprehending (`comprehendes` / `comprehendere`).
- The **development chain** is a real result: Chrysostom (extent of love,
  figured by a solid body) → Augustine (four members of the Cross, virtues
  assigned, three times differently) → Aquinas (keeps the cross-figure and the
  depth-as-hidden-grace and names the depth predestination). Aquinas does not
  cite Augustine by name at the cross-reading in the retrieved text, so the
  dependence is a comparison of what the texts say and not a documented
  citation.
- **Textual control the join produces:** the missal and the Clementine print
  `sublímitas`; Augustine's African text reads `altitudo` and he pauses at
  *Sermo* 165.2.2 to justify the translator's choice. A guide that quotes
  Augustine on *altitudo* beside the missal's *sublímitas* has crossed two
  Latin texts.
- **A fourth position, from the one commentator on this formulary.** Guéranger,
  at printed p. 359 (artifact PDF p. 380), takes the four dimensions **not of
  the Cross but of the indwelling**: "God alone … can strengthen in us the
  inward man enough to make us understand, as the saints do, the dimensions
  (breadth, length, height, and depth) of the great mystery of Christ dwelling
  in man, and dwelling in him for the purpose of filling him with the plenitude
  of God." So the checked witnesses hold **at least three** readings of Eph.
  3:18 — extent of love (Chrysostom), the Cross (Augustine, three times
  differently; Aquinas as one of his three), and the mystery of the indwelling
  (Guéranger) — and the cruciform reading may not be printed as *the* reading.
  THE-009.
- **Unverified:** the Greek cross-reading of Eph. 3:18 usually credited to
  Gregory of Nyssa was not opened at its own locus by any lane (§5.3).

### 0.3 The appointed Gospel: four direct commentators, reached by two lanes

`patristic-reception` and `theological-synthesis` both opened Ambrose and
Bede; `patristic-reception` alone opened Cyril and the *Catena aurea*;
`source-citation-coverage` measured what the library holds of each.

| Witness | Locus | Held by the library? |
| --- | --- | --- |
| Cyril of Alexandria, *Comm. on Luke*, Sermons 101 (14:1–6) and 102 (14:7–11) | Payne Smith (Oxford 1859) pp. 471–479, tertullian.org `cyril_on_luke_10_sermons_99_109.htm`, sha256 `f545b082…` | **No** — the registered Cyril artifact is the *sermons 110–123* delivery |
| Ambrose, *Expositio in Lucam* VII.195–196 | la.wikisource / Migne PL 15, book VII, sha256 `51667dd6…` | **No** — only book X is registered |
| Bede, *In Lucae euangelium expositio* | Migne PL 92 cols. 510D–513A, la.wikisource, sha256 `116db0ca…` | **Yes** — the registered artifact is the whole six-book commentary; digest re-verified 2026-09-05 |
| Aquinas, *Catena aurea in Lucam* cap. 14 lect. 1–2 | Corpus Thomisticum `clc14.html`, Turin 1953, sha256 `9e6d1cf1…` | No |

The two lanes' readings of Ambrose and Bede agree and complement each other:
Ambrose (VII.195) gives the whole pericope one paragraph, the dropsical man
being one "in quo fluxus carnis exuberans, animae gravabat officia" and
humility following as the next lesson; Bede argues the sequence
(PL 92, 511B: "per huius aegritudinem corporis, in illis exprimeretur aegritudo
cordis") and ties the first place at table to glorying in one's own merits
(512A: "non se, de meritis gloriando, quasi caeteris sublimior extollat").
Bede's is the load-bearing testimony for this formulary because *de meritis
gloriando* is the vocabulary of the Collect and the Communion; Ambrose gives
the sequence and not the merit vocabulary.

Ambrose's brevity is a bounded negative and not a gap in retrieval: books VIII
and IX were retrieved whole by `patristic-reception` and book VIII by
`source-citation-coverage`, and neither carries a second treatment; Ambrose's
own heading in book VII reads "Cap. XIV. — Vers. 2–14".

### 0.4 The 1962 formulary against the older books: three strands, three lanes

`liturgical-history` (LIT-003 to LIT-007, LIT-015, LIT-017 to LIT-021),
`source-citation-coverage` (COV-003) and `precedent-search` (PRE-007, PRE-009,
PRE-010) all worked the sacramentary and lectionary evidence. Joined in §4
(competing judgments) and carried as cross-proper claim C3 (§10.3). Where
COV-003 and LIT-003/LIT-005 read the same Wilson volumes, their readings agree
line for line, and COV-003 adds the physical line numbers and the re-verified
digests (Wilson 1915 `3613cce6…`; Wilson 1894 `039123ca…` with the second layer
`25586b16…`; Feltoe 1896 `afb6a8bc…`).

**Four things iteration 1 recorded as open on this strand are now closed, and
each closure is a book opened at its own page rather than a conspectus.**
Gerbert's *Monumenta veteris liturgiae Alemannicae* Pars I was read on the page
images of two independently produced scans at printed pp. 146, 178, 180 and 184,
which turns §4.1's Frankish Gelasian row from Wilson's Appendix into a reading
of the book and supplies the numbering arithmetic in the editor's own footnotes
(LIT-017, LIT-018). The general decree of 23 March 1955 was read at *Acta
Apostolicae Sedis* 47 (1955) 218–224 and settles which act reduced this Sunday
to one oration (LIT-019). The descent of the Sarum split into the English prayer
books was reached through Brightman's and Blunt's synopses (LIT-020). And the
modern printed chain 1862 → 1920 → 1947 → 1962 was collated at this formulary,
establishing that the ten appointed texts do not change across it and dating the
two apparatus changes that do (LIT-021).

### 0.5 The psalm-numbering hazards, which are three species of one problem

Three lanes each hit a verse-numbering offset and none of them is the same
offset. They are joined here because a guide that confuses them publishes the
wrong verses.

1. **Vulgate psalm number vs. modern psalm number** (SCR-024, and
   `propers/verified.md`, "The English"). Ps. 85, 97, 101, 70, 39 are Ps. 86,
   98, 102, 71, 40 in a modern Bible. Resolved element by element in
   `verified.md` and re-checked by `scripture-context` against the tracked
   concordance.
2. **Hebrew verse number vs. printed English verse number** (SCR-024). The
   Introit, Alleluia and Communion equivalences hold in both Hebrew and English
   numbering; **the Gradual and the Offertory hold only in Hebrew numbering**,
   because English Bibles leave the numbered Hebrew titles of Ps. 102 and Ps. 40
   unnumbered. A reader opening an English Bible at Ps. 102:16–17 finds the
   Gradual's second verse and the verse after it. Whoever states a modern
   number for the Gradual or the Offertory must say which convention it is in.
3. **New Advent's inline references inside the Enarrationes** (COV-008, and
   PAT-002 independently). The host prints a *Vulgate psalm number* with a
   *Hebrew verse number*, so its marginal figures run one behind the missal's
   citation at Ps. 101 and Ps. 39 and agree at Ps. 85, 97 and 70. The
   mechanism, checked in the tracked Clementine, is that Ps. 39:1 and Ps. 101:1
   are standalone title verses and Ps. 70, 85 and 97 fold their titles into
   verse one. `patristic-reception` reached the same conclusion at Ps. 101 from
   the other side and recorded that **section numbers, not marginal verse
   numbers, are the reliable join** between the NPNF page and the Migne Latin.

A fourth, unrelated numbering trap belongs with them: the NPNF/New Advent
series titles each exposition by the Hebrew psalm number, so Augustine on the
Introit's Ps. 85 is filed as "Psalm 86" (PAT-001).

**Three more species arrived with the three new psalm witnesses, and they do not
share a rule.** They are gathered here because each is invisible in the citation
it corrupts.

5. **Cassiodorus's own verse numerals, as monumenta.ch delivers Migne.** They
   run level with the Clementine and the missal at Ps. 85, Ps. 101 and Ps. 70;
   they run **three ahead** at Ps. 39, where Migne's numerals begin at
   `Exspectans exspectavi` and gain two further verses by splitting the
   Clementine's vv. 5 and 11, so the appointed Ps. 39:14–15 is his **Vers.
   17–18**; and they run **one ahead** from v. 1 onward at Ps. 97, where Migne
   splits the Clementine's single v. 1 in two, so the appointed Alleluia spans
   his Vers. 1 and the opening clause of his Vers. 2. **A locus taken from these
   pages must be cited by lemma and not by the page's verse number.** PAT-018 to
   PAT-021, PRE-034.
6. **Bellarmine's printed verse numbers, which are not uniform across his own
   book.** At Pss. 39 and 101 the printing omits the superscription the Vulgate
   numbers as v. 1 and therefore prints the appointed verses one lower — Vulgate
   14–15 as 13–14, Vulgate 16–17 as 15–16 — while at Pss. 70, 85 and 97 the
   printed numbers agree with the Vulgate. **A citation that assumes one rule for
   the whole book is wrong at two of this Mass's five.** COV-017, THE-037.
7. **The PG 80 facsimile's page-to-column map is not monotonic.** PDF pp.
   878–879 are a second scan of the same opening as pp. 876–877, both carrying
   cols. 1655–1658, so an artifact-page citation in the 870s–880s is ambiguous
   unless the column numerals are given with it. **The stable locus in this
   edition is the column**; the PDF page is an aid. COV-018, PAT-031.

**And one hazard that is not numbering but citation.** The argument line printed
above each psalm in the 1866 Bellarmine — for Ps. 85, "A prayer for God's grace
to assist us to the end", which reads like a one-sentence summary of this Mass's
Collect — is **the Challoner Douay-Rheims argument supplied by the edition and
not Bellarmine's own sentence**, as are the psalm texts printed above each
exposition. It may be used, attributed to the Douay argument; it may not be
attributed to Bellarmine. THE-037.

### 0.6 Where lanes reached the same fact and one supplies what the other lacked

- **The pre-1955 second and third orations.** `verified.md` records them from
  the 1862 Pustet. `liturgical-history` (LIT-009) supplies the rubrical reason
  in both books' own words (Pustet *Rubricae generales*, *De Orationibus* nn. 2
  and 11; 1962 RG n. 434 b). `precedent-search` (PRE-007) adds an independent
  second witness at OCR state: the Vatican typica 1604 payload's window at this
  formulary carries `alia Secreta` and `tertia ad libitum`, and at iteration 1 a
  wider read of the same window adds `ecunda oratid` with `tcrtia ad ubitum` in
  the Collect region and — separately — the Offertory's **printed refrain**, the
  antiphon's opening petition printed a second time at its close, in a book of
  1604. `liturgical-history` (LIT-021) then supplies what neither had: the
  Missal's **own name** for those two orations, `Orationes pro diversitate
  Temporum assignatae`, printed inside this formulary in the 1920 typical
  edition and the 1947 Benziger, which is word for word what the 1955 decree
  abolishes (LIT-019, Tit. V a) n. 1). The identification of `A cunctis` with
  the decree's phrase was an inference at iteration 0 and is now a reading.
- **The Alleluia's weak claim to its place.** `liturgical-history` reached it
  twice by independent routes (LIT-004: Wilson's Ottobonianus margin gives
  `Laudate dominum`; LIT-014: at AMS 188 the only alleluia in any of the six
  witnesses is `Laudate Dominum omnes gentes`, and `Cantate Domino canticum
  novum` has no AMS 188 entry at all). `precedent-search` (PRE-009) carries
  from claude leaf 54 the caution that Wilson's square brackets mark the
  Alleluia cues as later-hand additions and that **what the brackets assert
  about the manuscript is not established**. The join: the bracket caution
  disables the margin as sole evidence, and the independent database route
  supplies the positive result without it. The bracket meaning itself remains
  unestablished.
- **Guéranger at this Sunday.** Three lanes, two answers at iteration 0;
  **resolved at iteration 1 in favour of the two that found the chapter**, on a
  rendered page image. See §0.8 and §7.1.
- **Schuster at this Sunday.** `source-citation-coverage` (COV-013) estimated
  printed pp. 141–144 arithmetically from two registered anchors and said so;
  `liturgical-history` (LIT-001, LIT-002, LIT-008, LIT-012, LIT-013) then read
  the chapter and fixes it at **printed pp. 142–144**, artifact PDF pp. 158–160
  by the offset the two registered passages establish (printed + 16 = PDF).
  The estimate is superseded by the reading; the page image is still unopened.
- **The Communion's one other appointment.** `liturgical-history` (LIT-008)
  and `precedent-search` (PRE-017) reach Lent IV Thursday independently, from
  the 1962 book's own text layer and from the tracked registry; PRE-017 adds
  that the same Lenten feria reads the Fifteenth Sunday's Gospel (Luke 7:11–16,
  Naim), and Lasance 1945 corroborates the pairing at OCR state.
- **`in auxílium meum réspice`, where five lanes now converge and the picture
  changed.** `scripture-context` (SCR-020) establishes that the chant's
  non-Clementine reading is verbatim Ps. 70:12 — a verse of this Mass's *own
  Communion psalm*. `patristic-reception` (PAT-004) records that Augustine's
  lemma is a **third** form, `in adiuvandum mihi respice`;
  `theological-synthesis` (THE-016) that no publishable English answers it;
  `cultural-afterlife` (CUL-008) that the phrase with the real afterlife is
  Ps. 69:2's `Deus in adiutorium meum intende`, not this one. **The iteration-1
  sweep supplies what iteration 0 could not, and it corrects this brief.**
  Cassiodorus's lemma at Ps. 39:14 is `Domine, in auxilium meum respice` — word
  for word the chant's clause, in a sixth-century Latin exposition, with no
  manuscript variant recorded against it in Migne's apparatus (PAT-021). So the
  iteration-1 statement at §2.7 that *none* of the commentators' lemmas is the
  missal's is **withdrawn**: one of them is. Two things bound the correction.
  Theodoret's Greek at the same verse is the Septuagint's
  `εἰς τὸ βοηθῆσαί μοι πρόσχες`, which Migne renders with the Clementine's
  `ad adiuvandum me respice` and **not** with the chant's clause, so the Greek
  side does not support it (PAT-032); and Jerome, adjudicating this very verse
  at *Epistula* 106.23, has a **fourth** Latin form again, `in adiutorium meum
  respice`, while ruling for `respice` against a reported `festina` — which is
  the reading of Ps. 69:2, the verse this psalm doubles (PAT-034). **The drift
  between these two verses was already operating on Greek manuscripts in
  Jerome's lifetime.** What Jerome settles is the verb and not the noun. And
  after all of it: **no derivation may be asserted** (§5.8), and the chant's
  repetition of the clause as a printed refrain has a counterpart in no
  commentary checked.

### 0.7 The three further psalm commentators, reached by three lanes at once

`patristic-reception` (PAT-018 to PAT-034), `theological-synthesis` (THE-019 to
THE-037) and `source-citation-coverage` (COV-016 to COV-018, COV-021) all
opened Cassiodorus, Theodoret and Bellarmine at the five appointed psalm
passages in the same iteration, from different starting points and for different
purposes. The three accounts agree on locus and on evidence state and are joined
here; what each witness *says* is at §2, and the divergences among them are at
§7.10 to §7.13.

| Psalm (Vulg.) | Element | Cassiodorus, *Expositio psalmorum* | Theodoret, PG 80 | Bellarmine, O'Sullivan 1866 |
| --- | --- | --- | --- | --- |
| 85 | Introit | pars 2, in Ps. LXXXV §§2, 4, 6, 8, 10, 18, 23–24 | cols. 1553–1556 = artifact PDF pp. 825–826 | artifact PDF pp. 269–271 (printed 259–261) |
| 101 | Gradual | pars 3, in Ps. CI §§2–3, 5, 22–25 | cols. 1679–1682 = PDF pp. 890–891 | PDF pp. 324, 327 (printed 314, 317) |
| 97 | Alleluia | pars 2, in Ps. XCVII §§2, 4, 6–7, 14 | cols. 1657–1658 = PDF p. 877 | PDF p. 316 (printed 306) |
| 39 | Offertory | pars 1, in Ps. XXXIX §§13, 21–24, 27–28 | cols. 1159–1160 = PDF p. 614 | PDF p. 132 (printed 122) |
| 70 | Communion | pars 2, in Ps. LXX §§4, 21–23, 32–33 | cols. 1423–1426 = PDF pp. 750–751 | PDF pp. 220, 222–223 (printed 210, 212–213) |

**Routes, and the one that is a trap.** Cassiodorus is reachable at all five only
through the Corpus Corporum text as **monumenta.ch** delivers it, which the
library already registers
(`edition.cassiodorus.expositio-psalmorum.latin-corpus-corporum-monumenta-web-2026-07-28`);
its per-psalm address is a `rumpfid` of the form
`Cassiodorus, Expositio in Psalterium, <pars>, <psalm right-justified in five
characters>`, with Ps. 39 in pars 1, Pss. 70, 85 and 97 in pars 2 and Ps. 101 in
pars 3. **The la.wikisource route the iteration-1 brief pointed a later sweep at
reaches none of the five**: that transcription covers Psalms 1–30 only, its index
page nevertheless prints a table of contents naming all 150, and `/39`, `/70`,
`/85`, `/97` and `/101` each return HTTP 404 while the registered `/16` and
`/24` return 200. The third registered Cassiodorus edition, the Adriaen CCSL 98
scan, is `rights_status = "restricted"` and covers Psalms 71–150 only. COV-016,
THE-036, PRE-034.

**Theodoret and Bellarmine needed no acquisition at all**: both facsimiles were
already registered, and both re-fetched byte-identical this run (Bellarmine
56,448,883 bytes / `78b290d4…`; PG 80 129,500,554 bytes / `72ee8714…`).
§5.11's "open and not walked" is retired: they were walked, at all five loci in
each, in one pass, because both volumes carry a usable navigation layer —
printed psalm headings in Bellarmine, running column numerals in Migne — even
though neither's optical text is fit to quote from. COV-011, COV-017, COV-018.

**Evidence state, stated once for all three and applying to every use of them
below.** Cassiodorus is a dated web state of a Migne-derived public-domain
transcription, not Adriaen's CCSL 98 and not PL 70 read at a column: the section
numbers are the host's, no PL 70 column marker stands on any of the five pages,
and **any single word carrying an argument must be checked in CCSL 98 or PL 70
before it is printed**. Theodoret was read as rendered page images at six of the
eight column ranges (1159–1160, 1425–1426, 1555–1556, 1657–1658, 1679–1680,
1681–1682) and on the optical layer alone at cols. 1423–1424 and 1553–1554, with
Migne's facing Latin used as the control on the Greek; it is Migne's reprint of
Schulze's Halle recension and not a critical Greek text. Bellarmine was read as
rendered page images at PDF pp. 132, 270 and 327 and on the optical layer at
pp. 222–223, 269 and 316, and the edition is an English abridgement its own
translator declares. **Registration:** fifteen passage records are wanted, five
per witness; ten stand against artifacts the library already holds and five
against a registered edition whose per-psalm artifacts do not yet exist. That is
a provenance note (§6.1) and not a control.

**A dependence that constrains how the corroboration may be described.**
Cassiodorus is a genuine second Latin witness read at his own loci, but he is not
everywhere an independent one: he names `doctor Augustinus` inside these five
psalms (in Ps. LXXXV §18), and at the Communion's psalm he opens with Augustine's
own formula for prevenient grace almost word for word (`quae nullis meritis
praecedentibus gratis semper impenditur` against Augustine's `nullis nostris
meritis praecedentibus`). Where he agrees with Augustine the guide has
corroboration and **not two independent judgments**; where he differs — the
authorship of Ps. 101, the sense of `solíus`, the ages of the Communion's span —
the difference shows he is reading and not copying. Bellarmine cites Augustine
by name at the Introit and reproduces his Isaian proof at the Gradual, so he is
best presented as a late Latin restatement whose value here is that it is
publishable in English. **Theodoret is the only one of the three independent of
the Latin line throughout.** THE-035.

### 0.8 Guéranger at this Sunday, resolved

Three lanes disagreed at iteration 0 and the iteration-1 brief printed the
disagreement as unresolved with a stated resolution — one rendered page.
**The page was rendered and the question is closed**: the chapter stands at
printed pp. 356–371 = artifact PDF pp. 377–392 of
`artifact.prosper-gueranger.the-liturgical-year.english-duffy-1900-volume-11.ia-pdf-95ba98e2`,
and `source-citation-coverage` read the chapter heading, the printed folio, the
opening sentence and the Introit on the image at PDF p. 377.
`theological-synthesis`, whose iteration-0 negative was the dissent, retracts it
under its own id and states that the same search of the same byte-identical file
returns the chapter nine times over, so the iteration-0 report was a reading
error by that lane and not a difference in the bytes. §7.1 records the
disposition and what it changes; §2.2, §2.3, §2.4, §2.6, §2.7, §2.8, §2.9 and
§5.4 carry what he says, element by element, and §7.10 and §7.11 carry the two
places where he diverges from every exegete opened beside him. COV-012, THE-017,
LIT-013, THE-038 to THE-041.

---

## 1. The formulary, and the text facts the research rests on

Ten elements, marginal nos. 1592–1601, printed pp. 397–398 of the 1962 Vatican
typical edition, artifact PDF pp. 478–479. Rank `II classis`. Colour green by
RG 127 b, recorded in `verified.md` as an inference from the general rubrics
and not a reading of these two pages. `Credo.` and `Præfatio de Ssm̃a
Trinitate.` are the formulary's own printed rubrics; no Gloria direction, no
station, no commemoration, no second oration.

`propers/verified.md` owns every text fact and is not restated here. Four of
its results control what the research below may say, and are carried:

1. **The chants depart from the Gallican psalter at four of five elements and
   the Communion at none.** Introit five departures, Gradual three, Alleluia
   one plus a stop, Offertory two plus a printed refrain, Communion none.
   Consequence for reception: every checked Father's lemma differs from the
   missal at the departed places (§2), and no witness cited below is
   commenting on the missal's wording.
2. **The Communion's printed citation is `Ps. 70, 16-17 et 18` and is exact.**
   The calendar index and `research/chronology.toml` both carry `Psalm
   70:16-18`. The loci are identical; the citation form is not.
3. **`intellégimus`** at Eph. 3:20 is the missal's reading in both 1962
   witnesses against the Clementine's `intelligimus`, and is not a scan
   artifact. **`éxtrahet`** at Luke 14:5 is certain on the page at 200 and 400
   dpi and corroborated by the Benziger image and the 1862 Pustet page image;
   the controlling facsimile's own text layer misreads it `extranet`, and that
   is the one place in this formulary where the layer would mislead.
4. **No public-domain-English gap.** All ten elements have a registered
   witness: Douay–Rheims (Challoner) for the seven scriptural elements, the
   1861 Cummiskey hand missal for the three orations, the latter a free
   devotional rendering the guide must identify as such at first use.

`source-citation-coverage` (COV-001) confirms independently that this is the
one place where an absent library record would control publication — the
profile requires published English to be quoted from a registered witness —
and that both required witnesses are registered. **No claim identified anywhere
in this join has to be dropped from the guide for want of a witness.**

### 1.1 The lexical threads that run wholly inside appointed text

Established by `scripture-context` against `verified.md` and the tracked
Clementine; class 1 throughout.

- **`gloria`** in three elements: Eph. 3:13 `quæ est glória vestra`, 3:16
  `divítias glóriæ suæ`, 3:21 `ipsi glória in Ecclésia`; Ps. 101:16 `glóriam
  tuam`; Luke 14:10 `Tunc erit tibi glória coram simul discumbéntibus`. The
  senses differ — the Ephesians' honour in Paul's chains, God's own, a guest's
  standing before fellow diners (SCR-025).
- **`nomen`** in two: Ps. 101:16 `nomen tuum` and Eph. 3:15 `nominátur`
  (SCR-007).
- **`auxílium`** in two, and only two: the Offertory's petition, printed twice,
  and the Postcommunion's `capiámus auxílium` (THE-012).
- **`miserat-`/`miserére`** in two: the Introit and the Secret's `pérfice
  miserátus in nobis` (PRE-029).
- **Grammatical asymmetry**, class 1 and checkable on the two pages: every sung
  proper here speaks in the first person singular and all three orations in the
  first person plural (THE-006). **Refined at iteration 1**: the division runs by
  genre and not by position. All three *antiphons* speak in the first person
  singular and address God directly; the Gradual and the Alleluia carry no
  first-person form at all; and the **Alleluia is the only appointed chant that
  neither speaks in the first person nor addresses God in the second**. The
  Gradual does address God in its first half (`nomen tuum`, `glóriam tuam`) and
  only its versicle is wholly third person, which is why the statement separates
  first-person form from second-person address. The Epistle's petition is first
  singular turning to second plural (`flecto génua mea … ut det vobis`); the
  Gospel is third-person narrative carrying second-person singular instruction.
  The missal alters the person of no verb. SCR-044.
- **Five hapax legomena inside appointed text**, new at iteration 1 and
  mechanically checkable against the tracked Clementine: `hydrópicus` (Luke
  14:2), `accúbitus` (Luke 14:7), `patérnitas` (Eph. 3:15), `superabundánter`
  (Eph. 3:20) and `sénium` (Ps. 70:18) each occur **nowhere else in the whole
  edition**, and the phrase `invocántibus te` (Ps. 85:5) is likewise unique, the
  psalter's other two `invocantibus` verses reading `invocantibus eum`.
  `supereminéntem` stands at exactly two verses, Eph. 1:19 and the appointed
  Eph. 3:19. **Two bounds:** this is a fact about one Latin edition's vocabulary
  and not about the Greek or Hebrew behind it — `hydrópicus` and `patérnitas` in
  particular render Greek words whose own distribution was not checked — and **a
  hapax is a lexical fact and not an interpretation**; nothing follows from it
  about emphasis. What it supports is the precise statement that this Mass's
  appointed text is verbally unusual at five separate points, three of them in
  the two readings and two in the chants. SCR-036.
- **`legisperítus`**, the Gospel's word for its interlocutors, stands seven
  times in Luke and once elsewhere in the whole tracked Bible (Tit. 3:13), and
  Luke 14:3 is its **last** occurrence in that Gospel; the other synoptic sabbath
  controversies name the objectors otherwise. The observation is about the
  Vulgate's vocabulary, not about the identity of the persons: the appointed
  verse pairs the word with `pharisæos`, as Luke does at 11:53. SCR-042.

### 1.2 Threads that are NOT inside appointed text, recorded as controls

`scripture-context` recorded these so that a later stage does not present a
context-level echo as an appointed-text relation.

- **Poverty.** Only Ps. 85:1's `inops et pauper sum ego` is sung. `Oratio
  pauperis` is Ps. 101's unappointed title; `mendicus sum et pauper` is Ps.
  39's unappointed v. 18; `pauperes, debiles, claudos, et cæcos` falls two
  verses past the Gospel's end (SCR-026).
- **`mirabilia` and `tota die`.** Real in the psalms, thin in the appointed
  text; the Communion stops one clause short of `pronuntiabo mirabilia tua`,
  the word that would have joined it to the Alleluia (SCR-027).
- **The three orations quote no Scripture.** The chronology corpus assigns
  them no locus and the loci report prints `(no scripture)` for each. The
  Collect's `bonis opéribus` and the Postcommunion's `rénova … mentes nostras`
  share vocabulary with Eph. 2:10 and Eph. 4:23, both outside the appointed
  pericope, and the Secret's `mereámur esse partícipes` shares a stem with Eph.
  3:6's `comparticipes`. These are echoes; the profile forbids mislabelling them
  as direct quotations, and page 2 carries no dossier for them (SCR-031).
- **`gentes` stands inside appointed text exactly once**, in the Gradual's
  `Timébunt gentes nomen tuum, Dómine`. The Epistle's Gentile theme lies wholly
  in the part of Ephesians 3 the Mass does **not** read (2:11, 3:1, 3:6, 3:8,
  4:17), the appointed Gospel has no such word at all, and the psalms' other
  occurrences — Ps. 85:9, Ps. 97:2 — are one verse outside the Introit and the
  Alleluia. **A guide that presents this Mass as a Gentile-vocation formulary is
  reading the surroundings of its texts**; the one appointed occurrence says
  that the nations will fear the Lord's name, which is a different claim. One
  further caution from the English side: the tracked Douay renders `gentes` at
  Ps. 101:16 as "the Gentiles", so the guide's own English column makes the
  single appointed occurrence read more pointedly than the Latin does. SCR-041.
- **The Epistle stops one verse before the two dispositions this Mass is
  otherwise made of.** Eph. 4:1–2, the first sentence after the pericope's
  doxology, asks the Ephesians to walk `cum omni humilitate, et mansuetudine` —
  the humility the appointed Gospel ends on and the meekness the appointed
  Introit predicates of God. **Three bounds:** those words are Eph. 4:2 and are
  not appointed at this Mass; `mansuetudo` is a cognate of neither `mitis` nor
  `humilis`, so the tie to the Introit is a matter of sense and of the Douay's
  "mildness" and not of shared stems; and that the compiler ended at the doxology
  because of what follows is **not** asserted. SCR-034.
- **Two further psalm-level nets that reach no appointed word**, recorded with
  the same control. The formula of God's incomparability stands in three of the
  five psalms (Ps. 39:6, Ps. 70:19, Ps. 85:8) and **in none of the verses the
  Mass appoints** (SCR-039). The Offertory's two petitionary verbs are the
  psalter's own pair and both recur in the psalms of two other appointed
  elements — `confundántur` at Ps. 85:17 and Ps. 70:13, with Ps. 70:24 carrying
  both verbs together — but **of those four verses only Ps. 39:15 is appointed**,
  so what is shown is that the psalms this Mass sings from share a petition, not
  that the Mass sings it twice (SCR-040).

---

## 2. Passage-by-passage reception matrix

One row per distinct appointed passage. "Direct" means exegesis of the
appointed verses at the witness's own locus; "illumination" means doctrinal
reuse of a text the witness is not expounding. Every locus below was opened by
a lane at the bytes receipted in `build/tpt-runs/e4aebcbd941b6b1a/artifacts/`;
none is taken from a catena unless it is marked as such.

### 2.1 Introit — Ps. 85:3, 5 with the psalm verse Ps. 85:1 (no. 1592)

Also used at: no other 1962 formulary takes this centonisation. Ps. 85 is
drawn on at pentecost-15 (Introit, antiphon vv. 1–3 with verse v. 4),
lent-3-friday (Introit, v. 17), lent-1-ember-friday (Gradual, vv. 2, 6) and — new
at the iteration-1 re-measurement — at the Most Holy Name of Jesus, whose
Communion is Ps. 85:9–10 and whose Offertory is Ps. 85:12, 5 (PRE-008).

- **Direct ancient exegesis, checked, four witnesses.** At iteration 0 this row
  carried one; `CON-REC-002` was raised against exactly that, and it is answered
  here.
  - **Augustine**, *Enarratio in Ps. 85*, one sermon, whole. §2 on v. 1
    ("Inclinat aurem, si tu non erigas cervicem: humiliato enim appropinquat; ab
    exaltato longe discedit, nisi quem ipse humiliatum exaltaverit"), with the
    rich Pharisee boasting his merits against the needy Publican; §3 on the rich
    who are *in Deo pauperes* (1 Tim. 6:17); §5 on v. 3 ("Tota die, omni tempore
    intellige … corpus Christi tota die clamat, sibi decedentibus et
    succedentibus membris"); §7 on v. 5 ("Quid est mitis? Portans me, donec
    perficias me … nec meminit tantas quas incondite fundimus, et accipit unam
    quam vix invenimus"). §1 states the *totus Christus* frame ("qui et oret pro
    nobis, et oret in nobis, et oretur a nobis"). PAT-001, THE-004, THE-006.
  - **Cassiodorus**, *Expositio psalmorum*, in Ps. LXXXV, §§6, 8, 10, with the
    divisio at §4 and the conclusio at §§23–24. Structurally he assigns all three
    appointed verses to **Christ alone**: the divisio makes the whole psalm
    Christ's prayer, "in prima sectione dicens quae ipsi tantum probantur
    aptari", the section prayed "pro membris suis" beginning only at v. 11. On
    v. 1 the poor man is Christ *ex forma servi* — "Inclina, ostendit quia se ad
    ipsum extendere non poterat humana conditio, nisi ipse suam Maiestatem
    piissimus inclinaret", the poverty being "conditionem, quam susceperat
    humanitatis, quae ex se nihil habere potest, nisi quod largitate Divinitatis
    acceperit" — turned pastorally, "Audiant egeni et pauperes", without
    excluding the rich, "egenus enim et pauper Dei est, quisquis meruerit mundi
    istius perversitate vacuari". On v. 3 `tota die` is **the span of a single
    life** and not the Body's succession — "totius vitae tempus ostenditur, ut
    per multa tempora annorumque curricula quasi unius diei continuus clamor esse
    monstretur" — and the crying is done by works: "Magna siquidem voce ille
    clamat ad Dominum, qui quamvis lingua taceat, bonis tamen operibus
    perseveranter exclamat." On v. 5 he treats `suavis ac mitis` as a formal
    definition, "per quintam speciem definitionis, quae Graece dicitur kata ten
    lexin": "Suavis, quia post amaritudinem huius mundi dulcis est ad se
    recurrentibus. Mitis, quia diu sustinet peccatores. Copiosus in misericordia,
    quia licet sint nostra numerosa peccata, multo abundantior est pietas."
    PAT-018, THE-028, THE-029.
  - **Theodoret of Cyrus**, *Interpretatio in Psalmos*, PG 80 cols. 1553–1556 —
    **the first Greek psalm commentary opened at any of the five, and the one
    §5.3 recorded as missing.** Antiochene throughout: his hypothesis is
    historical ("Praecinit autem et Assyriorum in Hierosolymam impetum, et
    Ezechiae spem"), his gloss on the poor man philosophical rather than moral
    ("Nam uterque justitiae divitias possidens, et divinus David, et admirabilis
    Ezechias, has quidem non considerabant, ad naturae vero paupertatem
    respiciebant"), and `Inclina, Domine, aurem tuam` is "per metaphoram
    desumptam ab aegroto, qui ob imbecillitatem non potest clare loqui, et
    medicum cogit, ut aurem ori ejus admoveat". On v. 3 he does **not**
    allegorise `tota die` at all but reports a version: "Nam toto die, Symmachus
    singulis diebus dixit." On v. 5 he supplies the Greek the Latins could not:
    the lemma is `Ὅτι σύ, Κύριε, χρηστός, καὶ ἐπιεικής, καὶ πολυέλεος`, and
    "Pro mitis autem Aquila et Theodotio placabilis dixerunt. Mansuetudo igitur
    patientiam quoque innuit." PAT-029, THE-028.
  - **Bellarmine**, 1866 English, artifact PDF pp. 269–271 (printed 259–261).
    On v. 1 the prayer's form is the point — "He begins his prayer by touching on
    God's greatness and his own poverty, an excellent form of prayer … As I am
    the beggar sitting at the rich man's gate, incline thy ear to your poor
    servant" — and the poor man is a disposition and not a purse: "the person,
    who, though he may abound in the riches of the world, still does not put his
    trust in them, takes no pride in them", **citing Augustine** that "Lazarus was
    not taken up into Abraham's bosom by reason of his poverty, but on account of
    his humility". On v. 3 `tota die` is perseverance in prayer. On v. 5 he
    glosses each word of the antiphon in turn and **attributes the
    distracted-prayer reading of `mitis` to Augustine** before extending it with
    his own image of the judge and the culprit who turns aside to talk with his
    friends. PAT-024, THE-028, THE-029.
- **The strongest reception result at this element**, and it is a convergence
  across both traditions: **all four read `inops et pauper` as a confession of
  having nothing of one's own and not as a statement about wealth**, and two of
  them (Cassiodorus and Bellarmine) volunteer the same qualification that the
  rich are not excluded. Each supplies a different image for the bending of the
  ear — Theodoret's sick man too weak to speak, whom the physician must bend to;
  Cassiodorus's human condition unable to stretch upward; Bellarmine's beggar at
  the rich man's gate; Augustine's ear bent only to the un-stiffened neck.
  THE-028.
- **And the divergence that must travel with it: `tota die` is read four ways.**
  Augustine's is the Body's whole time; Cassiodorus's a single human life, and
  the crying is good works; Bellarmine's is fervour and perseverance in prayer;
  Theodoret's is Symmachus's "on each day" and nothing more. **Any argument that
  leans on the singularity of one long day is weakened by the fourth.** THE-029.
- **Textual state of the witnesses, and it now cuts two ways.** Augustine's lemma
  at v. 5 is `suavis es ac mitis`; his v. 3 is `Miserere mei` where the missal
  has `Miserére mihi`; his v. 1 `egenus et inops ego sum` where the missal has
  `inops et pauper sum ego`. **Cassiodorus's lemma at v. 5 is `Quoniam tu,
  Domine, suavis ac mitis es; et copiosus in misericordia omnibus invocantibus
  te` — the Introit antiphon's second half word for word**, against the tracked
  Clementine's `suavis et mitis, et multae misericordiae`, with no manuscript
  variant recorded against it in Migne's apparatus; but his v. 1 reads `aurem
  tuam ad me` against the missal's `mihi` and `egenus` against `inops`, and his
  v. 3 `Miserere mei` against `mihi`. Theodoret's Migne Latin at v. 1 reads
  `inops et pauper` and **matches the missal** where Cassiodorus does not.
  Bellarmine's English follows the Douay throughout. Whether the chant reading
  descends from a different Latin psalter is **still not established**: no Old
  Latin, Roman-psalter, Ambrosian or Mozarabic psalter is tracked (SCR-033), no
  recension was collated by any lane, and PAT-023 states in terms that the
  obvious explanation was **not** verified. §7.14 carries the pattern and its
  bound.
- **Later Latin.** Aquinas is not available at this psalm: the *Postilla super
  Psalmos* as Corpus Thomisticum serves it **breaks off in Psalm 54**, so he is a
  direct psalm commentator for this Mass's Offertory alone (PAT-014).
- **The formulary-level commentator.** Guéranger's chapter carries prose on the
  Introit (§0.8, THE-017); no lane quoted it at this element, and nothing here
  rests on him.
- **Bounded negatives.** No New Testament book quotes Ps. 85:1/3/5 (SCR-033).
  No cultural afterlife located (CUL-008): `Miserere mihi` is not the famous
  *Miserere*, which is Ps. 50, and the secular English lives of the word attach
  to Ps. 50.
- **Canonical relations, class 1, recorded and not asserted as derivations.**
  The chant's added dative gives Ps. 85:1 the petition-form `inclina aurem tuam
  mihi`, which in the tracked Clementine's psalter stands at Ps. 16:6 alone,
  **against** the `inclina ad me aurem tuam` of Ps. 30:3, Ps. 70:2 and
  Ps. 101:3 — the last two the psalms of this formulary's own Communion and
  Gradual, and not one of the three carrying `mihi` at all (SCR-003). **What is
  shared is that three-word petition-form and nothing wider; the two verses do
  not become verbally identical and nothing drawn from this may be stated as
  identity.** The verse as the Introit sings it is `Inclína, Dómine, aurem tuam
  mihi, et exáudi me: quóniam inops et pauper sum ego`; the tracked Clementine's
  Ps. 16:6 is `Ego clamavi, quoniam exaudisti me, Deus; inclina aurem tuam mihi,
  et exaudi verba mea`. They differ at the vocative (`Dómine` present, absent)
  and at the object of `exáudi` (`me` against `verba mea`), and Ps. 16:6 carries
  a whole opening clause the psalm verse has not. The identity wording this
  brief carried at iteration 0 was withdrawn on `CON-EVI-002`
  (`evidence-discipline`, this run's iteration-0 content evaluation); §6.2
  carries the wording constraint. `copiósus in misericórdia` corresponds to no
  phrase anywhere in the tracked Clementine; the psalter's own formula
  `multæ misericordiæ` stands at Ps. 85:5, Ps. 85:15, Num. 14:18 and Joel 2:13
  (SCR-002). `mitis` as a whole word stands in exactly two verses of the tracked
  Clementine: Ps. 85:5 and Matt. 11:29, which pairs it with `humilis corde` and
  follows immediately at 11:30 with `iugum meum suave est` — **the bridge to the
  antiphon's `suávis` is v. 30 and not v. 29**, and a sentence that asserts the
  pairing of v. 29 alone is contradicted by the verse it names (SCR-030;
  `CON-EVI-006` was raised against exactly that at `sections/20-themes.tex`).
  Apoc. 15:4 brings together the nations coming to adore (Ps. 85:9) and the fear
  of the divine name (Ps. 101:16), both psalms of this formulary, though Ps. 85:9
  is not appointed (SCR-028). **Exactly four psalms in the tracked Clementine
  open with `Oratio`, and this Mass appoints two of them** — Ps. 85 (`Oratio
  ipsi David`, the Introit) and Ps. 101 (`Oratio pauperis`, the Gradual) — while
  a third, Ps. 16 (`Oratio David`), is the psalm whose v. 6 the added dative
  reproduces in the clause. **Neither title is appointed**: the missal omits
  Ps. 85's, and Ps. 101's stands fifteen verses before the Gradual's excerpt, so
  this is a fact about the psalms the Mass draws on and not about the words it
  sings (SCR-037).
- **Four of the Introit's five departures leave no trace in the tracked
  English**, including the substantive one: the Douay renders `multae
  misericordiae` as "plenteous in mercy", which is what `copiósus in misericórdia`
  says, and the King James, the Revised Version and the Catholic Public Domain
  Version all agree. A reader comparing the printed English with the printed
  Latin sees a difference **only at the added dative**. This says nothing about
  the chant's ancestry — three English versions made from two different originals
  saying the same thing shows only that the Latin genitive and the Latin
  adjectival phrase are ordinarily Englished alike — and SCR-002's warning
  against inferring an Old Latin provenance stands untouched. SCR-043.

### 2.2 Collect — `Tua nos, quǽsumus, Dómine, grátia semper et prævéniat et sequátur` (no. 1593)

- **No direct patristic exegesis exists and none was expected**; the ordinary
  route — a Father commenting on a Sunday's own prayers — produced nothing here,
  which is the expected result for Roman sacramentary orations (PAT-016).
  **What iteration 1 adds is a commentator on this Mass**: Guéranger, printed
  p. 357 (artifact PDF p. 378), read on the rendered page image immediately above
  this Collect — "unless grace prevent, that is, anticipate, us, we cannot have
  so much as the thought of doing what is holy; and again, unless it follow up
  the inspirations it has given us, and lead them to a happy termination, we
  shall never be able to pass from the simple thought to the act of any virtue
  whatsoever. If, on the other hand, we be faithful to grace, our life will be
  one uninterrupted tissue of good works." He prints the Latin with the English
  "May thy grace, we beseech thee, O Lord, ever go before us, and follow us; and
  may it ever make us intent upon good works", and sets `prevent`, `follow`,
  `grace` and `good works` in italic. **This is the first witness in the join who
  is commenting on this Mass's Collect rather than on a text the Mass happens to
  use**, and it converts the reading of the Collect at §10.1 from a synthesis
  into a reading a checked commentator already gives. **Two bounds:** he writes
  for devotion and does not argue the point, so he witnesses *that* the Collect
  is read this way and is not the authority for the technical distinction, which
  is Augustine's and Trent's; and his "persevering continuity of this most
  precious aid" is his own phrase and **not** a rendering of `iúgiter`. THE-038.
- **Illumination, checked at two Augustinian loci.** *Enchiridion* 32
  ("Misericordia eius praeveniet me … Misericordia eius subsequetur me:
  nolentem praevenit, ut velit, volentem subsequitur, ne frustra velit"), and
  *De gratia et libero arbitrio* 17.33 ("operatur … cooperatur"). The scriptural
  substratum is Ps. 58:11 (verbatim in the tracked Clementine) and, by
  `theological-synthesis`'s own identification from the wording, Ps. 22:6,
  where the Clementine reads `misericordia tua subsequetur me` against
  Augustine's `eius`; that second identification is the lane's and not the
  edition's. PAT-015, THE-002.
- **Doctrinal reception, at three evidence states.** Trent, Session VI:
  **cap. XVI** ("virtus … bona eorum opera semper antecedit et comitatur et
  subsequitur"), **cap. X** and **can. 32** are registered and page-verified in
  this repository (`…latin-tauchnitz-1887/passages/sessio-6-decretum-16.toml`,
  `…decretum-10.toml`, `…canon-32.toml`, all `verified_on 2026-08-21`).
  **Cap. V** and **can. 3** were read here only in the item's uncorrected OCR
  layer (sha256 `588d7308…`) and are leads until the leaf image is read
  (§6.2). Cap. XVI shares two further words with the Collect at the doctrinal
  point — `iugiter` and `semper` — and the guide must not silently upgrade the
  Collect's two verbs into Trent's three by importing `comitatur` (THE-002).
- **Warrant, narrow.** Trent cap. X quotes a Sunday-after-Pentecost collect
  doctrinally, and the Tauchnitz printing's own footnote identifies it as
  *Dominica XIII post Pentecosten*. It establishes that a collect of this
  series is the kind of text a council will cite; it establishes nothing about
  *this* Collect, which Trent does not quote, and Trent quotes the Thirteenth
  Sunday's altered (THE-015).
- **Illumination at an appointed text, new at iteration 1 and a second Latin
  voice for the prevenient half.** Cassiodorus opens his exposition of the
  **Communion's** psalm by calling Christ's charity that "quae **nullis meritis
  praecedentibus gratis semper impenditur**" (in Ps. LXX §4) and closes it with
  "Cum totus hic psalmus gratiam Domini, **quae gratis datur**, summa intentione
  commendet" (§33); and at the **Offertory's** psalm he makes God's very looking
  our protection, "aliter enim liberari non possumus, nisi nos Divinitas
  propitiata respiciat" (in Ps. XXXIX §22). The first is Trent's `nullis eorum
  exsistentibus meritis` and Augustine's `nullis nostris meritis praecedentibus`
  in the same words. **The qualification is at §0.7 and is not optional**: at
  that locus Cassiodorus is corroborating and partly dependent on Augustine, not
  independent of him. THE-020, THE-031.
- **Not opened.** The Second Council of Orange (529), the other obvious locus:
  looked for among registered sources and not found, and no external witness
  retrieved (PAT-015).

### 2.3 Epistle — Eph. 3:13–21 (no. 1594)

Also read at: sacred-heart (Eph. 3:8–12, 14–19) and
s-margaritae-mariae-alacoque-virginis (Eph. 3:8–9, 14–19). Both **excise v. 13**,
the verse on which this pericope opens, and **vv. 20–21 are read only here** in
the tracked calendar (PRE-018).

- **Direct Greek exegesis, checked in English.** Chrysostom, Homily 7 on
  Ephesians, runs from 3:8 to the doxology of 3:21 and so covers the whole
  appointed pericope. Comments at Ver. 13 (the Apostle's tribulations are the
  readers' glory because God so loved them as to afflict his servants for them,
  with Hos. 6:5), Ver. 14–15 (the bowing of the knees shows the prayer is
  heartfelt, and "every fatherhood" means the tribes are now reckoned by their
  Creator rather than "according to the number of Angels"), Ver. 18–19, Ver. 20.
  The Greek of PG 62 was **not** opened by any lane, so nothing may be argued
  from Chrysostom's Greek wording; the reading rests on Gross Alexander's NPNF
  English. **Registration, closed at iteration 1**: Homily 7 is now registered as
  its own artifact with Homilies 6 and 8 beside it, all three re-fetched
  byte-identical; at iteration 0 the only registered Chrysostom-on-Ephesians
  artifact was Homily 13, which reaches no part of Ephesians 3. PAT-006, COV-005.
- **Direct Latin exegesis, checked.** Augustine, *Sermo* 165, headed
  "De verbis Apostoli (Eph 3, 13-18) … deque gratia et libera voluntate, contra
  Pelagianos" (augustinus.it Latin, sha256 `f07e6a62…`). §1.1 on the Epistle's
  hinge ("Quia ergo voluntatis habetis arbitrium: Peto. Quia vero voluntatis
  non sufficit arbitrium ad implendum quod peto: Huius rei gratia flecto genua
  mea ad Patrem … Peto enim a vobis, propter arbitrium voluntatis: rogo det
  vobis, propter auxilium maiestatis"); §2.2; §§3.3–5.5 on the four dimensions;
  §7.9 ("unde gratiam tuam meritum meum praecedat? Non"). **Two bounds:** the
  sermon covers 3:13–18 and stops three verses short of the pericope's
  doxology; and its opening remark that the day's Apostle, psalm and Gospel all
  agreed "ut spem non in nobis, sed in Domino collocemus" is evidence about
  Augustine's own African order — the psalm he says they had sung is Ps. 56:2 —
  and says nothing about this Roman formulary. THE-008.
- **Augustine on the dimensions elsewhere, checked.** *Ep.* 55.14.25 and
  *In Ioh. tract.* 118.5 (§0.2). Both name Eph. 3:18 explicitly as the text
  expounded, so the attribution is not an inferred echo; both were read whole
  on the retrieved pages. NPNF English only; CCSL 36 and CSEL 34 not opened.
- **Later saintly reception, checked.** Aquinas, *Super Ephesios* cap. 3 lect.
  4 (on v. 13) and lect. 5 (§0.2).
- **The formulary-level commentator, new at iteration 1.** Guéranger reads the
  appointed Epistle in the register §10.6 proposes for it — grace and the will's
  response — at printed p. 360 (artifact PDF p. 381): "Now, it depends on us to
  follow God's grace; nothing else but our own resistance prevents the Holy Ghost
  from making saints of us"; and at printed p. 359 he takes the four dimensions
  **of the indwelling and not of the Cross** (§0.2). He also observes, at printed
  p. 358, that the Church borrows more from Ephesians than from any other Pauline
  letter in this season, which bears on §4.7's course and is that section's to
  carry. THE-008, THE-009.
- **Not opened, and named.** Ambrosiaster, Jerome's *Commentarii in epistulam
  ad Ephesios*, Marius Victorinus, Gregory of Nyssa on the dimensions
  (PAT-017). Jerome's Ephesians commentary has **no work record in the
  library** at all (COV-010). **Unchanged after two iterations**: the Epistle is
  the element where the iteration-1 sweep added least, its whole effort having
  gone to the five psalm passages `CON-REC-002` named.
- **A registered-source hazard, not a gap.** The registered Cornelius a Lapide
  artifact titled *Commentaria in omnes D. Pauli Epistolas* (Antwerp 1614,
  577 images) **stops at Galatians 6:17 and contains no Ephesians commentary**;
  its OCR layer, 97,832 lines, has no `ad Ephesios` running head anywhere, and
  the repository's own discovery index nevertheless lists Lapide against this
  pericope. A citation of Lapide on Eph. 3 against that artifact would name an
  extent the bytes do not hold. COV-007. **Do not cite it.**
- **Canonical relations, class 1.** The pericope begins one verse before the
  sentence it completes: Eph. 3:1 opens `Huius rei gratia` and breaks off,
  vv. 2–13 are the digression, and v. 14 resumes with the same words — so the
  resumption is heard inside the reading and its first half is not, and the
  liturgical incipit removes the connective too (SCR-004). The pericope closes
  the doctrinal half of the letter, the parenesis opening at 4:1 with
  `Obsecro itaque vos` — the verb the liturgical incipit substitutes, recorded
  as a verbal coincidence and expressly not as a derivation (SCR-005). Every
  principal noun of the petition is a term Ephesians has already used
  (SCR-006). 2 Cor. 4:16–17 carries `non deficimus`, the inward renewal,
  tribulation and a weight of glory together (SCR-009); Col. 1:24 is the closest
  Pauline statement of the move Eph. 3:13 makes.

### 2.4 Gradual — Ps. 101:16–17 (no. 1595)

Also the Gradual of epiphany-3, -4, -5 and -6; Ps. 101:16 alone is the Alleluia
verse of pentecost-18, and Ps. 101:2 is the Alleluia of pentecost-17 and part of
the holy-wednesday Introit, Tract, Offertory and Communion (LIT-008, PRE-008,
PRE-016).

- **Direct exegesis, checked, four witnesses**, where iteration 0 had one.
  - **Augustine**, *Enarratio in Ps. 101*, sermo I §§16–17. §16 reads v. 16 as
    the ingathering of the Gentiles who become the second wall meeting Israel in
    the corner stone, **citing Eph. 2:20** — a verse of the appointed Epistle's
    own letter that the Mass does not read. §17 reads a **future**
    `aedificabit`: Sion is being built now ("Hoc agitur nunc"), and the seeing
    `in gloria sua` is the Judgment, set against the first coming when he was
    seen `in infirmitate sua` and "had no form nor comeliness" (Isa. 53:2). §18,
    on the verse the Gradual stops before, "Respexit in orationem humilium";
    §19, past the Gradual, "ex alto factus est humilis, ut humiles exaltaret" —
    which expounds v. 20 and is **three verses past the cut**, not one, correcting
    the distance this brief stated at iteration 0. PAT-002, THE-010.
  - **Cassiodorus**, in Ps. CI §§22–23, whose lemma carries the Missal's words at
    both disputed places: `Quia aedificavit Dominus Sion, et videbitur in
    **maiestate** sua`. On v. 16 he reads `timebunt gentes` historically and
    ascetically rather than ecclesiologically — the true Lord was not feared
    while the world served idols, and after the saving advent "gentes conversae
    sunt per timorem"; the `reges terrae` are those who bridled their own bodies,
    "qui corpora sua divinis regulis infrenantes, sui imperatores esse (Domino
    praestante) valuerunt". On v. 17 the building is **done** and the thing built
    is the Church, "hoc est mater Ecclesia, de vivis lapidibus fabricata, in qua
    Domini cultura usque ad finem mundi sine intermissione proficiet", and the
    seeing in majesty is the Judgment in the assumed body, "quando haedos
    sequestrat ab agnis". PAT-019.
  - **Bellarmine**, artifact PDF p. 327 (printed p. 317), his printed vv. 15–16.
    He holds together what Augustine and the Missal divide: the building is
    accomplished "in the present day, having established his Church in spite of
    all kings and nations", and the seeing is "in the time to come, when he shall
    come with all his Angels … When he began to build up Sion he was seen in his
    lowliness. 'We have seen him, and there was no sightliness' … but when he
    shall come to pass judgment, then 'he shall be seen in his glory.'" **That
    antithesis is Augustine's own, made from the same Isaian verse.** And one
    usable detail: at the preceding verse he glosses the psalm's "thy glory" as
    "that is, thy **majesty**" — a commentator reading `gloria` supplying
    `maiestas` as its sense unprompted, which is a gloss and not a textual
    witness, his printed lemma being the Clementine's "in his glory". PAT-025.
  - **Theodoret**, PG 80 cols. 1679–1682, and **he produces the sharpest
    disagreement in the whole sweep.** His Greek lemma at v. 17 is a **future** —
    `Ὅτι οἰκοδομήσει Κύριος τὴν Σιών, καὶ ὀφθήσεται ἐν τῇ δόξῃ αὐτοῦ` — which is
    Augustine's tense against the chant's perfect, while Migne's facing Latin
    quietly renders it with the Vulgate's `aedificavit` on the opposite column.
    And his exposition is **historical, not eschatological**: the rebuilding of
    the city is itself God's glory and answers the charge that the exile proved
    him weak — "Sione rursus aedificata, in pristina gloria universorum Deum
    omnes cernent". At v. 16 he holds the historical and the christological
    together and calls the fulfilment partial, "hoc vero proprie ac vere post Dei
    et Salvatoris nostri incarnationem contigit", with an explicit
    already-and-not-yet on Heb. 2:8 and Phil. 2:10. PAT-030, THE-023, THE-027.
- **The material discrepancy, restated — and this brief's own iteration-1
  statement of it is corrected.** Iteration 1 wrote that "the Clementine agrees
  with Augustine on both words". **It does not.** The tracked Clementine at
  Ps. 101:17 reads the **perfect** `aedificavit` with `in gloria sua`, so it
  agrees with Augustine on the noun and with the chant on the verb (SCR-011,
  PAT-019). What the four witnesses actually show is this: the **tense** divides
  by textual tradition — the Greek Septuagint tradition Theodoret expounds has
  the future, as Augustine's text does, while the Clementine, Cassiodorus and
  Bellarmine have the perfect — and the **noun** divides Latin from Latin, the
  chant and Cassiodorus reading `maiestate` where the Clementine, Augustine and
  Bellarmine's English read `gloria`. So the difference between the chant and
  Augustine is not a peculiarity of the missal: it is a difference between text
  traditions at the verb and an attested Latin variant at the noun. **No sentence
  built on `maiestáte` may still be attributed to Augustine**, and none of this
  settles which reading is original, which is a text-history question §5.8
  records as unpursuable from repository sources.
- **The exegetical divergence is independent of the tense and is equally
  sharp.** All three Latin witnesses refer `vidébitur` to the Judgment;
  Theodoret refers it to the restoration of Jerusalem. **A guide that presents
  the Gradual's second half as unanimously eschatological would be reporting the
  Latin tradition as the tradition.** §7.11.
- **A fifth reading, from the commentator on this formulary.** Guéranger, printed
  p. 363 (artifact PDF p. 384), immediately above this Gradual: "The Church,
  which is showing herself in the midst of the Gentiles, bears on herself the
  mark of her divine Architect; God shows Himself, in her, **in all majesty**;
  and, by her, the kings of the earth are made to fear Him." That is the majesty
  seen **now, in the Church**, at neither a second appearing nor a rebuilt city.
  It is an introduction to the chant rather than a construe of the psalm, and it
  should be presented as what it is; but it means the eschatological reading is
  not even the whole Latin position once a liturgical commentator is counted.
  THE-041.
- **Who speaks in this psalm is itself disputed, openly, between two Latins.**
  Augustine identifies the poor man of the title as Christ, "qui propter nos
  pauper factus est, cum dives esset, eique membra cohaerentia et per suum caput
  loquentia". **Cassiodorus records that reading and declines it** (in Ps. CI
  §2): "Quamvis aliqui praesentem psalmum Domini Salvatori aptandum esse
  putaverint, conveniens tamen videtur afflicti magis et gementis pauperis …
  quia multa sunt quae illi immaculatae sanctae incarnationi nequeunt convenire.
  Et primum, quod anxius nusquam fuisse legitur Dominus Christus" — and assigns
  the psalm to an afflicted penitent poor man who is nameless on purpose, "ut cum
  uni datur, omnes sibi pauperes Christi cognoscerent attributum" (§3). Theodoret
  is a third position: the speaker is the people in the Babylonian captivity.
  **The two Latins end at a corporate speaker either way** — Augustine's Christ
  speaks in his members, Cassiodorus's nameless poor man is every poor man of
  Christ — and the disagreement is about whether the head or the body is the
  grammatical subject. §10.2's christological pattern may no longer be presented
  as the Latin tradition's undisputed reading of this psalm. THE-024.
- **Sermo division verified** on the retrieved Latin: Augustine's §§16–17 fall
  inside Sermo I, before the "SERMO II. De secunda parte Psalmi" heading.
- **Numbering traps, three of them at this one element.** The NPNF page numbers
  these two verses "Psalm 101:15" and "Psalm 101:16", one behind Migne and one
  behind the missal (§0.5.3); Bellarmine's printing numbers them 15 and 16
  (§0.5.6); Cassiodorus's numerals run level here (§0.5.5).
- **The verse the Gradual stops before is itself read four ways.** Augustine and
  Cassiodorus agree that the poor whose prayer is regarded are the faithful of
  Christ, one and many; Bellarmine refers it to the martyrs of Apoc. 6:10;
  Theodoret to the captives whose prayer was admitted, "Non enim despexit, veluti
  captivos et servos". **The formulary's own cut therefore stops before a verse
  the tradition does not settle**, which is a reason to treat what follows the
  Gradual as context and never as the chant's meaning. THE-025.
- **Canonical relation, class 1.** The two verses stand at the psalm's hinge,
  where it turns from the wasting of one afflicted man to the rebuilding of
  Sion; the psalm's own title makes it the prayer of a poor man; and Heb.
  1:10–12 quotes Ps. 101:26–28 of the Son — outside the appointed excerpt
  (SCR-010, SCR-012). The Epistle's appointed `radicáti, et fundáti` shares its
  verb with `fundasti` at Ps. 101:26, which is the verse Heb. 1:10 quotes; **that
  verse is nine verses past the Gradual's excerpt and is not appointed**, and the
  Gradual's own building word is `ædificávit`, a different verb, so there is no
  appointed-to-appointed verbal contact here and none is claimed (SCR-045).
- **Bounded negatives.** The registered library holds no passage of any
  commentator at Ps. 101 (COV-021), so the four witnesses above are receipted
  retrievals and not registered passages — a provenance note (§6.1). No cultural
  afterlife located: the verse's distinctive English produced nothing, and
  "the Gentiles shall fear thy name" returns zero pages in *Chronicling America*
  (CUL-008). **And Ps. 101 is untouched everywhere else in this collection**: a
  sweep of 2,902 files and 332,704 lines returns zero mentions of it outside this
  leaf, against 33 for Ps. 85, 52 for Ps. 39 and 65 for Ps. 70, so the Gradual is
  one of the two appointed elements with no Triptych precedent of any kind
  (PRE-038).

### 2.5 Alleluia — Ps. 97:1 (no. 1596)

The same verse is the Introit of easter-4 and of easter-thursday and is cited at
the Introits of the Assumption, the Maternity of the BVM and the Octave of the
Nativity (PRE-008).

- **Direct exegesis, checked, four witnesses**, and they give **four different
  answers to the one question the chant leaves open — what the `mirabília`
  are.** The Alleluia prints exactly the two clauses these four are expounding
  and then stops, which is what makes the divergence usable rather than merely
  recorded.
  - **Augustine**, *Enarratio in Ps. 97* §1 only — nothing later in the psalm is
    appointed. The new song belongs to the new man, and because the psalm bids
    the whole round of the earth sing it, those who cut themselves off from the
    communion of the whole earth cannot sing it, "quia canticum novum in toto,
    non in parte cantatur"; the `mirabilia` are **the raising of the whole world
    from everlasting death** by the Lord's holy arm, which he identifies with
    Christ out of Isa. 53:1; and the passage moves from new song to new man to
    inward healing ("Quis est qui intus sanatur? Qui credit in eum … in novum
    hominem reformatus"). The reading is anti-Donatist and not sacramental.
    PAT-003, THE-011.
  - **Cassiodorus**, in Ps. XCVII §§6–7, whose lemma carries `Dominus` with the
    chant against the Clementine's bare `quia mirabilia fecit`. The new song is
    **regeneration and Incarnation**, and he gives it the sacramental term the
    Postcommunion uses: "Propheta fideles admonet Christianos, ut **novae
    regenerationis sacramenta sumentes**, novum canticum de Domini incarnatione
    concelebrent. Novus enim homo cantare debet canticum novum, non ille vetustus
    qui necdum Adae peccata deponens, in praevaricatione veteris hominis
    perseverat." On the wonders he first takes them as the Gospel healings —
    "quando caecis lumen, claudis gressum, surdis etiam donavit auditum" — and
    then at once denies that these are the singular thing, "Sed ista fecerunt et
    sancti eius", locating the novelty in the **Resurrection**. PAT-020, THE-026.
  - **Bellarmine**, artifact PDF p. 316 (printed p. 306), who answers the same
    question with an enumeration that **gathers both of the readings the Fathers
    give separately**: conceived of the Holy Ghost, born of a virgin, committed
    no sin, justified sinners, the deaf hearing and the blind seeing, the dead
    raised, "and, what is the most strange and wonderful of all, shewed himself
    alive within three days after he was buried … and, finally, **as St.
    Augustine says, conquered the world, not by the sword but by the cross**".
    He is therefore a witness to the compatibility of the earlier two rather than
    a fourth opinion. PAT-026.
  - **Theodoret**, PG 80 cols. 1657–1658, the most austere: the wonders are
    simply what exceeds nature and expectation — "Supra naturam enim et conceptum
    sunt ea quae a Deo universorum fiunt" — and the new song answers a **change
    of dispensation**, `καινήν τινα πολιτείαν`, a new polity or manner of common
    life, which Migne's Latin flattens to `religionem`. His lemma carries
    `ὁ Κύριος`, agreeing with the chant's `Dóminus` and not with the Clementine.
    And his rule that in this idiom "Manum actionem appellari, Dexteram vero,
    bonam actionem" is a lexical principle and not an allegory, which is the
    Antiochene difference in one line. He and Bellarmine also agree, in almost
    the same words, that the psalm foretells both advents and dwells on the
    first. PAT-031, THE-026.
- **The one place two witnesses agree against the Clementine, and it is the
  chant's own word.** Both Cassiodorus's Latin lemma and Theodoret's Greek carry
  the explicit subject `Dominus` / `ὁ Κύριος` that the chant supplies and the
  tracked Clementine leaves implicit. That is an agreement, recorded as one;
  §7.14 carries what may and may not be built on the pattern. PAT-023.
- **Cautions on the Augustinian witness.** His lemma for the second half of v. 1
  is `Sanavit ei dextera eius` — "healed", and "for him" — and he builds a whole
  distinction on it ("Multi enim sanantur sibi, non ei"); the Clementine reads
  `Salvavit sibi` and **Cassiodorus a third form, `salvavit eum`**. The appointed
  Alleluia stops before that clause entirely, so **a guide that quotes any of
  their sequels must not present it as a reading of the missal's text, and must
  fix which psalter's continuation it is quoting** (PRE-025). And the New Advent
  page is visibly abbreviated by the NPNF editors, with their own ellipses inside
  the sections: the Latin is the fuller witness. `source-citation-coverage`
  independently measures the same page as the shortest of the five (24,306 bytes)
  and warns that thin reception here is a property of the exposition, not of a
  failed search (COV-006).
- **Bellarmine's and Cassiodorus's readings of the unsung remainder**, recorded
  as controls and not as reception of appointed text: Bellarmine takes the holy
  arm as **humility and obedience**, quoting Phil. 2:8, and Cassiodorus turns the
  clause to the Resurrection against Nestorius. Both stand outside the Alleluia.
  PAT-026, PAT-020.
- **Canonical relations, class 1.** The chant supplies `Dóminus` as subject of
  `fecit` and stops before the Gentile horizon of vv. 2–3 (SCR-013).
  `Canticum novum` occurs at Ps. 32:3, 39:4, 95:1, 97:1, 143:9, 149:1, Isa.
  42:10, Apoc. 5:9 and 14:3 in the tracked Clementine — an exhaustive list, of
  which the **full incipit** `Cantate Domino canticum novum` stands at four,
  Ps. 95:1, Ps. 97:1, Ps. 149:1 and Isa. 42:10; two of them touch this
  formulary's other elements, Ps. 95:1 under the title *quando domus aedificabatur
  post captivitatem* beside the Gradual's `ædificávit Dóminus Sion`, and Ps. 149:1
  continuing `laus eius in ecclesia sanctorum` beside the Epistle's `cum ómnibus
  sanctis` and `glória in Ecclésia`; and Ps. 39:4 belongs to the Offertory's own
  psalm (SCR-014).
- **A convergence inside the Gradual's psalm that the chant order follows.** At
  Ps. 101:19, two verses past the Gradual's cut, all three commentators opened
  there reach for newness: **Cassiodorus quotes the Alleluia's own verse** —
  "Hic laudabit Dominum, novo scilicet cantico, sicut in alio psalmo dictum est:
  Cantate Domino canticum novum" — while Augustine and Theodoret independently
  quote 2 Cor. 5:17 on the new creation. **The join he makes is inside the psalm
  and not inside the Mass**, and nothing connects the compiler of the chant series
  to any of it; the usable form is that the Gradual's psalm moves from the nations
  fearing the Name to a people yet to be created who will praise him with a new
  song, and that this Mass sings the new song immediately after the Gradual.
  THE-033.
- **Bounded negative, and it is the sharpest liturgical-history result of the
  join.** `Cantate Domino canticum novum` has no AMS 188 entry in any of the
  six oldest Roman graduals as the gregorien.info index of Hesbert reports
  them; the only alleluia recorded at that formulary in any witness is
  `Laudate Dominum omnes gentes` (Senlis alone), which is also what Wilson's
  Ottobonianus margin gives. **The Alleluia is the element of this formulary
  with the weakest claim to antiquity in its present position, and that is a
  positive result rather than a gap.** LIT-004, LIT-014.
- **No cultural afterlife, and the reason is structural**: the clause is not
  distinctive to this locus, standing also at Ps. 95:1, Ps. 149:1 and Isa.
  42:10 (CUL-008). **And Ps. 97, like Ps. 101, is untouched everywhere else in
  this collection** — zero mentions in 2,902 files outside this leaf, and no
  registered passage of any commentator at it (PRE-038, COV-021).

### 2.6 Gospel — Luke 14:1–11 (no. 1597)

Luke 14 is read in the tracked calendar in three separated blocks —
14:1–11 here, 14:16–24 at pentecost-2, 14:26–33 and 14:26–35 in the sanctoral
and a Common — and **vv. 12–15 and v. 25 are appointed nowhere** (PRE-019).

- **Direct Greek exegesis, at translation state.** Cyril of Alexandria,
  Sermons 101 (Luke 14:1–6) and 102 (14:7–11) — two consecutive sermons
  dividing the pericope exactly where it divides internally. Sermon 101 turns
  the healing into an argument about the sabbath: the law was shadow and type
  waiting for the truth, "keeping the sabbath rationally" means ceasing from
  sins and not from mercy, the lawyers' silence is malice, and Cyril presses to
  sarcasm ("Commit your child with joy to the grave, that you may honour the
  Giver of the law"). Sermon 102 reads the seating parable as the ordinary
  virtue of a modest mind: seizing an honour not due is "like a theft … and the
  restitution of the stolen goods", worldly honour is grass on a housetop.
  **Evidence state, and it controls the use:** the commentary survives entire
  only in Syriac, Payne Smith's English translates that Syriac, and no Greek or
  Syriac witness was opened — so nothing may be argued from Cyril's wording,
  only from his argument. **And his lemma at Luke 14:5 reads "whose son of
  yours, or whose ox", on which his whole rhetorical push about a father's love
  for an endangered child depends; it does not transfer to the missal's
  `ásinus`.** PAT-008.
- **Direct Latin exegesis, checked, three witnesses.**
  - **Ambrose**, *Expositio* VII.195–196: the dropsical man is one "in quo
    fluxus carnis exuberans, animae gravabat officia, spiritus exstinguebat
    ardorem"; then humility taught by forbidding the appetite for the higher
    place, and taught gently, "so that the humanity of persuasion should
    exclude the harshness of coercion"; then hospitality, which is the Lord's
    kind only if spent on the poor, "nam hospitalem remuneraturis esse affectus
    avaritiae est". He passes over the sabbath controversy that occupies
    Cyril's whole sermon. PAT-009, THE-005.
  - **Augustine**, *Quaestiones euangeliorum* II q. 29: the dropsical man is
    compared to the animal fallen into the well "because he laboured under a
    humour", and then to the covetous rich man. **The retrieved wikitext
    carries obvious OCR damage in this very paragraph** (`hydronicum`,
    `concup scit`), so the wording may be quoted only after checking a printed
    edition; the sense is not in doubt. CCSL 44B numbering not checked.
    PAT-009.
  - **Bede**, PL 92 cols. 510D–513A, the fullest continuous Latin exposition:
    the etymology and pathology of dropsy (511A); the ox and the ass as the wise
    and the dull, or the two peoples, all found sunk in the pit of concupiscence
    and drawn out "iustificati gratis per gratiam ipsius" (Rom. 3:24) (511C);
    the marriage feast as the union of Christ and the Church and the first place
    as glorying in one's own merits (512A); "Tunc erit tibi gloria" held in
    **both** an eschatological and a present sense, without choosing (512D);
    and at v. 11 the argument that the conclusion proves the parable must be
    read *typice*, because it is plainly false that everyone who exalts himself
    before men is humbled by men, so the humbling and the exalting are the
    Lord's — "omnis qui se incaute de meritis allevat, humiliabitur a Domino"
    (513A). PAT-010, THE-005, THE-018.
- **The Bede caution, which Bede supplies himself.** In his answering letter to
  Acca, prefixed to the same work, he says he compiled it from Ambrose,
  Augustine, Gregory and Jerome and marked each borrowing with the author's
  initial in the margin. **The retrieved text carries no such marks.** This is
  not speculative: the dropsy-and-miser comparison at 511A stands almost word
  for word in Augustine's *Quaestiones*, and the *Catena* attributes it to
  Augustine. Attribute to Bede only what has been checked, or attribute as
  "Bede, drawing on Augustine". PAT-010.
- **The Catena as a map of leads, and four attributions that stay leads.**
  *Catena aurea in Lucam* cap. 14 lect. 1–2 follow the pericope exactly and
  name eight authorities. Four were verified at their own loci in this join —
  Cyril, Bede, Ambrose, Augustine's *Quaestiones*. **Four were not, and are
  leads only: Theophylact (PG 123), Gregory's *Moralia*, Basil on the order of
  places at table, and the Chrysostom excerpt at lect. 2.** The Catena's Latin
  of the Greek Fathers is a medieval translation, not the Greek. Its value here
  is that its Theophylact and Basil supply the only voices in the checked
  tradition that argue about the parable's weight (one would not call a doctor
  kind who cured gout but refused a toothache; the passion for first places is
  no small disease) and about the danger of a competitive humility (fighting to
  take the last place is itself a breach of order). A later pass wanting either
  must open PG 123 and the Basilian ascetica. PAT-011.
- **Reception of the closing sentence.** Benedict, *Regula* 7 (*De humilitate*)
  opens by quoting Luke 14:11 as the voice of Scripture itself — "Clamat nobis
  Scriptura divina, fratres, dicens: Omnis qui se exaltat humiliabitur et qui se
  humiliat exaltabitur" — draws from it that every self-exaltation is a species
  of pride, and builds on it Jacob's ladder and the twelve degrees. **The
  limit, which is easy to miss:** the sentence stands in Luke twice, at 14:11
  and 18:14, and again at Matt. 23:12, and Benedict names no chapter, so the
  Rule attests the reception of the *sentence* and not demonstrably of this
  pericope. The same caution governs Gregory the Great, *Regula pastoralis*
  III.18, where the NPNF editors refer the sentence to Luke 18:14; Gregory's
  nearest citation of this chapter is III.21 and is of Luke 14:12–14, which the
  Missal does not appoint. PAT-012.
- **Canonical relations, class 1.** The pericope cuts one continuous sabbath
  meal in half, keeping the healing and the seating parable and stopping before
  the instruction to invite the poor and the parable of the great supper; the
  bread motif frames the whole scene at v. 1 and v. 15 and only its first half
  is appointed (SCR-015). The sabbath argument repeats, with the same pair of
  animals, the argument of Luke 13:15, where Matthew's analogue (12:11) argues
  from one sheep; and this is the third and last of Luke's sabbath-healing
  controversies (SCR-016). The closing logion recurs verbatim at Luke 18:14 in
  another Pharisee setting and stands in a family with Matt. 23:12, Luke 1:52,
  Jas. 4:10, 1 Pet. 5:6 and, sapientially, Prov. 25:6–7 and Ecclus. 3:20–21;
  Prov. 25:7's `Ascende huc` is the nearest Old Testament wording to `Amíce,
  ascénde supérius`, in the same situation (SCR-017). `Amice` occurs in exactly
  five verses of the tracked Clementine, and Luke 14:10 and Matt. 22:12 are the
  only two where a host at a wedding feast addresses a guest so — in the second
  the guest is expelled (SCR-018). Phil. 2:8–11 carries both of the readings'
  governing motions in one sentence, the self-humbling that is exalted and the
  bowing of the knee (SCR-029). **The appointed Latin is one clause shorter
  than the Greek-based English at 14:3**: the missal and the Clementine read
  `Si licet sábbato curáre?` where the tracked Revised Version prints "or not";
  no Greek New Testament is tracked, so the manuscript question is not settled
  (SCR-019).
- **The formulary-level commentator, new at iteration 1, and he relays Ambrose.**
  Guéranger, printed pp. 367–368 (artifact PDF pp. 388–389): "she bids them
  listen to St. Ambrose, **whom she has selected as her homilist for this
  Sunday** … he may become like the man mentioned in to-day's Gospel, who had the
  dropsy; and dropsy, says our saintly preacher of Milan, is a morbid exuberance
  of humours, which stupefy the soul, and induce a total extinction of spiritual
  ardour. And yet, even if he were to have such a fall as that, let him not
  forget that the heavenly physician is ever ready to cure him." At printed
  p. 365 he makes the parable's wedding "that of heaven, of which there is a
  prelude given here below, by the union effected in the sacred banquet of holy
  Communion", and at p. 368 he joins humility directly to grace through
  **Ecclus. 3:20–21**: "The greater thou art, the more humble thyself in all
  things, and thou shalt find grace before God; for great is the power of God
  alone, and He is honoured by the humble." **Three things follow and one does
  not.** The Gospel-to-Communion link is his and not the guide's, and it is the
  only cross-element link any formulary-level witness in this join states
  outright; the join of the Gospel's axiom to grace is his, through a sapiential
  verse `scripture-context` independently identifies as the background of Luke
  14:11 (SCR-017) and whose rare `solius` also touches the Communion's psalm
  (SCR-038); and his relay of Ambrose is reception in English of a Father the
  join has at his own locus. **What does not follow is the Breviary claim**: that
  Ambrose is the Church's appointed homilist for this Sunday is Guéranger's
  statement, no lane verified it, and it is recorded as his and nothing more.
  Two bounds on his reading: he interprets the parable through Matt. 22:2, a
  different pericope, and his "divine feast of the nuptials" slides between the
  eucharistic banquet and the eschatological one. THE-039.
- **No Triptych treatment exists.** `hydropic` returns one line in the whole
  prose corpus and it is this leaf's own `verified.md`; `dropsy` returns zero;
  `ascende superius`, `novissimo loco` and `primos accubitus` each return one
  line, likewise this leaf's own record (PRE-019). **Registration, closed at
  iteration 1**: Ambrose's *Expositio* book VII and Cyril's sermons 99–109
  delivery are now both registered on their editions and both re-fetch
  byte-identical; at iteration 0 the registered Ambrose was book X only and the
  registered Cyril was the sermons 110–123 file, which reaches no part of this
  pericope. COV-004.

### 2.7 Offertory — Ps. 39:14–15 with the second half of v. 14 repeated (no. 1598)

Also the Offertory of lent-2-friday, and nowhere else; Ps. 39:10–11 is the
Gradual of s-pii-x-papae-confessoris and the Tract of the commune summorum
pontificum (LIT-008, PRE-008).

- **Direct exegesis, checked, five witnesses, plus a sixth who adjudicates the
  wording.** This is the best-attested of the five chants, and the one where the
  witnesses divide most sharply on what the psalm is doing.
  - **Augustine**, *Enarratio in Ps. 39* §§23–25: at v. 14 the heart that has
    forsaken me is the heart that cannot comprehend itself (Peter at Matt.
    26:35), and the cry is that of "membra sub ferramentis medici clamantia, sed
    sperantia"; at v. 15 the confounding of those who sought the soul is
    fulfilled in the Resurrection, since "illi gavisi sunt cum posuit, confusi
    sunt cum recepit" (John 10:18); and at the verse the Offertory does **not**
    print, `convertantur retrorsum` is read benevolently, that the proud who
    tried to walk in front of their Lord be turned into followers behind him.
    §24: "Christus in passione loquitur." PAT-004, THE-012.
  - **Cassiodorus**, in Ps. XXXIX §§21–24, **whose lemma is the Missal's
    wording**: `Complaceat tibi, Domine, ut eripias me: Domine, **in auxilium
    meum respice**`, with no manuscript variant recorded against the clause in
    Migne's apparatus. His gloss on it is the thesis Aquinas states seven
    centuries later: "ut intelligamus **respectum ipsius nostrum esse
    praesidium**; sicut est illud Evangelii: Respexit Petrum, et flevit amare.
    Aliter enim liberari non possumus, nisi nos Divinitas propitiata respiciat."
    On the imprecation he reads conversion — "Confundantur, dixit, mirabilium
    operatione turbentur. Revereantur autem, resurrectionis gloria corrigantur …
    sicut persecuti sunt, ita et praedestinati conversionis munere liberentur" —
    and distinguishes two ways of seeking a soul, "sive ad honorem, sive ad
    mortem", the added `ut auferant eam` fixing which is meant. At the following
    unprinted verse his lemma is `Avertantur retrorsum`, read *in bonam partem*
    with "Redi retro, Satanas". PAT-021, THE-031.
  - **Aquinas**, *Postilla super Psalmos* in ps. 39 nn. 6–7 (refs. 87201,
    87202): "Respectus Dei est auxilium nostrum"; the two confusions, of
    penitence (Rom. 6:21) and of punishment, both allowed; `convertantur
    retrorsum` taken "in bonum, idest sequantur Christum retro eum"; and, at
    `cor meum dereliquit me`, the distraction of fervour by venial sins, cited
    with **2 Sam. 7:27** — the very verse Augustine uses at the Introit's
    `suávis ac mitis` for the fugitive heart. That convergence is a real textual
    agreement between two checked witnesses at two different appointed elements,
    and is **not** evidence that either had this Mass in view. PAT-014.
  - **Bellarmine**, artifact PDF p. 132 (printed p. 122), his printed vv. 13–14,
    **and he breaks with the other Latins.** He reads the first verse as the
    Passion — "you seem as if you had for some time abandoned me … but now 'look
    down to help me,' that you may at once replenish me in the joy of a glorious
    resurrection" — and calls the imprecation a **prophecy in disguise**: "That
    he now prophesies in the form of an imprecation, a thing usual with the
    prophets … But immediately after, when they heard of his resurrection … 'they
    were confounded and ashamed'". And where Augustine, Cassiodorus and Aquinas
    all read the next verse's `turned backward` as a prayer for conversion,
    **Bellarmine does not**: it is more of the same confusion. His remark about
    "the Jews" is sixteenth-century polemical register reported as his, and
    `guidance/editorial.md` governs any quotation of it. PAT-027, THE-030.
  - **Theodoret**, PG 80 cols. 1159–1160, who supplies a **persona** no other
    witness gives. At v. 13, immediately before the appointed verses and
    governing his reading of them: "Sic igitur in hoc loco Dei Ecclesia, impiorum
    fluctibus concussa, non effertur, tanquam pugnare volens, sed quae accidunt,
    peccatis et delictis tribuit … nec Dei Ecclesia ex hominibus perfectis tota
    constat, sed habet etiam ignavos … Et quoniam unum est corpus, tanquam ex una
    persona et haec et illa proferuntur." **That is a different solution from
    Augustine's *totus Christus* to the same problem.** On the appointed verses
    his gloss is one sentence and it is about intent — "Non enim vulnerare
    volunt, sed sempiternae morti tradere" — and at the unprinted next verse he
    reads **rout, not conversion**: "Verte ipsos in fugam." PAT-032, THE-030.
  - **Jerome**, *Epistula* 106 (*Ad Sunniam et Fretelam*) §23, adjudicating this
    very verse: his correspondents found `σπεῦσον` / *festina* in their Greek,
    and he answers that the Septuagint has `πρόσχες` / *respice* and lets the
    Latin stand. **So the verb the Offertory repeats twice was already contested
    in the fourth century and Jerome ruled for it.** What he settles is the verb
    and **not** the noun: nothing in the letter bears on `auxilium` against
    `adiutorium`, and no sentence about the chant's noun may rest on him. The
    variant he corrects, `festina`, is the reading of Ps. 69:2 — the verse this
    psalm doubles — so the drift between the two was operating on Greek
    manuscripts in his lifetime. **Rights:** the registered artifact is Metlen's
    1937 English whose copyright the record marks unestablished and which permits
    bounded fact and very short quotation only; the Latin lemmata and the Greek
    words are quotable, the translator's English is not, and a guide printing any
    of this should cite an original-language edition. PAT-034.
- **The lemmas, corrected.** Iteration 1 wrote that **none** of the commentators'
  lemmas is the missal's. **That is withdrawn**: Cassiodorus's is, word for word,
  at the clause the chant repeats. The full picture is now five forms —
  Augustine's `Domine, in adjuvandum mihi respice`; the Clementine's and
  Theodoret's Migne Latin's `Domine, ad adjuvandum me respice`; Cassiodorus's and
  the missal's `Domine, in auxilium meum respice`; and Jerome's `Domine, in
  adiutorium meum respice`. **The refrain structure still has no counterpart in
  any commentary checked**, and no witness is expounding a chant. One further
  incidental, recorded and not built on: in Cassiodorus's psalter the clause at
  Ps. 70:12 reads `in adiutorium meum respice` while Ps. 39:14 reads `in auxilium
  meum respice`, which is **the reverse of the tracked Clementine** — so the
  verbatim relation between this Offertory and Ps. 70:12 that holds in the
  Clementine does not hold in his text. PAT-021, PAT-023.
- **A tension the formulary raises and all five witnesses refuse to read as a
  curse.** The Mass that teaches humility and grace sings `confundántur et
  revereántur` at the moment of the offering. **None of the five takes the Latin
  subjunctives as wishing the enemies' destruction** — but they relieve it four
  different ways: Augustine and Bellarmine as prophecy already fulfilled at the
  Resurrection, Cassiodorus as a prayer for the persecutors' conversion,
  Theodoret as a petition that the historical enemies be routed and fail of what
  they want, and Aquinas by allowing both the penitential and the punitive
  confusion. **The gentlest reading is a Latin tradition and not the tradition**,
  and a guide must not quote Cassiodorus's conversion reading as the received
  one. §7.12, THE-030.
- **A sixth reading, from the commentator on this formulary, and the only one
  that keeps the enemies as enemies.** Guéranger, printed p. 370 (artifact PDF
  p. 391), above this Offertory: "The greater the conquests made by the Church,
  the greater are the efforts of hell to destroy the souls of her dear children.
  This fearful danger calls for her fervent prayers; and our Offertory-anthem is
  one of these." THE-040.
- **Canonical relations, class 1.** The chant's reading is verbatim Ps. 70:12,
  a verse of this Mass's own Communion psalm, with the subject differing
  (SCR-020). The dropped `simul` is precisely the reading of the Ps. 69:2–6
  doublet at Ps. 69:3 — but the Offertory keeps `ut auferant eam`, which Ps.
  69:3 has not, and the two psalms differ in the verb at the following clause
  (`convertantur` against `Avertantur`), so the chant is not the Ps. 69 form and
  the agreement is partial (SCR-021). The psalm is that of `Ecce venio … ut
  facerem voluntatem tuam` (vv. 7–9), quoted at Heb. 10:5–7 of Christ entering
  the world; two limits travel with it — those verses lie outside the appointed
  excerpt, and the Latin of the quotation differs from the Latin of the psalm at
  the decisive clause (`corpus autem aptasti mihi` against `aures autem perfecisti
  mihi`) (SCR-022). Both of the chant's petitionary verbs recur in the psalms of
  two other appointed elements, and Ps. 70:24 carries both together — **but of
  those verses only Ps. 39:15 is appointed** (SCR-040).
- **A cross-proper dossier the collection already holds, and its constraint.**
  Ps. 39:14–18 is the doublet of Ps. 69:2–6, and Ps. 69:2–4 is the **Introit of
  claude leaf 52**, whose published record names Bellarmine and Cassiodorus as the
  two witnesses who state the doublet and prints, in its reader-facing body, the
  bounded negative that **Augustine nowhere notes it**, verified against the full
  Latin of both *Enarrationes*. So a guide here inherits both the claim and its
  negative, and **any statement that Augustine links the two psalms would
  contradict a published leaf**. What is established nowhere in the collection is
  whether Bellarmine's or Cassiodorus's remark is made at Ps. 39 as well as at
  Ps. 69. PRE-037.
- **No cultural afterlife, and the reason is a competitor**: `in auxílium meum
  réspice` is close enough to Ps. 69:2's `Deus in adiutorium meum intende`, the
  versicle that opens every Hour, that any candidate would be a use of that
  verse (CUL-008).

### 2.8 Communion — Ps. 70:16–17 et 18 (no. 1600)

Also the Communion of lent-4-thursday and of a votive Mass *pro quacumque
necessitate* with `T. P. Alleluia` added (LIT-008, PRE-008, PRE-017).

- **Direct exegesis, checked, four witnesses, plus Jerome on the wording.**
  Augustine's remains the strongest single cross-element result of the join; the
  three added at iteration 1 make the row's two hinges **disputed**, and both
  disputes must reach the reader.
  - **Augustine**, *Enarratio in Ps. 70*, sermo II §§1, 2, 4 — which are exactly
    vv. 16, 17 and 18, the antiphon's own extent.
    - v. 16: "Domine, memorabor iustitiae tuae solius. O solius! Quid addidit,
      solius? … Justitia tua sola me liberat; mea sola non sunt nisi peccata"
      (1 Cor. 4:7); "Gratia gratis data est: nam nisi gratis esset, gratia non
      esset … nihil tuum praecessit, ut acciperes."
    - v. 17: "Quid me docuisti? Quia tuae solius iustitiae memorari debeo …
      Debebatur poena; reddita est gratia … docuisti me nihil in me
      praecessisse."
    - v. 18: he notes the Greek pair *presbytes* / *geron* behind the Latin
      doublet, then gives two senses — individually, "usque ad ultimum meum, nisi
      mecum fueris, non erit aliquid meriti mei: gratia tua semper perseveret
      mecum"; ecclesially, "vox est enim Ecclesiae", the Church whose youth was
      the age of the apostles enduring to the end against those who predicted
      Christianity would last a season.
    - Sermo II §3 cites **Ps. 85:11** — the psalm of this Mass's own Introit —
      for the point that grace must lead as well as start.
    PAT-005, THE-003, THE-006, THE-007.
  - **Cassiodorus**, in Ps. LXX §§21–23 with the divisio at §4 and the conclusio
    at §33, and **his two results pull opposite ways.** On the psalm as a whole
    he corroborates Augustine twice over and in Augustine's own words: the
    speaker preaches "Christi Domini eximiam charitatem, **quae nullis meritis
    praecedentibus gratis semper impenditur**", and "Cum totus hic psalmus
    gratiam Domini, **quae gratis datur**, summa intentione commendet". On the
    antiphon's first clause he **disagrees**: `solius` does not exclude the
    singer's own righteousness but refers the remembering to the Judgment —
    "illo scilicet tempore cum agnos sequestrat ab haedis … Tunc enim vere memor
    erit iustitiae solius Domini, quoniam eam et mirabilem, et singularem esse
    cognoscit." On `a iuventute mea` youth is the age at which a man first comes
    to grace; on `usque in senectam et senium` he makes Augustine's philological
    observation independently and then periodises the **Church's** ages
    differently: her youth the Crucifixion and the martyrs, her `senecta` the
    present age near the end, her `senium` the last declining time "quando et
    saevus ille tyrannus adveniet". PAT-022, THE-020, THE-021, THE-022.
  - **Bellarmine**, artifact PDF pp. 222–223 (printed 212–213), **the
    literal-historical voice.** On `solius` he takes the exclusion as one of
    every other support — "I will lose sight completely of human counsel, of my
    own strength, or of my friends … 'thy justice alone,' by virtue of which you
    keep your promises" — standing between the two Fathers and taking both
    halves. On `a iuventute mea` he **declines allegory altogether**: "it was in
    consequence, that I, an unarmed youth, fought with a bear and a lion, and
    conquered both them and the giant Goliath." And on `usque in senectam` he
    makes the petition run to the completion of the psalter, "until I shall have
    finished the book of Psalms, through which I will shew forth thy arm to all
    posterity" — a striking reading for a Communion antiphon, but the clause
    carrying it is **outside** the appointed text. PAT-028, THE-021, THE-022.
  - **Theodoret**, PG 80 cols. 1423–1426, whose periodisation is unlike anything
    the Latins give: **youth is the age of Moses and the giving of the Law, and
    old age is the Law's end.** "Atque hinc manifestum est, eum magni Mosis
    tempus juventutem vocare. Per illum enim lex data fuit"; "Prophetice David
    futura praedicit, et senectutem vocat legis finem. Hoc autem post Domini
    Christi adventum contigit" — with **Heb. 8:13** quoted in support,
    "quod autem antiquatur et senescit, prope interitum est". On `memorabor
    iustitiae tuae` he anchors the clause in the preceding verse's justice, the
    just verdict by which God judged between him and his enemies. And he
    cross-refers `quoniam non cognovi litteraturam` to **Ps. 39:5–6**, a verse of
    this Mass's own Offertory psalm, as Migne's own footnote records. PAT-033,
    THE-021, THE-022.
  - **Jerome**, *Epistula* 106 §43, on two clauses of these very verses: against
    Greek copies reading `Deus meus` he holds that `meus` is superfluous in
    `Deus, docuisti me a iuventute mea`; and against copies reading `mirabilia
    tua` at `donec annuntiem brachium tuum` he holds that `mirabilia tua` has been
    carried up from the preceding verse and that `brachium` is right. **He
    adjudicates the exact wording the antiphon sings**, which makes him usable
    here under the documented-reception class provided the guide says what kind of
    witness he is. Same rights bound as at §2.7. PAT-034.
- **The row's first hinge is now disputed: what `solíus` excludes.** Augustine
  takes it to exclude any righteousness of the singer's own; Bellarmine to
  exclude human counsel and his own strength, which runs the same direction in a
  different key; **Cassiodorus** refers it to the Judgment, when the Lord's
  justice alone will be remembered as marvellous; **Theodoret** makes it God's
  just dealing with the speaker. **The grace-alone reading of the Communion is
  the Latin anti-Pelagian tradition's reading of it and not the undivided
  tradition's**, and an author who wants the anti-merit sense must attribute it
  to Augustine, may add Bellarmine, and may not generalise. §10.1's resolution
  stands because Augustine is commenting on the exact words the antiphon sings;
  what falls is the right to call it the tradition's. THE-021.
- **The row's second hinge is disputed the same way: what the three ages are.**
  Augustine's youth is the beginning of faith and, ecclesially, the age of the
  apostles and martyrs; Cassiodorus's is the coming to grace, with `senecta` the
  present age and `senium` the time of Antichrist; Bellarmine's is David's own
  boyhood; Theodoret's is the age of Moses, with old age the obsolescence of the
  Law. **All four read the span as a span of God's teaching and not of the
  psalmist's achievement**, which is what makes it answer the Collect (§10.1);
  **none reads it as a lifetime in the ordinary sense**, and an ecclesial-ages
  reading may not be presented as what the tradition says. THE-022.
- **A fifth reading, and the most uncomfortable, from the commentator on this
  formulary.** Guéranger, printed pp. 370–371 (artifact PDF pp. 391–392), above
  this antiphon: "Now that the Church is filled, by the holy Communion just
  received, with the true substantial Wisdom of the Father, she **promises God,
  as her thank-offering, that she will keep His justice, which is His law**, and
  that she will labour to make His divine teaching produce its fruits." That is
  close to the opposite of Augustine's "Nullam meam agnosco", and **the guide
  must not quote both as if they agreed.** He is describing what the Church is
  doing at this moment of this Mass rather than construing the psalm, and should
  be presented as that. THE-041.
- **One philological lead, flagged and expressly not used.** Theodoret's Greek
  reads `τῆς δικαιοσύνης σου μόνου`, where the genitive `μόνου` may attach to
  `σου` — "thy justice, of thee alone" — rather than to `δικαιοσύνης` as the
  Latin `iustitiae tuae solius` takes it. **Augustine's whole reading of the
  clause rests on `solius`**, so if the construal differs in Greek that matters;
  the lane that found it states it is not competent to settle the point from a
  facsimile and flags it for someone who reads the Greek properly. PAT-033.
- **Two bounds on quoting Augustine.** His most quotable formula on this
  doctrine, "sua dona coronabit, non merita tua", stands in sermo II §5, on
  v. 19, **one verse past where the antiphon stops**; quoting it as commentary
  on the sung text overstates the fit. And the NPNF English runs a single
  section series (18–22) across both discourses while the Migne Latin restarts
  at 1 for Sermo II, so a citation must give the verse.
- **One link inside a witness, recorded as such.** Cassiodorus's Judgment gloss
  here uses the same sheep-and-goats formula he uses at Ps. 101:17 for the
  Gradual's `videbitur in maiestate sua`, so **in this one commentator the
  Gradual's second half and the Communion's first clause name the same event**.
  That is a link inside a witness and not a link the Mass's compiler is shown to
  have made. PAT-022.
- **Canonical relations, class 1.** The antiphon is the only appointed
  scriptural element with **no verbal departure from the Clementine**; it is made
  entirely by where it starts and stops, and it restates the psalm's own earlier
  petitions at vv. 5 and 9 (SCR-023). Its rare genitive `solíus` occurs in only
  four verses of the tracked Clementine, and one of them, **Ecclus. 3:21**
  ("magna potentia Dei solius, et ab humilibus honoratur"), stands inside the
  sapiential humility passage that lies behind the appointed Gospel's conclusion
  — and is the verse Guéranger reaches for at §2.6. **Only `solíus` is inside
  appointed text**: `potentias Domini` is the unsung first half of v. 16, so the
  two-word pairing holds between the psalm verse and Ecclus. 3:21 and not between
  the antiphon and Ecclus. 3:21 (SCR-038). `sénium` occurs nowhere else in the
  tracked Bible (SCR-036).
- **No cultural afterlife.** The distinctive renderings were run through the
  Authorized Version and, at iteration 1, a **ninety-volume** Project Gutenberg
  corpus and five further *Chronicling America* phrase queries; the only
  recurring hits were "gray hairs" / "grey hairs", every one an ageing character
  described, and one 1808 seaman's petition where the words fall in that order by
  accident. "I will be mindful of thy justice" returns zero newspaper pages
  (CUL-008).

### 2.9 Secret and Postcommunion (nos. 1599, 1601)

- **No patristic or saintly reception was found for either, and nothing was
  retained.** The bound is exact and is a search, not a memory: every Latin
  corpus retrieved by `patristic-reception` was searched for `sacrificii
  praesentis`, `mereamur esse participes`, `caelestibus sacramentis` with its
  `coelestibus` spelling, and `Munda nos` — Augustine's *Enarrationes* on Ps.
  31–40, 61–70, 81–90, 91–100 and 101–110, his *Quaestiones euangeliorum*,
  Ambrose's *Expositio* VII–IX, Bede's *In Lucam* entire, Benedict's *Regula*
  entire, Aquinas's *Catena in Lucam* 14–18, *Super Ephesios* entire and *Super
  Psalmos* 31–40, and the Tauchnitz Trent text. **No hit for any of them.**
  PAT-016.
- **But the negative is no longer total, and that is this iteration's change at
  this row.** Guéranger, the formulary-level commentator §0.8 settles, reads
  **both** orations. Above the Secret, at printed p. 370 (artifact PDF p. 391):
  "the Sacrifice, at which we are present, and which is to be consummated, in a
  few moments, by the words of Consecration, is the most direct and efficacious
  of all the immediate preparations that we can make for the Communion of the
  Body and Blood, **which that Sacrifice produces on the altar**". Above the
  Postcommunion, at printed p. 371: "let us pray, with the Church, that we may be
  renewed by the purity, which these heavenly mysteries bring to us, who are well
  prepared for the gift: the effect of such a gift tells upon our bodies, **both
  in this and in the next life**." **Two consequences.** He supplies a direction
  of dependence — sacrifice first, then communion, the first the preparation for
  the second — which narrows the tension §7.9 records, though it does not close
  it: he is one witness, devotional, writing continuous prose around texts he
  prints, and it is offered as *his* answer and not as the answer. And his second
  sentence construes `præsens páriter et futúrum` **temporally**, which at
  iteration 1 rested only on the free Cummiskey English `verified.md` warns
  against; it now rests on a registered public-domain witness as well. THE-040.
- **Two routes deliberately not taken, and open**: the medieval *expositores
  missae* (Amalarius, Honorius Augustodunensis, Sicardus, Durandus), where
  reception of an oration would show up if anywhere, of which the library holds
  only Honorius — and at iteration 1 `liturgical-history` reached PL 105 far
  enough to establish that its Amalarian matter is the *Regula canonicorum* and
  the four books *De ecclesiasticis officiis*, whose treatment of the September
  fast is generic and names no Sunday of this series, so **nothing was taken from
  it** and the route stands open (PAT-016, LIT-016).
- **What the join does supply for these two elements**: their sacramentary
  provenance (§4.1), now read on Gerbert's own pages as well as in Wilson's
  conspectus and carrying Gerbert's per-oration sigla — the Secret and the
  Postcommunion marked Gelasian, Eligian and Gregorian together, the Collect
  Gregorian only (LIT-017); the closure of the 1862 `et` before `rénova` recorded
  in `verified.md`; §7.9's unresolved question, now narrowed by Guéranger; and
  the `rénova` / `auxílium` links to the Alleluia and the Offertory (THE-011,
  THE-012, THE-026). **What it does not supply is patristic or saintly
  reception**, and §11 position 5 records that as the coverage position.

---

## 3. Corpora, languages and instruments searched

Every retrieval below is receipted under
`build/tpt-runs/e4aebcbd941b6b1a/artifacts/research-NNNN-lane-NN-<lane>/` with
its URL, byte size, SHA-256 and retrieval date of 2026-09-05 — `research-0000`
for the first sweep and `research-0001` for the second, which is the one
`CON-REC-002` caused.

### 3.1 Scriptural corpora

Tracked in the repository and read as data, not from memory: the Clementine
Vulgate (`edition.catholic-church.vulgata-clementina.ebible-latvuc`), the
Douay–Rheims Challoner Gutenberg text, the King James Version (eBible engKJV)
and the Revised Version 1895, with the tracked psalm concordance
`…challoner-gutenberg-1581/artifacts/psalm-numbering-ee3c7757/psalm-numbering.tsv`
read through `scripts/_psalms.py`.

**Languages: Latin and English only.** No Greek New Testament, no Septuagint,
and no Old Latin, Roman, Ambrosian or Mozarabic psalter is tracked under
`src/sources/bibles/` — the tracked editions are clementine-vulgate,
douay-rheims, douay-rheims-american-1899, catholic-public-domain-version,
king-james-version, revised-version-1895 and world-english-bible-catholic. Every
scriptural observation in this brief is therefore at the level of the Latin and
its tracked English witnesses.

### 3.2 Reception corpora

**Opened and read at their own loci.** Augustine (*Enarrationes in Psalmos* 39,
70, 85, 97, 101; *Quaestiones euangeliorum* II; *Epistula* 55; *In Iohannis
euangelium tractatus* 118; *Enchiridion*; *De gratia et libero arbitrio*;
*Sermo* 165); **Cassiodorus** (*Expositio psalmorum*, in Pss. XXXIX, LXX,
LXXXV, XCVII, CI, each retrieved whole in both the suppressed-apparatus and the
apparatus delivery states); **Theodoret of Cyrus** (*Interpretatio in Psalmos*,
PG 80, at all five appointed psalms); **Robert Bellarmine** (*Explanatio in
Psalmos* in the 1866 English, at all five); **Jerome** (*Epistula* 106, §§23, 43,
56, 61, 63); Ambrose (*Expositio in Lucam* VII–IX); Bede (*In Lucam*, whole);
John Chrysostom (*Homilies on Ephesians* 6–8); Cyril of Alexandria (*Comm. on
Luke*, Sermons 99–109, Payne Smith's English of the Syriac); Benedict
(*Regula*); Gregory the Great (*Regula pastoralis* III); Thomas Aquinas
(*Catena in Lucam* 14–18, *Super Ephesios*, *Super Psalmos* 31–40); Council of
Trent (Session VI); **Guéranger** (*The Liturgical Year* vol. XI, printed
pp. 356–371, read on a rendered page image at printed p. 356 and on the
volume's own text layer through the chapter).

**Still named as not opened, after two iterations.** Chrysostom's *Expositiones
in psalmos*; Jerome's *Tractatus in psalmos*, his *Commentarioli* and his
*Commentarii in epistulam ad Ephesios*; Hilary, *Tractatus super psalmos*;
Arnobius the Younger; Prosper; Eusebius on the Psalms; the Greek psalm catenae;
the **Latin original** of Bellarmine's *Explanatio in Psalmos*, of which only the
abridged 1866 English was read; Ambrosiaster and Marius Victorinus on Ephesians;
Gregory of Nyssa on the dimensions of the Cross; Theophylact of Ohrid,
*Enarratio in Lucam*; the Basilian ascetica; Gregory the Great, *Moralia in Iob*;
Bernard, *De gradibus humilitatis et superbiae*; Francis de Sales,
*Introduction* III; the medieval *expositores missae*; the Second Council of
Orange. PAT-017.

**What changed, stated as the lane states it.** The five appointed psalm
passages now each carry **at least four direct commentators opened at their own
works and loci** — Augustine, Cassiodorus, Bellarmine and Theodoret at all five,
Aquinas additionally at the Offertory, and Jerome's textual adjudication at the
Offertory and the Communion — so no chant text rests on one Latin Father and
**the Greek psalm tradition has been sampled at every one of them**. That is
what the profile's "more than one where they materially differ or develop the
reading" asks, and they do materially differ at every one (§7.10 to §7.13).
**Three things this deliberately does not say.** It does not say the psalm
reception is complete. It does not say that Chrysostom, Jerome or Hilary have
nothing at these psalms — **nobody has looked**, no extent record for those works
is tracked, and guessing at their extents from memory is exactly what the
evidence discipline forbids. And it does not treat the 1866 Bellarmine as a
substitute for his Latin: the translator abridged it, and every Bellarmine
finding here is bounded to English. **The largest remaining route** is that Latin
*Explanatio*, which would put four readings on an original-language footing at
once; after it, a Greek catena is the cheapest way to reach a second Greek voice,
Theodoret being currently the only one. PAT-017.

**Routes that failed or bounded out, recorded so they are not retried blindly.**
augustinus.it serves the Latin *Enarrationes* only through frames whose target
filenames one lane could not resolve, and a second lane reached the same texts by
guessing the numbering, which is why §0.1 lists two Latin routes;
documentacatholicaomnia.eu could not be fetched at all, its TLS certificate not
verifying, and at iteration 1 it returned 404 for its *Acta Apostolicae Sedis*
vol. 47 file; the Corpus Corporum browser at mlat.uzh.ch is a JavaScript
application rather than a fetchable document tree; la.wikisource carries the
*Catena aurea* only for Matthew, so the *Catena in Lucam* came from Corpus
Thomisticum. **And the one that matters most, because the iteration-1 brief
pointed a later sweep straight into it:** la.wikisource's *Expositio in
Psalterium* transcribes **Psalms 1–30 only** while printing a table of contents
naming all 150, so `/39`, `/70`, `/85`, `/97` and `/101` return 404 and the route
reaches none of this Mass's psalms. The route that does reach all five is
monumenta.ch, whose addressing rule and silent-failure mode are at §0.7 and
§14.2. COV-016, THE-036, PRE-034.

**Registered, byte-verified and unread by choice**: the Adriaen CCSL 98
Cassiodorus, `rights_status = "restricted"` and covering Psalms 71–150 only, from
which nothing may be redistributed. COV-016.

### 3.3 Liturgical-history corpora

Read: Schuster, *The Sacramentary* vol. III (IA optical layer of the item whose
PDF is registered, sha256 `4d8c8988…`); Wilson, *The Gregorian Sacramentary
under Charles the Great*, HBS XLIX 1915 (sha256 `3613cce6…`); Wilson, *The
Gelasian Sacramentary*, Clarendon 1894, including the Appendix collating
Rheinau, St Gallen, Gerbert, Pamelius and Menard (sha256 `039123ca…`, with the
second registered layer `25586b16…`); **Gerbert, *Monumenta veteris liturgiae
Alemannicae* Pars I (St Blasien, 1777), read on the page images of two
independently produced Internet Archive scans at printed pp. 146, 178, 180 and
184, with two further scans retrieved and searched that do not reach those
pages**; Feltoe, *Sacramentarium Leonianum* 1896, searched whole (sha256
`afb6a8bc…`); Dickinson, *Missale ad usum … Sarum* (sha256 `1dccd4d1…`); the
*Liber Comitis* in Migne PL 30 (two independent digitisations plus seven page
images of leaves n261–n267 and the per-word coordinate file); **the Holy See's
own optical transcription of *Acta Apostolicae Sedis* 47 (1955) at vatican.va,
read at printed pp. 218–224 and at 200 dpi for Tit. V a) n. 1**; the Benziger
*editio iuxta typicam* 1962 text layer (sha256 `2a2da44d…`, finding aid only,
controls no wording); the tracked Pustet Ratisbon 1862 optical text; **the 1920
Vatican typical edition and the 1947 Benziger optical layers, both opened at this
formulary**; **Brightman, *The English Rite* vol. II, printed pp. 520–521, and
Blunt, *The Annotated Book of Common Prayer* (1866)**; Guéranger, *The Liturgical
Year* vols. X, XI, XIII, XIV, XV; Fortescue, *The Mass* 1922, searched whole; the
Catholic Encyclopedia article "Preface"; gregorien.info's index of Hesbert's
*Antiphonale Missarum Sextuplex* (day pages 816, 817, 819, 829, five chant
records, six per-manuscript indexes, the manuscript index); Cantus Index and
GregoBase for the modern side only; and **Migne PL 105, retrieved and found to
carry Amalarius's *Regula canonicorum* and *De ecclesiasticis officiis* only,
whose September-fast material names no Sunday of this series, so nothing was
taken from it**.

Twelve full-text missal payloads present in the working tree were searched by
`precedent-search`: Pustet 1862, Vatican typica 1604, Venice 1570, three
Ambrosian editions (Milan de Sirturis 1712, Sirturi 1640, Pachel 1499),
three Mozarabic (Monaldini 1755 in two scans, PL 85), Cummiskey 1843, Lasance
1945 and Keating 1806, with the calibration counts recorded at PRE-001 and
reproduced at iteration 1 within one hit of iteration 0. **The Ambrosian 1499
layer is unusable** (0 hits for `dominus`). The Sarum missal is now a registered
work, edition and artifact but **carries no text payload in the tree**, so it is
a thirteenth registered witness and not a thirteenth searchable payload.

**Four prayer-book digitisations were retrieved and failed** at iteration 1, on
top of the four that failed at iteration 0: no printing of the Book of Common
Prayer itself was ever collated, and what LIT-020 reads is two scholarly
synopses of it.

### 3.4 Precedent corpus

`precedent-search` swept four bodies of in-repository material, re-measured at
iteration 1 on the same commit: **2,902 `.tex` and `.md` files** under
`src/claude`, `src/gpt` and `src/common` through an accent-stripped case-folded
index of **332,704 lines**, of which **190** files are a document's `main.tex`;
the tracked registry `src/sources/calendars/roman-1962/propers.yaml` parsed as
data; the twelve missal payloads above; and the published `research/scope.md` and
`sections/*.tex` of the two provider liturgy trees.

**Three figures this brief carried at iteration 1 are corrected here.**

1. The prose-corpus figures move each time the leaf under work is authored: claude
   leaf 54's own statement counts 182 documents and 2,865 files; iteration 0 of
   this lane counted 2,885 files and 189 `main.tex`; **iteration 1 counts 2,902
   and 190, the whole increase being this leaf**. The iteration-1 brief printed
   the iteration-0 figures; these are the current ones and **no figure from any
   of the three sets may be quoted as though it were another's**.
2. The registry figures iteration 0 gave — "444 Mass formularies carrying 3,270
   proper elements" — **are not reproducible** by the iteration-1 parse and must
   not be quoted. The reproducible parse is **491 formularies across five
   sections** (seasonal 128, common 30, marian 18, christological 8, sanctoral
   307), of which **430 carry at least one proper element**, **3,259 proper
   elements** in total, **1,034 of them carrying Latin body text**. Only the last
   figure reproduces from iteration 0, and it is the one every lexical count in
   §9 rests on.
3. The precedent field is **wider than iteration 0 named it**. Enumerated by
   `main.tex`, the two provider liturgy trees hold **62 documents**, not the 21
   proper leaves iteration 0 listed: claude has 7 1962 proper leaves (48, 49, 51,
   52, 53, 54, 56), 2 postconciliar proper leaves, an ordinary, two reference
   works, a comparative and a postconciliar ordinary; gpt has 15 1962 proper
   leaves and a ritual leaf, 11 postconciliar proper leaves, an ordinary, 13
   reference works, a comparative and a postconciliar ordinary. **The thirteen
   postconciliar leaves were inside the index at both iterations and so inside
   every negative**, but iteration 0's statement of the corpus did not name them,
   and two of them bear on this Mass (PRE-035, §7.15).

**Not reached, and every "not located" in §9 is bounded by it**: any printed
chant repertory; any pre-Tridentine Latin commentary tradition; the sacramentary
editions themselves, which are §4's ground and were read there and not here; any
page image of any of the twelve payloads; and the Sarum text. PRE-001.

### 3.5 Cultural-afterlife corpora

The Authorized Version in full (Project Gutenberg eBook 10) and the registered
Douay–Rheims held in this repository; **ninety Project Gutenberg plain-text
volumes** at iteration 1, against thirty-five at iteration 0, the eBook numbers
enumerated in CUL-008's evidence and the ninety including the thirty-five; the
Library of Congress *Chronicling America* newspaper collection by phrase query
and by page-level OCR retrieval, with five further phrase queries at iteration 1;
Internet Archive full texts of Brewer's *Dictionary of Phrase and Fable*,
Hotten's *Slang Dictionary*, **Grose's *Classical Dictionary of the Vulgar
Tongue***, Webster's Unabridged 1913, *Life and Writings of Frank Forester*
**vols. 1 and 2**, Clifton Johnson's *Highways and Byways of the South*,
*Macmillan's Magazine* vol. IX, Rossetti's *Poetical Works* 1904,
**Chesterton's *Orthodoxy* (1909 printing), Burgess's *The Bible in Shakspeare*
(1903), Schmidt's *Shakespeare-Lexicon* vol. 2, Tyler's 1890 *Sonnets*, and the
1910 Zimmern translation of *Human, All-Too-Human***; **the Folger Shakespeare
Library's plain texts of *Love's Labour's Lost* and the *Sonnets*, and Open
Source Shakespeare's line-numbered view**; the Ohio State University Libraries
Knowledge Bank scan of *The Victorian Newsletter* no. 22; and general web search.

**Languages: English and Latin, with German and Spanish opened once each**, and
only because a named candidate led there — Nietzsche's *Menschliches,
Allzumenschliches* (PG 7207) with four further Nietzsche volumes searched to
place the aphorism, and Cervantes's *Quijote* in Spanish (PG 2000) beside
Ormsby's English (PG 996). **A psalm verse with a French, Italian or unprompted
German or Spanish afterlife would still not have been found.** **Hosts that could
not be opened:** Collins English Dictionary (403) and the OED (paywall); and no
public-domain German Bible could be obtained from this host, so the statement
about Luther's `soll` at CUL-011 is a lead and not a checked reading.
**Musical settings were deliberately not counted**: the gallery rule excludes a
bare setting unless it redirects the wording, and none met with does — a real
exclusion here, since all five chants of this Mass have substantial chant and
polyphonic afterlives.

### 3.6 Source-library enumeration

`source-citation-coverage` enumerated the library against this Mass by directory
listing on 2026-09-05 and then **re-fetched every bound remote artifact and
re-hashed every tracked one**: 103 bound source ids, of which 96 are artifacts
and 7 passages, every one resolving; `python3 tools/source-library validate`
passing over the whole repository with these bindings included; **34 tracked
artifacts all hashing to their registered values**; and **53 of 59 bound remote
artifacts re-fetching byte-identical**, 188 MB in all, including the 82.8 MB CMAA
facsimile of the 1962 typical edition, the 24.1 MB Benziger DjVu, the Wilson,
Feltoe, Dickinson and Schuster layers, both Guéranger artifacts, the Lapide
layer, and every Augustine artifact registered for the five psalms.

**The six that drifted are all newadvent.org and none disturbs a claim**: the
Gregory *Regula pastoralis* page and five Catholic Encyclopedia articles, each
short by 53 or 359 bytes. The Gregory drift was characterised exactly by diffing
against the retained registered payload — **the whole difference is one
stylesheet URL**, `A.screen6.css.pagespeed.cf.RtKUhVCPOJ.css` against
`../utility/screen6.css`, and the markup-stripped text is character-for-character
identical at 244,457 characters. The five encyclopedia pages carry no `pagespeed`
string at all, which places their uniform deficit in the same class; that
identification is an inference, their registered bytes not being retained
anywhere reachable. **The standing caution is about registration policy and not
about this guide**: a newadvent.org artifact's SHA-256 is not reproducible on
demand, because the host serves the same document with and without
PageSpeed-rewritten asset URLs, so a later staleness check will raise a false
alarm there and the same page registered twice on one day can carry two digests.
COV-019.

Its other results are carried at §6.1 (provenance notes), §6.3 (the extent
control) and §14.2 (the two silent-failure classes).

---

## 4. The formulary's three strands, and its rubrical frame

### 4.1 Where the three orations stand in the older books

| Witness | Heading | What stands there |
| --- | --- | --- |
| Sacramentarium Veronense (Feltoe 1896), 21,093 lines searched whole | — | **None of the three.** The one near miss, `tua nos semper gratia praeveniens laetificatur`, is a different prayer. COV-003 |
| Gelasianum Vetus (Wilson 1894), Bk III sect. XII no. 693, printed p. 231 | `ITEM ALIA MISSA` | **Secret and Postcommunion, word for word**, under the collects `Fac nos, Domine, quaesumus, prompta voluntate subiectos` and `Fac nos, Domine, quaesumus, tuis obedire mandatis`. `Tua nos … gratia semper et praeveniat et sequatur` is **not in the Old Gelasian's three books at all** — a whole-volume search for `gratia semper`, `praeveniat et`, `et sequatur` and `bonis operibus` returns it only in the Appendix. LIT-005, COV-003 |
| The immediately preceding Missa, no. 692, printed p. 230 | — | The 1962 **Fifteenth** Sunday's whole oration set. LIT-005 |
| Frankish Gelasian, **read on Gerbert's own page images**, printed p. 184 | `Dominica XX. Post Pentecosten. Gelas.` | **All three together**, plus a proper Preface `VD. … Precantes, ut Ihs Xps Filius tuus Dns noster sua nos gratia protegat`, and — the row's point — **Gerbert's own per-oration sigla**: `Tua nos` marked `gg.` (Gregorian as Muratori has it) alone, the Secret marked `g. El. gg.` and the Postcommunion `g. El. gg.` (Gelasian, Eligian and Gregorian together). LIT-017 |
| The same page, read a second time on an independently produced scan and a third time on both optical layers | — | Word for word the same as far as the first scan's clipped outer margin allows. LIT-017 |
| Gerbert, printed p. 180, running head `DOM. XIX. POST PENT.` | `Dominica vacat.` | A Mass with its own items, **printed as a Mass and not merely as a heading in a collation**, with Gerbert's footnote: "In Elig. inscribitur hebdomada XIX. post Pentecosten. Deficit vero omnino tam apud MURATORIUM, quam in Missali Romano." LIT-018 |
| Wilson's Appendix, printed p. 358, the same two entries | `Gerb. Hebd. xx post Pentecosten` / `Gerb. Dominica Vacat.` | The conspectus this brief rested on at iteration 1, now superseded by the book itself; the two agree. LIT-006, COV-003 |
| Gregorianum Hadrianum (Wilson 1915), sect. **XXXV**, printed p. 174 | `DOMINICA .XVII. POST PENTECOSTEN` | **All three, in this order**, as Collect, `Super oblata`, `Ad complendum`. Sect. XXXIIII carries the 1962 Fifteenth's collect and sect. XXXIII the 1962 Fourteenth's. LIT-003, COV-003 |
| Missale Romanum, Pustet Ratisbon 1862, printed pp. 339–341 | `Dominica XVI. post Pentecosten.` | The three, plus `Secunda Oratio. A cunctis nos.` / `Tertia ad libitum.` and the corresponding `Alia Secreta` and `Alia Postcommunio`. `verified.md`; LIT-009 |
| Missale Romanum, Vatican typica 1604 | — | The formulary present in the OCR window with `alia Secreta` and `tertia ad libitum`; an independent second witness at OCR state only. PRE-007 |

**The offset is not one number.** It is +1 in the Gregorian, and in the Frankish
Gelasian +2 at the Fifteenth Sunday and **+4 here**, the two extra places being
precisely the September Ember Sunday and the vacant Sunday (LIT-006). Wilson's
own footnote to no. 693 records that Pamelius joins the second collect of that
twentieth-Sunday Mass — which the Appendix shows to be `Tua nos` — to the same
Secret and Postcommunion at his **seventeenth** Sunday, exactly the number
Wilson's Gregorian gives it, so the Gregorian tradition is consistent across two
independent editors while the Frankish Gelasian is two Sundays further out.

**Evidentiary consequence, class 2:** the trio as the 1962 book has it is a
composition of the Gregorian tradition and not an inheritance entire from the
Gelasian.

**The arithmetic is now stated by the editor himself, in four of his own
footnotes.** Gerbert at printed p. 184 n. 1: "Cum duae praecedentes Dominicae hic
pro XVIII. & XIX. cum Elig. numerentur, desint autem in Missali Romano, & apud
MURATORIUM, nova variatio in numero Dominicarum oritur, unde **quae est hic Dom.
XX. in Missali est XVI. & apud MURAT. XVII.** & sic deinceps." At p. 146 n. 3 he
records the earlier, smaller offset — "quae enim hic est secunda, tertia, in
missali Rom. & apud MURAT. est prima, secunda; quae vero hic est quarta, in
missali plane omissa est" — which is why the offset is +2 at the Fifteenth Sunday
and +4 here. At p. 180 n. 1 he says the vacant Sunday is missing from Muratori
and from the Roman Missal alike. And at p. 178 n. 1 he says the September Ember
Sunday's Mass stands in the Roman Missal at the **twenty-third** Sunday after
Pentecost — **which it does**: the collect he prints there, `Absolve, quaesumus
Dne, tuorum delicta populorum`, is word for word the 1962 book's collect of
DOMINICA VIGESIMA TERTIA POST PENTECOSTEN, apart from `a peccatorum nostrorum
nexibus` for `a peccatorum nexibus`. **So the first of the two Sundays that
displace this formulary's number did not vanish from the Roman book; it was moved
seven Sundays later and the 1962 Missal still carries it.** The second, the
vacant Sunday, Gerbert says is missing outright, and nothing contradicts him.
Two small things are not established: whether the rest of that Ember Sunday Mass
travelled with its collect, and by what act it moved. LIT-018.

**Three independent corroborations of the Gregorian number.** Wilson's Hadrianum
prints these orations at `Dominica XVII` (LIT-003); Gerbert reports Muratori's
Gregorian at XVII (LIT-018); and Wilson's own footnote to no. 693 records that
Pamelius joins the second collect of that twentieth-Sunday Mass — which the
Appendix shows to be `Tua nos` — to the same Secret and Postcommunion at his
**seventeenth** Sunday. Two editors two centuries apart, working from different
manuscripts, put this formulary's orations at the same number.

**The arithmetic trap that remains.** `precedent-search` (PRE-010) carries from
claude leaf 54 the mapping of Wilson's Book III sects. I–XI to the 1962 Sundays
5–15, and the observation that the 1962 Sixteenth would fall at sect. **XII**,
which is precisely the break point where R and S insert the two September
Ember-week Sundays and rejoin at their twentieth. **The mapping cannot simply be
extended one step, and a lane that extends it will produce a confident wrong
answer.** LIT-006 and now LIT-018 confirm the break from two sides.

**One reference Gerbert makes and nobody followed**: at p. 146 n. 3 he refers the
cause of the earlier variation to "Disq. X. c. 1. p. 975", a cross-reference to a
disquisition outside the volume whose parent work the note does not name. It is
recorded and not resolved. LIT-018.

**Bound on the whole of §4.1, narrowed at iteration 1 and still real.** The
Veronense, Gelasian, Hadrianum and Sarum readings are from uncorrected optical
layers and no page image of any of those four was opened. **Gerbert is the
exception**: he was read on the page images of a public-domain 1777 printing, at
high zoom, on two scans — which establishes what Gerbert printed and **not** what
any manuscript reads, his principal manuscript being the one Wilson elsewhere
warns cannot now be traced. The critical editions that would settle the numbering
— Mohlberg 1960 (registered `restricted`) and Deshusses (not registered at all) —
were opened by nobody, so **no `Ha`, `GeV` or Supplement number is claimed
anywhere in this brief** and the numbering is Wilson's and Gerbert's own. One
retrieval bound belongs with the Gerbert row: the first scan clips the outer
margin of the right-hand column of p. 184, cutting two or three letters from most
of its lines, and every quoted line-end comes from the second scan. LIT-005,
LIT-016, LIT-017, COV-003.

**A caution the Gerbert page raises and the Roman book does not answer**: Gerbert
prints a **proper Preface** for this Mass, `Precantes`, marked Eligian, which the
Roman Missal has never had here and which the 1962 book replaces with the general
Sunday Preface of the Most Holy Trinity (§4.6). LIT-017.

### 4.2 Where the chants stand

- **Ottobonianus lat. 313's antiphonary cues**, in the margins of the Gregorian
  as Wilson prints them, put this formulary's Introit, Gradual, Offertory and
  Communion together against the heading `Dominica XV post Pentecosten`
  (sect. XXXIII, printed p. 173) — **one number below the 1962 heading and two
  below the sacramentary heading carrying the same Sunday's orations** — and the
  Alleluia they give is `Laudate dominum`, not `Cantate Domino`. Five
  consecutive Masses were checked and all five agree, so it is a systematic
  alignment in that manuscript and not a stray note. LIT-004. **The
  consequence, exactly: the 1962 Sixteenth Sunday marries a chant set this
  witness numbers XV to an oration set the same witness numbers XVII.**
- **A live disagreement about that attachment stands and is not settled here.**
  See §7.2.
- **AMS 188.** In the six oldest Roman mass antiphonaries as gregorien.info
  indexes Hesbert, this formulary is AMS 188, labelled `Dominica XVI post
  Pentecosten` — the same number the 1962 Missal gives it — but **only three of
  the six witnesses carry it, they disagree about the Gradual, and only one has
  an Alleluia**: Introit `Miserere mihi` B K S; Gradual `Liberasti nos` M,
  `Bonum est confidere` B, `Timebunt gentes` K S, `Misit Dominus verbum suum` B;
  alleluia verse `Laudate Dominum omnes gentes` S; Offertory B K S; Communion
  B K S. Compiègne and Rheinau have no entry at AMS 188 at all, and their
  indexes run to the end of the alphabet and are not truncated. LIT-014.
- **How the number was fixed**, since no page prints it as one string: the
  identification is the intersection of the AMS numbers cited across all eight
  chants on the day page, which is exactly {188}, checked against the six
  manuscript indexes; the ordinal printed at the head of a day page is a row
  counter, not the AMS number; and monotonicity was checked at days 816 and
  819. **The siglum key was reconstructed by cross-tabulation and is not printed
  by the site**: M Monza, R Rheinau, B Mont-Blandin, C Compiègne, K Corbie,
  S Senlis. It should be checked against Hesbert's own key before publication.
  LIT-014.
- **Nothing here is Hesbert's page.** See §6.4.
- **Four of the five chants are printed elsewhere in the same 1962 book**, so
  none is proper to this formulary in the sense of being unique to it: the
  Gradual also at the Third Sunday after Epiphany; the Offertory also at the
  Friday after Lent II; the Communion also at the Thursday after Lent IV and in
  a votive Mass; and the Gradual's own first verse returns as the Alleluia of
  the Eighteenth Sunday two Sundays later. Schuster asserts three of the four
  independently at printed pp. 143–144; the 1962 layer adds the other two,
  which he does not mention. LIT-008.
- **Measured against the tracked registry** (§3.4's corrected parse: 491
  formularies, 430 carrying propers, 3,259 elements, 1,034 with Latin), the
  Gradual is the Gradual of epiphany-3, -4, -5 **and** -6, not only the Third.
  Every second appointment iteration 0 recorded reproduces exactly at iteration
  1, and two more are added: Ps. 85:9–10 is the Communion and Ps. 85:12, 5 the
  Offertory of the Most Holy Name of Jesus, and Ps. 39:10–11 is the Gradual of
  s-pii-x-papae-confessoris and the Tract of the commune summorum pontificum.
  PRE-008.
- **The trap in that figure, and the rule that defeats it.** A resumed Epiphany
  Sunday keeps its own orations, Epistle and Gospel and **borrows the Twenty-third
  Sunday's chants**, as the repository's own reference work prints from
  Rubricae generales n. 18 and Missal rubric 298
  (`src/claude/liturgy/roman-rite/1962/reference/liturgical-calendar/sections/50-resumed-sundays.tex`).
  **So `Timebunt gentes` does NOT return with the resumed Sundays in November**,
  and anyone who writes that it does will be wrong. PRE-016.

### 4.3 Where the readings stand, and why this strand behaves differently

- In the *Liber Comitis* as Migne prints it (PL 30 col. 522, read on the page
  image of leaf n264), the Gospel Luke 14:1–11 stands under `Dominica mensis
  viii` — **paired with Ephesians 4:1–6, not with Eph. 3:13–21**, which is
  absent from that lectionary altogether. The negative is bounded by search:
  the whole optical text of PL 30 contains `deficiatis` exactly once, in the
  Pelagian commentary among the spuria; the eight `ad Ephesios` pericopes the
  Comes appoints are Eph. 1:3, 2:19, 4:1, 4:23, 4:29, 5:1, 5:11 and 5:15, and
  Ephesians 3 is not among them; a second independent digitisation returns the
  same negative; and neither of the two lacunae Migne marks falls where this
  Sunday's Epistle would stand. LIT-015.
- **Three cautions on the headings**, each read at high zoom on the page images
  because the optical text mangles the numerals: the `mensis` numerals VI /
  VIII / VII / VII are non-monotonic as Migne prints them and this is his
  exemplar and not an optical error; there is no `post sancti Angeli` series and
  no first or second Sunday `post S. Cypriani`; and `Desunt hic multa` marks a
  substantial gap after col. 525. LIT-015.
- **Consequence, and it inverts a sibling leaf's result.** The chants and the
  orations travel as sets and differ only in the number a book gives them; the
  readings do not travel as a set here at all. A sibling lane found the same
  lectionary agreeing with the 1962 Missal at the Fourteenth Sunday on both
  readings and called the lectionary strand the most stable of the three; at
  this Sunday it is the least stable. **Both readings stand.** LIT-015.
- **Not opened:** Klauser's *Capitulare Evangeliorum* and the Würzburg comes,
  neither registered anywhere under `src/sources/`. LIT-016.

### 4.4 Sarum: the split surviving whole in a medieval use

Dickinson's *Missale ad usum … Sarum* (printed cols. 506, 509–510, 512) puts
this formulary's **chants and Epistle** at `Dominica Decima sexta post
Trinitatem`, joined to the orations and the Gospel of the Roman Fifteenth
Sunday; and its **Collect and Gospel** at `Dominica Decima septima post
Trinitatem`, joined to the chants and Epistle of the Roman Seventeenth. The
split runs the same way as the Ottobonianus margin and in the same direction:
the chant strand sits one Sunday earlier than the oration strand. Two Sarum
readings differ from the Roman and must not be smoothed: its Alleluia at
Trinity XVI is `Qui timent Dominum sperent in eum` and at Trinity XVII
`Dextera Domini fecit virtutem`. LIT-007.

**Established at iteration 1, where iteration 1's brief recorded it as open.**
The Sarum split **is what the Book of Common Prayer inherited, and it has been in
the English books since 1549**. Brightman's *The English Rite* vol. II, printed
pp. 520–521, sets the Sarum Mass of Trinity XVII in its Sources column — collect
`Tua nos domine quesumus gratia semper preueniat & sequatur`, Epistle Eph. iv,
Gospel Luke xiv — against four parallel columns showing the arrangement unchanged
through **1549** ("Lorde, we praye thee that thy grace maye alwayes preuent and
folowe vs, and make vs continually to be geuen to all good workes"), **1552** and
**1661**. Blunt's *Annotated Book of Common Prayer* (1866) prints the same collect
at the Seventeenth Sunday after Trinity with Epistle Eph. iv. 1–6 and Gospel Luke
xiv. 1–11, and at the **Sixteenth** Sunday after Trinity tabulates Epistle Eph.
iii. 13–21 with Gospel Luke vii. 11–17 — **this formulary's Epistle standing one
Sunday earlier in the Prayer Book, exactly as it does in Sarum**. So the Prayer
Book did not create the split; it received it. LIT-020.

**A disagreement inside that closure, and neither side of it was resolved.**
Brightman tags the collect `(Greg. 172)` and Blunt tags it `Greg. Orationes
Quotidianae` — the Gregorian's **daily** orations rather than any Sunday — while
Wilson's Hadrianum prints it under `Dominica XVII post Pentecosten` (§4.1) and
Gerbert marks it `gg.`, Gregorian as Muratori has it. **Three witnesses agree the
collect is Gregorian and disagree about where in the Gregorian it stands.**
Brightman's `Greg.` is not expanded in the passage read and his page 172 was
matched to no edition; Blunt names no edition either. LIT-020.

**Bound, and it is the whole qualification:** both synopses were read on optical
text layers of Internet Archive scans, no page image was opened for either, and
**no printing of the Book of Common Prayer itself was collated** — what closes
the question is two scholarly synopses of it. Four further prayer-book
digitisations were retrieved and failed at iteration 1, on top of the four that
failed at iteration 0. LIT-007, LIT-020.

### 4.5 The Ambrosian rite reads this Epistle as a baptismal lesson

The Milan de Sirturis 1712 payload carries `flecto genua` exactly once, in a
window headed `sabbato in albis missa pro baptizatis`, and the pericope there
opens `Fratres obsecro uos ne deficiatis in tribulationibus meis pro uobis` —
**the same liturgical incipit adaptation the Roman book makes** — with the
neophyte chant `quasi modo geniti infantes` in the same stream. PRE-011.

**The extent is now established, and it is the same extent.** A wider read of
the same bytes at iteration 1 runs the window unbroken from `epiftola beati pauli
apoftoli ad ephefios [f]ratres obfecro vos ne deficia[t]is` through to `ipfi
gloria in eccle[fi]a in chrifto iefu in omnes generationes feculi feculorum amen`
— that is **Eph. 3:13–21 entire, closing on the doxology**, not the shorter
pericope iteration 0 could see. So the comparison is between two pericopes of
**identical extent with an identical liturgical incipit**, in two Western rites,
one reading it on a green Sunday and the other as the baptismal lesson of Easter
Saturday. That is a materially stronger fact than iteration 0 could state.
PRE-011.

Bounds, all of the rest of them and unchanged: OCR only, no page image; the
heading `sabbato in albis` and the rubric `missa pro baptizatis` were read in the
same noisy stream; the 1499 Ambrosian layer cannot corroborate anything; and an
eighteenth-century printing is evidence about that book and not about the
medieval Ambrosian lectionary. **Adjacency must be stated as adjacency and never
called design.** The Mozarabic payloads return zero for `flecto genua`, `radicati
et fundati` and `hydropic`, which is a bounded negative over a poor layer and not
an absence; `radicati` alone returns 9 in the 1712 Ambrosian, 3 in the 1640, 1 in
the 1499 and 2 and 1 in two Mozarabic payloads.

**Form precedent:** claude leaf 54 introduced the use of a non-Roman Western
rite as comparative evidence for an appointed text, recorded there that no
Triptych document had done so before, and has now published it
(`54-fourteenth-after-pentecost/sections/35-source-grounded-synthesis.tex:264`,
`sections/30-commentary.tex:263`). The form is available; its four bounds
travel with it.

### 4.6 The rubrical frame, 1862 to 1962

- **Rank and orations.** As a semiduplex Sunday in the 1862 Pustet the day took
  three orations, with `A cunctis` prescribed as the second from the octave of
  Pentecost to Advent (*Rubricae generales*, tit. II and *De Orationibus*
  nn. 2, 11). Under the 1960 Code it takes one: 1962 RG n. 434 b, "in dominicis
  II classis, nulla alia admittitur oratio, praeter commemorationem festi II
  classis". The rank itself is RG 12 and RG 91 row 15 as the repository's
  calendar record cites them. LIT-009.
- **Settled at iteration 1, where iteration 1's brief recorded it as open.** The
  step that reduced this Sunday to one oration was **the general decree of the
  Sacred Congregation of Rites of 23 March 1955**, *De rubricis ad simpliciorem
  formam redigendis*, and **not** the 1960 Code. It does the work on two counts
  at once: Tit. II n. 1, `Gradus et ritus semiduplex supprimitur`, with n. 5
  raising the Sundays that had kept that rite to duplex, removes the rank on
  which the 1862 three-oration rule for this day depended; and Tit. V a) n. 1,
  **`Orationes pro diversitate temporum assignatae abolentur`**, abolishes the
  seasonally assigned orations of which the `A cunctis` prescribed *ab Octava
  Pentecostes usque ad Adventum* is one. It binds `kalendis Ianuariis anni 1956`.
  The 1960 Code did not make that change; it inherited it, and its own
  contribution at this Sunday was the reclassification from duplex to second
  class and RG 434 b. **So "pre-1955 discipline" is the right name for what the
  1862 book prints, and this brief can now say why.** LIT-019.
- **And the identification that was an inference is now a reading.** The decree
  does not name `A cunctis`; that the `A cunctis` and its companions are the
  "orationes pro diversitate temporum assignatae" was inferred at first. **The
  1920 typical edition and the 1947 Benziger both print, at this formulary and
  immediately after the Collect, the direction `Orationes pro diversitate
  Temporum assignatae, ut supra`**, with `Aliae Secretae` and `Aliae
  Postcommuniones` matching — the decree's phrase, word for word, in the books
  this Sunday was celebrated from. The inference can be withdrawn. LIT-021.
- **Evidence state, and it is the whole qualification on LIT-019.** These bytes
  are the Holy See's own ABBYY-produced optical transcription of its own *Acta*,
  published at vatican.va, carrying **no page image of the 1955 printing**; the
  reading was taken from that text and from a 200 dpi rendering **of the
  transcription**, which is not a facsimile. One further route to a printed
  witness was tried and failed (documentacatholicaomnia.eu, 404). No second
  witness to the decree's wording was opened, and the page numbers 218–224 are
  the transcription's own running heads. LIT-019.
- **The Preface.** 1962 RG n. 494 b gives the Preface of the Most Holy Trinity
  "tamquam de Tempore … in omnibus dominicis II classis extra tempus natalicium
  et paschale", so **it is not proper to this formulary**. The 1862 book has the
  same rule in its *De Praefatione* n. 5 and prints **no** preface direction
  inside this Sunday's formulary; the 1962 prints one. **The printing change is
  now dated**: `Praefatio de Ssma Trinitate.` stands inside this formulary
  already in the **1920** typical edition and in the **1947** Benziger, so it
  changed with the Pius X typical edition and not with 1962. The 1955 decree does
  not touch it — its Tit. V b) n. 8 says only "Praefatio dicitur quae cuique
  Missae propria est; qua deficiente, dicitur praefatio de tempore, secus
  communis", leaving which preface is *de tempore* on a Sunday to the books.
  LIT-010, LIT-019, LIT-021. The 1759 Clement XIII
  date is the Catholic Encyclopedia's ("Preface", Fortescue, vol. 12, 1911) and
  was not checked against the decree; the article names no Acta or Decreta
  locus; and **Fortescue's own *The Mass* (1922), searched whole in its
  registered optical layer, does not carry the Sunday rule or the 1759 date at
  all**, so the article and the book by the same author do not corroborate each
  other. Cite it as a checked report of an unchecked act. LIT-010.
- **A comparative datum for the Preface, carried with its limit.** Gerbert's
  Mass carrying the 1962 **Fourteenth** Sunday's orations has a proper Preface
  of the priesthood rather than a Trinity Preface — evidence that the Preface at
  a Sunday Mass has varied, and evidence about that Mass and not this one.
  PRE-030, quoting claude leaf 54.
- **The Creed.** `Credo.` restates a general rule and is not this Sunday's
  decision: 1962 RG n. 475 a orders the symbol "in qualibet dominica", and the
  1862 book ordered it "in omnibus Dominicis per annum". The intermediate step
  narrowed the rule and left this Sunday inside it — the 1955 decree, Tit. V b)
  n. 7, "Credo dicitur dumtaxat in dominicis et festis I classis …" — so all
  three books order the Creed on any Sunday and **what changed between them is
  how much else keeps it** (LIT-019). This explains
  historically, not rubrically, the asymmetry `verified.md` records on the page:
  the Creed rule keys to the day being a Sunday, which the formulary states,
  while the Gloria rule (1962 RG n. 431 a) keys to the Office of the day, which
  it does not. LIT-011.
- **The textual stability of the formulary across the century before the
  target, which is the frame all of the above sits in.** Over **1862, 1920, 1947
  and 1962** the ten appointed texts of this formulary are the same texts, in the
  same order, with the same psalm citations, and the Alleluia is `Cantate Domino
  canticum novum` throughout. **So whatever displacement the older witnesses show
  at §4.1 to §4.4, none of it is happening in the modern printed tradition, where
  this formulary is fixed.** What changed around the texts is the apparatus: the
  rank printed at the head is `semiduplex` in 1920 and 1947 and `II classis` in
  1962, and the three supernumerary-oration cross-references present in 1920 and
  1947 are gone. **OCR caution:** these are optical layers of small-type altar
  books that damage numerals — the 1920 layer renders this Gospel's reference as
  `huc. 24, 2-22` and the Offertory's as `Ps. 39, 24 et 15`, both plainly corrupt
  — and nothing above rests on a numeral read only in that layer. **Not done:**
  the 1570 and 1604 tracked layers were opened and are too damaged at this
  formulary to collate, and the 1570's own source record forbids resting a
  negative on it, so **the chain begins at 1862 and the Tridentine end of it is
  not established here**. LIT-021.
- **An unresolved loose end, recorded and not published as a connection.** The
  1862 Creed rubric closes `vel Dominica vacet`, using the vocabulary of the
  vacant Sunday LIT-006 and LIT-018 find printed as a Mass in the Frankish
  Gelasian.
  Whether that is a survival of the same institution or the ordinary Tridentine
  sense — a Sunday whose own Mass is omitted because a feast occupies the day —
  was **not settled**, and the second reading is the likelier one. LIT-011.

### 4.7 Station, cycle and course

- **No Roman station is attested for this Sunday, and the absence is meaningful
  rather than merely unrecorded**, because **three** independent witnesses now
  name stations for the days immediately around it and none for this one —
  Gerbert's own p. 178 heads the September Ember Sunday `Die Dom. Ad S. PETRUM`
  while his p. 184, carrying this formulary's orations, has no station of any
  kind (LIT-012, LIT-017). The two already held: Schuster names one for the
  Seventeenth, one for the Nineteenth and one for each of the three September
  Ember Days, and Wilson's Appendix names the same September stations in the
  books' own words (`ad S. Petrum`, `ad S. Mariam`, `ad Apostolos`, `ad S.
  Petrum in xii Lect.`). **Bound:** this is the absence of a station in three
  witnesses that do name stations nearby, not a demonstration that no Roman
  church was ever assigned; the *ordines romani* and the modern stational
  literature were not opened, and a repository-wide sweep found no Roman station
  named anywhere in either provider's Sunday-after-Pentecost guides. LIT-012.
- **Schuster's title for the Sunday** is `Prima post natale Sancti Cypriani`,
  the hinge at which the cycle counted from St Lawrence ends and one counted
  from St Cyprian begins, running on through `Octava post Sanctum Cyprianum`.
  **Evidence state: a lead, not a collated manuscript reading** — Schuster
  prints the Latin title at the head of the chapter without naming there the
  manuscript or edition he takes it from, and he states elsewhere in the same
  series that the count of these feast-relative Sundays was not uniform between
  books. The 1962 book prints only `DOMINICA DECIMA SEXTA post Pentecosten`, and
  nothing here proposes the older title as the formulary's name. LIT-001.
- **This Sunday opens the temporal cycle's course of Ephesians**, and the single
  break falls at the Eighteenth Sunday, which Schuster judges to have been
  originally aliturgical — the Sunday after the September Ember Saturday. The
  1962 book confirms the shape and qualifies the extent: Ephesians is read on
  the Sixteenth, Seventeenth, Nineteenth, Twentieth and Twenty-first, broken
  exactly at the Eighteenth, which reads 1 Corinthians; **but Ephesians stops at
  the Twenty-first**, the Twenty-second and Twenty-third reading Philippians, so
  Schuster's "until the Twenty-third" holds only if taken of the captivity
  Epistles as a group or of a differently numbered series. Both are recorded;
  neither is resolved. LIT-002. **LIT-006 supplies the corroboration Schuster
  does not give**: the vacant Sunday is printed as a heading in the Frankish
  Gelasian, which is the only place any lane found it actually named in a
  source. A repository-wide sweep found `Dominica vacat` nowhere in either
  provider's proper guides, so the argument reaches this corpus for the first
  time here.

---

## 5. Material negative results

Every negative below is bounded by a stated search and is correctable. None is
a claim that nothing exists.

### 5.1 No New Testament book quotes the appointed verses

Searched in the tracked Clementine: Heb. 1:10–12 quotes Ps. 101:26–28 and
Heb. 10:5–7 quotes Ps. 39:7–9, but **both quoted runs lie outside the appointed
excerpts**, and no New Testament book quotes Ps. 85:1/3/5, Ps. 97:1, Ps.
39:14–15 or Ps. 70:16–18. A targeted New Testament grep on the distinctive
wording of each appointed chant — `invocantibus te`, `inops et pauper`,
`auferant eam`, `memorabor iustitiae`, `senectam et senium`, `timebunt gentes`,
`reges terrae gloriam` — returns no hit in any book from Matthew to the
Apocalypse. **Consequence, and it is the most useful negative of the join: any
christological reading of the chants rests on the psalms' wider context, on
typology, or on reception, and not on an apostolic citation of the words
actually sung.** SCR-033.

### 5.2 No patristic or saintly reception of the Secret or the Postcommunion

§2.9. The bound is the corpora named there, which are the ones the reception
lane had cause to retrieve for the scriptural elements; it is not a search of
the patristic corpus at large, and a phrase search cannot find a Father who
paraphrases an oration without quoting it. PAT-016. **The negative is no longer
total**: Guéranger reads both orations at printed pp. 370–371, which is
documented reception of a much later kind and is carried at §2.9 as that.
THE-040.

### 5.3 The Greek side, which iteration 1 recorded as empty at the psalms and no longer is

At iteration 0 two Greek authors only, and neither at a psalm: Chrysostom on the
Epistle, in English; Cyril on the Gospel, in an English translation of a Syriac
version. **`CON-REC-002` was raised against exactly that sentence, and it is
answered.** Theodoret of Cyrus's *Interpretatio in Psalmos* was opened at **all
five** appointed psalm passages in PG 80, read as rendered page images at six of
the eight column ranges and on the volume's optical layer at the other two, with
Migne's facing Latin as the control (§0.7, §2.1, §2.4, §2.5, §2.7, §2.8).

**What remains true of the Greek side, and it is not small.** No Greek New
Testament and no Septuagint is tracked in this repository (§3.1). Chrysostom's
Greek in PG 62 was not opened, so §7.5's disagreement with the Latins on Eph.
3:18 **rests on an English witness on one side** — an evidence-state limit on how
that disagreement may be worded and not a gap in retrieval (COV-005). Cyril
survives entire only in Syriac and no Greek or Syriac witness was opened, so
nothing may be argued from his wording (PAT-008). The Greek cross-reading of Eph.
3:18 usually credited to **Gregory of Nyssa** was **not verified at its own
locus** and is a lead and not a witness (PAT-007, PAT-017). Theodoret is **one**
Greek psalm witness and the lane that opened him names a Greek catena as the
cheapest way to reach a second (PAT-017). And Theodoret's English (R. C. Hill) is
in copyright: a repair that opens him must quote the Greek or Migne's facing
Latin, as this join does (PRE-036).

### 5.4 A formulary-level commentator does read this Mass as a whole, and iteration 1's negative is withdrawn

**Guéranger.** The iteration-1 brief printed this as an unresolved
three-lane disagreement (§7.1) and forbade quoting him here until a page was
rendered. **The page was rendered.** The chapter stands at printed pp. 356–371 =
artifact PDF pp. 377–392, the heading, the printed folio, the opening sentence
and the Introit were read on the image at PDF p. 377, and the lane whose negative
was the dissent retracts it (§0.8). **So this Mass has a checked commentator on
the whole formulary**, and §2.2, §2.3, §2.6, §2.8 and §2.9 carry what he says at
the Collect, the Epistle, the Gradual, the Gospel, the Offertory, the Secret, the
Communion and the Postcommunion.

**What that changes, and what it does not.**

- **It changes the class of two arguments.** §10.1's doctrine of grace and
  §10.2's join of the Gospel's axiom to grace are no longer only the guide's own
  synthesis: a checked commentator on this formulary states the first in the
  Collect's own two verbs (THE-038) and the second through Ecclus. 3:20–21
  (THE-039). At those two joints the guide may cite documented reception.
- **It does not make him a Father.** Guéranger is a nineteenth-century liturgist
  writing devotionally; the profile's claim classes rank him as documented
  reception of a much later kind, and the guide should cite him as what he is and
  not let him stand in for patristic testimony.
- **It does not give this Mass a liturgical history from him.** The negative
  §5.4 carried at iteration 1 is **substantively unchanged and now rests on two
  independent derivations of the same bytes**: a search of the whole chapter for
  `antiphonar`, `gradual`, `ancient`, `primitive`, `manuscript`, `Thomasi`,
  `liturgist`, `Ember`, `station`, `century`, `Amalarius`, `Rupert`, `Honorius`,
  `Durand` and `sacramentar` returns no historical statement at all, the only
  hits being `stationary` inside devotional prose, `members` and `remember`
  containing "Ember", and the chant heading GRADUAL above `Timebunt gentes`.
  **A guide that wants Guéranger here has him for reception and not for
  history.** LIT-013, COV-012.
- **Schuster** carries real chant history here (§4.2) but nothing that reads the
  Mass as one action; and at this Sunday, unlike at the Fourteenth, he carries no
  chant-history report from Blessed Thomasi either (LIT-013).
- **Evidence state.** The chapter heading and the printed folio were read on a
  rendered page image; the chapter's extent and the negative rest on extracted
  text from the digest-matched artifact, **so a quotation from any page other
  than printed p. 356 should be rendered before it is printed** (COV-012). The
  passages `theological-synthesis` quotes at §2.2, §2.6, §2.8 and §2.9 were read
  on rendered images at printed pp. 357, 359, 363, 365, 367–368 and 370–371
  (THE-038 to THE-041), which covers them.
- **Registration.** The artifact and edition are registered; what is absent is a
  **passage record at printed pp. 356–371**, the one registered Guéranger passage
  `vol-xi-p-271` belonging to a different Sunday. That is a provenance note
  (§6.1), not a control.

### 5.5 The five psalm elements produced no cultural afterlife, re-run wider and still negative

All five were swept again at iteration 1 over a corpus **more than twice the
size** of the first pass's — ninety Project Gutenberg volumes against
thirty-five, plus five further *Chronicling America* phrase queries on the
distinctive Douay renderings — and **none produced a qualifying candidate**; the
whole of this formulary's gallery material still comes from the Epistle and the
Gospel. The obstacles were checked rather than assumed: `Cantate Domino canticum
novum` is not distinctive to Ps. 97:1, standing also at Ps. 95:1, Ps. 149:1 and
Isa. 42:10; `Miserere mihi, Domine` is not the famous *Miserere*, which is
Ps. 50, and the secular English lives of the word attach there; and `in auxílium
meum réspice` is close enough to Ps. 69:2 that any candidate would be a use of
that verse. Of the wider sweep's recurring hits, "gray hairs" is always an ageing
character described and "new song" is always sheet music, Whitman, Plato or
Apocalypse 14; `he hath done marvellous things` returns nine newspaper pages,
`a new canticle` twenty-seven and all of them Catholic devotional columns, and
**`the Gentiles shall fear thy name` and `I will be mindful of thy justice`
return zero each**. One hit was opened and classified rather than assumed — an
1808 seaman's petition against impressment where "old age, and grey hairs" falls
in that order by accident — because the gallery rule excludes an independently
similar phrase. **The right reading is that these chants use common devotional
formulas that recur across the psalter, which is exactly the condition under
which the gallery rule's demand for a distinctive phrase cannot be met.**
CUL-008.

**And the scope judgment this lane made on the finding it was handed, recorded
because it is part of the answer to `CON-REC-002`:** that finding asks for a
second and a Greek **direct commentator** at these same five passages, which is
straight exegesis and is what the gallery rule excludes by name. Nothing this
lane could retrieve at Cassiodorus or Theodoret would answer it and nothing this
lane owns would be repaired by it. What it owed the same five passages was its
own sweep, and that was re-run in full and widened. CUL-008.

### 5.6 Gallery lines opened and closed, and two negatives that fell to a wider corpus

- **Luke 14:11 — the gap iteration 1 named as the one worth reopening is
  closed.** The wording check was always favourable, "whosoever exalteth
  himself" being unique to Luke 14:11 in the Authorized Version; what iteration 0
  could not find, iteration 1 found twice, and by widening the corpus rather than
  by a new kind of search: **Nietzsche**, *Menschliches, Allzumenschliches* I.87
  (§8.5) and **Cervantes**, *Don Quixote* I.xi (§8.6). The *Chronicling America*
  pass on this phrase was **not** extended at iteration 1 — the ranked first page
  of 250 hits remains the whole of what was inspected there — because the two
  candidates now held make a fuller newspaper pass unnecessary, not because it
  was exhausted. CUL-009, CUL-011, CUL-014.
- **Eph. 3:17 "rooted and grounded" — likewise superseded.** The ninety-volume
  corpus returns **Mark Twain**, *A Connecticut Yankee* ch. XXXIII, "his rooted
  and grounded superstitions" (§8.6). It is the weakest candidate the lane
  returns and is recorded with that judgment attached. CUL-009, CUL-015.
- **Still closed after both passes**, each searched across all ninety volumes:
  Eph. 3:19 "which passeth knowledge" — no occurrence anywhere in the corpus;
  Eph. 3:20 "exceeding abundantly above all that we ask or think" — no
  occurrence of "ask or think"; Eph. 3:15 "the whole family in heaven and earth"
  and the Douay's "all paternity" — neither occurs; Eph. 3:19 "filled with all
  the fulness of God" — no occurrence of "fulness of God". CUL-009.
- **Luke 14:7–8's "chief rooms" and "highest room"** produced three corpus hits
  and all three are ordinary architecture with no relation to the parable
  (Swift's palace and staircase, Dickens's man carrying a light through the chief
  rooms). The gallery rule excludes an independently similar phrase. CUL-009.
- **Luke 14:2 `hydrópicus`** was considered and dropped at both passes: W. K.
  Hobart's argument that Luke's vocabulary is a physician's is straight
  philological reception and changes no register, and the corpus's single hit for
  "the dropsy" is Sam Weller on "the old gen'l'm'n with the dropsy" — a disease
  named, not a verse used. CUL-009.
- **Two title-only candidates for "world without end"** — the 1956 Allied
  Artists film and Ken Follett's 2007 novel — rejected as bare titles under the
  gallery rule, neither having documentation that the title redirects the
  appointed clause. CUL-009.
- **The lesson the lane draws and this brief carries**: where a negative here
  rests on the corpus that was searched, **widening the corpus is what corrects
  it**, and two of these negatives fell to exactly that. CUL-009.

### 5.7 The chant repertories were not reached at all

No printed *Graduale Romanum*, *Antiphonale*, or Hesbert; the repository holds
no full-text payload of any of them and no artifact under any early-gradual
identity exists anywhere in `src/sources/works`, checked by directory listing.
**Consequence:** nothing in this brief bears on melodic tradition, on whether
the Introit of the Fifteenth and the Introit of this Sunday share a melody, or
on whether the Offertory's printed repetition is peculiar to this antiphon or an
ordinary convention of the genre. COV-009, PRE-001, LIT-016.

### 5.8 The text-history of the chants' departures cannot be pursued from repository sources

No Old Latin, Roman, Ambrosian or Mozarabic psalter is tracked (§3.1), and no
lane pursued the question externally. **Every departure recorded in §2 is
therefore an agreement or a difference and never a derivation**, and four
separate findings say so in terms: SCR-002, SCR-003, SCR-020 and PAT-004.

### 5.9 No Triptych precedent for this identity

No guide to this formulary exists in either provider tree, and the GPT tree has
no sixteenth-after-Pentecost leaf at all, so the same-identity cross-provider
control other leaves enjoy is unavailable. **Every precedent classification in
§9 is therefore against neighbouring identities and against the appointed-text
registry, which is a weaker control and is stated as such.** PRE-002.

**And two of this Mass's appointed elements have no precedent of any kind, not
even a passing citation.** A sweep of the iteration-1 index (2,902 files, 332,704
lines) for every form of the citation returns **zero** lines for Ps. 97 and
**zero** for Ps. 101 outside this leaf, against 52 for Ps. 39, 65 for Ps. 70 and
33 for Ps. 85; at phrase level, `cantate domino canticum novum` returns ten lines
all inside this leaf, `timebunt gentes` fifteen of which exactly one falls outside
(claude 54 quoting Wilson's cue list, not a reading of the chant), and
`aedificavit dominus sion` **zero anywhere in the corpus**. The registered library
agrees: none of the sixteen Bellarmine, nine Theodoret or four Cassiodorus psalm
passages it holds is at Ps. 97 or Ps. 101. **So the Alleluia and the Gradual are
where a sweep cannot be shortened by precedent**, and the Gradual's `vidébitur in
maiestáte sua` — the substantive one of its three departures — **has never been
examined anywhere in this collection** before this run. PRE-038.

### 5.10 The reception discovery index reconciles to nothing

`src/sources/commentary/mass-commentary-corpus.yaml` lists **twenty** works for
this Mass in the 261-line `roman-1962` `pentecost-16` block beginning at physical
line 51353, and **every one carries `work_id: null`**. The count of eighteen this
brief carried at iteration 1 was one short by two, four authors appearing twice;
the entry list printed then was already the full twenty, so only the number was
wrong. For six of the named authors the library holds no work record at all
(Nicholas of Lyra, Denis the Carthusian, Hugh of Saint-Cher, Albert the Great,
Bruno the Carthusian, Euthymius Zigabenus); for three more the author is present
but not the cited work (Peter Lombard, Athanasius, Jerome); and the Lapide row is
the partial case of §6.3. The file's sibling header states the condition in
general: "Every `work_id` in `passage-commentary-index.yaml` is still null."
**It is a lead map. No row in it supports a published claim by itself**, and the
medieval Latin postillators are the layer the repository is thinnest in.

**What iteration 1 shows the index is nonetheless worth.** Six of the twenty
reconcile by exact or declared title to a library work record — Augustine,
**Cassiodorus**, **Bellarmine**, **Theodoret**, Ambrose and Bede — and **the
three rows this run acted on are ranks two, eight and eleven of that list**, each
naming a work the library already registers with a fetchable edition. That is the
strongest available argument that the null `work_id`s **understate** the
collection's holdings rather than describing them. COV-010.

### 5.11 The two whole-volume routes are walked, and the third had the wrong address

Iteration 1's brief recorded Bellarmine's 1866 English *Explanatio in Psalmos*
(482-page registered facsimile) and Theodoret in PG 80 (1,068-page registered
facsimile) as open and not walked, with Cassiodorus as a third route "through
per-psalm web pages". **All three are now settled, and the third of those
descriptions was wrong in a way that would have cost a later sweep its whole
effort.**

- **Bellarmine and Theodoret needed no acquisition at all.** Both re-fetched
  byte-identical to their registered digests, and **all five loci in each were
  located in one pass**, because both volumes carry a usable navigation layer
  even though neither's optical text is fit to quote from. The cost estimate
  iteration 0 gave was right in kind and wrong in degree: a download and a
  rendered reading, but the download is minutes and the set of five is one pass.
  COV-011, COV-017, COV-018.
- **Cassiodorus's "per-psalm web pages" are two different editions and only one
  of them reaches this Mass.** The la.wikisource route the description fits
  covers Psalms 1–30 and reaches **none** of the five; monumenta.ch reaches all
  five and did so on the first attempt. §0.7 and §3.2 carry the addressing rule
  and the silent failure that attends getting it wrong. COV-016, THE-036,
  PRE-034.
- **What the walk left behind is registration, not research.** Fifteen passage
  records are wanted, five per witness; ten stand against artifacts the library
  already holds and five against a registered edition whose per-psalm artifacts do
  not exist. **None of it is a bar to publishing** (§6.1), and the receipts under
  `research-0001-lane-01-patristic-reception/`,
  `…-lane-03-theological-synthesis/` and `…-lane-04-source-citation-coverage/`
  are what `source-registration` would build them from. COV-016 to COV-018,
  COV-021.
- **And a form the collection already has for exactly this problem, recorded
  because it is cheap and nobody in this run kept one.** Three claude leaves (51,
  52, 53) keep a **per-psalm reception file beside `scope.md`** — a
  editions-read paragraph naming every text, edition and access route in one
  place; a lemma-against-chant table; a per-element witness list with locus and
  use; and, at claude 53, a summary matrix of witness against interpretive move,
  a material-negatives section and an **unreachable-resources list "recorded so
  searches are not repeated"**. Claude 54 keeps none and still reaches thirteen
  commentators, so the form is an aid and not a cause. **The part this run would
  actually have benefited from is the last**: had one been kept, the la.wikisource
  dead end would have been recorded once and not walked into. Whether this leaf
  should now gain such a file is not this stage's call. PRE-039.

---

## 6. Rejected and unresolved leads, provenance notes, and constraints on authoring

### 6.1 Absent library records, which are provenance notes and not controls

`guidance/sources.md` requires no machine identifier for every sentence, and a
claim whose work, edition and locus were checked is publishable on an
intelligible citation. **`source-registration` runs between this brief and the
author and registers what the lanes receipted, so some of the following may
already be in the library by the time the author reads this — but which, is not
knowable here.** None of it is a control the author must obtain before
publishing.

**Most of what iteration 1 listed here has since been registered, which is what
this note predicted would happen.** Closed between the two iterations, each
re-fetching byte-identical this run: Augustine's *Enarrationes* at all five
psalms on **three** editions, fifteen artifacts (COV-006); **Chrysostom's Homily
7 on Ephesians** with Homilies 6 and 8 beside it, where iteration 0 had only
Homily 13 (COV-005); **Ambrose's *Expositio* book VII** with books VIII and IX,
where iteration 0 had only book X, and **Cyril's sermons 99–109** delivery, where
iteration 0 had the 110–123 file that reaches no part of this pericope (COV-004).
Iteration 0's gap was a **registration** gap and not a research gap — the
witnesses had been read at their loci and the receipts are what the records were
built from.

**Receipted this run and not registered at the time of the sweep:**

- **The three psalm commentators of §0.7, at all five loci each.** Nothing in the
  library binds a Cassiodorus, Theodoret or Bellarmine passage at any of Pss. 39,
  70, 85, 97 or 101; the artifacts for Theodoret and Bellarmine exist and are
  byte-verified, and the five Cassiodorus HTML files are receipted and
  unregistered. Fifteen passage records are wanted. COV-016 to COV-018, COV-021.
- **Guéranger at printed pp. 356–371.** The artifact and edition are registered;
  no passage record exists at this Sunday, the one registered passage
  `vol-xi-p-271` belonging to the Tenth. COV-012.
- **Gerbert's *Monumenta veteris liturgiae Alemannicae*** at printed pp. 146,
  178, 180 and 184, read on two scans' page images and registered nowhere.
  LIT-017, LIT-018.
- **The Holy See's optical transcription of *AAS* 47 (1955)**, read at pp.
  218–224; neither the decree nor the *Acta* is registered here. LIT-019.
- **Brightman's *The English Rite* vol. II and Blunt's *Annotated Book of Common
  Prayer***, neither registered. LIT-020.
- **The 1920 typical edition and the 1947 Benziger optical layers**, opened at
  this formulary and not registered. LIT-021.
- **Jerome's *Epistula* 106** — registered as an edition, and the bytes
  hash-match, but the record marks the 1937 translation's copyright
  **unestablished** and permits bounded fact and very short quotation only
  (§6.2). PAT-034.
- The Catholic Encyclopedia article "Preface", not among the articles this
  repository has registered, though the rights record that would cover it
  already exists. LIT-016.

**The four items `verified.md` carries forward were three-quarters repaired
between the iterations**, and the leaf's own text control has not caught up.
Registered and closed: the two 1862 leaves n425 and n426 as artifacts, with the
`pentecost-16` Postcommunion's `provenance_confidence` raised from `medium` to
`high` and the raise recorded; the Cummiskey collect passage's `notes`, which
said "marginal number 1575" where the Collect is **no. 1593**, now corrected in
terms with an explicit "CORRECTION OF 2026-09-05" identifying 1575 as the
Fourteenth Sunday's Gradual; and the 1861 orations raised to `verified` with
`verified_on = 2026-09-05`, collated character for character against the page
images. **Only item 3 still stands** — the Communion's citation form flattened to
a range in two generated records — and it is a fidelity note and not a defect,
the loci being identical. COV-001, COV-002. **The consequence for the author is
a currency problem and not an evidence problem**: `verified.md`'s own list tells
a reader four items are open where one is, and `sections/90-scope.tex` beside it
says otherwise. The evaluator recorded that as an observation against no lane's
criteria, and §14.5 carries it as the registration work it is.

**And the whole-library check, which is the positive side of this section.** All
103 bound source ids resolve, the library validates with them, every tracked
artifact hashes correctly, and 53 of 59 bound remote artifacts re-fetch
byte-identical — including **every artifact controlling a published Latin form,
every reception witness at the five psalms, and both Guéranger artifacts**. The
six that differ are the newadvent.org stylesheet class of §3.6 and disturb no
claim. COV-019.

### 6.2 Evidence states that constrain what may be said

These are the places where the evidence in hand supports a narrower statement
than the obvious one. Each is a constraint on wording, not a bar to publishing.

| Claim | Constraint |
| --- | --- |
| The Introit verse's added `mihi`, against Ps. 16:6 | **A shared petition-form, never verbal identity.** `inclina aurem tuam mihi` is the form the tracked Clementine's psalter carries at Ps. 16:6 alone, against the `inclina ad me aurem tuam` of Ps. 30:3, Ps. 70:2 and Ps. 101:3, none of which uses `mihi`; the two verses still differ at the vocative and at the object of `exaudi`, and Ps. 16:6 has an opening clause the psalm verse has not. §2.1, §10.5, SCR-003, CON-EVI-002 |
| Trent Session VI, cap. V and can. 3 | Read only in the item's uncorrected OCR layer. Cap. X, cap. XVI and can. 32 are page-verified in the repository and may be cited freely; **for cap. V and can. 3 either read the leaf image of item `canonesetdecreta00coun_0` or cite them as OCR readings.** THE-002, PAT-015 |
| Theophylact, Gregory's *Moralia*, Basil, and the Chrysostom excerpt at *Catena* lect. 2 | **Leads only.** Verified at no locus by any lane. A pass wanting them must open PG 123 and the Basilian ascetica; they may not be quoted from the Catena. PAT-011 |
| Cyril of Alexandria | Argument only, never wording: English of a Syriac version, no Greek or Syriac opened. And his Luke 14:5 lemma reads "son … or ox", which does not transfer to the missal's `ásinus`. PAT-008 |
| Bede | Attribute only what has been checked against the possible sources, or as "Bede, drawing on Augustine": his own letter to Acca says the borrowings were marked and the transcription carries no marks. PAT-010 |
| Augustine, *Quaestiones euangeliorum* II q. 29 | Sense is safe; **wording may be quoted only after checking a printed edition**, the retrieved wikitext carrying OCR damage in that paragraph. PAT-009 |
| Every Augustinian locus | Cite by enarratio/sermo/section or by chapter, **never by Migne column**: the columns were not verified against a facsimile. PAT-001 |
| The Clement XIII decree of 3 Jan. 1759 | A checked report of an unchecked act; the encyclopedia article names no Acta locus and Fortescue's own book does not corroborate it. LIT-010 |
| The reduction to one oration | The 1862 rule and the 1962 rule were read; **the step between them was not**, and neither the 1955 decree nor the Acta is registered. LIT-009 |
| AMS 188 and the Ottobonianus Alleluia | Attributable to the gregorien.info database's report of Hesbert, not to Hesbert's page; the siglum key is reconstructed; the database cites the 1985 reprint, not the 1935 Vromant printing. §6.4 |
| Schuster's `Prima post natale Sancti Cypriani` | A reported title, not a collated manuscript reading; and read on an optical layer, not on the registered PDF's page image. LIT-001 |
| Every sacramentary reading in §4.1 | Optical layer, no page image, Wilson's numbering, no `Ha`/`GeV` number. LIT-005, COV-003 |
| Guéranger at this Sunday | **The bar is lifted**: the chapter is settled on a rendered page image and the passages quoted at §2.2, §2.6, §2.8 and §2.9 were themselves read on rendered images. A quotation from a page **other** than printed pp. 356–357, 359, 363, 365, 367–368 and 370–371 should be rendered before it is printed. Cite him as a nineteenth-century liturgist writing devotionally, never in place of patristic testimony. §5.4, COV-012, THE-038 to THE-041 |
| Cassiodorus, at any of the five psalms | A dated web state of a Migne-derived transcription delivered by monumenta.ch, **not** Adriaen's CCSL 98 and not PL 70 read at a column. The section numbers are the host's. **Where one word carries an argument — `maiestate` at the Gradual, `in auxilium meum respice` at the Offertory, `suavis ac mitis es … copiosus in misericordia` at the Introit — verify it in CCSL 98 or PL 70 before printing anything that rests on it.** Cite by lemma, never by the page's verse number (§0.5.5). PAT-018 to PAT-023 |
| Cassiodorus where he agrees with Augustine | **Corroboration, not a second independent judgment.** He names `doctor Augustinus` in these five psalms and reproduces Augustine's prevenient-grace formula almost verbatim at the Communion's psalm. Only where he differs is there a second judgment. §0.7, THE-035 |
| Theodoret, at any of the five psalms | Migne's reprint of Schulze's Halle recension with a facing Latin version, **not a critical Greek text**; the Greek and that Latin do not always agree in tense or person, and at Ps. 101:17 the Greek is a future where Migne's Latin prints the perfect. **Say whether you are quoting the Greek or Migne's Latin.** Cols. 1423–1424 and 1553–1554 rest on the optical layer alone and want rendering before quotation. His English (R. C. Hill) is in copyright and was not used. COV-018, PAT-029 to PAT-033 |
| Bellarmine, 1866 English | **Reception in English only**; O'Sullivan's translation is expressly abridged by its translator, who omitted the philological and versional discussion, so **no argument may be built on the absence of something from these pages** and nothing may be represented as Bellarmine's Latin. The argument line above each psalm and the psalm text are the **Douay–Rheims**, not Bellarmine (§0.5). Verse numbers run one below the Vulgate at Pss. 39 and 101 and level at Pss. 70, 85 and 97. PDF pp. 222–223, 269 and 316 rest on the optical layer alone. COV-017, THE-037, PAT-024 to PAT-028 |
| Jerome, *Epistula* 106 | The registered artifact is Metlen's 1937 English, whose copyright the edition record marks **unestablished**, permitting bounded fact and very short quotation only. Quote the Latin lemmata and the Greek words at issue, **not the translator's English**, and cite an original-language edition. The Latin original of the letter was not opened. PAT-034 |
| The pattern of lemma agreements at §7.14 | **Do not explain it.** That Cassiodorus expounds a Roman-psalter type text against the Clementine's Gallican was **not verified**: no recension was collated, no Roman psalter is tracked, and no study of the question was opened. State the agreement or verify the claim; do not do both at once. PAT-023 |
| The 1955 decree | Read in **one** witness, the Holy See's own optical transcription of its own *Acta*; no facsimile of the 1955 printing was collated and a second host returned 404. The page numbers are the transcription's running heads. LIT-019 |
| Gerbert | Page images of a public-domain 1777 printing establish **what Gerbert printed**, not what any manuscript reads; his principal manuscript is the one Wilson warns cannot now be traced. Quoted line-ends come from the second scan, the first clipping the outer margin of p. 184. LIT-017 |
| The Sarum-to-Prayer-Book descent | Two scholarly synopses, on optical layers, **no page image and no printing of the Prayer Book itself**. And they disagree with §4.1 about where in the Gregorian the collect stands; that disagreement stands. LIT-020 |
| Cornelius a Lapide on the Epistle | §6.3 |

### 6.3 The one silent-failure control

The registered artifact
`artifact.cornelius-a-lapide.commentaria-in-omnes-divi-pauli-epistolas.antwerp-1614.internet-archive-google-facsimile-pdf-6a83dd45`
is titled *Commentaria in omnes D. Pauli Epistolas* and **stops at Galatians
6:17**. Its OCR layer, 97,832 lines, was searched whole: the last running heads
are `COMMENT. IN EPIST. AD GALAT.`, there is no `ad Ephesios` running head
anywhere, and the 54 hits on `Ephes` variants are cross-references inside
commentary on other epistles. The repository's discovery index nevertheless
lists Lapide against this pericope. **The defect is silent — the title says
"omnes", the work is famous for covering all of them — and an author who cites
this artifact for Lapide on Ephesians 3 produces a citation that cannot be
checked in the bytes cited. Do not cite it.** The finding says nothing about
whether Lapide commented on Ephesians; he did. COV-007.

### 6.4 The standing rights bar, and what may be said meanwhile

Hesbert's *Antiphonale Missarum Sextuplex* (Vromant 1935) is registered in this
repository at **catalog level only** — work and edition records, no artifact, no
passage — and the edition record states that no exact book artifact was
inspected or registered, that Hesbert died in 1983, and that **"no affirmative
United States redistribution basis for exact edition bytes was established."**

**And two of the three fallback routes iteration 1 named are weaker than they
looked.** The registered Usuarium edition is
`edition.elte-usuarium.corpus-orationum-digital.web-2026-07-28` — the *Corpus
Orationum*, a **prayer** corpus whose one registered passage is CO 4829 — so it
does not reach the chant repertories at all. The digitised-manuscript route did
not resolve at the two hosts probed: gallica.bnf.fr refuses this client outright
(two IIIF manifest requests returned 403 and a page request 400, with and without
a browser user-agent), so no BnF-held witness was reached, and e-codices.unifr.ch
answered but its Zurich Zentralbibliothek collection lists 62 manifests, none of
which is Rheinau 30. **Three of the six witnesses were not probed at all**, and
Gallica's refusal is a client-level block a different retrieval route would
likely pass, so this is a bounded negative and **not** a finding that the
manuscripts are unavailable. **The route that remains open and untested is the
one listed first and already held**: the Hadrianum's own marginal chant cues in
Wilson 1915, a registered, byte-verified artifact. COV-009.

This is a control the maintainer owns and no lane may lift; it is not something
another pass through these seven lanes could supply, and it is therefore not a
ground to ask for changes. **What the evidence in hand supports meanwhile:**
the AMS results of §4.2 stated as the gregorien.info database's report of
Hesbert's numbering, attributed to the database, with the reconstructed siglum
key flagged and the substitution named as the declared downgrade this repository
has already made once at the Fourteenth Sunday. The routes that stay inside the
repository's own rules and were not walked: the Hadrianum's own chant cues,
already held; the Usuarium digital corpus, whose edition is registered; and
digitised manuscripts of the six antiphonaries themselves, which are ancient
text rather than Hesbert's 1935 apparatus. COV-009, LIT-016.

### 6.5 Leads rejected, and leads left open

**Rejected:**

- The 1862 Creed rubric's `vel Dominica vacet` as a survival of the Frankish
  vacant Sunday — the ordinary Tridentine sense is likelier and no source makes
  the connection. LIT-011.
- The Trinity Preface as thematically answering the Epistle — the preface is the
  general Sunday rule under the 1962 books and would stand here whatever the
  Epistle said, so it is evidence about the calendar and not about this
  formulary. THE-013, PRE-030. Retained only in the reduced form at §9.6's
  rejected list.
- `Ascende Superius` as an institutional motto (Don Bosco Technical College) —
  a bare motto in an aspirational reading, disqualified without documentation
  that it redirects the verse. CUL-007.
- The 1942 *Evening Star* "The Ox Is in the Ditch" — a Lutheran sermon title in
  a church-notices column, i.e. straight devotional reception. CUL-002.
- The 1859 *Dollar Weekly Mirror* "Friend, go up higher" — a Unitarian funeral
  address, the same disqualification. CUL-007.

**Closed since iteration 1, and listed so nobody reopens them:** Cassiodorus and
the Greek psalm commentary, the two the list called most consequential (§0.7,
§3.2); the 1955 decree (§4.6); Gerbert's *Monumenta* (§4.1); the descent of the
Sarum arrangement into the English prayer books (§4.4); Guéranger at this Sunday
(§5.4); Wiktionary's 1882 Herbert locus for the gastric "inner man", **found and
read at the work and page** — it stands in **volume 2**, p. 35, of *Life and
Writings of Frank Forester*, which is why the iteration-0 search of volume 1
missed it, and the Wiktionary citation is therefore no longer a lead but a
checked witness (§8.1); and Luke 14:11's gallery gap (§5.6).

**Open, and named so a later pass extends rather than repeats:**

- The remainder of §3.2's "not opened" list. **The two the iteration-1 list
  called most consequential are closed**; the largest of what is left is the
  **Latin original of Bellarmine's *Explanatio in Psalmos***, which would put
  four readings on an original-language footing at once, and after it a **Greek
  catena**, Theodoret being the only Greek voice held. Whether Chrysostom,
  Jerome or Hilary reaches any of these five psalms is **not established and must
  not be assumed**: no extent record for those works is tracked and nobody
  looked. PAT-017.
- The medieval *expositores missae*, where reception of a Roman oration would
  show up if anywhere; PL 105 was retrieved at iteration 1 and its Amalarian
  matter proves to be the wrong works, so **nothing was taken from it and the
  route is untouched**. PAT-016, LIT-016.
- **Whether Theodoret's Greek at Ps. 70:16 construes `μόνου` with `σου` rather
  than with `δικαιοσύνης`**, on which Augustine's whole reading of the Communion's
  first clause turns. Flagged by the lane that found it as beyond what a facsimile
  reading can settle. PAT-033.
- **A printed edition or a critical text for the four Cassiodorus lemmas** that
  agree with the chant, each of which is a single word doing an argument's work
  (§6.2). PAT-023.
- **Whether Ambrose is in fact the Breviary's appointed homilist for this Sunday**,
  which Guéranger states and no lane verified. THE-039.
- George E. Reedy's report that Lyndon Johnson announced catastrophe with "The
  ox is in the ditch!" (*New York Times*, 6 March 1987), cited at Wiktionary and
  **unverified at the underlying article**, the page not opening from the
  retrieval host. CUL-002.
- Whether the Epiphany and September appointments of `Timebunt gentes` are
  historically one borrowing or two, which no source in the checked corpus
  settles. PRE-016.
- Whether the Lenten feria or the Sunday has the older claim on the Communion
  antiphon, which needs the sacramentaries and antiphonals no lane opened.
  PRE-017.
- Why the Sacred Heart pericope skips Eph. 3:13, which no checked source states.
  PRE-018.

### 6.6 Missing evidence that should constrain authoring, in one list

Named as evidence, per the profile: a witness no lane reached, a locus nobody
opened, or a claim standing on a catena, an anthology or an aggregator. **The
list is shorter than it was**: items 5, 6, 7 and 10 of the iteration-1 list are
closed, and what remains is nine, of which one is a maintainer's control and the
rest are constraints on wording and citation form.

1. **Hesbert's pages** — a witness no lane reached, under a rights bar only the
   maintainer can lift, with the AMS claims standing on an aggregator (§6.4).
   **The one item here that genuinely controls what may be said**, and §6.4
   states what may be said meanwhile.
2. **Wilson 1915's page images** — a locus nobody opened in either iteration, and
   the attachment of the Ottobonianus cue block turns on it (§7.2). This is the
   one live disagreement the join leaves standing.
3. **The four unverified *Catena* attributions** — Theophylact, Gregory's
   *Moralia*, Basil, and the Chrysostom excerpt at lect. 2 (§6.2).
4. **Trent Session VI cap. V and can. 3 at the leaf image** (§6.2). Cap. X,
   cap. XVI and can. 32 are page-verified and may be cited freely.
5. **A critical text for the four Cassiodorus lemmas that agree with the chant**
   — CCSL 98 or PL 70 at Ps. 85:5, Ps. 101:17, Ps. 97:1 and Ps. 39:14. **A
   Migne-derived web transcription is a weak witness for exactly this kind of
   single-word agreement**, and four arguments rest on these four words (§6.2,
   §7.14).
6. **The Latin *Explanatio in Psalmos* of Bellarmine**, of which only the
   translator's abridged English was read, so nothing here is his Latin and no
   argument may rest on an absence from these pages (§6.2).
7. **PG 62 for Chrysostom's Greek**, on which §7.5's Greek-against-Latin
   disagreement at Eph. 3:18 rests from one side in English only (§5.3).
8. **Gregory of Nyssa on the dimensions of the Cross** — the one named Greek
   voice in the Eph. 3:18 chain, unverified at its own locus (§0.2, §5.3).
9. **A printed edition of Augustine's *Quaestiones euangeliorum*** at II q. 29,
   for wording only, the retrieved wikitext carrying OCR damage in that very
   paragraph (§6.2).

**Closed since iteration 1**, and named so the closure is visible: Guéranger
vol. XI at a rendered page (§5.4); Schuster's chapter, still optical-layer only
but no longer the sole route to a claim now doubly sourced (§4.7); the 1955
decree and the *Acta* (§4.6); and the two whole-volume psalm routes (§5.11).

**None of these is a rights basis a maintainer must settle before a claim may be
made, and none blocks the author**, item 1 excepted, which is a standing rights
control the maintainer owns and which §6.4 disposes of. The remainder are
satisfiable by writing the narrower sentence.

---

## 7. Competing historical judgments preserved

### 7.1 Does Guéranger's registered volume XI reach this Sunday? RESOLVED: yes.

**This is closed, and it is recorded here rather than deleted because the guide
must not carry the bar the iteration-1 brief imposed.** At iteration 0 two lanes
read the Internet Archive DjVu optical layer of item `V11TheLiturgicalYear`,
found `Sixteenth Sunday ----- 356` in the table of contents between `Fifteenth
Sunday - 344` and `Seventeenth Sunday - 372`, and read the chapter opening at
printed p. 356 — "THE SIXTEENTH SUNDAY AFTER PENTECOST. MASS. The resuscitation
of the son of the widow of Naim, on which our thoughts were fixed last Sunday,
has reanimated the confidence of our beloved mother, the Church" — running to
p. 371 (LIT-013, COV-012). A third lane extracted text from the registered
539-page PDF and reported that the volume stops at the Tenth Sunday (THE-017).
The brief printed the disagreement and named the resolution: one rendered page.

**The page was rendered.** `source-citation-coverage` rendered PDF p. 377 at 130
dpi and read on the image the printed folio 356, the verso running head TIME
AFTER PENTECOST, the Fifteenth Sunday's Magnificat antiphon above, the chapter
heading, the sub-heading MASS, the opening sentence and the Introit in both
columns; whole-file extraction of the same bytes puts recto running heads reading
SIXTEENTH SUNDAY at PDF pp. 378, 380, 382, 384, 388 and 392, and PDF p. 392
carries this Mass's Communion antiphon. Counts of capitalised headings through
the volume run ELEVENTH 10, TWELFTH 11, THIRTEENTH 12, FOURTEENTH 11, FIFTEENTH
7, SIXTEENTH 8, SEVENTEENTH 7, EIGHTEENTH 10 — **the volume reaches the
Eighteenth Sunday, not the Tenth**. COV-012.

**And the dissenting lane retracts, under its own finding id.** A case-insensitive
search of the whole-volume extraction of the exact registered PDF returns
"sixteenth sunday" nine times, and **the same search of the iteration-0
extraction of the byte-identical file returns the same nine** — so the
iteration-0 negative was a reading error by that lane and not a difference in the
bytes. What was right in that finding is kept: volumes XIII, XIV and XV are
sanctoral and carry no Sunday-after-Pentecost section, which the re-run confirms.
THE-017.

**Disposition: settled on the page image. The bar is lifted** (§6.2), §5.4 is
rewritten, and §2.2, §2.3, §2.6, §2.8 and §2.9 carry what he says. **What does
not change** is §5.4's substantive negative: the chapter supplies devotional and
doctrinal reading and no liturgical history, and that now rests on two
independent derivations of the same bytes rather than one.

### 7.2 Where does the Ottobonianus cue block attach? Two readings, one page image.

`liturgical-history` reads Wilson's antiphonary footnotes optically and attaches
this Sunday's chant set to sect. XXXIII, `Dominica XV post Pentecosten`
(printed p. 173), with five consecutive Masses agreeing (LIT-004).
`precedent-search` carries from claude leaf 54 a live and expressly unresolved
disagreement about the same block: a prior run, **reading the footnote reference
marks on page images**, placed the cue set at an offset of +2; a later run's
optical reading would make the offset zero. That leaf's adopted disposition was
"The page image controls and someone must go back to it", and it printed the
disagreement rather than harmonising it. PRE-009.

**Disposition: the disagreement stands, and this leaf is where it lands.**
`precedent-search` states the consequence plainly — the disputed cue block **is**
this Sunday's chant set, and the leaf that most naturally owns the revisit is
this one. No lane opened a page image of Wilson this run; LIT-004 says so in
terms. The guide states the alignment as disputed and names both readings, or
states only what does not turn on the attachment (that the four chants travel
together in that manuscript, and that its Alleluia is `Laudate dominum`).

### 7.3 Two mechanisms for the numbering offset, neither shown to be the cause

Wilson's is a difference of numeration base (`post Pentecosten` against `post
Octavas Pentecostes`); Schuster's is the interruption of the post-Pentecost
count by cycles reckoned from St Lawrence, St Cyprian and St Michael. **Both
stand; neither is shown here to be the cause**, and a sibling lane has already
ordered that they not be merged. LIT-003, LIT-001.

### 7.4 Schuster's extent of the Ephesians course

"Until the Twenty-third Sunday" against the 1962 book's Ephesians stopping at
the Twenty-first. Both recorded; neither resolved. §4.7, LIT-002.

### 7.5 Chrysostom against the Latins on Eph. 3:18

Genuine and to be preserved rather than harmonised: he takes the four dimensions
as the extent of love rendered by the figure of a solid body; Augustine and
Aquinas take them as the four limbs of the Cross. And Augustine differs from
himself three times over on what the limbs signify. §0.2.

### 7.6 Bede holds two readings of `Tunc erit tibi glória` and does not choose

Eschatological ("ne nunc quaerere incipias quod tibi servatur in fine") and
present ("Potest autem et in hac vita intelligi … quia quotidie Dominus suas
nuptias intrat"), at PL 92 col. 512D. **The guide should say so rather than
pick.** THE-018.

### 7.7 Ambrose and Cyril divide on what the Gospel's first half is about

Cyril spends a whole sermon on the sabbath controversy and presses it to
sarcasm; Ambrose passes over the controversy entirely and gives the healing one
clause, moving straight to humility. Bede takes a third route, arguing the
sequence from the disease of the body to the disease of the heart. §2.6.

### 7.8 The corpus's own preserved tensions about the dates

`research/chronology.toml` does not resolve them and neither does this brief:
the psalms boundary is `catholic-critical-v1` while every other claim on this
formulary is `catholic-traditional-v1`; the Epistle, the Gospel and the Nativity
claims are each `disputed` with two labels standing; and the Communion's Ps. 70
carries three distinct settings at once. §12.

### 7.9 One tension the appointed texts themselves do not resolve, now narrowed

How the Secret's `sacrifícii præséntis efféctu` relates to the Postcommunion's
`rénova cæléstibus sacraméntis` — offered sacrifice against received sacrament.
Nothing in either text states the relation. **Guéranger supplies a direction of
dependence** — the Sacrifice is "the most direct and efficacious of all the
immediate preparations that we can make for the Communion of the Body and Blood,
which that Sacrifice produces on the altar" — so the two orations are two moments
of one movement (§2.9, THE-040). **That narrows the tension and does not close
it**: it is one witness, devotional, and it is offered as *his* answer. If the
guide needs a general answer, the profile's Sacramental Appendix is where such
doctrine belongs, cited to its own sources, and not read out of these two
prayers. One further limit the Latin permits and he does not consider: whether
`eius` in the Secret refers to the sacrifice or to its effect. THE-018, THE-040.

### 7.10 What `iustítiæ tuæ solíus` excludes: four answers at one clause

Augustine excludes any righteousness of the singer's own ("Nullam meam agnosco");
**Bellarmine** excludes human counsel, his own strength and his friends;
**Cassiodorus** refers the remembering to the Judgment, when the Lord's justice
alone will be recognised as marvellous and singular; **Theodoret** makes it the
just sentence God passed in the speaker's favour. And **Guéranger**, from outside
the exegetical tradition, makes it the Church's promise after Communion **to keep
God's justice, which is his law** — which is close to the opposite of Augustine's
reading. **The grace-alone sense belongs to Augustine and, differently framed, to
Bellarmine; it is not the tradition's single voice, and the guide may not quote
Augustine and Guéranger in one paragraph as though they agreed.** §2.8, THE-021,
THE-041.

### 7.11 The Gradual's `vidébitur in maiestáte sua`: a tense that divides the traditions and a noun that divides the Latins

Theodoret's Greek lemma is the **future** `οἰκοδομήσει` with `ἐν τῇ δόξῃ αὐτοῦ`,
which is Augustine's tense; the Clementine, Cassiodorus and Bellarmine have the
**perfect**, which is the chant's. So **Augustine's future is not his own
peculiarity** and the difference between him and the chant is a difference
between textual traditions. The **noun** divides differently: the chant and
Cassiodorus read `maiestate`, the Clementine, Augustine and Bellarmine's English
`gloria` — and Bellarmine glosses the psalm's "thy glory" as "that is, thy
majesty" unprompted, which is a gloss and not a textual witness. **The
exegetical divergence is independent of both and is sharper**: all three Latins
refer the seeing to the Judgment, Theodoret to the restoration of Jerusalem, and
Guéranger to God showing himself now in the Church. **A guide that presents the
Gradual's second half as unanimously eschatological reports the Latin tradition
as the tradition.** §2.4, PAT-019, PAT-025, PAT-030, THE-023, THE-041.

### 7.12 The Offertory's imprecation: nobody reads it as a curse, and nobody relieves it the same way

Augustine and Bellarmine read a prophecy already fulfilled at the Resurrection;
Cassiodorus a prayer for the persecutors' **conversion**; Theodoret a petition
that the historical enemies be **routed** and fail of what they want; Aquinas
allows both the penitential and the punitive confusion. Guéranger, outside all
four, reads the antiphon as the Church's prayer against the assaults of hell —
**the only reading that keeps the enemies as enemies**. What all of them share is
that the Latin subjunctives are not read as wishing the enemies' destruction, and
that much is safe to state; **the gentlest reading is a Latin tradition and not
the tradition**. §2.7, THE-030, THE-040.

### 7.13 Who speaks, and over what span: two more divisions the psalms carry

**Who speaks in the Gradual's psalm.** Augustine identifies the poor man of the
title as Christ, "qui propter nos pauper factus est"; **Cassiodorus records that
reading and refuses it**, because Christ is nowhere said to have been *anxius* and
the psalm's eating of ashes cannot be fitted to the spotless Incarnation, and
assigns the psalm to a nameless afflicted poor man who stands for all Christ's
poor; Theodoret assigns it to the people in the Babylonian captivity. The two
Latins nonetheless end at a corporate speaker either way, and the disagreement is
**about whether the head or the body is the grammatical subject**. Theodoret, at
the Offertory's psalm, offers a fourth solution to the same problem: the speaker
is the Church, which does not claim to be in the right, ascribes what befalls her
to her own sins, and contains the slack as well as the perfect, "quoniam unum est
corpus, tanquam ex una persona". §2.4, §2.7, THE-024, PAT-032.

**Over what span the Communion measures.** Augustine's youth is the beginning of
faith and, ecclesially, the age of the apostles; Cassiodorus's is the coming to
grace, with `senecta` the present age and `senium` the time of Antichrist;
Bellarmine's is David's literal boyhood; Theodoret's is the age of **Moses**, with
old age the obsolescence of the Law on Heb. 8:13. **All four read it as a span of
God's teaching and none as a lifetime in the ordinary sense.** §2.8, THE-022.

### 7.14 The pattern of lemma agreements, which is a lead and not a conclusion

At **four of the five** chants Cassiodorus's Latin lemma stands closer to the
missal than the tracked Clementine does: `suavis ac mitis es; et copiosus in
misericordia` at the Introit, `videbitur in maiestate sua` at the Gradual,
`quia mirabilia fecit Dominus` at the Alleluia, `Domine, in auxilium meum
respice` at the Offertory; at the Communion his text and the Clementine both
agree with the antiphon. **The Greek confirms one of these and contradicts
another**: Theodoret's lemma at Ps. 97:1 carries `ὁ Κύριος`, which is the chant's
`Dóminus` against the Clementine, but his lemma at Ps. 101:17 is the future with
`ἐν τῇ δόξῃ αὐτοῦ`, so the Gradual's perfect and its `maiestate` are attested on
the Latin side only; and his Ps. 39:14 is the Septuagint's `εἰς τὸ βοηθῆσαί μοι
πρόσχες`, which Migne renders with the Clementine's clause and not the chant's.
Jerome, adjudicating that same verse, has a fourth Latin form again.

**Four things bound this and none of them is optional.** First, **the obvious
explanation was not verified**: that Cassiodorus expounds a Roman-psalter type
text of the kind the Roman chant repertory preserves, while the Clementine is
Gallican, is a recension claim nobody collated, no Roman psalter being tracked
here and no study of the question opened. Second, Cassiodorus was read in a
Migne-derived web transcription, **a weak witness for exactly this kind of
single-word agreement** (§6.2). Third, **agreement of a commentator's lemma with
a chant is not evidence that either was drawn from the other**, and nothing here
shows any relation. Fourth, the pattern is **not uniform once the Greek is
admitted**, which is the main thing this iteration adds to it. Anyone using the
pattern must either verify the recension claim or state the agreement without
explaining it. §5.8 records that the text-history cannot be pursued from
repository sources at all. PAT-023.

### 7.15 One thing the widened precedent field shows, recorded so it is not misused

The collection holds a **postconciliar** "Sixteenth Sunday in Ordinary Time, Year
A" in both provider trees, and the GPT one takes **Vulgate Ps. 85 as its
Responsorial** and reads it through Augustine's *Enarratio*, citing the same New
Advent file. **It shares no appointed element with this formulary except that
psalm, it is a different rite, and it is not a same-identity control and must not
be used as one.** What it is good for is a second published Triptych treatment of
this Mass's Introit psalm and an independent instance of the New Advent
file-number convention §0.5 tabulates as a hazard. The claude postconciliar leaf
of the same Sunday carries no psalm-85 material. PRE-002, PRE-036.

---

## 8. Notable-and-quotable audit

Five entries selected from the `cultural-afterlife` lane's **thirteen** qualifying
candidates, under the gallery rule of
`guidance/liturgy/roman-1962-propers.md`. Every field below is the lane's own
evidence carried through, not a summary of it. Every online witness carries its
work title, responsible creator or institution, edition or datestamp, stable
public URL, access date and exact usable locus. **All five come from the Epistle
and the Gospel; §5.5 records why the five psalm elements produced none.**

**One selection changed at iteration 2, and the reason is recorded rather than
left to be inferred.** The iteration-1 gallery spent a slot on Eph. 3:21's "world
without end, Amen" in Dickens's *Hard Times*. The iteration-1 join returned
**four** candidates on that one clause and the lane itself advises that a gallery
of three to five should spend at most one slot on it; and every one of the four
carries the same limit, that the clause is the *Gloria Patri*'s as well as the
Epistle's — this formulary cueing the Gloria Patri at its own Introit — so the
channel cannot be separated. Meanwhile the iteration-0 lane named **Luke 14:11**,
the Gospel's closing sentence and this formulary's hinge, as the gap most worth
reopening, and the wider iteration-1 corpus closed it twice. **Nietzsche's
aphorism is a verbatim rewriting of that sentence, published under a title that
claims to be correcting Scripture, and it puts the gallery's balance at two
Epistle entries and three Gospel entries rather than three and two.** Dickens
moves to §8.6 with his bundle intact, as the strongest unselected candidate.

Registers represented: gastric humour; American political idiom; a Victorian poem
of enforced self-effacement; the most quoted love poem in English; and a
philosopher's deliberate inversion.

### 8.1 "the inner man" — Epistle, Eph. 3:16

- **Appointed text and locus.** `ut det vobis secúndum divítias glóriæ suæ,
  virtúte corroborári per Spíritum eius in interiórem hóminem` (Eph. 3:16),
  *Missale Romanum*, editio typica (Vatican City: Typis Polyglottis Vaticanis,
  1962), printed pp. 397–398, marginal no. 1594, as collated at
  `propers/verified.md` §3, read 2026-09-05.
- **Later uses and loci.** (a) Jerome K. Jerome, *Three Men in a Boat (To Say
  Nothing of the Dog)*, first published London: J. W. Arrowsmith, 1889,
  **chapter XIX**, the supper after the Alhambra, in the paragraph beginning "I
  must confess to enjoying that supper": "the odour of Burgundy, and the smell of
  French sauces, and the sight of clean napkins and long loaves, knocked as a
  very welcome visitor at the door of our inner man." Project Gutenberg
  (Project Gutenberg Literary Archive Foundation) eBook **308**, plain text,
  `https://www.gutenberg.org/cache/epub/308/pg308.txt`, retrieved **2026-09-05**.
  (b) Anthony Trollope, *Barchester Towers* (London: Longman, Brown, Green,
  Longmans, & Roberts, 1857), **chapter VII, "The Dean and Chapter Take
  Counsel"**: "When I say up rose the archdeacon, I speak of the inner man,
  which then sprang up to more immediate action, for the doctor had bodily been
  standing all along with his back to the dean's empty fire-grate." Project
  Gutenberg eBook **3409**, `https://www.gutenberg.org/cache/epub/3409/pg3409.txt`,
  retrieved **2026-09-05**.
- **Relationship strength.** Strong for the verbal link and **presumptive for
  the locus**. "Inner man" is the sole occurrence of that collocation in the
  Authorized Version and it is at Eph. 3:16 — established by whole-text search
  of Project Gutenberg eBook **10**, "The King James Version of the Bible",
  `https://www.gutenberg.org/cache/epub/10/pg10.txt`, retrieved **2026-09-05**,
  on the line beginning "be strengthened with might by his Spirit in the inner
  man; 3:17 That". But the idiom's ancestry is Pauline in general: the AV
  renders the same Greek phrase "the inward man" at Rom. 7:22 and 2 Cor. 4:16,
  and Plato, *Republic* IX.589a–b supplies a pre-Christian "the man within".
  **Documented dependence on Pauline anthropology; presumptive dependence on
  this verse.**
- **Wording check.** AV "inner man" verbatim in both later texts. **The
  Douay–Rheims reads "the inward man" and does not carry the phrase**
  (`src/sources/bibles/douay-rheims/chapters/Eph/3.json`, v. 16, read
  2026-09-05), so an entry must say which version supplies it.
- **Context.** Jerome's narrator has been ten days on cold meat and jam;
  Trollope is describing a cathedral chapter meeting, and his joke is the same
  manoeuvre applied to an archdeacon — the Pauline interior self stands up while
  the body does not.
- **Translation and rights.** Jerome 1889, Trollope 1857 and the Authorized
  Version are public domain; quotation is from the underlying public-domain
  works and not from Project Gutenberg's added matter.
- **Cultural payoff.** The phrase Paul uses for the self strengthened by the
  Spirit is now most familiar as a polite word for the belly.
- **Limiting qualification.** Describe the gastric sense as **an idiom of the
  language**, not as a use Jerome invented.
- **Corroboration, and it is no longer a lead.** Wiktionary, "inner man", sense
  2, labelled "(humorous) The stomach or appetite", Wikimedia Foundation,
  `https://en.wiktionary.org/wiki/inner_man`, consulted **2026-09-05**, cites an
  1882 use by Henry William Herbert. **That locus was checked at the work and the
  page at iteration 1** and stands in **volume 2**, not volume 1 where iteration 0
  looked for it: Henry William Herbert, "The Yorkshire Moors", in [David W. Judd,
  ed.], *Life and Writings of Frank Forester (Henry William Herbert)*, vol. 2
  (New York: Orange Judd Company, **1882**), **p. 35** — "we should be there to
  refresh the inner man, and take up the fresh dogs for the afternoon" — the page
  fixed by the running head "THE YORKSHIRE MOORS. 35" standing immediately above
  it in the scan. Internet Archive copy
  `life-and-writings-of-frank-forester-v-2-1882`, full text at
  `https://archive.org/download/life-and-writings-of-frank-forester-v-2-1882/Life%20and%20writings%20of%20Frank%20Forester%20v2%201882_djvu.txt`,
  retrieved **2026-09-05**; the same text stands in copy
  `lifeandwritings00pictgoog`. **So the gastric sense is now attested in a checked
  witness of 1882, seven years before Jerome K. Jerome**, which is what makes the
  limiting qualification above a statement of fact and not a hedge.
- **Material negative results.** No headword "Inner Man" in E. Cobham Brewer,
  *Dictionary of Phrase and Fable* (Internet Archive `dictionaryphrase00brew`
  and `dictionaryofphra01brew`, both searched 2026-09-05; the only hit is under
  "Genius", glossing *genius* as "propensity, nature, inner man"); none in John
  Camden Hotten, *The Slang Dictionary* (PG 42108); no headword in Webster's
  Unabridged 1913 (PG 29765); **and none in Francis Grose, *A Classical
  Dictionary of the Vulgar Tongue* (PG 5402), searched at iteration 1**. Collins
  (403) and the OED (paywall) could not be opened. Searched without result in
  Dickens's *Pickwick Papers*, *Dombey and Son*, *Nicholas Nickleby*, *Bleak
  House*, *The Old Curiosity Shop*, *Great Expectations* and *Sketches by Boz*,
  and in Scott's *Waverley* and *Rob Roy*.
- Source: CUL-001.

### 8.2 "the ox is in the ditch" — Gospel, Luke 14:5

- **Appointed text and locus.** `Cuius vestrum ásinus, aut bos in púteum cadet,
  et non contínuo éxtrahet illum die sábbati?` (Luke 14:5), 1962 editio typica,
  printed p. 398, marginal no. 1597, `propers/verified.md` §6, read 2026-09-05 —
  where `éxtrahet` is recorded as certain on the page image against the
  facsimile's own faulty text layer.
- **Later uses and loci.** (a) *San Antonio Daily Light* (San Antonio, Tex.),
  **Thursday 7 October 1897, page 8** (image 8), editorial paragraph headed
  "THE EMERGENCY MET": "When the ox is in the ditch its no time to stop and
  discuss parliamentary ethics; the thing to do is to go to work and pull the ox
  out of the the mire. Thecity budget was stalled, and while City Dads Johnson
  and Hicks were figuring on parliamentary tactics. Mayor Callaghan with six
  faithful props, pulled the city out of the slough of despondency, ready for
  business." (Transcription as OCR'd.) Library of Congress, *Chronicling
  America*, page permalink
  `https://www.loc.gov/resource/sn86090439/1897-10-07/ed-1/?sp=8`, page OCR
  retrieved **2026-09-05**. (b) Clifton Johnson, *Highways and Byways of the
  South* (New York: The Macmillan Company, 1904), chapter "The Birthplace of
  Lincoln", **p. 169**, of Mrs Burton on the Lincoln farm near Hodgenville,
  Kentucky: "'The ox is in the ditch,' said she, referring to the New Testament
  excuse for Sabbath work where the need is great, 'and Billy must mend this
  gate if it is Sunday. It was broken yesterday, and I couldn't sleep last night
  for thinkin' the hogs might come in and turn over my kittle of soft soap.'"
  Internet Archive copy `highwaysbywaysof00john`,
  `https://archive.org/download/highwaysbywaysof00john/highwaysbywaysof00john_djvu.txt`,
  retrieved **2026-09-05**.
- **Relationship strength.** **Documented dependence on the passage** —
  Johnson's own gloss names it "the New Testament excuse for Sabbath work" —
  but **not verbatim wording**.
- **Wording check.** The idiom says "ditch"; the Latin says `púteum` and both
  Douay and AV say "pit". Present the idiom as a paraphrase of the appointed
  verse and never as a quotation of it. The rival ancestors were checked: Matt.
  12:11 has a sheep in a pit on the sabbath but no ox, and Deut. 22:4 / Exod.
  23:5 have the fallen ox but no sabbath, so **Luke 14:5 is the only locus
  carrying both**, which is why the idiom's sabbath sense points here.
- **Context.** In 1897, a city council quarrel over parliamentary tactics on the
  budget; in 1904, a Kentucky farm wife licensing Sunday gate-mending lest the
  hogs upset her kettle of soft soap.
- **Translation and rights.** Both witnesses public domain (an 1897 newspaper, a
  1904 book); the Library of Congress states the newspapers in *Chronicling
  America* are in the public domain or have no known copyright restrictions.
- **Cultural payoff.** The emergency shrinks from a drowning beast to a soap
  kettle and then to a stalled budget, and the verse survives as the standing
  American excuse for suspending a rule.
- **Diffusion, measured.** A phrase search of *Chronicling America* for "ox is
  in the ditch" returns **324 newspaper pages**, the retained hits running from
  1897 into the 1950s across Texas, Georgia, Pennsylvania, New Jersey, Arkansas,
  Mississippi and Washington, D.C. Query
  `https://www.loc.gov/collections/chronicling-america/?ops=PHRASE&qs=ox+is+in+the+ditch&searchType=advanced&fo=json&c=10`,
  run **2026-09-05**; only the first page of ten records was retrieved.
- **Limiting qualification.** Much of the phrase's newspaper life is straight
  devotional reception and must not be counted as afterlife.
- **Material negative results.** The top-ranked 1942 hit — *Evening Star*
  (Washington, D.C.), 26 September 1942, image 21 — is a Lutheran sermon title
  in a church-notices column and was set aside for that reason. George E.
  Reedy's report that Lyndon B. Johnson announced catastrophe with "The ox is in
  the ditch!" (*The New York Times*, 6 March 1987), cited at Wiktionary,
  `https://en.wiktionary.org/wiki/ox_is_in_the_ditch`, consulted 2026-09-05,
  **stands as an unverified lead**: the *Times* page could not be opened from
  the retrieval host, and iteration 1 did not reopen it.
- Source: CUL-002.

### 8.3 "Sit Down in the Lowest Room." — Gospel, Luke 14:10

- **Appointed text and locus.** `Sed cum vocátus fúeris, vade, recúmbe in
  novíssimo loco: ut, cum vénerit qui te invitávit, dicat tibi: Amíce, ascénde
  supérius` (Luke 14:10), 1962 editio typica, printed p. 398, marginal no. 1597,
  `propers/verified.md` §6, read 2026-09-05.
- **Later use and loci.** Christina G. Rossetti, **"Sit Down in the Lowest
  Room."**, *Macmillan's Magazine*, ed. David Masson, **No. 53, vol. IX**
  (London: Macmillan and Co., **March 1864**), **pp. 436–439**, first line "Like
  flowers sequestered from the sun"; volume contents list, entry "'Sit Down in
  the Lowest Room.' By CHRISTINA G. ROSSETTI 436"; running head at p. 437.
  Internet Archive copy `macmillansmagazi09macmuoft`,
  `https://archive.org/download/macmillansmagazi09macmuoft/macmillansmagazi09macmuoft_djvu.txt`,
  retrieved **2026-09-05**. Collected as "The Lowest Room" in *The Poetical
  Works of Christina Georgina Rossetti, with Memoir and Notes*, ed. William
  Michael Rossetti (London: Macmillan and Co., **1904**), poem at **pp. 16–19**
  (editorially dated 30 September 1856), editorial note at **pp. 460–461**;
  Internet Archive copy `poeticalworksofc00ross`,
  `https://archive.org/download/poeticalworksofc00ross/poeticalworksofc00ross_djvu.txt`,
  retrieved **2026-09-05**.
- **The documented quarrel.** W. M. Rossetti's note: "The original title of this
  poem was *A Fight over the Body of Homer* — perhaps the better title of the
  two… This is the poem on which Dante Gabriel Rossetti, in a published letter to
  his sister, dated 1875, made the following remarks: — 'A real taint, to some
  extent, of modern vicious style… what might be called a falsetto muscularity —
  always seemed to me much too prominent in the long piece called *The Lowest
  Room*.'… Christina, on receiving this letter, did not acquiesce in its
  purport… However, she always retained *The Lowest Room* in succeeding
  editions. … The real gist of *The Lowest Room* — i.e. the final acceptance, by
  the supposed speaker, of a subordinate and bedimmed position."
- **Relationship strength.** **Verbatim.** The 1864 title is the Authorized
  Version's imperative clause, quoted with its full stop and set over a secular
  poem. "Lowest room" occurs in the AV at Luke 14:9 and 14:10 only, both inside
  this appointed pericope (PG eBook 10, searched 2026-09-05).
- **Wording check.** AV "sit down in the lowest room" exactly in the title; the
  poem's body reads "Content to take the lowest place", which is the **Douay**
  wording (`…/douay-rheims/chapters/Luke/14.json`, v. 10, read 2026-09-05). The
  title and the body draw on different English versions and the appointed Latin
  lies behind both.
- **Context.** A dramatic dialogue between two sisters, one plain and bookish
  and stung by Homer's heroes, the other beautiful and married; twenty years on
  the speaker sits alone — "Not to be first: how hard to learn / That lifelong
  lesson of the past… So now in patience I possess / My soul year after tedious
  year, / Content to take the lowest place, / The place assigned me here" —
  ending "Yea, sometimes still I lift my heart / To the Archangelic
  trumpet-burst, / When all deep secrets shall be shown, / And many last be
  first."
- **Translation and rights.** The 1864 magazine, the 1904 edition and the
  Authorized Version are all public domain.
- **Cultural payoff.** A rule of banquet precedence and a promise of
  eschatological reversal becomes the name for Victorian women's enforced
  self-effacement, with the reversal deferred to the trumpet — a redirection
  sharp enough that the poet's own brother wanted the poem suppressed and she
  refused.
- **Limiting qualification.** The verbal link is carried by the **title**, not
  by a quotation inside the poem, so the entry must show why this is not the
  "bare title" the gallery rule excludes: the substitution of the Gospel
  imperative for the manuscript's *A Fight over the Body of Homer*, the poem's
  argued acceptance of the lowest place, and the documented family quarrel are
  what make it a use rather than a label.
- **Material negative result / confusion to avoid.** Rossetti also wrote a short
  devotional lyric "The Lowest Place" ("Give me the lowest place; not that I
  dare") and a separate devotional piece headed "Sit down in the Lowest Room";
  **those are straight devotional reception, do not qualify, and must not be
  confused with this poem.**
- Source: CUL-003.

### 8.4 "the depth and breadth and height" — Epistle, Eph. 3:18

- **Appointed text and locus.** `ut possítis comprehéndere cum ómnibus sanctis,
  quæ sit latitúdo, et longitúdo, et sublímitas, et profúndum: scire étiam
  supereminéntem sciéntiæ caritátem Christi` (Eph. 3:18–19), 1962 editio typica,
  printed p. 398, marginal no. 1594, `propers/verified.md` §3, read 2026-09-05.
- **Later use and locus.** Elizabeth Barrett Browning, *Sonnets from the
  Portuguese*, **Sonnet XLIII**, first published in *Poems* (London: Chapman
  and Hall, **1850**), **lines 1–4**: "How do I love thee? Let me count the
  ways. / I love thee to the depth and breadth and height / My soul can reach,
  when feeling out of sight / For the ends of Being and ideal Grace." Project
  Gutenberg eBook **2002**, `https://www.gutenberg.org/cache/epub/2002/pg2002.txt`,
  retrieved **2026-09-05**.
- **The scholarly identification.** John S. Phillipson (University of Akron),
  **"'How Do I Love Thee?' — an Echo of St. Paul"**, *The Victorian Newsletter*,
  ed. William E. Buckler, **No. 22 (Fall 1962), p. 22, note 7**: Barrett
  Browning "seems to echo St. Paul, Ephesians, III, 17–19, in her famous
  declaration"; and, closing the note, "In spirit and expression, then, Sonnet 43
  echoes St. Paul's thought and phraseology while adapting them to a new context.
  It extends the temporal to the eternal, mingling the sacred and profane and
  giving the profane a sacred character. St. Paul implies extension in three
  dimensions (height and depth being considered as one); Mrs. Browning implies
  an extension beyond her grasp in two dimensions." Scanned issue
  `Victorians_n22_Fall1962.pdf`, **The Ohio State University Libraries Knowledge
  Bank**, item handle **1811/103270**, file at
  `https://kb.osu.edu/server/api/core/bitstreams/15df302b-55a8-4dc3-be09-792b65c42322/content`,
  retrieved **2026-09-05**, the note read whole.
- **The lead that led to it, kept as a lead.** "Sonnet 43", *Poetry for
  Students* (Detroit: Gale, 1997), reproduced at Encyclopedia.com,
  `https://www.encyclopedia.com/arts/educational-magazines/sonnet-43`, consulted
  **2026-09-05**, citing Phillipson — checked against the article above and not
  relied on for the claim.
- **Relationship strength.** **An echo, and it must be described as one.**
  Phillipson's own verb is "seems to echo"; Barrett Browning never names the
  source and no statement of hers claiming the allusion was located. **What is
  documented is the scholarly identification, not the poet's intention.**
- **Wording check.** The sonnet has three of the four nouns in the AV's order
  reversed and the fourth ("length") dropped — "the depth and breadth and
  height" against the AV's "the breadth, and length, and depth, and height" and
  the Douay's "the breadth and length and height and depth"
  (`…/douay-rheims/chapters/Eph/3.json`, v. 18, read 2026-09-05). A re-use of
  the vocabulary and the measuring gesture, not a quotation.
- **Context.** Paul is praying that the Ephesians may take the measure of the
  love of Christ that passes knowledge; Barrett Browning is measuring her love
  for Robert Browning, and Phillipson notes that the sonnet keeps the religious
  lexis — "soul", "Grace", "faith", "saints" — around it.
- **Translation and rights.** The sonnet and the Authorized Version are public
  domain. **Phillipson's 1962 note is in copyright**; its scan is served openly
  by the Ohio State University Libraries, and quotation from it must stay short
  and attributed.
- **Cultural payoff.** The Pauline dimensions of divine love became the measure
  of one woman's love for a man, and from there the standard wedding reading and
  greeting-card formula: the appointed verse's afterlife runs through the most
  secular sentimental register in the language.
- **Limiting qualification.** The entry must say "echo" and must not claim
  dependence; and it should note that Phillipson reads the transfer as
  **sacralising the profane** rather than as secularising the sacred, which is
  the opposite direction from the gallery's usual turn and is part of what makes
  the case interesting.
- Source: CUL-004.

### 8.5 "he that humbleth himself shall be exalted" — Gospel, Luke 14:11

- **Appointed text and locus.** `quia omnis, qui se exáltat, humiliábitur: et
  qui se humíliat, exaltábitur.` (Luke 14:11), the sentence on which the
  appointed pericope ends, 1962 editio typica, printed p. 398, marginal no. 1597,
  `propers/verified.md` §6, read 2026-09-05. Douay–Rheims: "Because every one
  that exalteth himself shall be humbled: and he that humbleth himself shall be
  exalted" (`src/sources/bibles/douay-rheims/chapters/Luke/14.json`, v. 11, read
  2026-09-05).
- **Later use and locus.** Friedrich Nietzsche, *Menschliches, Allzumenschliches:
  Ein Buch für freie Geister*, Erster Band, Zweites Hauptstück ("Zur Geschichte
  der moralischen Empfindungen"), **aphorism 87, entire**: "Lucas 18,14
  verbessert. — Wer sich selbst erniedrigt, will erhöhet werden." Project
  Gutenberg (Project Gutenberg Literary Archive Foundation) eBook **7207**,
  plain text, `https://www.gutenberg.org/cache/epub/7207/pg7207.txt`, retrieved
  **2026-09-05**, the aphorism standing between 86 ("Das Zünglein an der Wage")
  and 88 ("Verhinderung des Selbstmordes"). **The published English**: Friedrich
  Nietzsche, *Human, All-Too-Human: A Book for Free Spirits*, Part I, translated
  by **Helen Zimmern**, introduction by J. M. Kennedy (Edinburgh and London:
  T. N. Foulis, **1910**), **printed p. 88**, aphorism 87 entire: "St. Luke
  xviii. 14, Improved. — He that humbleth himself **wishes to be** exalted."
  Internet Archive copy `HumanAllTooHumanPartIFriedrichNietzsche`, full text at
  `https://archive.org/download/HumanAllTooHumanPartIFriedrichNietzsche/Human%20All%20Too%20Human%20Part%20I%2C%20Friedrich%20Nietzsche_djvu.txt`,
  retrieved **2026-09-05**; the page is fixed by the running heads "88" and
  "THE HISTORY OF THE MORAL SENTIMENTS. 89" that bracket it.
- **Relationship strength.** **Verbatim in the clause, and the alteration is
  exact and legible.** Zimmern's English keeps the Authorized Version's "He that
  humbleth himself" untouched and changes only "shall be" to "wishes to be";
  Nietzsche's German keeps Luther's "Wer sich selbst erniedrigt … erhöhet werden"
  and changes only the modal. And the title claims the act: *verbessert*,
  "improved".
- **THE LIMITING QUALIFICATION IS THE HEADING, and an entry must carry it.**
  **Nietzsche names Lucas 18,14** — the Pharisee and the Publican — **and not
  Luke 14:11, which is the verse this Mass appoints.** The two carry the
  identical clause in the Clementine Latin the missal prints, in the Douay the
  guide quotes and in the Authorized Version — Clementine Luke 18:14 "quia omnis
  qui se exaltat, humiliabitur, et qui se humiliat, exaltabitur" against
  Clementine Luke 14:11 "quia omnis, qui se exaltat, humiliabitur: et qui se
  humiliat, exaltabitur"
  (`src/sources/bibles/clementine-vulgate/chapters/Luke/14.json` and `…/18.json`,
  read 2026-09-05) — **so the sentence he rewrites is word for word the sentence
  the appointed Gospel ends on; but he is citing the parallel, and the entry must
  say so** rather than let a reader believe he was correcting this Mass's Gospel.
  Note also that Matt. 23:12 carries the same reversal in different words, so the
  clause is not unique to Luke; the two Lucan verses are the ones that are
  verbally identical. `scripture-context` reaches the same family independently
  (SCR-017).
- **Wording check.** Appointed Douay "he that humbleth himself shall be
  exalted"; Zimmern "He that humbleth himself wishes to be exalted". The
  statement about Luther's `soll` is from the standing Luther text and is **a
  lead**: no public-domain German Bible could be obtained from the retrieval host
  on 2026-09-05. The Nietzsche wording itself is retrieved and checked.
- **Context.** Aphorism 87 stands in the chapter on the history of the moral
  sentiments, among a run of one-line unmaskings of moral motive; **its whole
  force is the title**, which claims to be repairing a scriptural text.
- **Translation and rights.** The 1878 German is public domain; Zimmern's 1910
  translation is public domain in the United States and, her death falling in
  1934, in life-plus-70 jurisdictions as well. The quoted matter is one sentence.
- **Cultural payoff.** The appointed Gospel's promise, spoken over a dinner table
  where guests were scrambling for the best couch, is answered eighteen centuries
  later by a philosopher who **agrees that the humble will be exalted and says
  that is exactly why they humble themselves** — the parable's cure re-described
  as the disease. It is the sharpest reversal of any appointed wording this
  formulary carries, and it stands against the reception at §2.6 and §10.2, where
  Bede argues the humbling and the exalting are the Lord's acts and not men's.
- **Misattribution guard, checked rather than assumed.** The aphorism is **not**
  in *Jenseits von Gut und Böse* — the German (PG 7204) and Zimmern's English
  *Beyond Good and Evil* (PG 4363) were both searched on 2026-09-05 and neither
  contains "erniedrig" or "humbles himself" — and it is not in *Also sprach
  Zarathustra*, *Götzen-Dämmerung*, *Ecce homo* or *Der Wille zur Macht*, all
  searched the same day. It stands where the evidence says: *Menschliches,
  Allzumenschliches* I.87.
- Source: CUL-011, with CUL-009 for the gap it closes.

### 8.6 Candidates returned and NOT selected, with the reason

Thirteen qualifying candidates were returned and five are above. The eight below
are recorded with enough of their bundle that a later pass can swap one in
without re-finding it, and with the disposition each carries.

- **CUL-005. Charles Dickens, *Hard Times. For These Times* (London: Bradbury
  and Evans, 1854), Book the First ("Sowing"), chapter V, "The Keynote"**, second
  paragraph: "…what you couldn't state in figures, or show to be purchaseable in
  the cheapest market and saleable in the dearest, was not, and never should be,
  **world without end, Amen**." Project Gutenberg eBook 786,
  `https://www.gutenberg.org/cache/epub/786/pg786.txt`, retrieved 2026-09-05.
  Against Eph. 3:21, `ipsi glória in Ecclésia, et in Christo Iesu, in omnes
  generatiónes sǽculi sæculórum. Amen.`, printed p. 398, marginal no. 1594.
  **Verbatim, and the English phrase is appointed wording in the guide's own
  translation tradition** — the Douay reads "unto all generations, world without
  end. Amen." — with the liturgical cadence left intact and the object of worship
  swapped, which is a sharper attack than parody. **This was §8.5 at iteration 1
  and is the strongest unselected candidate.** Not selected for two reasons
  taken together: the source is **over-determined**, the identical English closing
  the *Gloria Patri* of the Book of Common Prayer and this same formulary cueing
  the Gloria Patri at its own Introit, so Dickens's immediate channel cannot be
  separated and the entry can never claim he is quoting Ephesians in particular;
  and **four candidates stand on this one clause**, which the lane's own
  disposition says should take at most one gallery slot. **If it is restored, it
  displaces §8.5 and not one of the other four.**
- **CUL-012. G. K. Chesterton, *Orthodoxy*, chapter VII, "The Eternal
  Revolution"** (first published 1908; read in the Internet Archive copy
  `orthodox00ches`, John Lane, at **p. 219**, and in Project Gutenberg eBook
  16769, `https://www.gutenberg.org/cache/epub/16769/pg16769.txt`, retrieved
  2026-09-05): "canvassing is very Christian in its primary idea. It is
  encouraging the humble; it is saying to the modest man, **'Friend, go up
  higher.'**" Against Luke 14:10, `Amíce, ascénde supérius`, identical in Douay
  and AV. **Verbatim, quoted as a quotation, dependence not in doubt, a named
  book by a named author, and public domain.** Not selected because the gallery
  already carries a Luke 14:10 entry at §8.3 and this is **institutional and
  political redirection from inside the tradition** rather than the secular or
  ironic turn the gallery prefers; **it is the strongest candidate on that verse
  if §8.3 were ever dropped**, and it turns the verse in the opposite direction
  from CUL-007 below.
- **CUL-014. Miguel de Cervantes, *Don Quijote*, Primera parte, cap. XI**
  (Spanish, Project Gutenberg eBook 2000; John Ormsby's English, PG eBook 996,
  both retrieved 2026-09-05): "thou must seat thyself, because **him who humbleth
  himself God exalteth**; and seizing him by the arm he forced him to sit down
  beside himself" — the maxim used to **compel** a man out of the lowest place, at
  a meal, in a dispute about who sits where. Not selected because the wording is
  the Spanish **proverbial form and not the appointed clause**: `Dios le ensalza`
  adds an agent the Vulgate and the Douay have not, and, as with §8.5, the proverb
  answers Luke 18:14 and Matt. 23:12 as well. **The second candidate on Luke
  14:11 and the comic one**; opposite in temper to §8.5's attack, and either
  would serve.
- **CUL-010. Shakespeare, *Love's Labour's Lost* V.ii and Sonnet 57.5**, both
  hyphenating Eph. 3:21's clause into an adjective for duration felt as a burden
  — "A time, methinks, too short / To make a **world-without-end** bargain in" and
  "Nor dare I chide the **world-without-end** hour". Folger Shakespeare Library
  plain texts, `https://shakespeare.folger.edu/downloads/txt/loves-labors-lost_TXT_FolgerShakespeare.txt`
  and `…/shakespeares-sonnets_TXT_FolgerShakespeare.txt`, retrieved 2026-09-05;
  also PG eBook 100. Not selected: same clause as CUL-005 and the same
  over-determination, worse here because Shakespeare's England met the formula
  daily in the Gloria Patri, and no annotated edition glossing the phrase to
  Ephesians could be opened — Burgess's *The Bible in Shakspeare* (1903) files it
  among Shakespeare's scriptural matter and names no verse, Schmidt's
  *Shakespeare-Lexicon* vol. 2 and Tyler's 1890 *Sonnets* carry it not at all, and
  the OED is paywalled. **An echo of the liturgical-biblical formula, not a
  quotation of the appointed verse.**
- **CUL-013. Charles Dickens, *Dombey and Son* (1846–48), chapter XLIX**, Captain
  Cuttle: "as if you was a driving, head on, to the **world without end,
  evermore, amen**, and when found making a note of". PG eBook 821, retrieved
  2026-09-05. Same clause again, and the "evermore" is the Prayer Book's cadence
  and not Ephesians'; a fourth candidate on Eph. 3:21 and the comic member of that
  set.
- **CUL-006. James Joyce, *Ulysses* (Paris: Shakespeare and Company, 1922),
  episode 2 "Nestor"**, distributing "As it was in the beginning, is now… and
  ever shall be… world without end" across Mr Deasy's study. PG eBook 4300,
  retrieved 2026-09-05. Verbatim for three words, no "Amen"; **the clauses Joyce
  splices in belong to the *Gloria Patri* and not to the Epistle**, so the
  demonstrable channel is the doxology and the link is the weakest of the four on
  this clause.
- **CUL-007. *The Petal Paper* (Petal, Miss.), Thursday 15 May 1958, page 2**, a
  broadcaster's list of "Biblical quotations for program managers" in which
  "For passing the buck: 'Friend, go up higher.' (Luke…" is the label for kicking
  a decision upstairs. LoC *Chronicling America* permalink
  `https://www.loc.gov/resource/sn85044791/1958-05-15/ed-1/?sp=2`, page OCR
  retrieved 2026-09-05. Verbatim, identical in Douay and AV, genuinely comic, and
  a bounded negative comparator establishes that it is the exception — a phrase
  search for "friend go up higher" returns 157 pages overwhelmingly of sermons
  and funeral discourses. **Not selected** for two recorded reasons: the paper
  reprints an **unnamed** broadcaster's joke, so no author can be named; and the
  item is **under 95 years old**, so the Library of Congress's public-domain
  belief is qualified for possible third-party matter (LoC catalogue record
  `https://www.loc.gov/item/sn85044791/`, consulted 2026-09-05) and any published
  excerpt must be held to the one line and its label.
- **CUL-015. Mark Twain, *A Connecticut Yankee in King Arthur's Court* (1889),
  chapter XXXIII**, "his **rooted and grounded** superstitions", against Eph.
  3:17's `in caritáte radicáti, et fundáti`, whose English "rooted and grounded"
  is unique to that verse in the Authorized Version and **absent from the Douay**,
  which reads "rooted and founded in charity". PG eBook 86, retrieved 2026-09-05.
  **The weakest candidate the lane returns and it says so**: by 1889 the phrase
  was an ordinary English idiom for the deeply fixed and Twain gives no sign of
  quoting anything, so what is documented is a transfer of register and not an act
  of allusion. **If the gallery is ever full, this is the entry to drop first.**

---

## 9. Interpretive-proposal audit

Six proposals, each grounded in a conjunction the `precedent-search` lane
actually reached and classified. **That lane ran before this stage settled which
proposals are retained, so its nineteen conjunctions are searches of the
precedent field the appointed elements invite and not searches per retained
proposal; the coverage is stated as a set.** No proposal is retained here whose
conjunction the lane did not reach, and the classification each carries is the
lane's own, unchanged.

**The coverage is now checked rather than asserted.** At iteration 1 the lane ran
after the proposals were settled and mapped them one to one onto the conjunctions
it reached: P1 = PRE-021, P2 = PRE-027, P3 = PRE-023, P4 = PRE-022, P5 = PRE-025,
P6 = PRE-031. **Synthesis retained no proposal whose conjunction the lane did not
cover**, with thirteen of the nineteen reached and not retained (§9.7). No new
conjunction was reached at iteration 1 and none was expected: the conjunction
field is a function of the appointed elements, and those have not moved. What
iteration 1 adds is **two textual controls on retained proposals**, at P5 and P6.
PRE-032.

The lane's search boundary, which every "not located" below is bounded by, is
§3.4, with §5.7's chant repertories, the pre-Tridentine Latin commentary
tradition, the sacramentary editions themselves and every page image expressly
**not reached**. `not located in the checked corpus` is bounded and correctable
and **never** asserts that a connection is unknown, unprecedented, first, or
authored by a model.

### 9.1 — P1. Two systems of measurement in one formulary

- **Anchors (2 appointed elements).** Epistle, Eph. 3:18–19 (`quæ sit latitúdo,
  et longitúdo, et sublímitas, et profúndum: scire étiam supereminéntem sciéntiæ
  caritátem Christi`); Gospel, Luke 14:8–11 (`non discúmbas in primo loco`,
  `recúmbe in novíssimo loco`, `Amíce, ascénde supérius`, `qui se exáltat,
  humiliábitur`).
- **Mechanism.** The reading asks the hearer to take four measures of a charity
  it says surpasses knowledge; the Gospel ranks three seats and a comparative,
  and settles the ranking by an act that is not the guest's.
- **What the element-by-element reading misses.** Read separately, the Epistle's
  dimensions are a devotional flourish and the Gospel's places are table
  manners; read together, the Mass puts an immeasurable magnitude beside a
  measurable one and makes the measurable one the place to stand.
- **Nearest located precedent or analogue.** None for the pair. In **form**
  only: gpt 55 `sections/50-interpretive.tex`, "The proper's several clocks"
  (Int., Grad., Ep., Off.) and "Ear, eye, touch, and mouth" (Int., Gosp., Off.)
  — proposals built from one formulary's several registers of a single category.
- **Search boundary.** §3.4; `latitudo`, `sublimitas` and `ascende superius`
  each return exactly one line in the 326,844-line prose index, and it is this
  leaf's own `verified.md`. No commentary tradition on Eph. 3:18 is held by the
  registered library.
- **Classification: NOT LOCATED IN THE CHECKED CORPUS.**
- **Controlling limit.** The join is lexical at one end (four spatial nouns) and
  narrative at the other (three seat positions), which is weaker than a shared
  verb would give and must be stated as such. **The Epistle's dimensions are
  explicitly said to surpass knowledge; the Gospel's table must not become a
  measure of them.**
- Source: PRE-021, with SCR-008 and §0.2.

### 9.2 — P2. The swollen body and the cleansed mind

- **Anchors (3 appointed elements).** Gospel, Luke 14:2 (`Et ecce homo quidam
  hydrópicus erat ante illum`) and 14:4 (`Ipse vero apprehénsum sanávit eum`);
  Secret (`Munda nos … sacrifícii præséntis efféctu`); Postcommunion (`Purífica
  … mentes nostras benígnus, et rénova cæléstibus sacraméntis`).
- **Mechanism.** The Mass has an outward healing in its Gospel and asks for an
  inward cleansing and renewal in the two orations that follow the offering and
  the communion; the disease the Gospel heals is one of superfluity, and what
  the orations ask to be removed is not named.
- **What the element-by-element reading misses.** The Gospel's healing is
  ordinarily read as the occasion of the sabbath argument and dropped; the
  orations are ordinarily read as generic. Taken together the formulary moves
  from a body relieved of what it cannot hold to a mind asked for the same
  relief.
- **Nearest located precedent or analogue.** None for the join. **What is
  documented and must not be presented as the proposal**: Ambrose and Bede read
  the dropsy as a figure of the flux of the flesh and of avarice (§2.6), and
  Augustine at Ps. 97:1 moves from new song to new man to inward healing
  (§2.5). The proposal is the joining of the figure to the *cleansing orations*,
  which is not located.
- **Search boundary.** §3.4; `hydropic` returns one line in the prose index and
  it is this leaf's own record, `dropsy` returns zero, and no leaf anywhere
  treats the healing. Lexically, `renova` occurs in ten of the 1,034
  Latin-bearing propers of the tracked registry and `miserat-` in eight — a
  count over composed orations only, not over the missal.
- **Classification: NOT LOCATED IN THE CHECKED CORPUS.**
- **Controlling limit.** No checked witness joins the sabbath healing to the
  doctrine of grace; both Ambrose and Bede join it to avarice. **A guide that
  makes the healing a figure of prevenient grace is proposing, and must be in
  the exploratory section.** If a later reception sweep documents the join, that
  part moves out of this section.
- Source: PRE-027, with THE-018, THE-011, PAT-009, PAT-010.

### 9.3 — P3. Three acts of looking, and only one of them is asked for

- **Anchors (2 appointed elements).** Gospel, Luke 14:1 (`et ipsi observábant
  eum`) and 14:7 (`inténdens quómodo primos accúbitus elígerent`); Offertory
  (`Dómine, in auxílium meum réspice … Dómine, in auxílium meum réspice`), whose
  repetition `verified.md` §7 establishes is printed in full and is not a cue.
- **Mechanism.** Two human acts of looking, one surveillance and one
  calculation, stand against one divine act of looking that is petitioned — and
  petitioned twice, the antiphon returning to its first clause after the
  intervening plea.
- **What the element-by-element reading misses.** The Gospel's `observábant` is
  usually read as narrative setting; set beside the Offertory it becomes one
  term of a contrast the formulary makes across two ritual moments, between
  being watched and asking to be looked at.
- **Nearest located precedent or analogue.** gpt 55 `sections/50-interpretive.tex`,
  "Ear, eye, touch, and mouth" (Int., Gosp., Off.) — a sensory-series proposal
  on the **immediately preceding Sunday**, joining the same three element
  classes. Also supporting, and documented rather than analogous: Aquinas on
  Ps. 39, "Respectus Dei est auxilium nostrum" (§2.7).
- **Search boundary.** §3.4; `in auxilium meum respice` returns three lines in
  the prose index, all in this leaf's own `verified.md`.
- **Classification: NEAR ANALOGUE LOCATED.**
- **Controlling limit.** The analogue is close enough to be a hazard: the
  adjacent Sunday's guide already publishes a senses-across-the-formulary
  proposal, and this would read as the same move twice in consecutive guides.
  What distinguishes it is the **asymmetry** — the human looking here is
  appraisal and the divine looking is petitioned — which the Fifteenth's
  proposal has not. Whether the printed repetition is peculiar to this antiphon
  or an ordinary convention **cannot be answered**: no chant repertory was
  reached (§5.7).
- Source: PRE-023, with PAT-014.

### 9.4 — P4. What is built and what is conferred

- **Anchors (3 appointed elements).** Gradual (`Timébunt gentes nomen tuum,
  Dómine, et omnes reges terræ glóriam tuam. ℣. Quóniam ædificávit Dóminus
  Sion, et vidébitur in maiestáte sua`); Epistle (`in caritáte radicáti, et
  fundáti`; `quæ est glória vestra`; `secúndum divítias glóriæ suæ`; `ipsi
  glória in Ecclésia`); Gospel (`Tunc erit tibi glória coram simul
  discumbéntibus`).
- **Mechanism.** One building vocabulary runs from a city God has built to
  hearers rooted and founded; and `glória` is appointed in three elements, with
  the Gospel's the only occurrence a **host confers on a guest**.
- **What the element-by-element reading misses.** Each element's `glória` reads
  as a different word when the elements are taken singly — God's, the
  Ephesians', a diner's. Taken together, the formulary sets a glory that is
  seen, a glory that is given and a glory that is assigned at a table.
- **Nearest located precedent or analogue.** None for the pair. **A striking
  convergence to record but not to claim**: Augustine at the Gradual's own
  v. 16 reads the nations as the second wall meeting Israel in the corner stone
  and cites **Eph. 2:20** — a verse of the appointed Epistle's own letter, which
  the Mass does not read (§2.4). `radicati et fundati` and `aedificavit dominus
  sion` each return zero lines in the prose index.
- **Search boundary.** §3.4.
- **Classification: NOT LOCATED IN THE CHECKED CORPUS.**
- **Controlling limit.** The chant replaces the psalter's second `gloria` with
  `maiestáte`, so the Gradual says `glóriam tuam` once where the psalm said it
  twice, and **any count of `glória` across this formulary is a count over the
  appointed text and not over the psalter**. Augustine's Eph. 2:20 citation is
  at a verse of Ephesians the Mass does not appoint, and its coincidence with
  this Mass's Epistle is not evidence that anyone joined them.
- Source: PRE-022, with SCR-006, SCR-025, PAT-002.

### 9.5 — P5. What both psalm chants stop just short of saying

- **Anchors (3 appointed elements).** Alleluia (`Cantáte Dómino cánticum novum:
  quia mirabília fecit Dóminus`, stopping before `Salvavit sibi dextera ejus, et
  brachium sanctum ejus`); Communion (`… Deus, ne derelínquas me`, stopping
  before `donec annuntiem brachium tuum generationi omni quae ventura est`);
  Epistle, whose doxology ends `in omnes generatiónes sǽculi sæculórum`.
- **Mechanism.** Both chants cut immediately before the Lord's **arm** and, in
  the Communion's case, before its announcement to a **coming generation**; the
  Epistle's doxology, which the Mass does read, ends on generations. The
  Communion also stops one clause short of `pronuntiabo mirabilia tua`, the word
  the Alleluia sings.
- **What the element-by-element reading misses.** Each cut looks arbitrary
  alone. Together they show that the formulary sings the wonders and does not
  sing the arm, and that the one place it does say "generations" is the reading
  and not the chant.
- **Nearest located precedent or analogue.** claude 54
  `sections/50-interpretive.tex:137` and `sections/20-themes.tex:89, 93` carry
  the published "the hope-formula lies past the cut" proposal, with its audit at
  that leaf's `research/scope.md` §9.4.
- **Search boundary.** §3.4; `past the cut` and `lies past` return lines only in
  claude 54's brief and its two published sections.
- **Classification: NEAR ANALOGUE LOCATED, on form.**
- **Controlling limit, and it comes with the form.** claude 54's own audit
  records that its scripture lane found duller explanations for such cuts —
  metrical length, the ordinary bounds of an antiphon — and that **no intent is
  established; the antiphons' extents are inherited chant tradition and the cuts
  were not made to suppress anything.** That limit transfers here undiminished.
  **The material past the cut must be labelled as the source psalms' and never
  as the appointed chants'**, and §5.7 records that no chant repertory was
  reached that could speak to the cuts.
- **A second control, new at iteration 1 and it bites on this proposal's
  wording.** This brief states the Alleluia as stopping before `Salvavit sibi
  dextera ejus`. **Cassiodorus's psalter lemma at Ps. 97:1 reads `salvavit
  EUM`**, and Augustine's reads `Sanavit ei`. So **the material past the cut is
  not uniform across the Latin witnesses this repository can reach, and a
  proposal that quotes the continuation is quoting one psalter and not the
  tradition.** Which reading is the appointed psalter's is not settled anywhere in
  this join. PRE-025, PAT-003, PAT-020.
- Source: PRE-025, with SCR-013, SCR-023, SCR-027.

### 9.6 — P6. Poverty and plenitude, distributed by element

- **Anchors (3 appointed elements).** Introit psalm verse (`quóniam inops et
  pauper sum ego`) and antiphon (`copiósus in misericórdia`); Epistle
  (`secúndum divítias glóriæ suæ`; `ut impleámini in omnem plenitúdinem Dei`;
  `qui potens est ómnia fácere superabundánter quam pétimus, aut intellégimus`);
  Gospel (`recúmbe in novíssimo loco`).
- **Mechanism, corrected at iteration 2.** The Mass's one confession of poverty
  is sung; **abundance is predicated twice and of two different subjects** — the
  Introit antiphon sings it of God's mercy (`copiósus in misericórdia`) and the
  Epistle reads it of what God gives and does (`divítias glóriæ suæ`, `in omnem
  plenitúdinem Dei`, `superabundánter quam pétimus`) — and the Gospel's remedy is
  a **place** rather than a possession. **The iteration-1 wording of this
  mechanism said the abundance vocabulary is entirely read, which its own Anchors
  field contradicts, the antiphon's `copiósus` being sung**; the content
  evaluation recorded that against no lane's criteria and traced it to this brief.
  The corrected form is the stronger one: what is distributed is not
  poverty-sung-against-abundance-read but **God's abundance in both registers
  against the singer's poverty in one**.
- **What the element-by-element reading misses.** The Introit's `inops et
  pauper` looks like a formula of psalm supplication until the Epistle piles up
  riches, superabundance and fullness in the same Mass; the distribution across
  chant and reading is what the single-element reading loses. `superabundánter`
  occurs nowhere else in the tracked Bible (SCR-036), which is a lexical fact and
  not an interpretation.
- **Nearest located precedent or analogue.** None. `inops et pauper`,
  `plenitudinem dei` and `superabundanter` return four lines between them in the
  prose index, three of which are this leaf's own record and one of which is
  claude 51's treatment of Eph. 3:20 as an **echo** of the Eleventh Sunday's
  Collect `Omnipotens sempiterne Deus, qui abundantia pietatis tuae et merita
  supplicum excedis et vota` — published at echo strength and no more, so **a
  guide that upgraded that echo to dependence would contradict a published
  leaf.**
- **Search boundary.** §3.4.
- **Classification: NOT LOCATED IN THE CHECKED CORPUS.**
- **Controlling limit, and it is severe.** The strongest form of this
  conjunction rests on the Introit's **psalm verse** and not its antiphon, and
  claude 54's audit §9.6 records that a claim anchored in an Introit psalm verse
  is liable where the verse is not sung; **the boundary question — which part of
  an Introit counts as the appointed element — must be settled before this
  proposal is retained in the reader-facing section.** Independently, SCR-026
  records that the formulary's poverty language is mostly in the psalms'
  unappointed context: only Ps. 85:1 is actually sung, `Oratio pauperis` is Ps.
  101's unappointed title, `mendicus sum et pauper` is Ps. 39's unappointed
  v. 18, and the Gospel's `pauperes, debiles, claudos, et cæcos` falls two
  verses past the pericope's end. **A poverty theme built from this formulary is
  built from the context of the appointed texts and not from the appointed
  texts, and the difference must be visible to the reader.**
- **A second control, new at iteration 1, on the poverty word itself.**
  Cassiodorus's lemma at Ps. 85:1 reads `quoniam **egenus** et pauper sum ego`
  and at v. 3 `Miserere **mei**` where the antiphon prints `mihi`. **The poverty
  word the proposal turns on is not the word a second Latin witness
  lemmatizes.** This does not weaken the conjunction — `inops` is what the missal
  prints and `verified.md` collates it on the page image — but **a reception
  witness quoted in support may be expounding `egenus`, and the guide must not
  let the commentator's word stand in for the chant's.** PRE-031, PAT-018.
- Source: PRE-031, with SCR-026, SCR-002, SCR-036.

### 9.7 Conjunctions reached and NOT retained as proposals, with the reason

Thirteen of the nineteen. Recorded so that nobody revives one without its
defeater, and so that the coverage is visible as a set.

| Conjunction | Lane classification | Why not retained |
| --- | --- | --- |
| PRE-013 Ps. 85 exchanged between the Fifteenth's antiphon and this Introit's verse | not located | The two in-formulary members are the Introit's antiphon and its own psalm verse, i.e. parts of one element; the join's force is cross-formulary and the corroboration is another leaf's |
| PRE-014 `praeveni-`/`iugiter` bridge from the Fifteenth's Postcommunion to this Collect | near analogue | Cross-formulary, and the Collect's doctrine is carried as **source-grounded** claim C1, not as a proposal |
| PRE-015 Ps. 39 head and tail across the Fifteenth and two Lenten ferias | not located | Cross-formulary; an observation about appointment order and nothing more |
| PRE-016 the Gradual across Epiphany 3–6 and the Eighteenth Sunday | precedent located for the rule | Carried as **fact** in C4 and §4.2, with the resumed-Sunday correction; not a proposal |
| PRE-017 the Communion shared with Lent IV Thursday, which also reads the Fifteenth's Gospel | not located | Cross-formulary; secondary evidence only |
| PRE-018 the Epistle's v. 13 excised at the two other appointments; the doxology read only here | precedent located for the doxology | Carried as fact in §2.3; the doxology half is constrained by claude 51's published echo |
| PRE-019 Luke 14 in three blocks with vv. 12–15 appointed nowhere | precedent located for the adjacent block | Cross-formulary; and the registry does not encode ferial and votive Gospels exhaustively enough for the negative to be more than bounded |
| PRE-020 the `exaltat`/`humiliat` logion shared with the Tenth Sunday | near analogue | Carried as fact and as a **control** in C2: the logion is the shared conclusion of two parables in two Masses and must not silently be made this Sunday's own |
| PRE-024 `extrahet` against `auferant`, Gospel and Offertory | not located | Retained as a **reading available to P3's element pair** rather than as a seventh proposal; the join is a contrast of agents and not a shared lexeme, and the verbs differ |
| PRE-026 the Collect's before-and-after against the Communion's youth-to-old-age | near analogue | The three spans are class 1 and the doctrine is class 4; both are carried in C1, so a proposal would restate the source-grounded section |
| PRE-028 the nations' fear against the lawyers' silence | not located | `gentes` in the psalm is nations and not the Gentiles of Pauline usage; the shift of sense is a move the guide would be making and would have to own, and the Gradual makes no reference to the Gospel's audience |
| PRE-029 mercy vocabulary at Introit and Secret | near analogue on form | The form's known weakness applies with more force here: this formulary's mercy vocabulary is the ordinary vocabulary of Roman prayer and the Introit's is a psalm's |
| PRE-030 the Trinity Preface against the Epistle's triadic prayer | not located, with a strong defeater | The Preface is the general Sunday rule under the 1962 books and would stand here whatever the Epistle said (§4.6, THE-013). Retainable **only** as a proposal about what the general Sunday Preface does when it lands on this particular Epistle, and only if it says the Preface is not proper to the day |

**No shortfall to record.** The lane's floor was six distinct conjunctions and
it reached nineteen; six are retained above and thirteen are disposed of here.
**Synthesis retained no proposal whose conjunction the lane did not reach**, and
at iteration 1 the lane checked that mapping one to one rather than assuming it
(PRE-032). Every lexical control the conjunctions rest on re-verifies exactly:
`praeveni` in 6 orations, `iugiter` in 18 and their intersection exactly
pentecost-15's Postcommunion and this Collect; `sequatur` in 5; `renova` in 10;
`miserat` in 8.

### 9.8 Two counting instruments, and what each may be used for

- The **tracked registry** (`src/sources/calendars/roman-1962/propers.yaml`)
  carries Latin body text for only the three orations of each Sunday — 3 of 10
  propers at every Sunday after Pentecost checked, and **1,034 of 3,259**
  elements overall on the reproducible iteration-1 parse (§3.4; the "3,270"
  iteration 0 gave does not reproduce and must not be quoted). **Every lexical count taken from it is a control over composed
  orations and says nothing about chants or readings**, and it is a repository
  derivative and not a facsimile collation.
- **Any count across this Mass's ten elements must be made on this leaf's own
  `propers/verified.md`**, which holds the complete collated Latin. That is how
  §1.1's threads were counted and it is the only instrument that reaches them.

---

## 10. Cross-proper claims settled for the synthesis commentary

Six claims. **This is the redistilled argument, not an abridged procession
through the propers**: each unit below draws together several ritual moments,
several scriptural contexts and several reception witnesses, and no unit is
about one element. Every claim is **source-grounded synthesis (class 4)** built
on class 1, 2 and 3 material named at each.

**One thing changed at iteration 2 and it changes what may be said about two of
these claims.** The iteration-1 brief stated that **none** of them is documented
reception, because no commentator was known to read this formulary as a whole.
**Guéranger does** (§0.8, §5.4), and at two joints he says what C1 and C2 say:
the Collect's prevenient-and-subsequent grace in the Collect's own two verbs
(THE-038), and the Gospel's humility joined to grace through Ecclus. 3:20–21
(THE-039). **At those two joints the guide may cite documented reception (class
3); everywhere else the rule stands** — the ten-element argument in the shape
stated below is the guide's own, and no sentence may imply that a commentator has
said *that* about this formulary. And Guéranger is a nineteenth-century liturgist
writing devotionally, so he is cited as what he is.

**The strongest argument, and its shape.** The Mass says one thing in three
registers that do not repeat a word of each other — a doctrine of grace in the
orations, a christological pattern in the chants, and a parable of place in the
Gospel — and the commentators who supply the standing exposition of its five
psalms read them in the terms its Collect prays in. C1 and C2 are the two halves
of that; C6 shows the Epistle is not an interlude between them but their centre;
C3, C4 and C5 are what the historical and textual evidence permits to be said
about how a Mass that says this came to look like this. **The argument's own
limit is that the coincidence is a coincidence of doctrine and not a documented
dependence, and nothing in the join establishes that any compiler intended the
arrangement.**

**And the iteration-1 sweep imposes a second limit that runs through C1, C2 and
C5 alike, and it is a gain and not a loss.** Where iteration 1 could say "the
Father" and mean Augustine, the guide must now say **which** witness, because at
every one of the five psalms four commentators are open and they materially
differ: on what `solíus` excludes (§7.10), on the tense and reference of
`vidébitur in maiestáte sua` (§7.11), on how the Offertory's imprecation works
(§7.12), on who speaks and over what span (§7.13). **The argument survives every
one of those divergences; what it loses is the right to call any of its readings
"the tradition's".**

### 10.1 — C1. Grace before and after, said three times in three registers, and read that way by the Father who expounds the verses the Mass sings

- **Ritual moments.** Collect, Secret, Communion, Postcommunion.
- **Textual observation (class 1).** The Collect's paired verbs `prævéniat` and
  `sequátur`, with `iúgiter` governing the good works; the Secret's `mereámur`
  standing in a purpose clause under `pérfice miserátus in nobis`, so the merit
  is God's completed work in us; the Communion's `iustítiæ tuæ solíus`; and
  three spans of three different kinds — the Collect's before-and-after, the
  Communion's youth-to-old-age, the Postcommunion's present-and-future.
  THE-002, THE-003, THE-007.
- **Documented reception (class 3).** Augustine, *Enchiridion* 32 ("nolentem
  praevenit, ut velit, volentem subsequitur, ne frustra velit") and *De gratia
  et libero arbitrio* 17.33; and — the load-bearing witness — *Enarr. in Ps. 70*
  sermo II §§1, 2, 4, which are exactly the antiphon's own three verses:
  "nihil in me praecessisse", "Debebatur poena; reddita est gratia", "gratia tua
  semper perseveret mecum". Trent Session VI cap. XVI ("bona eorum opera semper
  antecedit et comitatur et subsequitur"), cap. X and can. 32, all page-verified
  here; cap. V and can. 3 at OCR state only. PAT-005, PAT-015, THE-002, THE-003.
- **A second Latin witness at an appointed text, new at iteration 1.**
  Cassiodorus opens his exposition of the Communion's own psalm by calling
  Christ's charity that "**quae nullis meritis praecedentibus gratis semper
  impenditur**" and closes it with "gratiam Domini, **quae gratis datur**", so
  the psalm the Mass sings at Communion is read as the psalm of gratuitous grace
  by **two** Latin commentators and not one; and at the Offertory's psalm he
  makes God's very looking our protection. **The qualification is not
  optional**: his phrase is Augustine's almost word for word and he names
  Augustine inside these five psalms, so at this locus he corroborates and does
  not judge independently (§0.7, THE-035). THE-020, THE-031.
- **And a commentator on this Mass, which is what raises this joint from class 4
  to class 3.** Guéranger, above this Collect, states the distinction in the
  Collect's own two verbs and draws from it exactly the consequence the second
  clause asks for (§2.2, THE-038). He is a witness that the Collect **is** read
  this way; the authority for the technical distinction remains Augustine and
  Trent.
- **Why the join is strong.** Augustine is commenting on the exact verses the
  antiphon sings and not on a parallel place; his `nihil in me praecessisse` is
  the Collect's `prævéniat` stated as a confession, and his `gratia tua semper
  perseveret mecum` sets `semper` beside the Collect's. Trent's cap. XVI shares
  `iugiter` and `semper` with the Collect at exactly the doctrinal point. And
  Augustine's *Sermo* 165 on the appointed Epistle is headed "deque gratia et
  libera voluntate, contra Pelagianos" and closes on the Collect's question put
  as an interrogation: "unde gratiam tuam meritum meum praecedat? Non." THE-008.
- **Limits that must travel.** Trent's triplet adds `comitatur` where the
  Collect has two verbs and **the guide must not silently upgrade two into
  three**. Augustine's most quotable formula, "sua dona coronabit, non merita
  tua", stands on v. 19, **one verse past the antiphon**. Nothing shows that the
  Collect's compiler was reading Augustine, and nothing shows that Trent had this
  Collect in view — Trent quotes the **Thirteenth** Sunday's prayer, and quotes
  it altered (THE-015). The Douay of Ps. 70:16 does read "I will be mindful of
  thy justice alone", so **the Communion is the one place where Latin and
  publishable English agree** and the doctrine can be stated to a reader on the
  appointed words (THE-016). **And the newest limit is the sharpest**: at that
  same clause the four checked witnesses do **not** agree on what `solíus`
  excludes (§7.10), so the anti-merit sense is attributable to Augustine, may be
  supported from Bellarmine, and **may not be generalised to the tradition** —
  and Guéranger, reading the clause as the Church's promise to keep God's law,
  must not be quoted in the same paragraph as though he agreed.
- **What would defeat it.** An argument that `mereámur` is an independent
  optative rather than a purpose clause under `pérfice`, which the Latin as
  printed does not support.

### 10.2 — C2. The formulary's humility is Christ's descent before it is a rule of conduct, and the Gradual carries the pattern the Gospel states

- **Ritual moments.** Introit, Gradual, Gospel; and the Epistle's `flecto génua`.
- **Textual observation (class 1).** Luke 14:11's `omnis, qui se exáltat,
  humiliábitur: et qui se humíliat, exaltábitur` closes the pericope; the
  Gradual's `vidébitur in maiestáte sua` follows `ædificávit Dóminus Sion`; the
  Introit's psalm verse is `inops et pauper sum ego`; the Gospel's own scene is
  `in domum cuiúsdam príncipis pharisæórum`; and the canon states both motions
  together at Phil. 2:8–11, with `humiliávit`/`exaltávit` against Luke 14:11 and
  `genu flectátur` against Eph. 3:14 (SCR-029).
- **Documented reception (class 3).** Augustine at the Introit's own psalm
  verse: "Inclinat aurem, si tu non erigas cervicem: humiliato enim
  appropinquat; ab exaltato longe discedit, nisi quem ipse humiliatum
  exaltaverit", with the boasting Pharisee against the confessing Publican
  (THE-004). Augustine at the Gradual's own vv. 16–17: he was seen from Sion
  `in infirmitate sua` and will be seen `in gloria sua` at the Judgment
  (PAT-002, THE-010). **Bede at Luke 14:11: the humbling and the exalting are
  the Lord's** — "omnis qui se incaute de meritis allevat, humiliabitur a
  Domino, et qui provide se de benefactis humiliat, exaltabitur ab eo"
  (PL 92, 513A) — and the conclusion proves the parable must be read *typice*,
  because it is plainly false that everyone who exalts himself before men is
  humbled by men (PAT-010, THE-018). Benedict makes the sentence the head of
  *Regula* 7 (PAT-012).
- **Why the join is strong, and it is stronger at iteration 2 than at
  iteration 1.** It answers the objection that would otherwise collapse the Mass
  into moralism: the humbling and the exalting are God's acts because they are
  first Christ's own, seen in weakness and to be seen in majesty, and Bede says
  the agent is the Lord in terms. **Three things now stand under it that did
  not.** (a) The exchange is stated at an **appointed psalm** by a checked
  witness: Cassiodorus at Ps. 101 — God raises sinners by his gifts, and "dum in
  superbiam tumida mortalium corda conscenderint … a collata largitate
  subtrahitur; ut illi solerter advertant **non fuisse propria bona**", calling
  the casting-down happy — which is the Collect's doctrine and the Gospel's
  axiom said together by one commentator at a psalm this Mass sings, though at
  v. 11 of that psalm and not at the appointed vv. 16–17 (THE-034). (b) The
  christological ground is reached **through Philippians 2 at three different
  appointed chants and in both traditions**: Cassiodorus quotes `Humiliavit
  semetipsum factus obediens usque ad mortem` at the Introit's psalm, Bellarmine
  the same sentence at the Alleluia's verse, and Theodoret `omne genu ipsi
  flectendum esse` at the Gradual's own v. 16 — three commentators who did not
  read one another at those places, from the fifth, sixth and seventeenth
  centuries, reaching the same Pauline hymn while expounding three different
  psalms this Mass appoints. That is **evidence about how these texts are heard
  and not about the compiler**; Philippians 2 is among the most quoted passages
  in patristic exegesis, so what makes it usable is that at each locus it is
  quoted **to explain the appointed words** and not in passing, and the appointed
  Epistle is from Ephesians, not Philippians (THE-027). (c) Guéranger joins the
  Gospel's humility to grace **at this formulary**, through Ecclus. 3:20–21
  (§2.6, THE-039).
- **Limits that must travel.** **Augustine's lemma is `gloria` and the chant
  prints `maiestáte`, so no sentence built on `maiestáte` may be attributed to
  him**; his verb is a future `aedificabit` where the chant prints the perfect
  `ædificávit`. **But the discrepancy is no longer his peculiarity**: the future
  is the Greek tradition's, which Theodoret expounds, and the perfect is the
  Clementine's, Cassiodorus's and Bellarmine's, so what stands between the chant
  and Augustine is a difference of text traditions (§7.11). **The two-appearings
  pattern is the Latin line's**: Cassiodorus and Bellarmine hold it with
  Augustine, and Bellarmine states it in English at the verse, which partly
  relieves the English scarcity §10.5 records; **Theodoret does not hold it at
  all**, reading the verse of the restored city, and Guéranger reads the majesty
  as seen now in the Church. **Attribute the pattern to the Latin line and not to
  the tradition** (§2.4). Augustine's Pharisee is Luke 18's and not Luke 14:1's, so that
  link is doctrinal illumination joining two Lucan scenes and not exegesis of
  this pericope (THE-004). Benedict names no chapter and the sentence stands
  three times in the canon, so the Rule attests reception of the **sentence**
  (PAT-012); and the sentence is the shared conclusion of two parables in two
  Masses, this one and the Tenth Sunday's, whose guide prints it and never
  comments on it (PRE-020). **Bede holds both an eschatological and a daily
  reading of `Tunc erit tibi glória` and does not choose** (§7.6).

### 10.3 — C3. The Sunday's number is the least stable thing about it, and its three strands were assembled on different schedules

- **Ritual moments.** All ten, taken as three strands.
- **Documented historical orientation (class 2), with every witness at §4.** The
  orations: absent entire from the Veronense; Secret and Postcommunion together
  in the Old Gelasian under a collect the Roman Missal does not use here, with
  `Tua nos` not in that book's three books at all; all three together in the
  Gregorian Hadrianum at `Dominica XVII`; all three together in the Frankish
  Gelasian at `Hebd. xx`, four numbers out, with the September Ember Sunday and
  a printed `Dominica Vacat` accounting for exactly the two extra places. The
  chants: the Ottobonianus margin numbers this set XV, two below the sacramentary
  heading that carries the same Sunday's orations. The readings: the *Liber
  Comitis* puts this Gospel where the 1962 book puts it relative to its
  neighbours **but attaches Ephesians 4:1–6 to it**, and Eph. 3:13–21 is not in
  that lectionary at all. Sarum splits the formulary across Trinity XVI and
  XVII, chants and Epistle at one and Collect and Gospel at the other.
- **The consequence, and it is the argument.** The 1962 Sixteenth Sunday marries
  a chant set one witness numbers XV to an oration set the same witness numbers
  XVII; the readings do not travel as a set at all; and where a sibling
  production found the lectionary strand the most stable of the three, at this
  Sunday it is the least stable. **Both readings stand.**
- **What iteration 1 adds to the claim, and it is corroboration and not a
  change.** The Frankish Gelasian row is now read on **Gerbert's own page
  images**, in two scans, and he states the arithmetic himself: "quae est hic Dom.
  XX. in Missali est XVI. & apud MURAT. XVII." He prints the vacant Sunday as a
  **Mass** with a running head numbering it XIX and says it is missing from
  Muratori and the Roman Missal alike; and his per-oration sigla mark `Tua nos`
  Gregorian only against the Secret and Postcommunion marked Gelasian, Eligian and
  Gregorian — **which is exactly the negative LIT-005 reached from the other
  direction on Wilson's Gelasian text**, two independent editors two centuries
  apart agreeing that the Collect is the Gregorian member of the trio. **The
  Sarum split's descent into the English prayer books is established**: the Prayer
  Book carries this collect and this Gospel at the Seventeenth Sunday after
  Trinity and this Epistle at the Sixteenth, unchanged from 1549 through 1661,
  and it received the split rather than creating it (§4.4). **And the modern
  printed chain is fixed**: across 1862, 1920, 1947 and 1962 the ten appointed
  texts do not change, so none of the displacement above is happening in the
  modern tradition (§4.6). §4.1, §4.4, §4.6, LIT-017 to LIT-021.
- **Limits that must travel.** Every sacramentary reading except Gerbert's is
  optical-layer with no page image, Wilson's numbering, no critical-edition
  number; **Gerbert's page images establish what Gerbert printed and not what any
  manuscript reads.** The Ottobonianus attachment is **disputed** and is the one
  live disagreement the join leaves standing (§7.2). Two mechanisms for the
  offset stand and neither is shown to be the cause (§7.3). Schuster's older title
  is a reported title (§4.7). The Ambrosian appointment of the same Epistle as an
  Easter Saturday baptismal lesson is OCR-only, though **its extent is now
  established as Eph. 3:13–21 entire, the same extent with the same liturgical
  incipit** (§4.5). The Sarum-to-Prayer-Book descent rests on two synopses and no
  printing of the Prayer Book, and the three witnesses that agree the collect is
  Gregorian **disagree about where in the Gregorian it stands** (§4.4). The
  Tridentine end of the printed chain is not established, the 1570 and 1604 layers
  being too damaged at this formulary to collate (§4.6).

### 10.4 — C4. Not one of this Mass's chants is proper to it, and its Alleluia has the weakest claim of the five to its place

- **Ritual moments.** Introit, Gradual, Alleluia, Offertory, Communion.
- **Textual observation and class 2, at §4.2.** Four of the five are printed
  elsewhere in the same 1962 book; the Gradual serves four Sundays after the
  Epiphany and its first verse returns as the Alleluia two Sundays later; the
  Offertory has one other appointment and the Communion two. Only three of the
  six oldest Roman graduals carry this formulary at all, they disagree about the
  Gradual, and the only alleluia any of them has is `Laudate Dominum omnes
  gentes` — which is also what the Ottobonianus margin gives, by a wholly
  independent route.
- **The corrections the claim carries.** `Timebunt gentes` does **not** return
  with the resumed Epiphany Sundays in November: a resumed Sunday borrows the
  Twenty-third Sunday's chants (§4.2, PRE-016). And the Communion's one other
  appointment, Lent IV Thursday, is the feria that also reads the **Fifteenth**
  Sunday's Gospel, so a single Lenten Mass holds together what the two September
  Sundays hold apart (PRE-017).
- **Limits that must travel.** The AMS results are the gregorien.info
  database's report of Hesbert and not Hesbert's page, with a reconstructed
  siglum key (§6.4). The registry measurements are a repository derivative, not
  a facsimile collation, and no page-image control was run for any second
  appointment. The Ottobonianus Alleluia cues are bracketed by Wilson as
  later-hand and **what the brackets assert is not established** (§0.6). No chant
  repertory was reached (§5.7).

### 10.5 — C5. The chants depart from the psalter at four elements of five, and the one that does not is where the Mass's doctrine can be said in English

- **Ritual moments.** Introit, Gradual, Alleluia, Offertory, Communion, against
  the Epistle and Gospel's two incipit adaptations.
- **Textual observation (class 1), from `verified.md`.** Introit five
  departures, Gradual three, Alleluia one plus a stop, Offertory two plus a
  printed refrain the psalm has not, Communion **none** — every word the
  Clementine's, the antiphon made entirely by where it starts and stops.
- **What the scriptural sweep adds.** `copiósus in misericórdia` corresponds to
  no phrase in the tracked Clementine and breaks the psalm's own internal
  repetition; the added `mihi` gives Ps. 85:1 the petition-form `inclina aurem
  tuam mihi`, which the psalter carries at Ps. 16:6 alone, against the `inclina
  ad me aurem tuam` of Ps. 30:3, Ps. 70:2 and Ps. 101:3 — **a shared
  petition-form and not verbal identity**, the two verses differing elsewhere
  (§2.1); `in auxílium meum réspice` is
  verbatim Ps. 70:12, **a verse of this Mass's own Communion psalm**; the dropped
  `simul` is precisely the Ps. 69:3 doublet's reading, though the chant is not
  the Ps. 69 form. SCR-002, SCR-003, SCR-020, SCR-021.
- **What the reception sweep adds, and iteration 1 inverts what iteration 1's
  brief said here.** The iteration-1 statement was that **every** checked
  Father's lemma differs from the missal at the departed places. **It does not.**
  At **four of the five** chants Cassiodorus's lemma stands **with the missal**
  and against the tracked Clementine — `suavis ac mitis es … copiosus in
  misericordia`, `videbitur in maiestate sua`, `quia mirabilia fecit Dominus`,
  `Domine, in auxilium meum respice` — and at the Alleluia Theodoret's Greek
  carries the chant's `Dóminus` too. What remains true, and is still the sharpest
  control, is that **Augustine's** lemma differs at three places where the
  difference is load-bearing for what he says: `gloria` at the Gradual, `Sanavit
  ei` at the Alleluia's unsung half-verse, and the third form `in adiuvandum mihi
  respice` at the Offertory. And the Greek cuts the other way at two of the four:
  Theodoret's tense at the Gradual and his clause at the Offertory are the
  Clementine's and not the chant's. **§7.14 states the pattern and its four
  bounds, of which the first is that the obvious explanation was not verified.**
  PAT-002, PAT-003, PAT-004, PAT-019 to PAT-023, PAT-032, PAT-034.
- **What the English adds, with one constraint partly lifted.** The Douay renders
  the psalter and not the chant, so it does not answer `maiestáte` or `in
  auxílium meum réspice`; **the two Latin words on which the strongest
  cross-element arguments turn still have no English in the witnesses this guide
  may quote**, and any argument that turns on either must be made about the Latin
  explicitly and at the element. **What iteration 1 lifts is narrower and real**:
  Bellarmine's 1866 English, a registered public-domain witness, states the
  Gradual's two-appearings argument at the verse — "When he began to build up
  Sion he was seen in his lowliness … but when he shall come to pass judgment,
  then 'he shall be seen in his glory'" — so **the argument can be carried by an
  English quotation even though the word cannot**, his printed lemma still reading
  "glory". At the Offertory nothing changes: his English there is the Douay's
  "look down, O Lord, to help me". And Guéranger supplies publishable English for
  what the guide wants to say at the Collect, the Epistle, the Gospel, the Secret
  and the Postcommunion (§5.4). THE-016, THE-023, and `verified.md`'s four
  warnings.
- **Limits that must travel.** No derivation may be asserted for any departure:
  no Old Latin, Roman, Ambrosian or Mozarabic psalter is tracked (§5.8). The
  Communion's printed citation form `Ps. 70, 16-17 et 18` is exact and must not
  be normalised into a range.

### 10.6 — C6. The Epistle is the formulary's doctrinal centre, and it is the place where the tradition most visibly develops and divides

- **Ritual moments.** Epistle, with the Collect it answers and the
  Postcommunion's `rénova` and the Alleluia's `cánticum novum`.
- **Textual observation (class 1).** The pericope begins one verse before the
  sentence it completes and ends at the close of the letter's doctrinal half;
  every one of its petitions is that God give; every principal noun is a term
  Ephesians has already used; and it is a prayer to the Father, through the
  Spirit, that Christ may dwell. SCR-004, SCR-005, SCR-006.
- **Documented reception (class 3), and it is a chain, not a consensus.**
  Chrysostom takes the four dimensions as the extent of God's love figured by a
  solid body and **does not read them as the Cross**; Augustine reads them as the
  Cross in three works with three different sets of virtues; Aquinas holds three
  readings together and names the hidden depth **predestination**; and
  **Guéranger, the one commentator on this formulary, takes them of the mystery
  of Christ's indwelling and not of the Cross at all**, keeping the emphasis this
  claim needs — that it is God alone who strengthens the inward man enough to
  understand them. **So the cruciform reading is one of at least three positions
  the checked witnesses hold, and may not be printed as the reading.** §0.2,
  THE-009.
- **The Epistle's tie to C1.** Augustine's *Sermo* 165 expounds Eph. 3:13–18
  under the heading "deque gratia et libera voluntate, contra Pelagianos" and
  reads the Epistle's hinge as the very distinction the Collect prays: "Peto
  enim a vobis, propter arbitrium voluntatis: rogo det vobis, propter auxilium
  maiestatis" — where `auxilium` is the word the Offertory and Postcommunion of
  this Mass both use. THE-008.
- **The Alleluia's tie.** Augustine at Ps. 97:1 moves from new song to new man
  to inward healing, which is where the Epistle asks for strengthening
  (`in interiórem hóminem`) and what the Postcommunion asks for (`rénova`).
  THE-011.
- **Limits that must travel.** *Sermo* 165 covers 3:13–18 and **stops three
  verses short of the doxology**, and its remark that the day's readings agreed
  is about Augustine's own African order — the psalm sung there was Ps. 56:2 —
  and says nothing about this Roman formulary. The missal prints `sublímitas`
  where Augustine's text reads `altitudo` and he justifies the choice; the
  missal prints `intellégimus` against the Clementine. The outward-inward pairing
  of the Gospel's healing with the Postcommunion's petition is the guide's
  synthesis and licensed only to class 4 (THE-011). Gregory of Nyssa, the one
  named Greek voice in the cross-reading chain, was not verified.

---

## 11. Section-by-section evidence coverage

The `Reader-Facing Order` of `guidance/liturgy/roman-1962-propers.md` fixes the
sections a reader is given. For each that carries reader-facing content, this
section states whether the brief supplies the evidence that section needs.
**This is a statement of fact, not a bar cleared.** Two positions are recorded
as **not supplied**, with the corpora, languages and loci checked and the limit
reached; the guide carries that bound in place of the claim.

**Position 1 — Page 1: propers map and four senses. SUPPLIED.** All ten
elements with printed heading, reference, incipit and marginal number from
`propers/verified.md`; the scriptural or grammatical axis of each from §1 and
§2; a demonstrable connection for each from §1.1, §2 and §10. The four senses
are grounded: literal from §2's canonical contexts; allegorical from Augustine
at the Gradual (Sion built, the Judgment) and at the Alleluia (the new man) and
from Bede's `typice` at the Gospel; moral from Ambrose, Bede and Cyril on the
seating parable and from Augustine on the Introit's `humiliato appropinquat`;
anagogical from Augustine on `vidébitur in maiestáte sua` and from Bede's
eschatological reading of `Tunc erit tibi glória`, whose second, daily reading
§7.6 requires be kept beside it.

**Position 2 — Page 2: `Scriptural Date and Location`. PARTLY SUPPLIED, and the
part that is not is named.**

- **Dates: fully supplied and fully constrained.** §12 transcribes the corpus's
  answer for all seven appointed Scriptures, with `subject`, `relation`,
  `profile` and the source's own `label` carried so the author prints through
  `\chronology{subject}{relation}{label}` without asking again. Seven distinct
  passages, no repetitions to consolidate; in Catholic canonical order and then
  verse order they are Ps. 39:14–15, Ps. 70:16–18, Ps. 85:1/3/5, Ps. 97:1,
  Ps. 101:16–17, Luke 14:1–11, Eph. 3:13–21.
- **Composition place, first audience and life stage: NOT SUPPLIED, and this is
  unchanged after two iterations and two full sweeps.** No lane retrieved a
  source stating the place of composition, the first audience or the writer's
  life stage for any of the seven passages. What was checked: the
  Scripture chronology corpus, which answers date and setting only and is the
  sole place a biblical date may reach the page from; the tracked Clementine,
  Douay–Rheims, King James and Revised Version, read for text and context and
  not for introductions; and the reception corpora of §3.2, which expound and do
  not orient. **The limit reached is that the corpus's own cited sources — the
  Catholic Encyclopedia articles on Ephesians (`…volume-5…newadvent-05485a…`)
  and on St Luke (`…volume-14…newadvent-14530a…`), both registered artifacts —
  were opened by no lane for anything but their chronology labels.** Those two
  articles are the nearest route and would answer for the Epistle and the
  Gospel; nothing comparable was identified for the five psalms, and §12 records
  that the corpus's only composition claim for any of them is a boundary shared
  by the whole psalter. **The iteration-1 reception sweep does not fill this and
  was never going to.** What the four psalm commentators supply is a *hypothesis*
  about each psalm's speaker and setting — Theodoret's Sennacherib and Hezekiah at
  Ps. 85, his Babylonian captives at Ps. 101, Bellarmine's David with the bear and
  the lion at Ps. 70, Cassiodorus's Christ *ex forma servi* at Ps. 85 — and **that
  is reception, reported as what the source says and attributed to it, never as
  the passage's date, place or audience** (§12's rule; SCR-032). The route remains
  what it was: those two registered encyclopedia articles.
- **The Gospel's narrated event: NOT SUPPLIED, and the corpus forbids supplying
  it.** The corpus's status for the Gospel is `composition-only`; it carries no
  event assertion for Luke 14:1–11. **No date for the sabbath dinner may be
  supplied from a commentary, a chronological table or recall**, and the Date
  cell states that absence. The event's *location* — a chief Pharisee's house,
  on the sabbath, in the stretch of Luke's journey narrative between the third
  sabbath-healing controversy and the parable of the great supper — is a textual
  observation the brief does supply (SCR-015, SCR-016, SCR-042), and it is not a
  date.
- **Place in Israel's and salvation history: supplied only where the corpus
  supplies it.** The Communion's Ps. 70 carries a `historical-setting` (David's
  flight from Absalom) and two `superscription-setting` claims (the first
  captivity of Juda), and the Alleluia's Ps. 97 carries two `prophetic-referent`
  claims on the Nativity. **For the Introit, Gradual, Offertory, Epistle and
  Gospel the corpus carries composition only**, and the guide states that rather
  than filling it.

**Position 3 — `The Propers: Themes and Movement`, pages 3–4. SUPPLIED.** §10's
six claims are the argument, and §10's preamble states its shape and its own
limit. Three to five developed functional units accounting for every appointed
element can be drawn from C1, C2 and C6 with C5 supplying the textual spine;
C3 and C4 are historical orientation and belong in the commentary and the
terminal apparatus rather than in the thematic movement.

**Position 4 — The complete appointed text (research edition only).
SUPPLIED.** `propers/verified.md` holds the collated Latin of all ten elements,
the identified public-domain English of all ten, the divergence tables, and the
rights basis; §1 carries the four results that control what may be said about
it. Nothing here is this brief's to add.

**Position 5 — `The Propers: Detailed Commentary`. SUPPLIED for all ten
elements; for two, the patristic and saintly reception is a bounded negative
that a later witness partly fills.**

- Introit, Epistle, Gradual, Alleluia, Gospel, Offertory, Communion and Collect
  each have complete-context scriptural research (§2), at least one direct
  witness checked at its own work and locus, and — at every one of the five
  psalms, at the Epistle, at the Gospel and at the four dimensions — **more than
  one where they materially differ or develop the reading** (§0.2, §0.7, §2.6,
  §7.5, §7.7, §7.10 to §7.13).
- **This is the position `CON-REC-002` was raised against, and it is the one the
  iteration-1 join changes most.** At iteration 1 the psalm reception rested on
  one Latin Father, with Aquinas reaching the Offertory alone and **no Greek
  psalm commentary at all**. **It now carries four direct commentators at each of
  the five** — Augustine, Cassiodorus, Bellarmine and Theodoret — with Aquinas
  additionally at the Offertory and Jerome adjudicating the wording at the
  Offertory and the Communion, and **the Greek tradition sampled at every one**.
  The four materially differ at every element, which is what makes the section
  able to compare reasoning rather than stack names (§7.10 to §7.13). **The bound
  that remains is stated and is not a gap in this position**: Chrysostom's,
  Jerome's and Hilary's psalm works were not opened and **nobody knows whether
  they reach these psalms**; the Bellarmine reading is bounded to an abridged
  English; and Theodoret is one Greek voice (§3.2, §5.3).
- **Secret and Postcommunion: no patristic or saintly reception was found and
  none is supplied.** §2.9 and §5.2 record the bounded negative in the corpora's
  own names, and the guide carries that bound. **What iteration 1 adds is a
  formulary-level reading of both from Guéranger** — the Sacrifice as the
  immediate preparation for the Communion it produces, and the Postcommunion's
  effect on the body "both in this and in the next life" (§2.9, THE-040) — which
  is documented reception of a much later kind and must be cited as that. The
  brief also supplies their sacramentary provenance (§4.1), now read on Gerbert's
  own pages with his sigla; their text-critical state including the 1862 `et`
  before `rénova`; their relation to the Alleluia's `cánticum novum` and the
  Offertory's `auxílium` (§10.6, §1.1); and the question of how their two
  efficacy vocabularies relate, which Guéranger narrows and does not close
  (§7.9).

**Position 6 — `Source-Grounded Synthesis Across the Propers`. SUPPLIED.**
§10's six claims, each with its evidence classes and its limits named.

**Position 7 — `The Propers: Notable and Quotable`. SUPPLIED.** Five entries at
§8 with the complete citation bundle each — appointed text and locus, later use
and locus with creator, edition or datestamp, stable URL and access date,
relationship strength, wording check, context, translation and rights, cultural
payoff, limiting qualification and material negative results. **Eight further
candidates at §8.6** with the reason for non-selection and enough bundle to swap
one in; §5.5 and §5.6 record the negatives, including which appointed elements
produced nothing and why. **One selection changed at iteration 2** and §8's
preamble states why: Luke 14:11 gains an entry and Eph. 3:21 loses one.

**Position 8 — `The Propers: Interpretive Possibilities`. SUPPLIED.** Six
proposals at §9, each joining at least two precisely named appointed elements,
each grounded in a conjunction `precedent-search` reached, each carrying that
lane's classification unchanged and its own controlling limit; thirteen further
conjunctions disposed of at §9.7.

**Position 9 — `Sacramental Appendix`. NOT REQUIRED, and no evidence is
needed.** The profile requires it only where a ritual Mass is celebrated with or
specifically for a non-Eucharistic sacrament. This is a second-class Sunday of
the temporal cycle: `verified.md` records that pp. 397–398 print no ritual
prayer, blessing, seasonal substitution or alternative form. §7.9 notes that if
the guide wants a general answer on offered sacrifice against received
sacrament, that appendix is where such doctrine would belong, cited to its own
sources — but the profile does not require it here and this brief supplies none.

**Position 10 — `Appendix: Scope and Qualifications`. SUPPLIED.** Edition and
formulary identity and rank from `verified.md`; text-verification state from the
same; source scope from §3; included and excluded material from §4 and §5;
search limits from §3, §5 and §6; rights boundary from `verified.md` and §6.4;
material global qualifications from §6.2 and §14.

**Position 11 — `References`. SUPPLIED.** Every retained witness in §2, §4 and
§8 carries author, work, edition and exact locus sufficient to verify the claim
made on it; §6.2 records where the citation must be narrower than the obvious
form.

**Position 12 — `Generation Metadata`.** Mechanical; no evidence position.

**Summary of what is not supplied**, so that the author blocks on nothing they
could not have known here: **position 2's composition place, first audience and
life stage for all seven passages; position 2's narrated-event chronology for
the Gospel, which the corpus forbids being supplied at all; and position 5's
patristic and saintly reception of the Secret and the Postcommunion**, which
Guéranger partly fills at a much later date. Every other reader-facing position
has its evidence. **Two positions that were "not supplied" or "supplied under a
bar" at iteration 1 are supplied now**: position 5's psalm reception, which was
single-witness and is now four-witness in both traditions, and every position
that wanted Guéranger, whose bar is lifted (§7.1).

---

## 12. Scriptural chronology audit

Transcribed from
`src/claude/liturgy/roman-rite/1962/propers/temporal/56-sixteenth-after-pentecost/research/chronology.toml`,
which `resolve-context` wrote from the Scripture chronology corpus with
`tools/tpt proper-chronology record` and which nothing in this workflow may
edit. `schema = 2`, `calendar = "roman-1962"`, `mass = "pentecost-16"`,
`system = "vulgate"`, `profile = "catholic-comprehensive-v1"`,
`formulary = "appointed"`, `formulary_reason = ""`.

**Re-read at iteration 1 and unchanged.** `scripture-context` re-read the file
and re-ran `tools/tpt proper-chronology loci --document
liturgy/roman-rite/1962/propers/temporal/56-sixteenth-after-pentecost`, which
reproduces the element table exactly and prints `(no scripture)` against the
Collect, the Secret and the Postcommunion; the transcription below is therefore
current as well as faithful. SCR-031, SCR-032.

**This record is the whole of what this brief may say about when a passage was
written or when what it tells of happened.** No lane finding, commentary or
chronological table may add to it. **This bites hardest at iteration 2**, because
the sweep that answered `CON-REC-002` returned four commentators with historical
hypotheses about every one of the five psalms — Theodoret dating Ps. 85's
occasion to Sennacherib's assault and Ps. 101's to the Babylonian captivity,
Bellarmine reading Ps. 70 of David's own boyhood, Cassiodorus reading Ps. 85 of
Christ in the assumed humanity. **Every one of those is reception**: it is
recorded in §2 as what that source says, attributed to it, and **never as the
date or setting of the passage**. A lane that reported a date the record does
not carry reported **reception**, and it is recorded in §2 as what that source
says, attributed to it, and never as the date of the passage.

For every element below, `publication_claims` — the across-all-loci
intersection the generated one-cell annotation may display — is **identical to
`claims`**. Every claim reaches its loci by inheritance (`inherited = true`).
`label` is the source's own words and is the only value a manually authored
guide may display; `date` is the normalized form and is recorded here only so
the two are not confused. **No element of this formulary is
`undated-in-tradition` or `research-pending`.**

### 12.1 Introit — `refs = ["Psalm 85:3, 5", "Psalm 85:1"]`, `loci = ["Ps.85.3", "Ps.85.5", "Ps.85.1"]`

`status = "composition-only"`, `reason = ""`;
`publication_status = "composition-only"`, `publication_reason = ""`. One claim.

- `relation = "composition"`; `subject = "critical.psalms.latest-composition-boundary"`;
  `title = "The latest composition boundary shared by the Psalms"`;
  `label = "before the Maccabean period, around 165 B.C.; no individual psalm can be dated securely"`;
  `date = "before c. 165 B.C."`; `precision = "boundary"`;
  `disposition = "preferred"`; `answerability = "answerable"`;
  `basis_class = "catholic-critical"`; `profile = "catholic-critical-v1"`;
  `sources = ["passage.united-states-conference-of-catholic-bishops.new-american-bible-revised-edition.english-usccb-web-2026-07-28.psalms-introduction"]`.
  Reaches Ps.85.1, Ps.85.3 and Ps.85.5, each `inherited`, `scope = "Ps"`.

### 12.2 Collect — `refs = []`, `loci = []`, `status = ""`

**The element cites no Scripture and carries no assertion.** SCR-031 confirms
this independently against `tools/tpt proper-chronology loci`, which prints
`collect (no scripture)`. Page 2 carries no dossier for it.

### 12.3 Epistle — `refs = ["Ephesians 3:13-21"]`, `loci = ["Eph.3.13"…"Eph.3.21"]`

`status = "composition-only"`; `publication_status = "composition-only"`. **Two
claims, both `disposition = "disputed"`, both standing side by side.**

- `relation = "composition"`; `subject = "composition.epistle-to-the-ephesians"`;
  `title = "The Epistle to the Ephesians"`;
  `label = "a period between 58 and 63"`; `date = "58 A.D. to 63 A.D."`;
  `precision = "interval"`; `answerability = "answerable"`;
  `basis_class = "traditional-catholic"`; `profile = "catholic-traditional-v1"`;
  `sources = ["artifact.catholic-encyclopedia.volume-5.new-york-1909.newadvent-05485a-66d722ae"]`.
- `relation = "composition"`; same `subject` and `title`;
  `label = "(Philemon; Colossians; Ephesians; Philippians), 61"`;
  `date = "61 A.D."`; `precision = "year"`; `answerability = "answerable"`;
  `basis_class = "traditional-catholic"`; `profile = "catholic-traditional-v1"`;
  `sources = ["artifact.catholic-encyclopedia.volume-11.new-york-1911.newadvent-11567b-bff0dda8"]`.

Both reach all nine appointed loci, each `inherited`, `scope = "Eph"`.

### 12.4 Gradual — `refs = ["Psalm 101:16-17"]`, `loci = ["Ps.101.16", "Ps.101.17"]`

`status = "composition-only"`; `publication_status = "composition-only"`. One
claim: the psalms composition boundary of §12.1, verbatim in every field,
reaching Ps.101.16 and Ps.101.17, each `inherited`, `scope = "Ps"`.

### 12.5 Alleluia — `refs = ["Psalm 97:1"]`, `loci = ["Ps.97.1"]`

`status = "dated"`; `publication_status = "dated"`. **Three claims.**

- The psalms composition boundary of §12.1, verbatim, reaching Ps.97.1
  `inherited`, `scope = "Ps"`.
- `relation = "prophetic-referent"`; `subject = "life-of-christ.nativity"`;
  `title = "The Nativity of Our Lord"`;
  `label = "the year of Rome 750 which he styles 3 B.C."`; `date = "3 B.C."`;
  `precision = "year"`; `disposition = "disputed"`; `answerability = "answerable"`;
  `basis_class = "reported-traditional"`; `profile = "catholic-traditional-v1"`;
  `sources = ["artifact.catholic-encyclopedia.volume-3.new-york-1908.newadvent-03738a-5eb03e5b"]`.
  Reaches Ps.97.1 `inherited`, `scope = "Ps.67 Ps.95 Ps.96 Ps.97"`.
- `relation = "prophetic-referent"`; same `subject` and `title`;
  `label = "probably the year 7 B.C."`; `date = "about 7 B.C."`;
  `precision = "approximate-year"`; `disposition = "disputed"`;
  `answerability = "answerable"`; `basis_class = "traditional-catholic"`;
  `profile = "catholic-traditional-v1"`;
  `sources = ["artifact.catholic-encyclopedia.volume-3.new-york-1908.newadvent-03731a-f5f96f04"]`.
  Reaches Ps.97.1 `inherited`, `scope = "Ps.67 Ps.95 Ps.96 Ps.97"`.

### 12.6 Gospel — `refs = ["Luke 14:1-11"]`, `loci = ["Luke.14.1"…"Luke.14.11"]`

`status = "composition-only"`; `publication_status = "composition-only"`. **Two
claims, both `disposition = "disputed"`.** The corpus carries **no event
assertion for this pericope**; see §11, position 2.

- `relation = "composition"`; `subject = "composition.gospel-of-luke"`;
  `title = "The Gospel of St Luke"`; `label = "About the year 70"`;
  `date = "about 70 A.D."`; `precision = "approximate-year"`;
  `answerability = "answerable"`; `basis_class = "traditional-catholic"`;
  `profile = "catholic-traditional-v1"`;
  `sources = ["artifact.catholic-encyclopedia.volume-14.new-york-1912.newadvent-14530a-0a19aa2c"]`.
- `relation = "composition"`; same `subject` and `title`;
  `label = "before the end of the Roman imprisonment, when the Acts was finished"`;
  `date = "before the Acts of the Apostles, and therefore before the end of the Roman imprisonment, and not as late as the destruction of Jerusalem"`;
  `precision = "relative"`; `answerability = "answerable"`;
  `basis_class = "traditional-catholic"`; `profile = "catholic-traditional-v1"`;
  `sources = ["passage.pontifical-biblical-commission.de-auctore-tempore-et-veritate-evangeliorum-marci-et-lucae.latin-aas-4-1912.responsa-i-ix"]`.

Both reach all eleven appointed loci, each `inherited`, `scope = "Luke"`.

### 12.7 Offertory — `refs = ["Psalm 39:14-15"]`, `loci = ["Ps.39.14", "Ps.39.15"]`

`status = "composition-only"`; `publication_status = "composition-only"`. One
claim: the psalms composition boundary of §12.1, verbatim, reaching Ps.39.14 and
Ps.39.15, each `inherited`, `scope = "Ps"`.

### 12.8 Secret — `refs = []`, `loci = []`, `status = ""`

**The element cites no Scripture and carries no assertion.** The loci report
prints `secret (no scripture)`.

### 12.9 Communion — `refs = ["Psalm 70:16-18"]`, `loci = ["Ps.70.16", "Ps.70.17", "Ps.70.18"]`

`status = "dated"`; `publication_status = "dated"`. **Four claims, carrying
three distinct settings at once.**

- The psalms composition boundary of §12.1, verbatim, reaching all three loci
  `inherited`, `scope = "Ps"`.
- `relation = "historical-setting"`;
  `subject = "israel.monarchy.david-flight-from-absalom"`;
  `title = "David's flight from the face of Absalom"`;
  `label = "when he fled from the face of his son Absalom"`;
  `date = "when he fled from the face of his son Absalom"`;
  `precision = "relative"`; `disposition = "preferred"`;
  `answerability = "answerable"`; `basis_class = "scripture"`;
  `profile = "catholic-traditional-v1"`; `sources = ["bible:douay-rheims:Ps.3.1"]`.
  Reaches all three loci `inherited`, `scope = "Ps.62 Ps.70"`.
- `relation = "superscription-setting"`;
  `subject = "israel.exile.first-captivity"`;
  `title = "The first captivity of Juda, under Joakim"`; `label = "A.M. 3398"`;
  `date = "3398 A.M."`; `precision = "year"`; `disposition = "alternate"`;
  `answerability = "answerable"`; **`basis_class = "reported-excluded"`**;
  `profile = "catholic-traditional-v1"`;
  `sources = ["passage.george-leo-haydock.douay-rheims-with-haydock-commentary.2014-loreto-feeney-memorial.psalm-70-captivities-usher-chronology"]`.
  Reaches all three loci `inherited`, `scope = "Ps.70"`.
- `relation = "superscription-setting"`; same `subject` and `title`;
  `label = "In the third year of the reign of Joakim, king of Juda"`;
  `date = "In the third year of the reign of Joakim, king of Juda"`;
  `precision = "relative"`; `disposition = "preferred"`;
  `answerability = "answerable"`; `basis_class = "scripture"`;
  `profile = "catholic-traditional-v1"`; `sources = ["bible:douay-rheims:Dan.1.1"]`.
  Reaches all three loci `inherited`, `scope = "Ps.70"`.

### 12.10 Postcommunion — `refs = []`, `loci = []`, `status = ""`

**The element cites no Scripture and carries no assertion.** The loci report
prints `postcommunion (no scripture)`.

### 12.11 Tensions the corpus preserves and does not resolve

Carried so the guide states them rather than smoothing them (SCR-032):

- The psalms boundary is `catholic-critical-v1` while **every other claim on
  this formulary is `catholic-traditional-v1`**.
- The Epistle, the Gospel and the Nativity claims are each `disputed` with
  **two labels standing side by side**.
- **The Communion carries three distinct settings at once** — Absalom, the first
  captivity by Daniel's dating, and Ussher's A.M. figure, the last
  `reported-excluded` — so a single Date cell for it **must choose among
  assertions the corpus itself leaves side by side**, and a `\chronodate`
  naming several elements may print only a claim the corpus makes at every
  element the cell names.
- The Alleluia's two Nativity claims reach Ps.97.1 through the corpus scope
  `Ps.67 Ps.95 Ps.96 Ps.97`, i.e. by inheritance across a group of psalms and
  not by an assertion made of Ps. 97 alone. The Communion's Absalom claim
  likewise reaches through `Ps.62 Ps.70`.

### 12.12 One fidelity note that is not a defect

The missal prints the Communion's citation `Ps. 70, 16-17 et 18`; this record
carries `Psalm 70:16-18`, as does the calendar index. **The loci are identical
and nothing resolves wrongly.** `verified.md` records the disposition: the guide
prints the missal's own form for the appointed text and may use the range where
it is speaking about verses.

---

## 13. Prior-production carry-forward

**Three sources were checked, in this order, before this brief was written, and
they were re-checked at each iteration. All three are silent about a prior
production of this target, and the three silences are of different kinds.**

1. **The leaf's own tracked record of what an evaluation left standing.**
   `src/claude/liturgy/roman-rite/1962/propers/temporal/56-sixteenth-after-pentecost/evaluations/blocking-findings-v1.toml`
   **did not exist when this brief was first written, and neither did the
   `evaluations/` directory**; the leaf then held two directories and three
   files. That was "nothing was ever written", not "nothing stands" and not "the
   record was deleted". **The file now exists and it is this production's own
   record, not a prior production's.** `tpt` rewrote it after this run's
   iteration-1 content evaluation and it states `run_id = "e4aebcbd941b6b1a"`,
   `stage = "content-evaluation"`, `iteration = 1`,
   `disposition = "CHANGES_REQUIRED"`, `standing = 12`, with **six observations**
   recorded beside the findings. **It was read in full at this iteration**, and
   what it holds is set out at §13.2. **Nothing in it comes from an earlier
   production of this target.**
2. **Run directories still on this machine.**
   `grep -l '"proper": "liturgy/roman-rite/1962/propers/temporal/56-sixteenth-after-pentecost"' build/tpt-runs/*/state.json`
   returns exactly one path, `build/tpt-runs/e4aebcbd941b6b1a/state.json`,
   **which is this run**, and `build/tpt-runs/` contains exactly one directory.
   **An empty or single-entry result from that grep is not by itself evidence
   that this target has no prior production**: `build/` is ignored, `make clean`
   deletes it, and `wt tidy` sweeps it without asking, so a finished run leaves
   nothing there once anyone has tidied.
3. **The `Prior-production carry-forward` section of the brief being
   rewritten.** At iteration 0 `research/scope.md` **did not exist before this
   stage wrote it**, so there was no inherited brief and no previous integrator's
   copy of this material. At iterations 1 and 2 the section being rewritten is
   **this stage's own from the previous iteration of this same run**, which is
   not a prior production either. Three lanes recorded the iteration-0 leaf state
   independently: COV-015, SCR-033 and PRE-002.

**What resolves the ambiguity in source 2**, and it is corpus evidence rather
than run-directory evidence: `precedent-search` swept 2,902 `.tex` and `.md`
files across `src/claude`, `src/gpt` and `src/common` and found **no Triptych
guide to this formulary in either provider tree**, and the GPT temporal series
stops at `55-fifteenth-after-pentecost` with no sixteenth-after-Pentecost leaf at
all (PRE-002, re-verified at iteration 1). A prior production that had reached
authoring would have left a `main.tex` and a `sections/` directory in the tracked
tree, and at iteration 0 neither was there; a prior production that had reached
this stage would have left `research/scope.md`, and it was not there either.
**The 24 files the leaf now holds are all this run's.**

**Conclusion, stated with the sources it rests on: no prior production of this
target is evidenced.** That rests on the tracked leaf's own contents and on the
prose-corpus sweep, **not on the grep alone**. **Nothing stands from an earlier
production of this target, and nothing was found to have been lost.**

### 13.1 Standing material from an adjacent production, which is not the same thing

Four items reached this join from a **sibling** leaf's published production and
are addressed to whoever works this formulary. They are recorded here, plainly
labelled as adjacent and not as prior productions of this target, because the
whole cost of the earlier production's evaluation would otherwise be spent twice.

- **A live, unresolved disagreement that this leaf owns.** claude leaf 54
  recorded that Wilson's Ottobonianus cue block — the disputed one — **is this
  Sunday's chant set**, that its two readings of the footnote attachment differ
  by two Sundays, and that "the page image controls and someone must go back to
  it". `precedent-search` states that the leaf which most naturally owns the
  revisit is this one. **Unresolved by the current research after two
  iterations**: no lane opened a page image of Wilson in either. §7.2, PRE-009.
- **A named categorical defect the collection carries and this leaf must not
  carry forward — and, at iteration 1, does not.** Six claude 1962 proper leaves
  define a `Governing thesis` box as a `format.tex` macro and fire it in
  `sections/20-themes.tex`; thirteen GPT leaves plus a ritual leaf carry the same
  box; six GPT leaves carry `Reading order.` as a run-in label and three carry
  `at a glance` in a box title. `guidance/editorial.md` 152–162 and
  `guidance/liturgy/roman-1962-propers.md` 303 and 380 make one occurrence a
  categorical structural defect, and `PROJECT-WORK.md`, 3,310 lines, mentions
  none of these labels or macros, **so the recurrence looks undetected rather
  than accepted**. **The leaf under work is clean**: a grep of its whole tree for
  the five forbidden labels returns one line, and it is this brief recording the
  nonconformity of other leaves; no `.tex` file in the leaf defines or fires such
  a macro, and it uses no `studybox` or `massbox` anywhere. **This entry is now a
  record of what must not be reintroduced.** And iteration 1 corrects the
  iteration-0 statement that `gpt 55` is the one 1962 leaf without it: **`gpt 39`
  is also without it and is the better model**, because it titles every box with
  a substantive claim — "The Collect supplies the rule of reading", "An
  exegetical guardrail", "Textual and historical boundary" — which shows what a
  conforming box title looks like rather than only that boxes can be omitted.
  PRE-003.
- **A shortfall in the file that is otherwise the best form precedent, and it was
  not copied.** claude leaf 54's `sections/50-interpretive.tex` is the conforming
  five-field proposal shape — Anchors, Mechanism, Fruit, What the
  element-by-element reading misses, Controlling limit, with the precedent
  classification kept out of the reader's body — but it carries **six proposals
  and only five "What the element-by-element reading misses" fields**, which the
  profile does not allow. **The leaf under work carries six of six**, and prints
  no `Precedent result` field. **Resolved by not reproducing it.** PRE-004.
- **A divergence recorded and expressly not adjudicated.** gpt 52 and gpt 55
  print a `Precedent result` field in the reader-facing interpretive section
  (five and six times respectively); gpt 51, 53, 54 and all six claude leaves
  print none. Whether an audit verdict in the body is audit-in-the-body is the
  content evaluator's call and neither `precedent-search` nor this stage makes
  it. PRE-004.

### 13.2 What this run's own tracked evaluation record holds, read at this iteration

Not carry-forward from an earlier production — source 1 above establishes there
is none — but read and recorded here because the file exists, because it is the
one durable record of this production's evaluation, and because **three of its
six observations name defects that originate in this brief and are repaired in
it**.

**Twelve blocking findings stand as of the iteration-1 evaluation**, of which
**one is this stage's** — `CON-REC-002`, `repair_target: research`, answered by
the seven-lane join this brief integrates (§0.7, §2, §3.2, §5.3, §5.11, §11
position 5) — and **eleven are `repair_target: authoring`**: `CON-EVI-006`,
`CON-EVI-007`, `CON-REC-003`, `CON-CIT-005`, `CON-CIT-006`, `CON-CIT-007`,
`CON-CIT-008`, `CON-PRO-001`, `CON-PRO-002`, `CON-PRO-003`, `CON-PRO-007`.
**None of the eleven is this stage's to repair and none is restated here**; they
are named so that the author knows the record exists and where it is.

**Three observations bear on this brief and are acted on here.**

- **`evidence-discipline`** observes that three of the four items
  `propers/verified.md` carries forward were repaired in the source library after
  that record was written, so the leaf's own text control now tells a reader four
  items are open where one is. §6.1 records the current state item by item and
  §14.5 carries it as the registration work it is. The observation notes that
  **this brief's own §14.5 anticipated it in terms**.
- **`reception-sweep`** observes, for the **second consecutive iteration**, that
  §5.1's material negative — that **no New Testament book quotes any verse this
  formulary appoints**, and its stated consequence — reaches the guide at one
  element of five and its consequence in neither edition. **The brief records the
  negative and the consequence at §5.1 and the lane calls it "the most useful
  negative of the join"**; that it is not carried into the prose is the authoring
  stage's, and the observation itself judges the recurrence to be a **missing lane
  criterion** rather than a fact about this document. It is repeated here so that
  it is impossible to miss.
- **`synthesis-argument`** observes that P6's stated mechanism is contradicted by
  the appointed text its own Anchors field names, and traces the tension to this
  brief. **§9.6's mechanism is corrected at iteration 2**, and the corrected form
  is the stronger one.

Three further observations are recorded and are not this stage's: within-edition
duplication between the brief synthesis and the integrated commentary in the
synthesis edition; a contribution string in `generation-metadata.tex` saying
thirteen divergences where the leaf collates fifteen, in a macro that renders
nothing to a reader; and the word "lane" — this workflow's own internal role name
— printed to a reader at `sections/90-scope.tex`.

---

## 14. Operational qualifications displaced from the PDF

### 14.1 Rights posture, by source class

- **The appointed Latin.** Settled once for the repository at
  `src/sources/inventories/missale-romanum-1962-facsimile-rights-v1.toml`:
  17 U.S.C. 103(b) plus a public-domain witness. All ten elements publishable;
  the three orations recorded `provenance_status = "collated"`,
  `publication_status = "permitted"`, `publication_basis = "public-domain"` in
  `roman-1962-proper-latin-provenance-v1.toml`, the Collect and Secret at
  confidence `high` and the Postcommunion at `medium` for the one reason
  `verified.md` now closes on the 1862 page image. The CMAA scan's own
  `rights_status` is `unresolved` and nothing rests on it.
- **The appointed English.** Douay–Rheims (Challoner) and the 1861 Cummiskey,
  both registered, both public domain by age. No translation under copyright is
  used, quoted or consulted.
- **Reception witnesses.** New Advent's markup is `rights_status = "unresolved"`
  and the underlying NPNF translations are United States public domain: quote
  short clauses and attribute the translation, never the host's presentation.
  The registered Cyril artifact's `rights_status` is `restricted` and the host
  modernizes Payne Smith's public-domain 1859 English: quote short and attribute
  to the translation, not to the host's markup. Fortescue's *The Mass* 1922 is
  registered `unresolved`.
- **Gallery witnesses.** §8's five entries rest on public-domain works
  throughout, with one exception: **Phillipson's 1962 note is in copyright**, is
  served openly by the Ohio State University Libraries, and must be quoted short
  and attributed (§8.4). Zimmern's 1910 English of Nietzsche is public domain in
  the United States and, her death falling in 1934, in life-plus-70 jurisdictions
  as well (§8.5). Of the unselected candidates, **CUL-007's 1958 newspaper is
  under 95 years old** and the Library of Congress's public-domain belief is
  qualified for possible third-party matter (§8.6).
- **Two reception witnesses carry a copyright bound that reaches wording.**
  **Jerome's *Epistula* 106** is held only in Metlen's **1937** English, whose
  copyright the edition record marks **unestablished**, permitting bounded fact
  and very short quotation: the Latin lemmata and the Greek words at issue are
  quotable, **the translator's English is not**, and a guide printing any of it
  should cite an original-language edition (§2.7, §2.8, PAT-034). **Theodoret's
  English (R. C. Hill) is in copyright and was not used**; the join reads the
  Greek with Migne's facing Latin beside it, and a guide quoting him must quote
  the Greek or Migne's Latin and say which (§6.2, PRE-036).
- **One route registered and deliberately unused on rights grounds**: the Adriaen
  CCSL 98 Cassiodorus, `rights_status = "restricted"`, from which nothing may be
  redistributed (§3.2).
- **The one standing rights control the maintainer owns** is Hesbert's, at §6.4,
  and nothing in this brief is published from it.
- **Unresolved rights questions for any text of this formulary: none**
  (`verified.md`, "Rights").

### 14.2 Evidence-state discipline

- **Optical layers locate and identify; they do not control wording.** Every
  sacramentary, missal and lectionary reading in §4 is from an uncorrected
  optical layer except the *Liber Comitis* headings, which were read on page
  images at high zoom precisely because the layer mangles the numerals.
- **The controlling facsimile's own text layer misled once in this
  formulary**, at `éxtrahet` / `extranet`, and `verified.md` settles it on the
  page image.
- **A missal payload that returns zero for a heading may still carry the
  formulary.** The Vatican typica 1604 layer returns 0 for `post pentecosten`
  and demonstrably carries this Sunday's whole formulary in one badly recognised
  stream. **It is usable for positives here and unusable for negatives**, and
  the correction runs one way only. PRE-007.
- **A running head in the Benziger optical layer names the following page.**
  The layer interleaves each page's head into the preceding column, which is why
  the two Lenten identifications at §4.2 were made from the Gospel pericope
  printed in the formulary and not from the adjacent head. LIT-008.
- **A whole-calendar view can be truncated silently.** The gregorien.info
  whole-AMS calendar is capped by the host at 500 rows and stops at AMS 93, so
  no independent listing of the post-Pentecost series could be got from it; that
  is recorded as a bound and not as evidence. LIT-014.
- **Cantus Index record pages load their concordance tables by a later
  request**, so only the "usual feast" line and the text are witnessed in the
  retrieved bytes. LIT-014.
- **Two silent failures found at iteration 1, both of which produce a plausible
  artifact rather than an error, and both of which a later run will meet.**
  (a) **gregorien.info returns HTTP 200 with a zero-byte body over HTTP/2**,
  because it emits an illegal `upgrade: h2` header: `curl` reports `http_code
  200`, `http_version 2` and `size_download 0`, and a retrieval loop that checks
  the status code rather than the byte count records a successful fetch of
  nothing. **Forced to HTTP/1.1 the host serves the correct bytes**, and all four
  registered gregorien.info artifacts then re-verify byte-identical. This lane's
  own first pass recorded all four as drifted before the cause was found. **Given
  §6.4, the natural misreading — that the source has gone away — would cost this
  collection its only route to the Hesbert material at the moment the rights bar
  leaves no alternative.** The correctable instruction is exact: **fetch
  gregorien.info with the client pinned to HTTP/1.1, and check `byte_size` and
  not only the status code.** COV-020.
  (b) **monumenta.ch answers a malformed `rumpfid` with HTTP 200 and a stub.**
  The psalm number is right-aligned in a fixed field of five characters after the
  pars number — `1,+++39`, `2,+++70`, `3,++101` — and getting the padding wrong
  returns a 1,017- or 1,266-byte document rather than an error. PRE-034,
  THE-036.

### 14.3 Retrieval traps, gathered

**Fifteen, of three species**, where iteration 1 counted eight of two.

**Numbering (seven).** The four at §0.5.1–4 — Vulgate against modern psalm
number, Hebrew against printed English verse number, New Advent's Vulgate psalm
with Hebrew verse, and the NPNF series title by Hebrew number — and the three
that arrived with the new psalm witnesses: Cassiodorus's Migne numerals, level at
three psalms, three ahead at Ps. 39 and one ahead at Ps. 97; Bellarmine's printed
numbers, one below the Vulgate at Pss. 39 and 101 and level at the other three;
and the PG 80 facsimile's **non-monotonic** page-to-column map, pp. 878–879
reprinting the opening of pp. 876–877.

**Extent (six).** The Lapide artifact stopping at Galatians (§6.3); the
registered Cyril artifact having been the wrong sermon range and the registered
Chrysostom artifact Homily 13, both since corrected (§6.1); the *Postilla super
Psalmos* breaking off at Psalm 54 (§2.1); **la.wikisource's Cassiodorus stopping
at Psalm 30 while printing a table of contents for all 150** (§3.2); the AMS
calendar's 500-row cap (§14.2); and the Guéranger PDF extraction stopping six
Sundays early, **which was a lane's extraction failure and not a property of the
artifact** (§7.1).

**Silent failure — a transfer that produces a plausible artifact instead of an
error (two, and both are new).** The gregorien.info HTTP/2 defect and the
monumenta.ch `rumpfid` padding, both at §14.2. The species already had two
members in this formulary — the 1962 facsimile's own text layer giving `extranet`
for `éxtrahet`, and `scripts/_psalms.py` answering for the wrong psalm when given
a Vulgate number — and **it is the class this brief most wants a later reader to
recognise**.

**And one citation trap that is none of the three**: the argument line and psalm
text printed above each exposition in the 1866 Bellarmine are the **Douay–Rheims**
and not Bellarmine, and the Ps. 85 line reads like a summary of this Mass's
Collect (§0.5).

### 14.4 What no gate can check

`check-content-preflight`'s `chronology-claims-supported` reaches the **Date
column and nothing else**. A year in the page-2 explanatory row, in the
commentary, or anywhere else in the guide is governed by the same rule and read
by a human reviewer; no check sees it. **Moving a figure out of the Date cell to
get it past the gate is the defect, not the workaround.** Nothing in this brief
supplies a biblical date from outside §12, and §11 records that the Gospel's
narrated event has no corpus date and that the guide states that absence.

### 14.5 Observations for the stages that own the manifest and the source records

Recorded here because no lane owns them and they would otherwise be lost.

- **`research/source-bindings.toml` now exists** — 1,005 lines, 103 bindings, all
  resolving, and the whole library validating with them — and it carries the four
  governing notes its header promises, including the Lapide extent control and the
  numbering hazards. **One line in it has been overtaken by this run's own work
  and should not be carried forward as written**: its `NOT REACHED` list names
  **Cassiodorus and Theodoret on the Psalms**, both of which have since been
  opened at all five appointed loci with receipts, and the Cassiodorus entry in
  particular names the work as unreached **without recording that the library
  already registers three editions of it**. That is a note for whoever next writes
  the file and not a defect in the guide. COV-015.
- **`source-registration`'s work at this iteration, receipted and mechanical.**
  **Fifteen passage records** at the five appointed psalms, five each for
  Cassiodorus, Theodoret and Bellarmine — ten against artifacts the library
  already holds and byte-verified this run, five against a registered edition
  whose per-psalm artifacts do not yet exist, all five of those receipted as HTML
  under `research-0001-lane-04-source-citation-coverage/cassiodorus/` (§0.7,
  §5.11, COV-016 to COV-018, COV-021). **A Guéranger passage record at printed
  pp. 356–371**, the artifact and edition being registered and the one existing
  passage belonging to a different Sunday (COV-012). **Gerbert, the *AAS* 47
  transcription, Brightman, Blunt and the 1920 and 1947 missal layers**, none
  registered (§6.1). **And a note on the gregorien.info edition record saying how
  the host must be fetched** (§14.2, COV-020) — no change to any of the four
  artifact records is needed, only that note.
- **What `source-registration` completed between iterations 0 and 1, so nobody
  redoes it**: Augustine's *Enarrationes* at all five psalms on three editions;
  Chrysostom's Homilies 6, 7 and 8 on Ephesians; Ambrose's *Expositio* books VII,
  VIII and IX; Cyril's sermons 99–109; the two 1862 leaves n425 and n426; the
  Postcommunion's `provenance_confidence` raised to `high`; the Cummiskey
  collect's marginal number corrected from 1575 to **1593**; and the 1861
  orations raised to `verified`. COV-002, COV-004 to COV-006.
- **One item of the four `verified.md` carries forward still stands**: the
  Communion's citation form flattened to a range in
  `src/sources/calendars/roman-1962/propers.yaml` and in
  `research/chronology.toml` line 889, where the missal prints `Ps. 70, 16-17 et
  18`. **It is a fidelity note and not a defect** — the loci are identical and
  nothing resolves wrongly — and it belongs to `source-registration` and to
  whatever generates the calendar index, **not to any research lane and not to
  the author**. It is worth carrying because it is the kind of flattening that
  becomes invisible once a generated record is quoted back: `et 18` records that
  the antiphon skips nothing but is cited as two units, and a range erases that.
  COV-002.
- **A currency problem the evaluator recorded and no lane owns.**
  `propers/verified.md`'s own "Discrepancies and open items carried forward" still
  lists four items as open where **one** is, three having been repaired in the
  library after that record was written, while `sections/90-scope.tex` beside it
  reports them correctly. **`verified.md` is another stage's file and this stage
  may not amend it**; the fact is recorded here so that whoever can, does. §6.1.
- **The reception discovery index reconciles to nothing mechanically and to six
  records by hand** (§5.10). It is a lead map and no row in it discharges a
  sweep — but the three rows this run acted on all named works the library already
  registers with fetchable editions, which is the strongest available argument
  that its null `work_id`s understate the collection rather than describe it.
- **A form the collection has and this run did not use**, recorded for whoever
  owns the leaf's research directory: three claude leaves keep a **per-psalm
  reception file** beside `scope.md`, whose fourth part is an
  **unreachable-resources list**. Had one been kept here, the la.wikisource dead
  end would have been recorded once instead of walked into. **Whether this leaf
  should gain such a file is not this stage's call**, and `precedent-search`, which
  is read-only, expressly decides nothing about the repository. PRE-039.
