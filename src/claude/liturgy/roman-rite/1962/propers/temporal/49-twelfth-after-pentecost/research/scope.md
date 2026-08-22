# Twelfth Sunday after Pentecost — Research Scope and Audits

Audit record for the canonical full research edition at
`liturgy/roman-rite/1962/propers/temporal/49-twelfth-after-pentecost` and its
mechanical `-synthesis` companion. Text control, collation method, witness
identities, and rights are in `propers/verified.md`; machine bindings are in
`research/source-bindings.toml`. This file records the sources, corpora and
languages searched, claim roles, material negative results, rejected and
unresolved leads, the reception matrix, and the audits the profile requires.
It is an audit record, not a diary. Compiled 2026-08-19/20.

Three per-element records sit beside this file and carry the loci, quotations,
rights notes and bounded negatives in full; this file states the guide-wide
audit and does not repeat them:

- `research/epistle-2-corinthians-3.md`
- `research/offertory-and-orations.md`
- `research/psalm-chants.md`

## Sources and corpora searched

**Text control.** CMAA facsimile of the 1962 Vatican typical edition (SHA-256
matched against the registered artifact before reading; printed pp. 392–393 =
PDF pp. 473–474, rendered at 300 and 600 dpi); Internet Archive page images of
the 1962 Benziger *editio iuxta typicam* (leaves n462–n464 = printed
pp. 386–388) as the independent second edition; the item's DjVuTXT OCR as a
finding aid only. Clementine Vulgate collation from the repository's tracked
Clementine chapter files (Ps 33, 69, 87, 103; Ex 3, 32, 33; Lk 10; 2 Cor 3).
Rights preexisting-material check against the tracked Pustet 1862 and Venice
1570 OCR text layers (loci in `propers/verified.md`).

**English.** Douay–Rheims (Challoner) tracked verse files for every scriptural
element (Ps 33:1–4; 69:1–6; 87:1–3; 103:12–16; Ex 32:9–15; Lk 10:22–38;
2 Cor 3:3–10 read with boundary verses); Cummiskey 1861 temporal-orations
transcription for the three orations, with the neighbouring Sundays' rows read
to prove the filing does not slip by one (the 11th's "abundance of thy
goodness" and the 13th's "increase of faith, hope, and charity" stand on
either side of this Sunday's rows at printed pp. 420–423).

**Reception.** Searched in Latin, Greek in translation, and English, across
the major reasonably accessible corpora relevant to each appointed passage:
Origen's Lucan homilies in Jerome's Latin; Irenaeus; Clement of Alexandria;
Ambrose on Luke; Augustine (Quaestiones Evangeliorum, Sermones, De doctrina
christiana, De spiritu et littera, Enarrationes); Cyril of Alexandria on Luke
(Payne Smith 1859); Chrysostom (Homilies on Matthew, on Second Corinthians);
Gregory the Great (all forty Homiliae in Evangelia enumerated, Moralia,
Regula pastoralis); Bede on Luke; Cassiodorus and Theodoret on the Psalms;
Basil; Cassian; the Rule of St Benedict; Ambrosiaster; Aquinas (Catena aurea,
Super II Cor, Summa theologiae); Bellarmine on the Psalms; Guéranger,
Schuster, Gihr; the Gelasian (Wilson 1894) and Gregorian (Wilson 1915)
sacramentaries for the orations. Catholic Encyclopedia (1907–13) and NABRE
introductions for historical orientation, the latter summarised, never
quoted. The repository's commentary-corpus index
(`src/sources/commentary/mass-commentary-corpus.yaml`, `pentecost-12` block)
was read as a lead list only; every retained witness was verified at its own
work and locus.

## Collation findings of record

1. **Introit vs Clementine.** The antiphon inserts `inimíci mei` (Clementine
   Ps 69:3 has none); the verse reads `qui cógitant mihi mala` against the
   Clementine's `qui volunt mihi mala`. Chant-psalter (Psalterium Romanum
   type) readings, verified as printed; no Psalterium Romanum witness was
   collated, so derivation is not asserted.
2. **Lk 10:27.** The missal prints `ex ómnibus víribus tuis` where the
   Clementine reads `ex omnibus virtutibus tuis`. Verified at 300 dpi on the
   facsimile and in the Benziger images. The Douay's "with all thy strength"
   renders either reading without showing which.
3. **2 Cor 3:4.** The incipit `Fratres:` displaces the Clementine's `autem`.
4. **Offertory.** Old-Latin (Septuagint-shaped) adaptation of Ex 32:11–14:
   five verified divergence classes tabulated in the commentary, including
   matter of the uncited v. 12 (`Parce iræ ánimæ tuæ`), `Iacob` for `Israël`,
   the milk-and-honey formula (accusative `lac et mel` = LXX, vs Clementine
   ablative `lacte et melle` at Ex 3:8/33:3), and the LXX shape of v. 14.
5. **Communion.** V. 13b inverted with an inserted vocative `Dómine`; v. 14a
   omitted exactly as the printed citation `13 et 14-15` declares.
6. **Edition differences (typical vs Benziger).** Eight tabulated in
   `propers/verified.md`; the substantive one for the singer is Benziger's
   printed repetition cue `Deus.` after the Gloria Patri.
7. **Venice 1570 leads (OCR-level only, not collated on images).** The 1570
   text layer shows the Gallican `qui volunt mihi mala` in the Introit verse
   and `tribue nobis, quesumus` in the Collect, against the 1962 readings.

### Divergences from the repository calendar index (for the index's owner)

`src/sources/calendars/roman-1962/propers.yaml` (`pentecost-12`) diverges from
the collated 1962 typical text at three points. The index is a lead, not a
source of record, and this leaf's `propers/verified.md` controls; the items
are recorded here so the index's owner can review them (this lane does not
edit the calendar index):

1. Offertory: index `Domini, Dei sui` — the typical edition prints
   `Dómini Dei sui` with no comma (Benziger agrees).
2. Offertory: index `Abraham, Isaac et Jacob` — the typical edition prints
   `Abraham, Isaac, et Iacob` with a comma before `et` (Benziger agrees).
3. Postcommunion: index `tribuat et munimen` — the typical edition prints
   `tríbuat, et munímen` with a comma (Benziger agrees).

## Reception matrix

One row per distinct appointed passage or material scriptural adaptation.
"Direct" means exegesis of the passage itself; "reuse" means doctrinal or
liturgical illumination from elsewhere. Verification state names what was
actually done; witnesses consulted only in copyrighted translations are
summarised in the guide, never quoted.

| Passage | Used by | Direct ancient exegesis checked | Medieval, Doctoral and later reception checked | How each retained witness is used | Works, loci, languages and corpora searched | Material negative results |
| --- | --- | --- | --- | --- | --- | --- |
| Ps 69:2–4 (Vulg) | Introit | Augustine, *En. in Ps.* 69 §§1–4, 7 (NPNF 1/8 "Psalm 70", with the Latin at augustinus.it); Cassiodorus, *Expositio* 69 (PL 70, coll. 493–494); Theodoret, *Interpretatio* 69 (PG 80, coll. 1415–1418, read on the registered facsimile) | Cassian, *Conf.* X.10 (NPNF 2/11); Rule of St Benedict cc. 17–18, 35 (Latin + Verheyen 1902); Bellarmine, O'Sullivan 1866, artifact p. 220 | Augustine for the whole-Christ voice and for the chant's own verb `cogitant`; Cassiodorus for the gloss on `intende`/`festina` and for the Cassian citation; Cassian and the Rule for the verse's passage into the Office; Theodoret as the Antiochene historical pole; Bellarmine for the accomplished liturgical fact | Latin (Migne, augustinus.it, thelatinlibrary), Greek with Migne's parallel Latin, English (NPNF, ANF, O'Sullivan 1866) | Augustine nowhere remarks the Ps 39/69 doublet — verified against the full Latin of both *Enarrationes* and both New Advent pages; Theodoret's Ps 69 columns carry no doublet remark either; Basil preached no homily on this psalm (PG 29 grep + corpus enumeration) |
| Ps 33:2–3 (Vulg) | Gradual | Augustine, *En. in Ps.* 33, two sermons (New Advent carries only the second; Sermo I read in Latin); Basil, *Hom. in Ps. 33* (PG 29, coll. 349–356); Cassiodorus, *Expositio* 33; Theodoret, *Interpretatio* 33 (PG 80, coll. 1101–1109) | Bellarmine, O'Sullivan 1866, artifact pp. 100–105 | Basil and Cassiodorus on `semper laus`; Cassiodorus's `non dixit, lege docti … sed mansueti` as the reception that answers the Gospel's lawyer; Augustine for the Vetus Latina `ferebatur in manibus suis` and the eucharistic reading; the four rival solutions to the Achimelech/Achis title, one per witness; Bellarmine on `always` | Latin (Migne PL 70, augustinus.it), Greek with Migne's Latin (PG 29, PG 80), English (NPNF, O'Sullivan) | No public-domain English of Basil's homily exists (NPNF 2/8 lacks the psalm homilies; FC 46 in copyright, neither quoted nor consulted); CE "Psalms" (1911) does not treat this title or the name problem; PL 70 column numerals for this psalm were not legible and are therefore not cited; NABRE note unreachable (403) |
| Ps 87:2 (Vulg) | Alleluia | Augustine, *En. in Ps.* 87 §§1–2; Cassiodorus, *Expositio* 87 (PL 70, col. 623 seen); Theodoret, *Interpretatio* 87 (PG 80, coll. 1567–≈1573) | Bellarmine, O'Sullivan 1866, artifact pp. 275–278 | The three Latin witnesses as the *vox Christi patientis* line, with the day/night pair progressively concretised; Theodoret as the documented counter-pole (exilic Israel, fallen human nature); the guide rules between them nowhere | Latin, Greek with Migne's Latin, English | No checked Father calls this psalm formally the darkest of the psalter — the observation is modern and is labelled so; NABRE note unreachable (403); Basil preached no homily on this psalm |
| Ps 103:13–15 (Vulg) | Communion | Augustine, *En. in Ps.* 103 Sermo 3 §§12–14 (= NPNF "Psalm 104" §§19–21); Cassiodorus, *Expositio* 103; Theodoret, *Interpretatio* 103 (PG 80, coll. 1693–1707) | Bellarmine, O'Sullivan 1866, artifact pp. 333–339 | Theodoret and Bellarmine as the literal-providential pole; Augustine for Christ the bread, the sober inebriation and the chrism; Cassiodorus for the explicit consecration language and for his cross-reference to Ps 33:6, the Gradual's own psalm | Latin, Greek with Migne's Latin, English | Cassiodorus's PL 70 columns for this psalm were not legible and are not cited; NABRE note unreachable (403); Basil preached no homily on this psalm; no witness was located that joins these verses to the Samaritan's oil and wine (the conjunction is published only as an exploratory proposal) |
| 2 Cor 3:4–9 | Epistle | Chrysostom, *Hom. in 2 Cor.* 6 §2 and 7 §§1, 5 (NPNF 1/12); Ambrosiaster ad 3:6–9 (PL 17); Origen, *De princ.* I.1.2 and *C. Cels.* VII.20 (ANF 4) | Augustine, *De doctr. christ.* III.5.9 and *De spiritu et littera* 4.6, 14.23–25, 19.34; Aquinas, *Super II Cor.* c. 3 lect. 1–2 and *ST* I-II q. 106 aa. 1–2; Bernard, *SCC* 7.5 (PL 183, 809B) | Origen for the hermeneutical equation; Chrysostom and Ambrosiaster for the juridical reading; Augustine against himself, with the later text's own `vel maxime` ruling printed; Aquinas for the mechanism (`occasionaliter`) and the radicalisation (even the Gospel's letter); Bernard for the verse's monastic afterlife; Augustine's *Quaest. Ev.* II.19 cross-read for `ministerium Veteris Testamenti` | Latin (Migne, Corpus Thomisticum, wikisource), Greek in translation, English (NPNF, ANF, public-domain *Summa*) | No Gregory the Great locus for 2 Cor 3:6 located (full-text *Moralia* search and domain-restricted searches); Origen's *De princ.* IV does **not** quote the verse (only the veil allusion at IV §6); Aquinas does **not** cite *De spiritu et littera* in *Super II Cor.* c. 3; Theodoret (PG 82, from col. 376) verified as reachable but **not** verified at sentence level, Hill's English in copyright — nothing printed as his words; Ambrose, *Exp. in Ps. CXVIII* full-text hit for `littera occidit` could not be pinned to a sermo, lead only |
| Lk 10:23–24 | Gospel | Cyril of Alexandria, Sermon 67 (Payne Smith 1859); Bede III (PL 92, 467C–D, registered passage record); Chrysostom, *Hom. 45 on Matthew* on the parallel Mt 13:16–17, labelled as a parallel | *Catena aurea* cap. 10 lect. 7 | Cyril for the distinction between spectacle and recognition; Bede for `beati oculi parvulorum` and the `reges magni`; Chrysostom for the disciples' own act and the prophets' `per speculum` | Latin, Greek in translation, Syriac in translation, English | Ambrose, *Exp. Luc.* VII passes from v. 22 to v. 25 — no comment on these verses (lemma scan of the whole book); no Augustine treatment located in the corpora checked |
| Lk 10:25–37 | Gospel | Origen, *Hom. 34 in Lucam* (Jerome's Latin, PL 26/wikisource); Ambrose, *Exp. Luc.* VII.69–84 (PL 15, 1717–1720); Augustine, *Quaest. Ev.* II.19, *Sermo* 131.6, *De doctr.* I.30; Cyril, Sermon 68; Bede III (PL 92, 467C–470D); Irenaeus, *Adv. haer.* III.17.3 and Clement, *Quis dives* 28–29 (ANF) | Gregory, *Moralia* XX, *Reg. past.* II.6, *Hom. in Ev.* II.18.2 (`custos` on Jn 8:48); *Catena aurea* cap. 10 lect. 8–9; Calvin's rejection (Pringle, CCEL); CE "Parables" (vol. 11, 1911); John Paul II, *Salvifici doloris* 28–30 | Irenaeus and Clement to date the Samaritan-as-Christ reading before Origen; Origen for the received scheme, his correction of it, and the `custos` etymology; Ambrose for `Non enim cognatio facit proximum, sed misericordia`; Augustine for the classic table, `semivivum`, and `adhuc curatur`; Cyril as the Greek dissenter who never allegorises; Gregory for wine-and-oil as discipline-and-mercy and for `custos namque humani generis venerat`; Bede for the governing both-senses rule; Calvin and *Salvifici doloris* as the two later poles | Latin, Greek in translation, Syriac in translation, English | No genuine Chrysostom treatment of the parable located; the *Catena*'s long "Chrysostom" extracts are margin-flagged *Hom. in loc. Ed. Lat.* and preface-assigned to an early imitator; Gregory's forty Gospel homilies contain no lection from this pericope (all forty enumerated); Titus of Bostra and Isidore absent from this pericope's chain |
| Ex 32:11–14 (Old-Latin chant adaptation) | Offertory | Augustine, *Quaest. in Hept.* II qq. 10, 141–149, and *De civ. Dei* XV.25; Chrysostom, *Hom. 16 on Romans*; Tertullian, *Adv. Marc.* II.26 | Gregory, *Moralia* IX.xvi.23 and XX.v.14; Verona/Gelasian/Gregorian transmission of the Mass-set; Johner (1940) pp. 296–297; Ott, *Offertoriale* (1935) no. 59; Palestrina 1593 and Lassus LV 858 | Augustine q. 143 both for the doctrine of penal "evil" and, decisively, for the Vetus Latina lemma that proves the chant's text-form pre-Jerome; q. 149 for `dilectio tua in illos intercedit mihi`; *De civ. Dei* for the guard-rail on divine anger; Gregory for intercessory boldness; Tertullian as the single checked witness for the Moses-as-type-of-Christ reading; Johner for the melody and for the same typology under this chant; Ott for the dropped verses; the settings for existence only | Latin (augustinus.it, thelatinlibrary, Wilson 1894/1915, Feltoe 1896), English (ANF, NPNF, Library of the Fathers), printed chant editions | The Septuagint was **not** collated: the LXX could not be quoted from a reachable source, so the guide names the Greek as the explanation of the chant's shape and quotes none of it (a Greek clause in an earlier draft was removed on 2026-08-20 for that reason); no printed Vetus Latina edition of Ex 32 consulted; no Jerome locus on Ex 32:32 verified (the "ad Algasiam" attribution fails against *Ep.* 121); the Secret is **not** in Feltoe's Verona collection; Gihr cites none of the three orations; no parody mass on this offertory verifiable; no `poenitet me` verse exists in Ott |

Second-century pre-Origen attestation of the Samaritan-as-Christ reading
(Irenaeus, Adv. haer. III.17.3; Clement, Quis dives 28–29) was verified in the
public-domain ANF translations and is used to correct the common attribution
of the allegory to Latin allegorising.

## Spot-verification of delegated research

Reception research was executed in delegated read-only lanes and integrated
only after spot-verification in this lane. Verified directly against the named
sources before use: Origen's presbyter-scheme and custos passages (wikisource
Latin, verbatim match); Ambrose VII.73–84 key sentences including the custos
etymology, the two-Testaments denarii, `Non enim cognatio facit proximum`
(wikisource Latin, verbatim); Augustine Quaest. Ev. II.19 complete table
(augustinus.it Latin, verbatim); Bede's rule and blessed-eyes passages
(wikisource Latin, verbatim, and hash-matched to the registered artifact —
passage record `iii-lk-10.23-37` added under the existing Bede edition);
Cyril Sermons 67–68 (tertullian.org, Payne Smith 1859, key sentences located
on the page); Calvin's refusal (CCEL, verbatim); the four notable-and-quotable
entries (see the audits below, each re-verified at its primary locus in this
lane).

## Notable-and-quotable audit

Retained entries (all four independently re-verified in this lane at the
stated loci on 2026-08-19):

1. **Lord Atkin, Donoghue v Stevenson [1932] A.C. 562 at 580.** Appointed
   wording: Lk 10:29 `Et quis est meus próximus?` / Douay "And who is my
   neighbour?". Verified verbatim in the Scottish Council of Law Reporting
   transcription (scottishlawreports.co.uk, Lord Atkin page 2): "The rule that
   you are to love your neighbour becomes in law you must not injure your
   neighbour; and the lawyer's question 'Who is my neighbour?' receives a
   restricted reply…". Relationship: explicit, self-announced ("the lawyer's
   question"). Turn: the parable's evaded question becomes the foundation of
   negligence law. Rights: UK judgment, quotable. Limit: Atkin cites no
   evangelist.
2. **Darley & Batson, "From Jerusalem to Jericho," JPSP 27.1 (1973) 100–108.**
   Appointed wording: Lk 10:30 route, exact in the title; "passed by."
   Verified in the article PDF (journal header p. 100; abstract; discussion
   p. 107 "literally stepped over the victim as he hurried on his way!").
   Turn: the pericope run as a controlled experiment on seminarians, hurry
   defeating piety. Rights: APA copyright — only short sentences quoted with
   citation. Limit: the abstract's "pass by" idiom is KJV-shaped; the Douay
   reads "passed by."
3. **Frankfurter, dissenting, U.S. ex rel. Knauff v. Shaughnessy, 338 U.S.
   537 (1950), at 548 and 550.** Appointed wording: 2 Cor 3:6 `líttera enim
   occídit` / "the letter killeth." Verified in the official U.S. Reports PDF
   (Library of Congress tile service). Turn: covenant theology conscripted as
   a canon of statutory construction, in favour of an excluded war bride.
   Rights: public domain. Limit: the maxim is the naturalised idiom, not
   Paul's argument.
4. **Monteverdi, Vespro della Beata Vergine (Venice: Amadino, 1610), opening
   versicle-response.** Appointed wording: the Introit's Ps 69:2 verbatim.
   The Orfeo-toccata borrowing verified in Jennifer More Glagov's 2016 Music
   of the Baroque programme note; the work and print are public domain. Turn:
   the liturgy's barest cry for help delivered as a ducal fanfare. Limit: the
   register reading is the standard musicological account of a documented
   self-borrowing, not a recorded intention; the versicle's hour-opening use
   belongs to the Office (and not to Matins, which opens otherwise).

Located, verified, and excluded (with reasons; these are not defects in the
entries above):

- **Thatcher, Weekend World, 6 Jan 1980** (Margaret Thatcher Foundation doc
  104210, verified verbatim in this lane: "No-one would remember the good
  Samaritan if he'd only had good intentions; he had money as well," closing
  exchange with Brian Walden). Excluded because the dependence is narrative
  (the Samaritan's money), not an exact appointed phrase; the gallery's
  standard here is a verbal link.
- **MLK, "I've Been to the Mountaintop" (3 Apr 1968)** — the reversed Jericho
  question. Excluded: retells rather than quotes, and the estate's copyright
  is enforced; recorded as a lead.
- **George W. Bush, First Inaugural (2001)** "we will not pass to the other
  side" (Avalon Project). Excluded: KJV idiom, mildest register turn.
- **"Good Samaritan" statutes** (California H&S 1799.102; Minnesota 604A.01;
  Code pénal art. 223-6). Excluded: the parable lives in the statutes'
  nickname, not their wording; the voluntariness-inversion observation is
  kept as a lead.
- **Franklin's "beer is proof God loves us"** — apocryphal; the genuine
  Morellet letter riffs on Cana, not Ps 103:15 (Quote Investigator trail).
  Bounded negative for the Communion verse.
- **Krzhizhanovsky, "The Letter Killers Club"** — title echo of 2 Cor 3:6
  plausible but no checkable documentation of the allusion located; lead
  only.
- **Ex 32:14 "the Lord repented"** — no verifiable non-theological afterlife
  located within scope; bounded negative.
- **Gradual and Alleluia wording** — no register-turning afterlife of the
  exact wording located; gospel-music settings of "I will bless the Lord at
  all times" are devotional and excluded by the profile.
- Hansard and BAILII were intermittently unfetchable; the Scottish Law
  Reports transcription and the U.S. Reports PDF were used instead. On
  2026-08-20 the `scottishlawreports.co.uk` and `sclr.scot` hosts presented an
  expired TLS certificate; the reference therefore prints the reporter's
  `scottishlawreports.org.uk` judgment index, and the controlling locus
  remains the printed report, [1932] A.C. 562 at 580.

## Interpretive-proposal audit

Five proposals are published in `sections/50-interpretive.tex`. Each names its
anchors, mechanism, fruit and controlling limit there; this audit records the
targeted precedent search and the novelty classification.

**Search boundary, stated once and applying to all five.** Two boundaries were
used. (a) *The guide's checked corpus* — every work named in the reception
matrix above, searched for the proposal's own conjunction rather than for
either of its anchors separately. (b) *A targeted open-web search* run on
2026-08-20 for each proposal's distinctive conjunction, in English, against the
general web; devotional and homiletic commentary on this Sunday was included.
Search-engine summaries were treated as leads only: a precedent counts as
located only where an identifiable source makes the connection. Neither
boundary supports a claim that a connection is universally unknown,
unprecedented, or first.

1. **Half-dead is a diagnosis of exactly what the letter can reach.**
   Anchors: Lk 10:30 `semivivo relicto` with Augustine's gloss (*Quaest. Ev.*
   II.19), and 2 Cor 3:6 with Aquinas's `dat solam cognitionem peccati`
   (*Super II Cor.* c. 3). Mechanism: the line Augustine draws through the man
   (alive in the part that can know God) is the line Aquinas draws through the
   letter's competence (knowledge without healing). Precedent result: **near
   analogue located.** The reading of priest and Levite as the Law that could
   not save is standard and is already published in the commentary from
   Augustine's own words; devotional summaries of the parable also pair the
   Law with "knowledge, not the doing away, of sin." What was *not* located is
   any source joining Augustine's anthropology of `semivivus` to Aquinas's
   mechanism of the letter. Controlling limit as published: the two authors are
   not in conversation, and Augustine's point at `semivivum` is the survival of
   the image, not the failure of written law.
2. **The road supplies two of the three medicines; the rail supplies all
   three.** Anchors: Lk 10:34 `infundens oleum et vinum`; Ps 103:14–15 as sung
   at the Communion; Cassiodorus's cross-reference to Ps 33:6. Precedent
   result: **near analogue located.** The sacramental reading of the
   Samaritan's oil and wine (chrism and the Blood) is common in devotional
   commentary on this Sunday and was located there by the open-web search; the
   sacramental reading of the Communion's wine and oil is Cassiodorus's own and
   is published in the commentary. What was not located is any source that
   joins the two lists or observes that the Communion adds the bread the
   roadside could not carry. Controlling limit as published: the orders differ,
   the psalm's triad is agricultural with no wound in it, and the early
   pairing of these chants with this Gospel proves association, not purpose.
3. **The day's danger is a verb of thinking.** Anchors: the Introit's
   chant-psalter `cogitant` (against the Clementine `volunt`), 2 Cor 3:5
   `cogitare aliquid a nobis`, and the lawyer `volens iustificare seipsum`.
   Precedent result: **not located in the checked corpus.** The open-web search
   returned commentary on the Introit and on the Epistle separately and no
   source that joins them on this verb; Augustine's gloss on `cogitant` is
   published in the commentary as reception of the psalm alone. Controlling
   limit as published: `cogitare` at 2 Cor 3:5 renders a verb of reckoning, not
   of plotting; the lawyer's verbs are different words; and the chant's reading
   is a fact of psalter history, not a choice made for this Sunday.
4. **An unanswered cry, then someone else's prayer with the answer printed in
   it.** Anchors: the Alleluia (Ps 87:2) and the Offertory (Ex 32:11, 13, 14),
   with Augustine's `dilectio tua in illos intercedit mihi` supplying the
   mechanism of substituted petition. Precedent result: **not located in the
   checked corpus.** The open-web search located the two chants named together
   only as an assignment list (they also stand together on one postconciliar
   Sunday) and no source reading their sequence as answered-versus-unanswered
   prayer. Controlling limit as published: only Ps 87's opening confession is
   appointed, so the psalm's darkness is supplied by the reader; the Latin
   phrases differ; Theodoret's reading makes the lament Israel's; and chant
   assignment is commonly musical and cyclical.
5. **The office named by an etymology is asked for as an effect of
   Communion.** Anchors: the `custos` etymology in Origen, Ambrose, Augustine
   and Gregory, and the Postcommunion's `munimen`. Precedent result: **not
   located in the checked corpus.** The open-web search returned the etymology
   and the Postcommunion separately, with no source joining them; the only
   text linking them was a search-engine summary, which is not a source.
   Controlling limit as published: `custos` and `munimen` are unrelated words
   with unrelated images, the etymology is contested reception rather than
   settled philology, and the oration's own transmission carries no Gospel.

No proposal in this section is offered as historical intent, attributed
teaching, or documented reception, and the section opens with that notice.

## Historical-orientation sources (page-2 dossiers)

- **Luke:** Catholic Encyclopedia, "Gospel of Saint Luke" (C. Aherne, 1910):
  Lucan authorship from unanimous external witness, composition dated before
  A.D. 63. NABRE introduction (summarised): traditional attribution
  maintained, non-eyewitness, ca. 80–90, largely Gentile audience. Event
  geography: the Jerusalem–Jericho descent; Jerome, Ep. 108.12 (Adummim, "the
  Place of Blood"); Basil's geography via the Catena at v. 30.
- **2 Corinthians:** Catholic Encyclopedia, "Epistles to the Corinthians"
  (1908) and NABRE introduction (summarised): written from Macedonia on the
  third journey, c. A.D. 57; the Exodus 34 background (Moses' shining face,
  tables of stone) is the passage's own narrated allusion.
- **Exodus:** CE "Pentateuch" (1911): the 1906 Pontifical Biblical Commission
  responses on Mosaic authorship (secretaries, sources, post-Mosaic additions
  permitted); the documentary hypothesis reported as the modern judgment. CE
  "Golden Calf" (Driscoll, 1909) for the narrated event. The Exodus's date is
  left as the open fifteenth-vs-thirteenth-century question; nothing here
  settles it.
- **Psalms:** Vulgate superscriptions verified in the tracked Clementine and
  Douay files (Ps 69:1 "in rememorationem…"; Ps 33:1 the Achimelech title
  with the 1 Kings 21 narrative discrepancy — the narrative names Achis of
  Geth; Ps 87:1 sons of Core / Eman the Ezrahite; Ps 103:1 "Ipsi David").
  CE "Psalms" (1911) and NABRE notes (summarised) for
  traditional-vs-modern judgment. Ps 69's near-identity with Ps 39:14–18 is
  the psalter's own doublet.

## Bounds and unresolved items

- Theodoret was consulted for the psalms in the PG 80 facsimile identified in
  the source library (remote artifact, hash recorded) and for 2 Corinthians
  in PG 82 scans; Robert Hill's modern English translations are in copyright
  and are summarised, never quoted. Column ranges are printed only where they
  were actually seen.
- Cassiodorus's ACW translation (Walsh) is in copyright; he is quoted only
  from the public Latin or summarised.
- No exhaustive search of Syriac originals, chant manuscripts, untranslated
  homiliaries, subscription databases, or current specialist monographs is
  claimed; negatives above are bounded by the corpora named.
- The library does not presently hold artifacts for: Ambrose, Expositio in
  Lucam Book VII (only Liber X is registered under the existing edition);
  Augustine's Enarrationes on Vulgate Pss 33, 69, 87, 103 (the registered New
  Advent artifacts cover other psalms); Cassiodorus on these four psalms;
  Origen's Lucan homilies; Cassian; the Rule of St Benedict; Irenaeus;
  Clement of Alexandria; Cyril of Alexandria's Luke sermons 66–80. These were
  verified at stable public loci named in the references; central registration
  is left to the source library's owner, since this lane's boundary does not
  include creating work, edition, or artifact records.
- The commentary-corpus index's `pentecost-12` lead list includes works not
  retained here (Nicholas of Lyra, Cornelius a Lapide on 2 Cor, Denis the
  Carthusian, Hugh of Saint-Cher, Peter Lombard, Albert the Great, Euthymius
  Zigabenus, Bruno the Carthusian, Hilary on Ps 69, Walafrid's Glossa). These
  remain unverified leads: no reasonably accessible public edition was
  examined for them within this lane's bounds, and nothing is cited from
  them.

## Decisions of record in the completion pass (2026-08-20)

1. **Reader order.** The profile's fixed macro-order and its publication gate
   require the dossier sheet alone on physical page 2 and the two-page thematic
   movement on pages 3–4; the complete appointed formulary is not a member of
   that macro-order, and the profile's "full research sequence" sentence and its
   Reader-Facing Order list appear to place it differently. The completion pass
   first printed it **after** the element-by-element commentary and referred the
   reader forward to it.

   That reading was corrected on 2026-08-20 after the coordinator checked the
   current-standard exemplar. `src/gpt/liturgy/roman-rite/1962/propers/temporal/24-tenth-after-pentecost/main.tex`
   prints the complete appointed formulary **before** the element-by-element
   sweep, which satisfies the gate and the "full research sequence" sentence at
   once; `23-ninth-after-pentecost` is legacy under the profile's own rule and
   is not the model. This leaf now follows the exemplar — the formulary opens at
   page 5 and the element-by-element commentary follows it — so that leaves 25,
   26 and 27 agree with each other and with the exemplar, and
   `\latinpolicynote` refers back to it rather than forward. Both editions were
   re-proved against the gate after the change:
   `triptych:brief-synthesis:start/end/next` resolve to pages 3, 4 and 5 in both
   `.aux` files, with zero overfull boxes, and every page of both editions was
   re-inspected. The profile prose that invited the divergent reading is
   recorded for the maintainer as a clarification request.
2. **Page-1 and page-2 compression.** The map, four-senses and dossier prose
   were tightened until page 1 carries the complete map with exactly four
   senses rows and page 2 carries the complete seven-passage dossier alone, at
   the profile's fixed table geometry. No dossier field, event row or evidence
   was dropped to achieve it; the compression is verbal. This is the redesign
   the profile permits when the complete inventory will not otherwise fit.
3. **A Greek quotation withdrawn.** An earlier draft of the Offertory
   commentary quoted a Septuagint clause. No Greek witness was collated in this
   lane and the LXX could not be quoted from a reachable source, so the clause
   was removed and replaced by a Latin-only collation with the Greek named as
   the explanation of the chant's shape. Nothing in the published guide is
   quoted from Greek that was not read.
4. **Catholic Encyclopedia volume years corrected.** Two references dated
   "1913" were corrected to 1911 ("Offertory" and "Parables", both vol. 11).
   The claim that the Roman psalter remained in liturgical use after the
   Gallican revision is now cited to the article "Breviary" (vol. 2, 1907) and
   quoted from it verbatim, having been verified at that article.
5. **Two typesetting primitives added to the leaf's `format.tex`**: the
   `correctionstable` environment used by the commentary, and Unicode
   declarations for U+01FD/U+01FC so that the missal's accented ligature in
   `quǽsumus` is set as printed rather than silently normalised.
6. **Guéranger was read and is not cited.** His chapter on this Sunday
   (vol. 11, pp. 288–307) was consulted; no claim published in this guide rests
   on it, so it is absent from the references, as the profile requires.

## Operational qualifications displaced from the PDF

- The guide treats the reusable temporal formulary only; occurrence,
  commemorations, particular calendars, and celebration-mode branches for any
  civil year belong to the assembly workflow.
- Internal release and distribution states are not reader-facing and appear
  nowhere in the publication.
