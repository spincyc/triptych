# What Death Does Not Finish — source audit

Rewrite of 2026-10-16. Every quotation printed in the body was read at the
locus named below on 2026-10-16 (UTC) in the witness named. Supersedes the
audit of July 2026. Where a witness is an OCR text layer, the page image was
read for every quoted passage unless stated otherwise. Normalisations applied
to every quotation: typographic quotation marks and apostrophes; spaces before
colons and semicolons in French-style setting closed up; footnote and sigla
markers omitted; stress accents in the liturgical Latin omitted; the ligature
æ printed as ae in Latin (except where Alphonsus's own `tuæ viæ` is quoted
inside his English); line-end hyphenation closed up. No wording was altered.
Omissions are marked with ellipses.

Working copies used for reading were not retained in the repository.

## Scripture

| Text | Witness | Check |
| --- | --- | --- |
| Matt 12:36–37; 24:3, 30–31, 35–36, 42, 44; 25:31–34, 37, 40, 41, 44, 46; 26:1–2 | Douay–Rheims, Challoner, PG 1581, library per-chapter JSON `src/sources/bibles/douay-rheims/chapters/Matt/*.json` | Printed from the JSON verse text; all quoted verses compared by script and by eye. |
| Luke 12:2–3; 16:22, 26; 21:25–28; 23:43 | same, `Luke/` | same |
| John 4:6; 5:22, 27–29; 1 John 2:1; 4:17–18 | same | same |
| Rom 2:15–16; 1 Cor 3:13–15; 4:5; 2 Cor 5:8, 10; Phil 1:23; 2:12; Heb 4:15–16; 9:27; Tit 2:13 (two words); Apoc 20:11–12; 22:20; 2 Mach 12:43, 46 | same | same. Matt 25:37 corrected during review to quote through "gave thee drink?" rather than ending at "fed thee". |

Liturgical assignments: 1962 Last Sunday after Pentecost, Matt 24:15–35
(`src/sources/calendars/roman-1962/propers.yaml:15981`); 1962 Advent I, Luke
21:25–33 (`:663`); 1962 All Souls, three Masses, first Mass Gospel John
5:25–29, Sequence *Dies irae*, Offertory *Domine Jesu Christe*
(`:47760–47960`); Postconciliar Christ the King, Year A, Matt 25:31–46
(`src/sources/calendars/postconciliar/propers.yaml:38840`). Public domain.

## Liturgy

| Quotation | Witness and locus | Check | Rights |
| --- | --- | --- | --- |
| *Dies irae*, strophes 1–2 (§1), 5–6 (§5), 10 (§4) and 7–19 (§9, the closing prayer) | *Missale Romanum* (Tournai: Desclée, 1889), *Missae pro Defunctis*, p. 92*; library artifact `…1889-tournai-desclee-leo-xiii-recognitum.ia-djvu-ocr-715f57fd` (OCR locates it at lines 89031–89090) | Every line read at the IA page image `missaleromanumex1889cath/page/n827.jpg`; the OCR's `Cundla stridle`, `didturus`, `maledidtis` etc. corrected from the image. Punctuation as printed (`tuae viae,`). | PD (pre-1931). The 1962 typica's own text is rights-withheld in the library, hence the 1889 printing. |
| Offertory *Domine Jesu Christe … et semini ejus* | same, p. 93*, page image n828 | read at image; `Michaël` printed with diaeresis, normalised to Michael | PD |
| Irons, stanzas 1, 3, 4–10 | *Hymns Ancient and Modern*, complete ed., hymn 398, pp. 307–309; library TSV `dies-irae-irons-en` | Every line compared with the page images n322–n324 (`hymnsancientmode0000unse_s2j4`). Stanza 5 line 4 "sought me," — the comma is broken in the print; read as comma, agreeing with the TSV. | PD (author d. 1883; text 1850s) |
| *Judex crederis esse venturus* | J. H. Blunt, *Annotated Book of Common Prayer* (London, 1866), p. 12, Latin column; library artifact `…london-1866.ia-djvu-text-gtu-32400003882739-f3f87210` | read at page image `gtu_32400003882739/page/n157.jpg` | PD |
| *Te ergo quaesumus tuis famulis subveni …* with English "We therefore beseech thee …" | Alphonsus, *Preparation for Death* XVI, Affections (Duffy 1843), p. 204 | page image n220 | PD |

## Magisterium

| Quotation | Witness and locus | Check | Rights |
| --- | --- | --- | --- |
| Lateran IV, *qui omnes cum suis propriis resurgent corporibus, quae nunc gestant* | Denzinger, DS 801, patristica.net Latin Enchiridion | Refetched 2026-10-16; sha256 604f24c4… equals the registered artifact. | Latin act PD; compilation's apparatus not reproduced |
| Lyons II DS 856 (*poenis purgatoriis seu catharteriis, sicut nobis frater Iohannes … explanavit, post mortem purgari*; the body's quoted Latin is attributed to Florence, DS 1304, alone), 857–858 (*mox*), 859 (*nihilominus*) | same | read | same |
| Florence DS 1304 *eorum animas poenis purgatoriis post mortem purgari* | same | read; DS 1304–1306 read through to 1307: no judgment clause (cold-review D1 confirmed) | same |
| *Ne super his* DS 990–991 | same | read; the English given is a prose paraphrase outside quotation marks | same |
| *Benedictus Deus* DS 1000–1002: defining formula, *in quibus nihil purgabile fuit …*, *cum post mortem suam fuerint purgatae*, *mox*, *etiam ante resumptionem …*, *visione intuitiva et etiam faciali*, *immediate … nude, clare et aperte*, *usque ad finale iudicium …*, DS 1002 entire | same | read | same |
| CCC 679, 1021–1023, 1030–1032, 1038–1041, 1861 | Holy See archived IntraText pages `__P1W`, `__P2L`, `__P2M`, `__P2N`, `__P2P`, `__P6C` | fetched and read. The pages print spaced hyphens for dashes and lowercase some sentence-initial "the"; em dashes are typeset; no word changed. | Official copyrighted text, quoted briefly |
| CDF, *Letter on Certain Questions concerning Eschatology* (1979), point 5 | vatican.va English | read; quoted only for the Parousia "distinct and deferred" (cold-review D2). The parenthetical citation of *Dei Verbum* inside the sentence is marked by an ellipsis. Point 7 cited (not quoted) in Appendix A. | Official, brief |
| *Spe salvi* 41 (including the Creed's English, "he will come again in glory to judge the living and the dead", quoted from 41), 43, 44, 45, 47, 48 | vatican.va English | read; 47's fire-as-Christ is attributed as Benedict XVI attributes it, to "some recent theologians" | Official, brief |
| Trent XXV, Decree concerning Purgatory | Waterworth (1848), Burns and Oates reprint, pp. 232–233 | page images `cu31924029369760/page/n505`, `n506` read | PD |

## Fathers

| Quotation | Witness and locus | Check | Rights |
| --- | --- | --- | --- |
| Tertullian, *De corona* 3, "As often as the anniversary comes round …" | ANF 3 (Thelwall), New Advent `fathers/0304.htm` | fetched and read | PD |
| Cyril, *Myst. Cat.* 5.8 (phrase), 5.9 (block), 5.10 (sentence) | NPNF II/7 (Gifford), library CCEL text `ccel-text-56d84cfa`, lines 21670–21697 | read | PD |
| Chrysostom, *Hom. Matt.* 79.1–2 (four passages) | NPNF I/10, library CCEL text `ccel-text-adb8f1c9`, lines ~43858–43950; homily identity confirmed against New Advent `fathers/200179.htm` | read | PD |
| Chrysostom, *Hom. Phil.* 3 | NPNF I/13, Oxford translation revised by John A. Broadus (title, line 16493), library CCEL text, lines 18007–18010 | read | PD |
| Chrysostom, *Hom. 1 Cor.* 41 (NPNF section 8) | NPNF I/12, library CCEL text, lines 22668–22698 | read; CCC 1032 cites as 41, 5 (PG division) | PD |
| Augustine, *De civ.* XX.1, XX.2, XX.14 | Dods 1871, library `pg45305-body-lf`, lines 13879–13996, 14884–14951 | read | PD |
| Augustine, *De civ.* XXI.13, "temporary punishments are suffered by some in this life only, by others after death, by others both now and then; but all of them before that last and strictest judgment" | Dods 1871, library `pg45305-body-lf`, chapter 13 heading line 17541, sentence lines 17588–17590 | read (added on review, 2026-10-16) | PD |
| Augustine, *De civ.* XXI.26, "this I do not contradict, because possibly it is true" / *non redarguo, quia forsitan uerum est* | Dods, lines 18429–18440; CSEL 40.2 TEI, lines 24365–24375 | read. The CSEL protasis reads *spiritus defunctorum*; the body's paraphrase follows the Latin. | PD |
| Augustine, *Enchiridion* 110 | NPNF I/3 (Shaw), New Advent `fathers/1302.htm` | fetched and read | PD |
| Augustine, *Confessions* IX.11.27 | NPNF I/1 (Pilkington), library CCEL text, lines 12972–12981 (the original "you" forms; New Advent's modernised text not used) | read | PD |
| Augustine, *Sermo* 18.4 | as quoted at CCC 1039 only | read in CCC | Official, brief |
| Gregory, *Dialogues* IV.39, IV.55 | P. W. (1608), ed. Gardner (London: Philip Lee Warner, 1911), pp. 233–234, 249–252, at tertullian.org | fetched and read; edition identified from the site's introduction page | PD |

## Doctors and saints

| Quotation | Witness and locus | Check | Rights |
| --- | --- | --- | --- |
| Aquinas, *ST* III q.59 a.2 corpus, a.3 corpus, a.5 corpus and ad 1–3 | English Dominican translation, PG 19950 body, library artifact `pg19950-body-4597132e`, lines ~29790–29960 | read | PD |
| Supplement q.88 a.1 corpus, ad 1, ad 2; Appendix I q.2 a.1 corpus ("punishment by corporeal fire") | English Dominican translation (London: Burns Oates and Washbourne, 1922), library OCR `ia-ocr-21251eee`, lines 581–654 and 10290–10294 | read in OCR; text clean at the quoted words | PD |
| RB 4.44–46 | Latin Wikisource text, library `regula-latin-text`, line 26 | read; æ as ae. No PD English held: the registered Henderson (1910) witness abridges ch. 4 (checked at Wikisource). Gloss is prose, not a translation in quotation marks. | PD |
| *Imitation* I.24, §§1, 2, 4 | Benham, PG 1653 | fetched and read | PD |
| Ignatius, fourth rule of the second way of election | Mullan 1914, library OCR `historical-ocr-fe256c5b`, lines 4405–4425 (pp. 92–93) | read in OCR; footnote numerals omitted | PD |
| de Sales, *Introduction* I.14, consideration 5; affections 2; conclusion | Rivingtons 1876, library OCR, lines 2794–2866 | page images `introductiontod00salegoog/page/n61`, `n62` | PD |
| Alphonsus XXIV, first point (p. 289), Ancina (pp. 289–290), affections (p. 292), second point (p. 293), third point (p. 299) | Duffy 1843, library OCR `historical-ocr-d25bba22` | page images n305, n306, n308, n309, n315 of `preparation_for_death_1893-st_alphonsus_m_liguori` | PD |
| Catherine of Genoa, *Treatise on Purgatory* ch. 2 | London: Burns and Lambert, 1858, IA `treatiseonpurga00cathgoog` | page images n15, n16; title page n7 (date 1858; OCR's "1868" and "Joy" capitalisation are OCR errors) | PD |
| John of the Cross, *Dichos* 64 | as quoted at CCC 1022 | read in CCC | Official, brief |

## Removed or paraphrased rather than quoted

- *Ne super his* and the defining formula of *Benedictus Deus*: an English
  rendering first drafted inside quotation marks was recast as prose
  paraphrase, since no published English of these sentences was read.
- RB 4.44–46 and the *Quaerens me* strophe: given in Latin with commentary,
  not with an English in quotation marks.
- The English Te Deum line "we believe that thou shalt come to be our Judge"
  was dropped: the only English held (Blunt's Prayer Book column) was not read
  at its page image.
- From the inventory's leads, not used: *Passion of Perpetua* 7–8; Newman,
  *Dream of Gerontius*; Lumen gentium 48; the *Libera me* and *Absolve* (no
  page-image witness of the Rituale read).

## Needs registration

- Tertullian, *De corona* (ANF 3, New Advent `fathers/0304.htm`), ch. 3.
- Gregory, *Dialogues* IV, P. W./Gardner 1911 edition
  (`https://www.tertullian.org/fathers/gregory_04_dialogues_book4.htm`),
  IV.39 and IV.55 (bound at work level only).
- Thomas à Kempis, *Imitation of Christ*, Benham, PG eBook 1653, I.24.
- Catherine of Genoa, *Treatise on Purgatory* (London, 1858), IA
  `treatiseonpurga00cathgoog`, ch. 2, pp. 3–4.
- CCC 1023 page `__P2M` (bound at edition level).

## Review corrections of 2026-10-16

Applied after the content and quotation reviews: Augustine's teaching on
purification after death quoted from *De civ.* XXI.13 and his reserve limited
to the reading of 1 Cor 3; "What the schools commonly taught" for the
definition of 1336; Aquinas III q.59 a.2 restated (headship first, then three
reasons of fittingness); Gregory "allows" the verse to be read of the fire to
come; Lyons and Florence Latin distinguished; the Latin schools' corporeal
fire (Supplement App. I q.2 a.1) and Florence's silence on fire added; Catherine
labelled as the private revelation of a canonized saint and Justus's
appearance as a reported apparition (pious tradition); the 1962 Missal named
for the All Souls sequence and Gospel; the Offertory gloss now includes *de
poenis inferni*; 2 Mach 12:43 and 12:46 cited separately; DS 1001 noted;
Broadus named; Nahum (LXX) attributed as Aquinas's objection.

Declined in part: Bellarmine is not named for the real-fire opinion, because
no text of Bellarmine on purgatory was read this session; the "Greek reserve"
is stated only as the verifiable fact that Florence's decree (DS 1304) names
purgatorial pains without naming fire.
