# Hell — Source Audit (Claude edition)

Publication: `articles/faith/four-last-things-03-hell` (provider `claude`).
All web witnesses checked 2026-07-25. Machine-readable bindings are in
`source-bindings.toml`; this file carries the roles, loci, ceilings, and
consequential negative results that the binding schema does not express.

## 1. Scripture

### 1.1 English — Douay–Rheims (Challoner), tracked

Role: **direct witness** for every English scriptural quotation in the article.
Edition `edition.english-college-of-douay.douay-rheims-bible.challoner-gutenberg-1581`.
Read at exact loci in the tracked per-book verse-text derivatives (one LF line
per verse) on 2026-07-25:

| Book artifact | Loci read |
| --- | --- |
| Matthew | 5:22, 29–30; 7:13–14; 10:28; 13:41–42, 49–50; 18:8–9; 25:31–46 (whole); 26:24 |
| Mark | 9:42–49 (Vulgate numbering; whole passage) |
| Luke | 13:23–28; 16:19–31 (whole) |
| John | 17:12 |
| Acts | 1:25; 3:19–21 |
| Romans | 5:18–19; 11:32 |
| 1 Corinthians | 15:22–28 |
| Colossians | 1:19–20 |
| 2 Thessalonians | 1:6–10 |
| 1 Timothy | 2:1–6 |
| Jude | 1:6–7, 13 |
| Apocalypse | 14:9–11; 20:9–15; 21:8 |
| Isaias | 66:24 |
| Ezechiel | 18:23, 32; 33:11 |
| Wisdom | 11:24–27 |
| 2 Peter | 3:9 |
| 1 John | 4:18 |
| Philippians | 2:9–11 (read, not quoted) |

Ceiling: the Gutenberg/Challoner edition record lists 1859 verses in which this
electronic state preserves an older Challoner reading against the settled
reading of the 1899/1914 American edition. **No verse used here was checked
against that divergence table.** The translation is an identified working
witness, not a critical edition, and no wording-critical argument in the
article rests on a single English word.

Numbering: Vulgate throughout. Two divergences were material and are stated in
the article at the point of use — Mark 9:42–47 here is 9:43–48 in Greek
editions, and Apocalypse 20:9–10 is divided differently, so that the Douay
sentence about the beast and the false prophet breaks across the verse boundary.

### 1.2 Greek — Robinson–Pierpont Byzantine Textform, tracked

Role: **textual control** for the eternity argument and the lexical objections.
Edition `edition.robinson-pierpont.greek-new-testament-byzantine-textform.rp2018-byztxt-unicode-csv`.
Loci read 2026-07-25: Matt 7:13–14; 10:28; 25:41, 46. Mark 9:43–49. Luke
13:23–24; 16:23–26. 2 Thess 1:8–9. Jude 6–7. Apoc 14:10–11; 20:10, 14–15.

Three artifacts were **registered with this revision** from the same pinned
repository state (`27a45ff1b7be6c17ccbfeac414f3f55732ae8e28`) as the existing
Matthew, Luke, John, Acts, Galatians, Jude, 1 Peter, and 2 Peter files:

- `ccat-csv-mar-b58af87a` (Mark, 196,848 bytes)
- `ccat-csv-2th-232a58b8` (2 Thessalonians, 11,821 bytes)
- `ccat-csv-rev-ddfbc25d` (Revelation, 155,423 bytes)

Ceiling: this is an edition of the Byzantine textform, not a critical edition.
Its inline `{NA ...}` and `{Byz ...}` braces are a divergence note, not an
apparatus. The article reports that Nestle–Aland omits Mark 9:44 and 9:46 on
the strength of those braces and expressly declines to adjudicate the text.
Robinson's official CCAT files, from which the CSVs were generated, were not
acquired. Greek is quoted only in transliteration because the typeface used
carries no Greek; every transliteration is the authoring agent's and each is
accompanied by the registered edition and exact locus.

Negative result worth recording: the tracked corpus does not include 1 John, so
the claim about the semantic range of *kolasis* at 1 John 4:18 is stated in the
article only as far as the Latin and English witnesses carry it, and the
article says so and declines to rest its conclusion on the point.

## 2. Magisterial acts

### 2.1 Denzinger — the route for every pre-modern act

Editions `edition.denzinger.enchiridion-symbolorum.latin-patristica-web-2026-07-25`
(Latin, revised and older numbering in parallel) and
`edition.denzinger.enchiridion-symbolorum.english-deferrari-patristica-web-2026-07-25`
(older numbering, English).

Loci read 2026-07-25, each in its surrounding context: DS 76 (*Quicumque*
vv. 29–42); DS 397 (Orange II conclusion, with the preceding paragraphs on
grace); DS 403–411 (nine canons against Origen, whole set); DS 433
(Constantinople II canon 11, with canons 1–14 skimmed and 9–12 read); DS 801
(Lateran IV *Firmiter*, chapter read whole) with DS 802; DS 858 with DS 857 and
859; DS 926 (John XXII to the Armenians); DS 1000–1002 (*Benedictus Deus*); DS
1304–1306 (Florence *Laetentur caeli*); DS 1351 (Florence *Cantate Domino*,
with the surrounding decree paragraphs); DS 1541 (Trent 6, ch. 13); DS 1567
(Trent 6, can. 17); DS 1575 (Trent 6, can. 25, with cann. 26–27); DS 1705
(Trent 14, can. 5); DS 1997 (Paul V, 1607).

**Ceiling, stated in the article and in the references:** Denzinger is a
compilation and a finding aid to its underlying documents, not a substitute
witness. The registered edition is a dated web transcription that does not
identify its printed exemplar and that reproduces editorial query marks
(e.g. the `(-!)` at *Quicumque* v. 41) rather than resolving them. **No printed
Denzinger, no conciliar critical edition, no Mansi volume, and no papal
register was collated for this article.** Every claim resting on these acts is
bounded by that.

**Consequential negative result (misattribution).** The nine canons against
Origen are printed by Denzinger under the heading "published in the Synod of
Constantinople in 543; Anathematisms against Origen," under Pope Vigilius, and
*before* the acts of Constantinople II. The council's own canon 11 (DS 433)
names Origen in a list of heretics without stating which of his propositions is
meant. The article reports exactly this and declines to adjudicate the long
scholarly question about the fifteen anathemas circulating under the council's
name, because the conciliar acts were not reached.

**Consequential textual observation.** *Benedictus Deus* defines the immediacy
and reality of the descent to hell (`mox post mortem suam ad inferna descendunt,
ubi poenis infernalibus cruciantur`) without any word for eternity, four lines
after using `usque in sempiternum` of the beatific vision. Checked in the Latin
at DS 1000–1002. The article reports it as an observation about that act and
states in the same paragraph that the doctrine does not depend on it.

**Consequential weighting observation.** DS 1575 (Trent 6, can. 25) is cited by
CCC 1035 but treats eternal punishment as a shared premise of a dispute about
the good works of the justified rather than as the thing defined. The article
reports it as evidentially weaker than the rest of the file.

### 2.2 Vatican web texts

- *Catechism of the Catholic Church*, edition `edition.catholic-church.catechism.english-vatican-web-2026-07-25`. Pages read 2026-07-25: `__P2N.HTM` (1030–1032), `__P2O.HTM` (1033–1037 with note 615), `__P2R.HTM` (1051–1060), `__P3M.HTM` (1261), `__P6C.HTM` (1854–1864). Role: direct witness and, for CCC 1035 n. 615, the article's organizing document. Ceiling: quoted briefly with attribution; the Latin typical edition was not collated, and IntraText delivery artifacts (lowercased sentence-initial articles, spaced hyphens) are present in the delivery and do not affect quoted wording.
- *Lumen gentium* 14 and 16, English Vatican web text, read whole. Role: authoritative interpretation of the condition in *Cantate Domino*. Ceiling: the Latin and the AAS text were not consulted.
- Paul VI, *Solemni hac liturgia* n. 12, English Vatican web text, complete document read. Ceiling: the AAS Latin was not consulted; no claim turns on the Latin wording.
- John Paul II, general audience of 28 July 1999, nn. 1–4, English Vatican web text, complete address read. Role: the article's principal warrant for the negative claim about the census, and for the boundary between the doctrine and its imagery. Ceiling: delivered in Italian; the Italian was not collated. Weight: ordinary papal magisterium in its least solemn form, stated as such in the article.
- Benedict XVI, *Spe salvi* nn. 45–48, English Vatican web text. Ceiling: the AAS Latin was not consulted.

## 3. Patristic witnesses

| Witness | Loci read | Route | Role and ceiling |
| --- | --- | --- | --- |
| Justin Martyr, *2 Apol.* | 7–9 (whole) | New Advent delivery of ANF 1; cross-read in the tracked ANF 1 OCR | Earliest witness both to the doctrine and to the objection that it is a bugbear. Chapter numbering varies between editions; Greek not consulted. |
| Irenaeus, *Adv. haer.* | V.27.2 (whole section, chapter heading read) | Tracked ANF 1 OCR at artifact lines 72024–72062, **registered as a passage with this revision**; independently cross-checked at New Advent | Earliest sustained account of hell as self-chosen separation. The OCR is a locator aid, not textual control; the surviving text is a Latin translation of a lost Greek; no critical edition collated. |
| Origen, *De principiis* | I.6.1–2 (whole chapter); II.10.2–6 | New Advent delivery of Crombie/ANF 4 | Direct witness for the exploratory genre disclaimer and for the conscience-fire and medicinal readings. **The treatise survives complete only in Rufinus's Latin.** |
| Rufinus, Prologue to *De principiis* | Whole prologue, printed p. 237 | CCEL delivery of ANF 4 (**registered as a second edition of the work with this revision**, because New Advent's delivery omits the front matter) | Direct witness for the translator's own editorial rule. This is the article's evidence for the transmission problem, and without it the claim would have been unsourced. |
| Gregory of Nyssa, *Oratio catechetica magna* | XXVI (whole chapter, with the editors' footnotes) | CCEL delivery of NPNF 2/5 | Direct witness that a canonized Father taught the healing of the author of evil. Greek not consulted; the Krabinger marginal note is reported at second hand from the editors' footnote and was not inspected. |
| Chrysostom, *Hom. in Matt.* | 23, §9 (and §§7–10 read) | New Advent delivery of NPNF 1/10 | Direct witness for the two-punishment ranking. Section divisions editorial; Greek not consulted. |
| Augustine, *De civitate Dei* | XXI.9, 11, 12, 17, 23 (each chapter read whole); XXI.1–3, 10, 13, 18, 24 read for context | Tracked Dods 1871 transcription; **five passages registered with this revision** with exact artifact line ranges | Direct witness for the correlativity argument, the proportionality reply, the *misericordes*, the proportion claim, and the explicit release of the reader on the mode of the fire. Nineteenth-century translation, not a critical edition; Latin not collated. |

Registered Augustine passages: `21.9` (17321–17392), `21.11` (17451–17508),
`21.12` (17511–17538), `21.17` (17748–17782), `21.23` (17958–18013).

## 4. Thomistic and philosophical sources

- *Summa theologiae*, English of the Fathers of the English Dominican Province at New Advent. Questions read whole on 2026-07-25: I q. 19 (a. 6 with all replies), I q. 23 (a. 3 with replies), I q. 64 (a. 2), I-II q. 87 (all eight articles), Suppl. q. 94, q. 97, q. 98, q. 99. Role: the tradition's principal analysis. Ceiling: **work-level binding**; no Latin of the *Summa* was collated for this article, and no printed or Leonine edition was consulted.
- *Scriptum super libros Sententiarum* IV, d. 46, q. 1, a. 3 and q. 2, a. 1, Latin at Corpus Thomisticum page `snp4045`, paragraphs 21988–22024, read 2026-07-25. Role: **textual control on the status of the Supplement.** The comparison with Suppl. q. 99 a. 1 was made article by article on structure and content — same title question, same six objections, same three *sed contra* arguments, same corpus with one principal reason and four *rationes a sanctis assignatae*, same six replies — and confirms the derivation. Ceiling: the Latin of the Supplement was **not** consulted, so this is a structural and substantive comparison and not a collation; the article says so.
- Aristotle, *Rhetoric* I.10.17, Greek (Ross 1959) and English (Freese 1926) as delivered by the Perseus Digital Library, read 2026-07-25. Role: the locus for the *kolasis*/*timoria* distinction on which a standard lexical objection rests, read at its own place rather than through a secondary report. Ceiling: no printed edition collated; Perseus states its markup is CC BY-SA 3.0 US; Freese's rendering is identified in the article as a translator's choice.

## 5. Rights

Douay–Rheims (Challoner) and the Robinson–Pierpont CSVs are public domain and
tracked with recorded distribution bases. All patristic translations used are
public-domain nineteenth-century work; the hosts delivering them (New Advent,
CCEL) hold rights in their own markup and revisions, which are not reproduced.
Freese's 1926 translation is out of United States copyright by publication
date. Denzinger's Latin compilation as delivered is used as a finding aid; the
underlying acts are public domain, and printed Denzinger editions retain their
own editorial rights. Vatican texts remain the property of the Libreria
Editrice Vaticana and are quoted briefly with attribution. Nothing quoted in
the article is project-created expression except the prose, tables, and
organization, which are covered by the repository's CC BY 4.0 grant.

## 6. Outstanding

- Mansi and the conciliar critical editions for the 543 canons and Constantinople II.
- A printed Denzinger for every DS number used.
- The Latin of the *Summa* and of the Supplement.
- The Greek of Gregory of Nyssa, Chrysostom, and Justin.
- The Latin of *Lumen gentium*, the *Credo*, and *Spe salvi* in the AAS.
- The 1899/1914 American Douay–Rheims divergence table for the verses quoted.
- The modern literature on the hope for universal salvation, deliberately excluded from scope.
