# Ninth Sunday after Pentecost — Research Scope

**Provider:** Anthropic Claude
**Last updated:** 2026-07-25

Audit record for the published guide. It holds the search boundaries, source
roles, competing judgments, negative results, and operational qualifications
that the PDF compresses or omits. The complete collated Latin, its witnesses,
and the edition-difference table live in
[`../propers/verified.md`](../propers/verified.md); the raw finding aid is
[`../propers/retrieved.txt`](../propers/retrieved.txt).

## 1. Formulary identity and text control

- The work is the temporal formulary printed `DOMINICA NONA / post Pentecosten`,
  `II classis`, on printed pp. 388–389 of the 1962 *Missale Romanum*, editio
  typica, marginal nos. 1522–1531. Green follows the general rubrics for
  Sundays after Pentecost; it is **not** printed on those pages, and the guide
  says so rather than treating the colour as a reading of the formulary.
- The controlling witness is the CMAA facsimile PDF (SHA-256
  `648fdb…3518a`), PDF pp. 469–470. The downloaded copy was hashed and matched
  the digest registered in the repository's source library **before** any
  reading was taken from it. Collation was done at 300 dpi for the whole page
  and 600 dpi for every disputed letter and accent, on 2026-07-25.
- A **second edition** was collated independently: the 1962 Benziger *editio
  iuxta typicam*, printed pp. 382–383, from the page images of Internet
  Archive item `MissaleRomanum1962RomanMissalColorLatin`, leaves `n458`–`n460`.
  Benziger is a different edition, not a second photograph of the Vatican
  book, so the differences found are edition differences, not doubtful
  readings. The scan carries a `FATIMAMOVEMENT.COM` footer watermark.
- The Internet Archive DjVuTXT OCR (SHA-256 `2a2da4…85ce`) located the
  formulary and controls nothing. Its recognition failures (`II claasis`,
  `raciet`, `Cnc6de`, `Prrcfatio de Sama Trinitate`, `DOMINICA DECEMA`) are
  preserved deliberately in `retrieved.txt`.
- **Scope exclusion.** This is a reusable study of the formulary, not an
  assembly sheet for a civil date. Occurrence, commemorations, particular
  calendars, and celebration-mode branches are outside it and were not
  researched.

### Edition differences found (published in the guide)

| Place | Vatican typica | Benziger iuxta typicam |
| --- | --- | --- |
| 1 Cor. 10:8 | `vigínti tria mília` | `vigínti tria míllia` |
| Lk. 19:45 | `cœpit eícere` | `cœpit eiícere` |
| Introit close | `℣. Glória Patri.` | `℣. Glória Patri. Ecce Deus.` |
| Secret conclusion | long form to `in unitáte` | `Per Dóminum.` |
| Collect, Postcomm. conclusion | `Per Dóminum nostrum.` | `Per Dóminum.` |
| Communion reference | `Io. 6, 57` | `Ioann. 6, 57` |
| Heading style | `Ant. ad …`, two-line title | `Antiphona ad …`, `POST PENTECOSTEN` in capitals |

No reading in either witness was unclear enough to need a third witness, and
nothing was blended.

### Chant text against the Bible text

Three divergences between the appointed chants and the Clementine Vulgate were
verified directly and are published as textual observations:

1. Introit antiphon omits `enim` at Ps. 53:6 (`Ecce Deus` vs `Ecce enim Deus`).
2. Introit psalm verse reads `líbera me` at Ps. 53:3 where the Clementine
   reads `judica me`.
3. Communion reads `et ego in eo` where the Clementine John 6:57 reads
   `et ego in illo`.

The Introit's closing `protéctor meus, Dómine` has **no counterpart** anywhere
in Clementine Ps. 53:6–9. The natural explanation of all four facts is that the
chant preserves an older Latin psalter; the *Catholic Encyclopedia* article
"Revision of the Vulgate" is cited only for the existence of Jerome's Roman and
Gallican recensions and the Roman one's continued liturgical use. **No
*Psalterium Romanum* witness was collated**, so the derivation is not asserted.

**Consequence recorded in the guide:** Augustine, the Angelic Doctor and
Bellarmine all read and expound `iúdica me` at Ps. 53:3, and Augustine's lemma
at 53:7 reads `in virtute tua`, not the Introit's `in veritáte tua`.
Attributing their exegesis to the Introit's wording without saying so would be
a false attribution. Theodoret alone among the four reads `in veritáte`.

## 2. Corpora, languages, and method

Languages: Latin, English, French; Greek only through translation. Corpora
searched, with the delivery actually used:

- **Augustine** — *Enarrationes in Psalmos* (Latin at augustinus.it; English
  NPNF 1/8 at newadvent), *Tractatus in Iohannem* (NPNF 1/7), sermons,
  letters, *De civitate Dei*, *De consensu evangelistarum*, *Quaestiones
  Evangeliorum*, *De sancta virginitate*, *De bono viduitatis*, *De
  correptione et gratia*, *De natura et gratia*; Latin phrase searches over
  the Corpus Corporum Augustine set.
- **Ambrose** — *Expositio Evangelii secundum Lucam*, all ten books
  (la.wikisource / Corpus Corporum transcription of Migne), plus a phrase
  search of the whole Corpus Corporum Latin index.
- **Origen** — *Homiliae in Lucam* in Jerome's Latin (PL 26 facsimile page
  images on Wikimedia Commons; transcription at la.wikisource).
- **Gregory the Great** — *Homiliae in Evangelia* 39, Latin, cross-checked
  against the PL 76 scan OCR at archive.org.
- **Bede** — *In Lucae Evangelium Expositio* V (Corpus Corporum transcription
  with embedded Migne column markers).
- **Chrysostom** — *Homilies on First Corinthians* and *Homilies on John*
  (NPNF 1/12 and 1/14).
- **Cyril of Alexandria** — *Commentary on Luke* (Payne Smith 1859) and
  *Commentary on John* IV (Pusey), both at tertullian.org.
- **Ambrosiaster** — *Commentaria in Epistolam ad Corinthios Primam*, PL 17
  (1845 printing) at la.wikisource.
- **Theodoret of Cyrus** — *Interpretatio in Psalmos*, in Robert Hill's English
  translation only.
- **Thomas Aquinas** — *Super Psalmos*, *Super Ioannem*, *Super I ad
  Corinthios*, *Catena aurea* on Luke (1843 Oxford edition), and the complete
  Latin *Summa theologiae*, all from Corpus Thomisticum with English at
  isidore.co.
- **Bellarmine** — *Explanatio in Psalmos*, O'Sullivan's 1866 English.
- **Official texts** — Vatican.va official Latin of *Sacrosanctum Concilium*
  and *Presbyterorum ordinis*, official English of *Nostra aetate*, the
  Pontifical Biblical Commission's 2001/2002 document, and the 1985 *Notes* at
  christianunity.va (the former vatican.va `relations-jews-docs/` tree is
  retired and returns 404).
- **Scripture** — Clementine Vulgate and Douay-Rheims at drbo.org; Nova
  Vulgata at vatican.va for the John 6 numbering demonstration.

Not searched, and not claimed: Syriac originals, chant manuscripts,
untranslated homiliaries, subscription databases, current specialist
monographs, the Dolbeau sermons and Divjak letters of Augustine, and any
critical apparatus.

## 3. Passage-by-passage reception matrix

| Appointed passage | Direct ancient exegesis checked | Medieval / Doctoral / later saintly | Material result and boundary |
| --- | --- | --- | --- |
| **Ps. 8:2** (Gradual) | Augustine, *Enarr.* 8 §4 (Latin + NPNF); Theodoret, *Interp.* 8 | Aquinas, *Super Ps.* 8 n. 1; Bellarmine, Ps. VIII v. 1 | Augustine reads the second colon as the Ascension. Aquinas defines wonder as effect-seen-cause-unknown and uses the exaltation against two errors. Bellarmine answers the objection that few admire. Theodoret takes the "how" as extent, not comparison. Heb. 2:6–8 quotes vv. 5–7 verbatim in the Vulgate, verified by side-by-side comparison. |
| **Ps. 18:9–12** (Offertory) | Augustine, *Enarr.* 18 Sermo I §§9–12 and Sermo II §§9–12; Theodoret, *Interp.* 18 | Aquinas, *Super Ps.* 18 nn. 5–7; Bellarmine, Ps. XVIII vv. 8–11 | Aquinas gives three reasons spiritual delights exceed bodily ones and presses `in custodiendis illis` against `pro custodia`. Augustine's Sermo I supplies the honey/honeycomb image; Sermo II is pneumatological and anti-Donatist and is **not in the public-domain English**, so it was read in Latin. Theodoret qualifies the sweetness to "those truly human". |
| **Ps. 53:3, 6–7** (Introit) | Augustine, *Enarr.* 53 §§4, 8–9; Theodoret, *Interp.* 53 | Aquinas, *Super Ps.* 53 nn. 1, 3–4; Bellarmine, Ps. LIII vv. 1, 4–5 | The Ziphites-as-flourishing image is shared by Augustine and Aquinas. Aquinas and Bellarmine agree that the imprecation is to be read as prediction. **All of them except Theodoret expound a different Latin text from the Introit's** (see §1). |
| **Ps. 58:2** (Alleluia) | Augustine, *Enarr.* 58 Sermo I §§1–4; Theodoret, *Interp.* 58 | Bellarmine, Ps. LVIII argument and v. 2 | Augustine, Theodoret and Bellarmine independently read the watched house of the psalm title as the guarded tomb. Augustine's lemma is Old Latin (`Erue … redime me`). **Negative: Aquinas wrote no commentary on this psalm** — *Super Psalmos* ends at Ps. 54 with `Deo gratias`, confirmed from the Corpus Thomisticum index and the end of the file itself. |
| **Lk. 19:41–47** (Gospel) | Origen, *Hom. in Lucam* 38 (PL 26, 302B–303D); Cyril, *Comm. on Luke* Serm. 131–132; Gregory, *Hom. in Ev.* 39 §§1–10 (PL 76, 1293–1301) | Bede, *In Lucae Ev. Exp.* V (PL 92, 570C–574B); *Catena aurea* on Lk. 19 lect. 5–6 as a reception map | Gregory is the spine: two passes, historical then moral, with Vespasian and Titus named and `ruina populi maxime ex culpa sacerdotum fuit`. Origen founds the beatitude of mourners on the tears and turns the siege on the lapsed Christian. Cyril treats the tear as demonstration of compassion and softens the ruin with Rom. 11:25. **Bede's exposition is substantially Gregory transcribed**; his own contribution is the Exod. 12 typology at 573C–574B. |
| **Jn. 6:57** (Communion) | Augustine, *Tract. in Ioh.* 26 §§11–18 and 27 §§1, 6; Chrysostom, *Hom. in Ioh.* 47; Cyril, *Comm. on John* IV.2 | Aquinas, *Super Ioannem* c. 6 lect. 7 n. 976 (authentic Thomas) | Augustine separates sacrament from virtue and reaches the clause at §18; Chrysostom's term is "blended"; Cyril illustrates with wax and leaven and argues *against* abstention; Thomas makes the verse the major premise of a syllogism and the criterion distinguishing fruitful from feigned reception. **Correction: 1 Cor. 10:17 is cited in Tractate 26 only, not in 27.** |
| **1 Cor. 10:6–13** (Epistle) | Chrysostom, *Hom. on 1 Cor.* 23 (to v. 12) and 24 (v. 13); Ambrosiaster ad loc. (PL 17, 1845 printing, coll. 144–145) | Peter of Tarantaise, in the Thomistic corpus, c. 10 lect. 2–3 | Chrysostom traces the catalogue to luxury and denies that the capacity of v. 13 is natural. Ambrosiaster reads v. 12 socially and v. 13 as an exhortation. **Major correction: the exposition of this chapter in the Aquinas corpus is not Aquinas.** |

## 4. Consequential negative results

These are published in the guide, not buried here.

1. **Augustine has no exegesis of Luke 19:41–44.** Searched: the Latin sermon
   corpus, all 150 *Enarrationes*, all 124 *Tractates*, all 22 books of *De
   civitate Dei*, *De consensu evangelistarum*, *Quaestiones Evangeliorum*, and
   the letters, by phrase (`flevit super`, `cognovisses`, `visitationis`, `in
   hac die tua`, `coangustabunt`, `prosternent te`, `lapidem super lapidem`).
   Two loci only: *Ep.* 199 IV.12, where he replies to *someone else's* use of
   the verse and refers it to the first advent, and one clause in *De sancta
   virginitate* 28. Telling secondary negatives: *De consensu* II.66 jumps
   from the triumphal entry to the cleansing at II.67, and *Quaestiones
   Evangeliorum* II has no question on 19:41–44 at all.
   *Boundary:* the Dolbeau sermons and Divjak letters are outside the searched
   corpus; the result is bounded to material printed before 1980.
2. **Ambrose has no exegesis of Luke 19:41–44 anywhere**, and never quotes
   `domus orationis` or `spelunca latronum`. His Temple exposition is *Exp.
   Lc.* **IX.16–22**, not Book X, and its lemmas are Matthew 21:12 and John
   2:15 — he is not commenting on Luke's wording. His §22 contains a
   supersessionist sentence (`ut nusquam Synagogae locus in orbe remaneret`)
   which the guide reports rather than suppresses.
3. **The *Summa theologiae* never cites Luke 19:41 or 19:45–46.** `Luc. XIX`
   occurs four times, each a different verse; `flevit` once, inside a Hilary
   quotation at III q. 15 a. 5 ad 1; `spelunca latronum` and `videns
   civitatem` not at all. III q. 15 a. 6 (sorrow) uses Mt. 26:38; a. 9 (anger)
   uses Jn. 2:17; II–II q. 100 (simony) uses no temple-cleansing text.
4. **Aquinas wrote no commentary on Psalm 58.**
5. **The exposition of 1 Corinthians 10 in the Thomistic corpus is Peter of
   Tarantaise's.** Corpus Thomisticum's editorial note: *A capite vero X
   amissa est lectura, ac lacuna repleta ex commentario Petri de Tarantasia
   breviato forte a Nicholao de Gorran*. Larcher's English prints the bracket
   "[CHAPTERS 7:15—10:33 (nos. 347–581) supplied by Peter of Tarantaise]" in
   place of the text. Both were opened and read directly. **No Marietti `n.`
   is cited for this passage in the guide**, because none could be pinned to
   an authentic Thomistic text.
6. **Chrysostom and Ambrosiaster do not raise the 23,000 / 24,000 problem.**
7. **No Augustinian citation of 1 Cor. 10:12 was established.** Two verified
   loci for v. 13 (*De sancta virginitate* 47, *De bono viduitatis* 17) are
   doctrinal reuse, not exegesis; his lemma reads `exitum`, not `provéntum`.
   The *Enarrationes* and *Sermones* were not exhaustively searched for v. 12,
   so this is recorded as "not established", not "absent".
8. No patristic or medieval commentary on the wording of the **Collect**,
   **Secret** or **Postcommunion** as compositions was located. The guide's
   analysis of them is labelled source-grounded synthesis.

## 5. Competing judgments and unresolved leads

- **Date of the Passion.** The 1910 *Catholic Encyclopedia* computes AD 29 from
  the fifteenth year of Tiberius and the consulship of the Gemini. Later
  discussion commonly works within AD 30–33. The guide reports both horizons
  and settles nothing.
- **Luke's composition.** The *Catholic Encyclopedia* reports Achaia and a
  pre-70 date (with the Biblical Commission's 1913 ruling); the NABRE reports
  the same attribution but a post-70 date, commonly AD 80–90, and no place.
  Both are printed on page 2.
- **The murmuring of 1 Cor. 10:10.** `exterminator` has no lexical counterpart
  in the Vulgate of Numbers 14 or 16. Ambrosiaster anchors it at Num. 14,
  Peter of Tarantaise at Num. 16:41. The guide reports the disagreement rather
  than choosing.
- **Exodus 32:6 at 1 Cor. 10:7.** In the **Clementine** the two agree word for
  word (`sedit populus manducare, et bibere, et surrexerunt ludere`), verified
  at drbo.org. A differently-edited Latin text consulted at vulgate.org reads
  `comedere ac bibere`, but that site names no edition, so no attribution is
  made and the guide states the agreement as a fact about the Clementine only.
- **The 23,000.** No witness to Num. 25:9 that could be opened reads 23,000:
  the Masoretic text, the Septuagint and the Vulgate all read 24,000. Peter of
  Tarantaise gives two options (`maior numerus non excludit minorem` / `forte
  vitium scriptorum est`). The guide reports the difference and adopts no
  harmonisation. Nineteenth-century harmonisations found in commentary
  aggregators were treated as leads only and are not published.
- **Peter of Tarantaise's maxim `Augustinus: propter Christum pati humana
  tentatio est` is verbatim Ambrosiaster.** Verified in both texts. The guide
  flags it as a gloss-transmission misattribution.
- **Column numbers.** Theodoret's PG 80 columns are those printed inline in
  Hill's translation, not read from a Migne scan; Bede's PL 92 columns come
  from a transcription's embedded markers. Column numbers for Chrysostom,
  Cyril and Augustine's Tractates were not verified beyond the volume level and
  are therefore **not printed** in the guide.
- **Unresolved lead, not used:** the Magnificat antiphon for this Sunday in
  the Office of Guéranger's day restores `cunctis gentibus` to the Lucan
  saying. The guide reports it only as a liturgical conflation to be avoided,
  and does **not** claim it for the 1961 *Breviarium Romanum*, which was not
  collated.

## 6. Rights and translation control

- The 1962 Latin propers are received liturgical text in the public domain;
  the project has composed, translated, paraphrased, modernised, conflated and
  adapted nothing.
- Every English rendering of an appointed text in the guide is **Dom Laurence
  Shepherd's**, from *The Liturgical Year … Time after Pentecost*, vol. II,
  2nd ed. (Stanbrook Abbey: Burns & Oates, 1909) — title page verified in the
  scan — at pp. 224, 225–226, 229, 229–230, 249 and 250, each named at the
  point of use. Published 1909, US public domain.
- **The same volume carries the reading the guide rejects.** Its commentary
  speaks of "the Jewish deicides" and "the apostate nation" (pp. 227, 230) and
  opens the Mass with "Israel had made himself the enemy of the Church"
  (p. 224). These pages were read in the page images, not only the OCR. The
  guide quotes them so that its own translation source is not laundered.
- Public-domain and quoted: Payne Smith 1859 (Cyril on Luke), Pusey (Cyril on
  John), NPNF (Augustine, Chrysostom), Newman's *Catena aurea* (1843),
  O'Sullivan 1866 (Bellarmine), Bierce 1911, Page 1908, Blomefield.
- In copyright and **summarised only, never quoted**: Robert Hill's Theodoret
  (FOTC 101). No public-domain English Theodoret on the Psalms was located.
- No public-domain English exists for Origen's *Hom. in Lucam* 38, for
  Gregory's *Hom.* 39 §§3–10, for Bede's Luke commentary, or for Augustine's
  *Ep.* 199 and *Enarr. in Ps.* 18 Sermo II. In each case the Latin is quoted
  and the English around it is analysis, never a substitute translation.
- Johner's *Chants of the Vatican Gradual* (1940, US publication) shows no
  renewal in the standard renewal record — negative evidence pointing to but
  not establishing public-domain status. Paraphrased, quoted only in short
  compass, and the limitation is stated in the guide.
- Both digitisations of the missal are third-party artifacts whose rights
  status the repository's source records list as **unresolved**. Neither is
  redistributed; only focused extracts and citations are kept.

## 7. Notable-and-quotable audit

Checked under the cultural-afterlife rule on 2026-07-25. Straight exegesis,
devotional reuse, bare titles, mottoes, artworks and musical settings were
excluded by rule.

| Proper phrase | Later use and locus | Wording and context check | Rights | Cultural payoff | Controlling limit |
| --- | --- | --- | --- | --- | --- |
| Epistle, 1 Cor. 10:12, "he that thinketh himself to stand, let him take heed lest he fall" | Monument to Jonathan Lewes (d. 7 April 1704, by a fall from a horse), St George Colegate, Norwich, in Blomefield, *History of Norfolk*, vol. 4, printed **p. 469** | Found by an `insource:` phrase search of Wikisource, then verified independently in the British History Online edition of Blomefield, which supplies the page number and the surrounding monument to Bryant Lewis | Inscription and Blomefield long out of copyright | A metaphor for spiritual presumption is re-cut as a literal pun on a fatal fall, addressed to a reader physically standing on the church floor | The witness is Blomefield's transcription, not the stone; survival of the monument was not investigated |
| Gospel, Lk. 19:46, "den of thieves" | Ambrose Bierce, *The Devil's Dictionary* (1911), s.v. `WALL STREET` | Verified in the Project Gutenberg text of the 1911 edition (ebook 972) at the entry itself; the Wikisource copy reads "A symbol **for** sin", Gutenberg "A symbol **of** sin", and the guide quotes only the sentence common to both | US public domain (1911) | Temple accusation becomes financial cliché, and Bierce then turns it against the people who use it — a second-order reversal | Dependence is on the naturalised English idiom, not demonstrably on Luke; and the "money changers" usually invoked with it are **not** in the appointed Lucan text |
| Gospel, Lk. 19:46, "den of thieves" | Curtis Hidden Page's English *Misanthrope* (1908), Alceste's closing speech, Act V | Both texts opened: Molière's French reads `Je vais sortir d'un gouffre où triomphent les vices`; Page renders "I'll leave this den of thieves vice reigns among" | US public domain (1908; French 1666) | The phrase has become so natural an English container for institutional corruption that a translator imports it where the original has none | The dependence is the **translator's**, not Molière's; the entry claims no biblical allusion by Molière |

**Material negative results.** Franklin D. Roosevelt's First Inaugural
(4 March 1933) was verified at the American Presidency Project — "the money
changers have fled from their high seats in the temple of our civilization" —
and **rejected**, because the money-changers are absent from the appointed
Lucan pericope; the phrase depends on Mark, Matthew and John. The Cromwell
"Dissolution of the Long Parliament" speech (`turn'd the Lord's temple into a
den of thieves`) is a superb register change but rests on a disputed
eighteenth-century compilation and was not retained. Defoe's *Farther
Adventures of Robinson Crusoe* and Chekhov's "The Horse-Stealers" (Garnett)
both use "den of thieves" verifiably but add nothing the retained entries do
not already show, and a fourth Gospel entry would have unbalanced the gallery
further. "Sweeter than honey" hits in Homer, Aristophanes and Bierce's
*Devil's Dictionary* (s.v. L) are the independent classical topos or Samson's
riddle, not the appointed psalm, and were rejected under the
independently-similar-phrase rule. Chronicling America searches on "one stone
upon another", "rose up to play" and "sweeter than honey and the honeycomb"
returned almost exclusively religious-press usage with no register change.

**Method limitation.** The session's web-search budget was exhausted early, so
discovery used phrase search over Wikisource's `insource:` index, the Library
of Congress Chronicling America JSON API, Project Gutenberg and British
History Online rather than open-ended search. That is a real and stated bound
on how widely the gallery was hunted.

## 8. Interpretive-proposal audit

Each proposal was tested against the corpus in §2 and against a targeted
search for its own conjunction. Classifications apply to that bounded corpus
only and are correctable; nothing is claimed to be unprecedented anywhere.

| Proposal | Anchors and mechanism | Novelty result | Bounded search / nearest analogue | Fruit | Controlling limit |
| --- | --- | --- | --- | --- | --- |
| The day begins with the verb the city could not perform | Gospel `non cognóveris tempus visitatiónis`; Introit `Ecce Deus ádiuvat me` and the missal's inversion of the psalm's order | not located in the checked corpus | Gregory, Bede and Origen all expound the unrecognised visitation, and Bellarmine reads the Introit's `Ecce` as "a sudden light from God"; no checked witness relates the Introit's construction to the Gospel's diagnosis | Recognition presented as something a rite trains | The inversion may be pure chant-repertory habit; the texts share no vocabulary; no compiler intent is claimed |
| The granted prayer is the danger the Collect is built against | Collect `fac eos … postuláre`; Epistle `Non simus concupiscéntes malórum` and Numbers 11 | not located in the checked corpus | Chrysostom and Ambrosiaster both root the Epistle's catalogue in luxury; no witness on the Collect was located at all (see §4.8), so no analogue exists in the checked corpus | Petition as something to be converted, not merely offered | The Collect never mentions the wilderness; `desideráta` is neutral; this is adjacency, not dependence |
| Sweetened judgment is not softened judgment | Gospel Temple action and Jer. 7; Offertory `iudícia eius dulcióra … nam et servus tuus custódit ea` | near analogue located | Aquinas (`in custodiendis illis` is itself the reward) and Theodoret (sweet "not to all") each condition the sweetness on the keeper; Johner independently says the Offertory is sung "more subdued" after this Gospel. No witness joins Ps. 18 to Lk. 19 | The day's severity and sweetness stop competing | Ps. 18 has nothing to do with a temple; the centonisation may long predate any pairing with this Gospel |
| The Gospel's last clause and the Secret's `quóties` share one grammar | Gospel `et erat docens cotídie in templo`; Secret `quóties … exercétur` | near analogue located | Gregory makes the equivalent move allegorically at *Hom.* 39 §7, `quotidie Veritas in templo docet`, and Bede repeats it — but about instruction, not sacrifice. No witness makes the grammatical observation | Repetition as the shape of both revelation and redemption | `cotídie` and `quóties` differ in force; the parallel is structural, not verbal; the Secret's date and origin were not investigated |
| The Alleluia is sung from inside the sepulchre | Alleluia Ps. 58:2; the tomb-guard reading in Augustine, Theodoret and Bellarmine; the Gospel's approach | near analogue located | The tomb reading itself is well documented in three checked witnesses; what is not located is anyone applying it to this chant's **position** before this Gospel | The lament is heard from a vantage that already contains the answer | Reception, not the psalm's sense; Augustine expounds a different Latin text; Alleluia verses are commonly assigned on musical grounds |

## 9. Production and review boundary

The settled source was compiled twice under the deterministic build path,
producing a **25-page** PDF with SHA-256
`b597e9bc4932c1ad98dae764db9323c8c0ad89edf518bb19411b569237922676`. The final
log contains no fatal error, undefined reference, overfull or underfull box, or
unresolved rerun or layout warning. Review rasters were produced with
`scripts/pdf-review` and **every rendered page was inspected at full size** for
clipping, density, heading and table breaks, artificial whitespace, and the
terminal rights colophon; three whitespace defects found in review (a spilled
page-2 dossier row, an orphaned gallery entry, and a half-empty section-end
page) were fixed and the document rebuilt. Generation metadata validated;
Letter page size, embedded and subsetted fonts with Unicode maps, and nonempty
text extraction (15,475 words) were checked. `qpdf` is not installed in this
environment, so the structural check by that tool was **not** performed. The
reviewed build was installed at its mirrored `doc/` path and verified
byte-identical. The document was **not** added to any `library/` catalog page,
because concurrent work was in progress there; that listing remains
outstanding.

This is **internal production review only**. It is not independent editorial,
liturgical, theological, specialist, rights or ecclesiastical review, and it is
not an imprimatur, a nihil obstat, or distribution approval. The
work-specific `liturgical-text-permission` question recorded for this leaf
family remains **open**; nothing in this record weakens or redescribes it. Any
exact-snapshot distribution clearance attaches to specific PDF bytes and to
nothing else.
