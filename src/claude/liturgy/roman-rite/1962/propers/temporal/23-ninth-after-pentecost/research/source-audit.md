# Ninth Sunday after Pentecost — source audit

Provider: Anthropic Claude. Every check recorded here was performed on
**2026-07-25** against the named witness — a page image, a downloaded file, or
a live web text — unless a different date is stated. "Read as image" means a
rendered page was looked at; "read as text" means a transcription or HTML text
was read and no image was consulted. Nothing is recorded that did not happen,
and no check is upgraded beyond what its delivery supports.

## 1. The appointed Latin — image collation

| Witness | Delivery | Loci read | Role |
| --- | --- | --- | --- |
| *Missale Romanum*, editio typica (Vatican, 1962) | CMAA facsimile PDF, downloaded, SHA-256 verified against the digest registered in `src/sources/` **before** reading; rendered at 300 dpi whole-page and 600 dpi for disputed letters | Printed pp. 388–389 = PDF pp. 469–470; formulary boundaries checked into the preceding formulary (no. 1521) and the following heading (no. 1532) | **Controlling text** for every Latin form published |
| *Missale Romanum*, editio iuxta typicam (Benziger, 1962) | Internet Archive page images, leaves `n458`, `n459`, `n460`, downloaded as JPEG and read as images; leaf-to-printed-page offset established by reading leaf `n500` (printed p. 424) | Printed pp. 382–383, plus p. 384 for the following formulary's boundary | **Second edition witness** for the discrepancy table |
| Same Internet Archive item, DjVuTXT OCR | Downloaded whole file, SHA-256 checked, lines 58,575–58,733 extracted | Locating aid only | **No control over wording** |

Every one of the ten elements, its printed heading, its scriptural reference,
its accentuation and punctuation, the `II classis` rank, the `Credo` rubric
and the `Præfatio de Ssma Trinitate` rubric were read on the images of both
editions. The readings `cœpit eícere`, `spelúncam`, `mandúcat` and `vigínti
tria mília` were re-read at 600 dpi because they are the points at which the
two editions were expected to differ. The complete collation and the
discrepancy table are in `../propers/verified.md`.

## 2. The English translation — image collation

| Witness | Delivery | Loci read | Role |
| --- | --- | --- | --- |
| Guéranger, *The Liturgical Year … Time after Pentecost*, vol. II, 2nd ed., tr. Laurence Shepherd (Stanbrook Abbey / Burns & Oates, 1909) | Internet Archive item `V11TheLiturgicalYear`; whole OCR downloaded for location, then **page images read** for every page actually cited; leaf-to-page offset established by reading leaf `n250` (printed p. 230) | Title page (leaf `n3`, imprint and translator verified); pp. 224, 229–230, 249, 250 read as images; pp. 225–226 read as text | **The only source of English for any appointed text** |

The same volume's own commentary at pp. 224, 227 and 230 — "Israel had made
himself the enemy of the Church", "the Jewish deicides", "the apostate nation"
— was read on the images of pp. 224, 230 and as text at p. 227, and is quoted
in the guide so that the translation source is not laundered.

## 3. Scripture — text checks

All at drbo.org unless stated. Read as text.

| Locus | Claim served |
| --- | --- |
| Ps. 8 (Clementine), title and vv. 2–3 | Gradual matches the psalter exactly; title `pro torcularibus` |
| Ps. 18 (Clementine), title and vv. 9–12 | The Offertory is a centonisation; the exact source of each fragment |
| Ps. 53 (Clementine), title and vv. 3, 6, 7 | Introit omits `enim`; reads `líbera me` for `judica me`; `protéctor meus, Dómine` has no counterpart |
| Ps. 58 (Clementine), title and v. 2 | Alleluia matches word for word; the title's watched house |
| Ex. 32:6 (Clementine) | Word-for-word agreement with 1 Cor. 10:7 **in this edition**; a differently-edited text at vulgate.org reads `comedere ac bibere`, but that site names no edition and is therefore not cited |
| Lk. 19:41–48, Latin and Douay | The pericope's boundary at v. 47a; Luke's **short** form of the Temple saying |
| Mk. 11:15–18 (Clementine) | Mark keeps `omnibus gentibus`; Luke does not |
| Is. 56:7 and Jer. 7:11 (Clementine) | The two fused quotations and their own contexts |
| Jn. 6 (Clementine), vv. 51, 52, 56, 57; chapter length 72 verses | The verse-numbering demonstration; `et ego in illo` against the antiphon's `et ego in eo` |
| Nova Vulgata, Jn. 6 (vatican.va) | The critical numbering, 71 verses, and the split at v. 51 |
| 1 Cor. 10:6–13, Latin and Douay | The lesson's wording and the standard English idioms |
| Heb. 2:6–8 (Clementine) | Verbatim quotation of Ps. 8:5–7 |

## 4. Magisterial and official texts — checked directly

Each was opened and the exact sentence and its note read; none is reported
from a secondary source.

| Source and locus | What was read | Witness |
| --- | --- | --- |
| *Sacrosanctum Concilium* 2, official Latin, with note 1 | `opus nostrae Redemptionis exercetur`; note 1 = `Missale romanum, oratio super oblata dominicae IX post Pentecosten` | vatican.va |
| *Presbyterorum ordinis* 13, official Latin, with its source note | `opus nostrae redemptionis continuo exercetur` — `continuo` confirmed present; note 105 identifies the same prayer | vatican.va |
| *Nostra aetate* 4, official English | "Jerusalem did not recognize the time of her visitation" with **note 9 = Cf. Lk. 19:44**; "the Jews should not be presented as rejected or accursed by God"; the passion-guilt sentence; the anti-Semitism sentence | vatican.va |
| *Notes on the Correct Way to Present the Jews and Judaism* (1985), **VI.1** | "The history of Israel did not end in 70 A.D."; "We must rid ourselves of the traditional idea of a people *punished*" | christianunity.va (the former vatican.va `relations-jews-docs/` tree is retired) |
| Pontifical Biblical Commission (2001/2002), §§51, 53, 71, 74 | The "tearfully foresees" phrase; the Jeremiah analogy and its immediate qualification; the rule about threats not directed at Jews as Jews; the pairing of Lk. 19:41–44 with 23:28–31 | vatican.va |

## 5. Patristic, medieval and later witnesses

| Witness and locus | Delivery | Limit |
| --- | --- | --- |
| Ambrose, *Exp. Lc.* IX.16–22 | Latin transcription of Migne, read as text; whole *Expositio* downloaded and phrase-searched | Column figures reported as **PL 15** on the transcription's own metadata; the Wikisource header's volume link is wrong. Cited by book and section, which is stable across CSEL 32/4 and CCSL 14 |
| Origen, *Hom. in Lucam* 38 | **PL 26 facsimile page images** read for cols. 302B–303D; transcription used in parallel | The inline figures 363–366 in the transcription are an earlier edition's marginal numbers, not PL 26 columns; they are not cited |
| Gregory, *Hom. in Ev.* 39 | Latin read as text and cross-checked sentence-by-sentence against the PL 76 scan OCR for the column range 1293–1301 | Column range read off OCR running heads, not off page images |
| Bede, *In Lucae Ev. Exp.* V | Transcription with embedded Migne column markers, read as text | **PL 92 columns come from the transcription's markers, not a facsimile.** The Gregory dependence was established by comparing the two Latin texts directly |
| Augustine, *Enarr.* 8, 18 (I and II), 53, 58, 130 | Latin at augustinus.it; English NPNF 1/8 | *Enarr. in Ps.* 18 Sermo II has **no public-domain English**; read in Latin only. NPNF's page headings use Hebrew numbering while its in-text brackets use Vulgate numbering — an offset that has to be handled when citing |
| Augustine, *Tract. in Ioh.* 26–27 | NPNF 1/7, tr. John Gibb | 1 Cor. 10:17 verified present in Tr. 26 only |
| Augustine, *De sancta virginitate*, *De bono viduitatis*, *Ep.* 199, *De consensu*, *Quaest. Ev.* | Latin and NPNF where available | *Ep.* 199 has no public-domain English |
| Chrysostom, *Hom. on 1 Cor.* 23–24; *Hom. on John* 47 | NPNF 1/12 and 1/14 | PG columns **not** verified; not printed in the guide |
| Cyril, *Comm. on Luke* Serm. 131–132; *Comm. on John* IV.2 | Payne Smith 1859 and Pusey, at tertullian.org | PG columns not verified; not printed |
| Ambrosiaster, ad 1 Cor. 10:6–13 | PL 17 (1845 printing) transcription | **CSEL 81/2 (Vogels) was not consulted.** A later Migne printing uses a different column system; only the 1845 coll. 144–145 are cited |
| Theodoret, *Interp. in Ps.* 8, 18, 53, 58 | **Robert Hill's English translation only** — in copyright | Summarised, never quoted. PG 80 columns are those printed inline in that translation, not read from Migne |
| Aquinas, *Super Ps.* 8, 18, 53 | Corpus Thomisticum Latin | Coverage limit (ends at Ps. 54) confirmed twice: from the index and from the file's own closing `Deo gratias` |
| Aquinas, *Super Ioannem* c. 6 lect. 7 n. 976 | Corpus Thomisticum Latin, Larcher English | Authentic Thomas; Marietti number verified |
| Aquinas, *Summa theologiae*, complete Latin | Downloaded and searched for `Luc. XIX`, `flevit`, `spelunca`, `domus orationis`, `videns civitatem`; candidate articles then opened | The negative result is bounded to the *Summa* proper; the *Supplementum* was excluded as not his |
| "Aquinas", *Super I ad Cor.* c. 10 | **Corpus Thomisticum editorial note read directly**; Larcher's bracket read directly at isidore.co | The text is **Peter of Tarantaise's**. No Marietti number is cited for it in the guide |
| *Catena aurea* on Lk. 19 | Latin/English at isidore.co; 1843 Oxford edition text for the marginal source references | Compilation, used only as a reception map; the 1843 preface's warning about the Greek citations is reported |
| Bellarmine, *Explanatio in Psalmos*, Pss. VIII, XVIII, LIII, LVIII | O'Sullivan's 1866 English at archive.org | His verse numbers run one behind the Clementine because the title is unnumbered |
| Johner, *Chants of the Vatican Gradual*, pp. 134–135, 279–282 | Archive.org full text | 1940 US publication; **no renewal found** in the standard renewal record — negative evidence, not proof of public-domain status. Paraphrased; quoted only in short compass |

## 6. Cultural afterlives

| Entry | What was opened | Limit |
| --- | --- | --- |
| Blomefield, *History of Norfolk* vol. 4, p. 469 | Found by phrase search of Wikisource; **verified independently** in the British History Online edition, which supplied the printed page number and the surrounding Bryant Lewis monument | Blomefield's transcription of a monument, not the monument |
| Bierce, *The Devil's Dictionary*, s.v. `WALL STREET` | Project Gutenberg text of the 1911 edition (ebook 972), downloaded and read at the entry | Gutenberg reads "A symbol **of** sin", Wikisource "A symbol **for** sin"; only the sentence common to both is quoted |
| Molière / Curtis Hidden Page | Page's English at Wikisource (translator and 1908 date read from the page header); Molière's French at fr.wikisource | The biblical phrase is the translator's importation, verified by comparing the two |

Rejected after verification: Roosevelt's First Inaugural (money-changers are
not in the appointed Lucan text); Cromwell's "Dissolution of the Long
Parliament" (disputed eighteenth-century compilation); Defoe and Chekhov
(verified but redundant); all "sweeter than honey" hits (Homeric topos or
Samson's riddle, not the appointed psalm).

## 7. Outstanding

- No independent liturgical, theological, specialist, rights or ecclesiastical
  review. Internal production review only.
- The work-specific `liturgical-text-permission` question for this leaf family
  remains **open**.
- CSEL 81/2 for Ambrosiaster, a Migne scan for Theodoret's and Bede's columns,
  a *Psalterium Romanum* witness for the Introit's text, and the 1961
  *Breviarium Romanum* for the Office antiphon are all identified gaps, not
  closed questions.
