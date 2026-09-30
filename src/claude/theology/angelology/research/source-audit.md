# Source Audit

Every witness the publication relies on, grouped by the unit that reads
it: edition or translation, the URL and date of the reading, the loci
read and quoted, the rights basis, and the verification ceiling. All
readings were made on 2026-09-29 unless an entry says otherwise.

## Scripture, the faith of the Church, and the magisterial chronology

### Witness: Douay–Rheims Bible (Challoner revision), Project Gutenberg eBook 1581

- Repository ids: `work.english-college-of-douay.douay-rheims-bible` (existing); `edition.english-college-of-douay.douay-rheims-bible.challoner-gutenberg-1581` (existing).
- URL: https://www.gutenberg.org/cache/epub/1581/pg1581.txt
- Retrieved: 2026-09-29T12:58:58Z
- SHA-256 of the bytes read: 7d10da78d8ec97db53b4e2bd8719cc01e16106b44937a673ba34aa534a04c007 (5880580 bytes)
- Loci read: every verse quoted in the three files (see the Scripture table below; pulled with `.scratch/lanes/l8-scripture-faith/dr.py`, verse pulls in `v1.txt`–`v4.txt`)
- Quoted: all Scripture quotations in `sec:scripture`; `sec:faith` and `app:chronology` carry no fresh biblical quotation beyond what acts quote (Heb 2:14 inside DS 1511)
- Rights: public domain (Challoner 1749–1752; Gutenberg transcription)
- Ceiling: web transcription, Vulgate numbering; spot-checked chapter/verse but not collated with a print Douay; Douay book names kept (3/4 Kgs, Tobias, Osee, Apocalypse), Hebrew/modern numbering in brackets where it differs

### Witness: Denzinger–Hünermann, *Enchiridion symbolorum* (patristica.net transcription)

- Repository ids: `work.denzinger.enchiridion-symbolorum` (existing).
- URL: https://patristica.net/denzinger/enchiridion-symbolorum.html
- Retrieved: 2026-09-29T12:56:36Z
- SHA-256 of the bytes read: 604f24c46e0bc71c2018f25dc787a9ab421d4b2e9cf7d1cee1f43e910ef2708f (2333435 bytes)
- Loci read: DS 125, 150, 286, 325, 403–411, 455–464, 797, 800–801, 1333, 1336, 1511, 3002–3003, 3025, 3891
- Quoted: DS 150 (phrase), 286 (Latin block), 325, 457 (Latin block), 797, 800–801 (Latin block), 1333 (phrase), 1511 (phrase), 3002 (Latin block), 3025 (phrase), 3891 (Latin phrase)
- Rights: public-domain Latin acta
- Ceiling: web transcription without apparatus; not collated with the print 43rd edition; DS numbering as the site gives it (old numbers in parentheses on site)

### Witness: Augustine, *Enarrationes in Psalmos*, Ps 103 s. 1 (augustinus.it Latin; NPNF1 vol. 8 as English control)

- Repository ids: `work.augustine.enarrationes-in-psalmos` (existing).
- URL: https://www.augustinus.it/latino/esposizioni_salmi/esposizione_salmo_125_testo.htm (augustinus.it's own psalm numbering); control: https://ccel.org/ccel/s/schaff/npnf108/cache/npnf108.txt
- Retrieved: 2026-09-29T13:16:09Z; control 2026-09-29T13:10:36Z
- SHA-256 of the bytes read: c09f35f1aea0164d253248d7975fa0b8184a000566ca740f929de651fc603b3e (60734 bytes); d6841950333024906294e6e829f7512d08b3adf62ae6cee3615d18a7ad0020e9 (5029159 bytes)
- Loci read: Enarr. in Ps. 103, sermo 1 entire as transcribed, esp. §15
- Quoted: §15 (Latin block, `sec:scripture`)
- Rights: Latin public domain (PL 37 basis)
- Ceiling: web transcription, not collated with CCSL; NPNF1 vol. 8 abridges this psalm and omits §15, so no English quotation was taken from it

### Witness: Augustine, *De civitate Dei* (NPNF1 vol. 2, Dods translation)

- Repository ids: `work.augustine.de-civitate-dei` (existing).
- URL: https://ccel.org/ccel/s/schaff/npnf102/cache/npnf102.txt
- Retrieved: 2026-09-29T12:55:19Z
- SHA-256 of the bytes read: 5c973feda803f3e58a88ed7df210b42d436f5466741eb8dbeae713ab56dedae4 (3692898 bytes)
- Loci read: XVI.29
- Quoted: XVI.29 (two short phrases, `sec:scripture`)
- Rights: public domain (NPNF, 1887)
- Ceiling: English translation only; Latin not consulted

### Witness: Augustine, *De Trinitate* (NPNF1 vol. 3, Haddan translation)

- Repository ids: `work.augustine.de-trinitate` (registered with this publication).
- URL: https://ccel.org/ccel/s/schaff/npnf103/cache/npnf103.txt
- Retrieved: 2026-09-29T12:55:20Z
- SHA-256 of the bytes read: cc8d3ff7ce4d4ba293f50a06200af03ff0e5abdeb5200db3a59b4dbe2cad7bdb (3357503 bytes)
- Loci read: III.11.22–25
- Quoted: III.11.22 (short phrase, `sec:scripture`)
- Rights: public domain (NPNF)
- Ceiling: English translation only; Latin not consulted

### Witness: Gregory the Great, *Homiliae in Evangelia*, hom. 34 (repository Wikisource Latin edition)

- Repository ids: `work.gregory-the-great.homiliae-in-evangelia` (existing); `edition.gregory-the-great.homiliae-in-evangelia.wikisource-web-2026-09-17` (existing).
- URL: repository edition artifact (Wikisource web capture), no fresh fetch
- Retrieved: edition dated 2026-09-17
- Loci read: Hom. 34.6–10
- Quoted: 34.6, 34.7, 34.8, 34.8–9, 34.9 (Latin phrases, `sec:scripture`; `sec:faith` cites 34.7 without quotation)
- Rights: public domain (PL 76 text via Wikisource)
- Ceiling: wiki transcription; English renderings of the Latin are mine; no public-domain English of Hom. 34 was at hand

### Witness: Thomas Aquinas, *Summa Theologiae* (New Advent, English Dominican Province 2nd rev. ed. 1920; Corpus Thomisticum Latin for key terms)

- Repository ids: `work.thomas-aquinas.summa-theologiae` (existing).
- URL: https://www.newadvent.org/summa/1047.htm … (`na-summa-1047`, `1050`–`1064`, `1106`–`1114`); Latin https://www.corpusthomisticum.org/sth1050.html etc.
- Retrieved: 2026-09-29T12:53:50Z–12:54:36Z
- Loci read: I q. 50 a. 1 s.c., a. 3 s.c.; q. 51 a. 3 ad 5; q. 58 a. 1 ad 2; q. 61 a. 3; q. 62 a. 9 ad 3; q. 63 aa. 5, 7, 8; q. 108 aa. 3, 5 (incl. ad 1), 6; q. 112 a. 1 s.c., a. 2 ad 2, a. 3 corpus/ad 3, a. 4 ad 2; q. 113 aa. 1, 2, 3, 8
- Quoted: those loci (short English phrases)
- Rights: public domain (1920 translation)
- Ceiling: New Advent web text; Latin spot-checked against the ct- files for key terms only

### Witness: *Catechism of the Catholic Church* (vatican.va English)

- Repository ids: `work.catholic-church.catechism` (existing).
- URL: https://www.vatican.va/archive/ENG0015/__P1A.HTM, `__P1B.HTM`, `__P1C.HTM`
- Retrieved: 2026-09-29T12:56:38Z, 13:10:38Z, 13:10:40Z
- Loci read: 328–336, 391–395, 414
- Quoted: 328, 330, 331, 332 (list, elided), 333 (phrases), 334, 336 (incl. Basil as the CCC quotes him), 391, 392, 393 (incl. Damascene as the CCC quotes him), 395, 414; 329 is cited, not quoted, in `sec:scripture`
- Rights: Vatican-site document, short quotations with attribution (per brief)
- Ceiling: English as posted (1997 typical-edition translation); Latin typical edition not consulted

### Witness: *Compendium of the Catechism of the Catholic Church* (2005)

- Repository ids: `work.catholic-church.compendium-of-the-catechism` (registered with this publication).
- URL: https://www.vatican.va/archive/compendium_ccc/documents/archive_2005_compendium-ccc_en.html
- Retrieved: 2026-09-29T13:10:42Z
- SHA-256 of the bytes read: a35594fda5cf56333ff59388de407e152f5cd41e012d68e34f2bf75bbfa691a8 (378892 bytes)
- Loci read: 59–61, 74–75
- Quoted: 60, 61, 74–75 (short phrases, `sec:faith`)
- Rights: Vatican-site document, short quotations with attribution
- Ceiling: English as posted

### Witness: Lateran IV, *Firmiter credimus* (Latin via Denzinger; Tanner English as control only)

- Repository ids: `work.fourth-lateran-council.firmiter-credimus` (existing).
- URL: https://www.papalencyclicals.net/councils/ecum12-2.htm (control only, not quoted)
- Retrieved: 2026-09-29T12:56:39Z
- SHA-256 of the bytes read: b93f45cd1f95cd2b5c994110637699fc665e207040d813107fe4c38c342bef45 (228156 bytes); 604f24c46e0bc71c2018f25dc787a9ab421d4b2e9cf7d1cee1f43e910ef2708f (2333435 bytes)
- Loci read: cap. 1 (DS 800–801)
- Quoted: DS 800–801 Latin (via Denzinger); body English is my rendering of the Latin
- Rights: Latin public domain; the papalencyclicals English is Tanner's copyrighted translation and is not quoted (brief CAUTION)
- Ceiling: as Denzinger

### Witness: Vatican I, *Dei Filius* (vatican.va Latin; Tanner English as control only)

- Repository ids: `work.first-vatican-council.dei-filius` (existing).
- URL: https://www.vatican.va/archive/hist_councils/i-vatican-council/documents/vat-i_const_18700424_dei-filius_la.html; control https://www.papalencyclicals.net/councils/ecum20.htm (not quoted)
- Retrieved: 2026-09-29T12:56:42Z; control 2026-09-29T12:56:40Z
- SHA-256 of the bytes read: cdb6433e97aaa0fd31cd148d513392324c39779f0137402208ad66d19e8d7016 (29192 bytes); 80e25e52ffe10ebb389c1fdc2a9caf44cfca125fc0e75c92d481f2e9c89d242f (155629 bytes)
- Loci read: ch. 1 (DS 3002–3003), can. 1.5 (DS 3025)
- Quoted: ch. 1 and can. 5 Latin
- Rights: Latin public domain; Tanner English not quoted
- Ceiling: vatican.va Latin transcription

### Witness: Council of Florence, *Cantate Domino* (via Denzinger)

- Repository ids: `work.council-of-florence.cantate-domino` (registered with this publication); `work.council-of-florence.laetentur-caeli` (existing).
- URL: via Denzinger (above)
- Retrieved: 2026-09-29T12:56:36Z
- SHA-256 of the bytes read: 604f24c46e0bc71c2018f25dc787a9ab421d4b2e9cf7d1cee1f43e910ef2708f (2333435 bytes)
- Loci read: DS 1333, 1336
- Quoted: DS 1333 (phrase)
- Rights: public-domain Latin
- Ceiling: Denzinger text only; not read in the conciliar acta

### Witness: Council of Trent, Session V (via Denzinger)

- Repository ids: `work.council-of-trent.canones-et-decreta` (existing).
- URL: via Denzinger (above)
- Retrieved: 2026-09-29T12:56:36Z
- SHA-256 of the bytes read: 604f24c46e0bc71c2018f25dc787a9ab421d4b2e9cf7d1cee1f43e910ef2708f (2333435 bytes)
- Loci read: DS 1511
- Quoted: DS 1511 (phrase incl. its quotation of Heb 2:14)
- Rights: public-domain Latin
- Ceiling: Denzinger text only

### Witness: Pius XII, *Humani generis* (1950)

- Repository ids: `work.pius-xii.humani-generis` (registered with this publication).
- URL: https://www.vatican.va/content/pius-xii/en/encyclicals/documents/hf_p-xii_enc_12081950_humani-generis.html
- Retrieved: 2026-09-29T12:56:44Z
- SHA-256 of the bytes read: 95455e6c9667fd5049c721ccd157eb2711540d5e7b5bc028a295a99e39fbca57 (72589 bytes)
- Loci read: n. 26 (DS 3891)
- Quoted: n. 26 English (short) and DS 3891 Latin phrase (via Denzinger)
- Rights: Vatican-site document, short quotation with attribution
- Ceiling: English page; Latin via Denzinger only

### Witness: Paul VI, *Credo of the People of God* (*Solemni hac liturgia*, 1968)

- Repository ids: `work.paul-vi.solemni-hac-liturgia` (existing).
- URL: https://www.vatican.va/content/paul-vi/en/motu_proprio/documents/hf_p-vi_motu-proprio_19680630_credo.html and the `_la.html` twin
- Retrieved: 2026-09-29T13:10:44Z (en), 13:10:45Z (la)
- SHA-256 of the bytes read: 8108a76f218bc8f70f8dbefd1606d070de70506467abeb287cde6ddcfcec6598 (58147 bytes); ee842d279fea0571802c3f83125e161ce0fe787127f0371af73839f1784c90ed (60038 bytes)
- Loci read: 3, 8, 29 (en and la)
- Quoted: 3, 8, 29 (short)
- Rights: Vatican-site document, short quotations with attribution
- Ceiling: as posted

### Witness: Paul VI, general audience of 15 November 1972 (*Liberaci dal male*)

- Repository ids: `work.paul-vi.general-audience-1972-11-15` (registered with this publication); `work.paul-vi.general-audience-1966-01-12` (existing).
- URL: https://www.vatican.va/content/paul-vi/it/audiences/1972/documents/hf_p-vi_aud_19721115.html
- Retrieved: 2026-09-29T12:56:50Z
- SHA-256 of the bytes read: ade46aabccf08b76fcb0ea47f159fe252585939feb0db6d1f649a6be8eb589fe (50375 bytes)
- Loci read: whole address (Italian)
- Quoted: five short Italian phrases; English renderings mine
- Rights: Vatican-site document, short quotations with attribution
- Ceiling: Italian only; no official English on vatican.va

### Witness: CDF, *Fede cristiana e demonologia* (26 June 1975)

- Repository ids: `work.congregation-for-the-doctrine-of-the-faith.christian-faith-and-demonology-1975` (existing).
- URL: https://www.vatican.va/roman_curia/congregations/cfaith/documents/rc_con_cfaith_doc_19750626_fede-cristiana-demonologia_it.html
- Retrieved: 2026-09-29T13:10:47Z
- SHA-256 of the bytes read: c3ebeb93cc0b27dcd02a6b98e4021f44c49b1c37e913d7a9425d5c62613036aa (85871 bytes)
- Loci read: prefatory note; magisterium section; conclusions
- Quoted: four short Italian phrases; English renderings mine
- Rights: Vatican-site document, short quotations with attribution
- Ceiling: Italian version only; the original French publication (L'Osservatore Romano) was not fetched

### Witness: John Paul II, six general-audience catecheses on the angels and demons (July–August 1986)

- Repository ids: `work.john-paul-ii.general-audience-1986-07-09` (registered with this publication); `work.john-paul-ii.general-audience-1986-07-23` (registered with this publication); `work.john-paul-ii.general-audience-1986-07-30` (registered with this publication); `work.john-paul-ii.general-audience-1986-08-06` (registered with this publication); `work.john-paul-ii.general-audience-1986-08-13` (registered with this publication); `work.john-paul-ii.general-audience-1986-08-20` (registered with this publication); `work.john-paul-ii.general-audience-1999-07-28` (existing).
- URL: https://www.vatican.va/content/john-paul-ii/it/audiences/1986/documents/hf_jp-ii_aud_1986{0709,0723,0730,0806,0813,0820}.html
- Retrieved: 2026-09-29T13:11:17Z–13:11:26Z
- Loci read: all six addresses in full
- Quoted: 30 July (`angelo`/`malak` sentence), 6 August (*senza attribuirvi un valore assoluto*), 20 August (reference); English renderings mine
- Rights: Vatican-site document, short quotations with attribution
- Ceiling: Italian only (English pages are empty stubs); a possible 16 July 1986 audience was not checked (see Open issues)

### Witness: Council of Laodicea, canons (NPNF2 vol. 14, Percival translation)

- Repository ids: `work.council-of-laodicea.canons` (existing).
- URL: https://ccel.org/ccel/s/schaff/npnf214/cache/npnf214.txt
- Retrieved: 2026-09-29T12:55:33Z
- SHA-256 of the bytes read: 5b8d0c6518fd71b1de8d626ebf1d6b59c9967d2e7f5d2e0379654b5cbbf0c914 (2570287 bytes)
- Loci read: canon 35 with Percival's notes (Hefele dating 343–381; Theodoret on Col 2:18)
- Quoted: canon 35 (short, `app:chronology`)
- Rights: public domain (NPNF, 1900)
- Ceiling: Percival translation; Greek not checked

### Witness: Roman synod of 745 under Pope Zachary (MGH, *Concilia aevi Karolini* II.1, ed. Werminghoff; archive.org OCR)

- Repository ids: `work.holy-see.roman-synod-745` (registered with this publication).
- URL: https://archive.org/download/conciliaaevikaro2pt1werm/conciliaaevikaro2pt1werm_djvu.txt
- Retrieved: 2026-09-29T13:11:51Z
- SHA-256 of the bytes read: a246239977995d40164f867ff7297f93c5763150115fc2b2d67527d997f1b35a (2099550 bytes)
- Loci read: actio III (pp. 37–44 as OCR'd)
- Quoted: two short Latin phrases (the three-name ruling; *magis demones*)
- Rights: public domain (MGH 1906 scan)
- Ceiling: OCR only, not collated with print; Aldebert's pseudo-angel names (Uriel, Raguel, Tubuel, Adinus, Tubuas, Sabaoc, Simiel) as OCR'd

### Witness: CDWDS, *Directory on Popular Piety and the Liturgy* (2001)

- Repository ids: `work.congregation-for-divine-worship-and-the-discipline-of-the-sacraments.directory-on-popular-piety-2001` (registered with this publication).
- URL: https://www.vatican.va/roman_curia/congregations/ccdds/documents/rc_con_ccdds_doc_20020513_vers-direttorio_en.html
- Retrieved: 2026-09-29T12:56:46Z
- SHA-256 of the bytes read: a9d30018f650a6854f3f13d3691a068a6519c2ebdb8d1fc9a2418ad13b90ed38 (531807 bytes)
- Loci read: 213–217
- Quoted: 217 (short phrase); 215 cited with its Scripture loci
- Rights: Vatican-site document, short quotations with attribution
- Ceiling: English only

### Witness: CDF, Decree on the Opus Angelorum (6 June 1992)

- Repository ids: `work.holy-see.cdf-decree-opus-angelorum-1992` (registered with this publication).
- URL: https://www.vatican.va/roman_curia/congregations/cfaith/documents/rc_con_cfaith_doc_19920606_opus-angelorum_lt.html
- Retrieved: 2026-09-29T13:10:59Z
- SHA-256 of the bytes read: 81d6d107d271c5220db4dad98bfa8be8f22032d6e91d90490f5c9b64865f1d9b (7696 bytes)
- Loci read: whole decree (short)
- Quoted: none verbatim in the body; paraphrased in `app:chronology`
- Rights: public act, Latin
- Ceiling: vatican.va Latin; the 24 Sept 1983 decisions (AAS 76 [1984] 175–176) are known only through this decree's recital and are so marked

## The Greek Fathers before Nicaea

### Clement of Rome, First Epistle to the Corinthians
- Witness: Clement of Rome, *1 Clement*, tr. in ANF vol. 1 (Roberts/Donaldson/Coxe, 1885), CCEL plain text.
- Repository ids: `work.ante-nicene-fathers.volume-1` (existing).
- URL: https://ccel.org/ccel/s/schaff/anf01/cache/anf01.txt
- Retrieved: 2026-09-29T12:55:11Z
- SHA-256 of the bytes read: ee9c7f0ac3f4df08d07ddf81cd7e061e82a35e0d27de611cae06f1e05b2fb991 (3149312 bytes)
- Loci read: chs. 29, 34, 36 (and chapter scan for all angel mentions, chs. 1–59).
- Quoted: 29; 34 (block); 36.
- Rights: public domain (1885 translation).
- Ceiling: CCEL e-text of ANF; not collated with print or with the Greek.

### Ignatius of Antioch, Letters to the Trallians, Smyrnaeans, Ephesians
- Witness: Ignatius, *Trall.*, *Smyrn.*, *Eph.*, shorter and longer Greek recensions in parallel, ANF vol. 1.
- Repository ids: `work.ignatius-of-antioch.letter-to-the-smyrnaeans` (existing).
- URL: https://ccel.org/ccel/s/schaff/anf01/cache/anf01.txt
- Retrieved: 2026-09-29T12:55:11Z
- SHA-256 of the bytes read: ee9c7f0ac3f4df08d07ddf81cd7e061e82a35e0d27de611cae06f1e05b2fb991 (3149312 bytes)
- Loci read: Trall. 5 (both recensions), Smyrn. 6, Eph. 13, 19 (both recensions); ANF introductory note on the recensions.
- Quoted: Trall. 5 (shorter; and longer recension marked as such); Smyrn. 6; Eph. 13, 19 (shorter).
- Rights: public domain.
- Ceiling: English only; the longer recension identified as an interpolated expansion on the ANF introductory note's authority.

### Epistle of Barnabas; Epistle to Diognetus; Martyrdom of Polycarp
- Witness: ANF vol. 1 translations.
- Repository ids: `work.ante-nicene-fathers.volume-1` (existing).
- URL: as above. Retrieved: 2026-09-29T12:55:11Z. Cache: text/ccel-anf01.txt
- Loci read: Barn. 18; Diogn. 7; Mart. Pol. 2, 14.
- Quoted: all four loci.
- Rights: public domain.
- Ceiling: English only.

### Hermas, The Shepherd
- Witness: *The Pastor of Hermas*, ANF vol. 2 (1885).
- Repository ids: none registered; the entry cites the edition directly.
- URL: https://ccel.org/ccel/s/schaff/anf02/cache/anf02.txt
- Retrieved: 2026-09-29T12:55:12Z
- SHA-256 of the bytes read: ae8e15414a21fe8d54a30fee7c3fbd1ee6a018e624dcd681d030da5c1cabbcac (3768675 bytes)
- Loci read: Vis. III.1–7, IV.1–2, V; Mand. VI.1–2, VII, XI, XII.4–6; Sim. V.5–6, VI.1–3, VII, VIII.1–3, IX.1, 12–14, 25, 27, X.1–4.
- Quoted: Vis. III.2, 3, 4 (block), 5; IV.2; V; Mand. VI.2 (block), VII, XI, XII.4, 5; Sim. V.5–6, VI.2–3, VIII.1, 3 (block), IX.12, 14, X.1, 2.
- Rights: public domain.
- Ceiling: English only; ANF's composite text (Vatican/Palatine/Ethiopic variants noted in its footnotes, not weighed).

### Justin Martyr, First and Second Apologies, Dialogue with Trypho
- Witness: ANF vol. 1.
- Repository ids: `work.justin-martyr.first-apology` (existing); `work.justin-martyr.second-apology` (existing).
- URL: https://ccel.org/ccel/s/schaff/anf01/cache/anf01.txt
- Retrieved: 2026-09-29T12:55:11Z. Cache: text/ccel-anf01.txt
- Loci read: 1 Apol. 5, 6, 13, 16, 28, 63; 2 Apol. 4–9 (ANF numbering: ch. 5 "How the angels transgressed"); Dial. 56–60, 79, 103, 124–125, 128, 141.
- Quoted: 1 Apol. 6 (block), 16, 28, 63; 2 Apol. 5 (block), 7; Dial. 56, 57, 60, 79, 125, 128, 141.
- Rights: public domain.
- Ceiling: English only; ANF's footnote on the grammar of 1 Apol. 6 read, not reproduced.

### Athenagoras, A Plea for the Christians (Legatio)
- Witness: ANF vol. 2.
- Repository ids: none registered; the entry cites the edition directly.
- URL: https://ccel.org/ccel/s/schaff/anf02/cache/anf02.txt
- Retrieved: 2026-09-29T12:55:12Z. Cache: text/ccel-anf02.txt
- Loci read: Leg. 10, 24–28.
- Quoted: 10 (block), 24 (block and inline), 25, 26, 27.
- Rights: public domain. Ceiling: English only.

### Tatian, Address to the Greeks
- Witness: ANF vol. 2 (with the ANF introductory note on Tatian's later Encratism).
- Repository ids: none registered; the entry cites the edition directly.
- URL / Retrieved / Cache: as ANF 2 above.
- Loci read: Or. 7–9, 12–16, 20; introductory note.
- Quoted: 7, 12, 14, 15, 16. Greek term `angelos protogonos` from the American editor's note [441] at ch. 7.
- Rights: public domain. Ceiling: English only.

### Theophilus of Antioch, To Autolycus
- Witness: ANF vol. 2.
- Repository ids: none registered; the entry cites the edition directly.
- URL / Retrieved / Cache: as ANF 2.
- Loci read: II.8, II.28, II.29.
- Quoted: II.8, 28, 29. Greek `apodedrakenai` as printed in ANF; the gloss joining it to `drakon` is editorial exposition of Theophilus's stated etymology.
- Rights: public domain. Ceiling: English only.

### Irenaeus, Against Heresies
- Witness: ANF vol. 1.
- Repository ids: `work.irenaeus.adversus-haereses` (existing).
- URL: https://ccel.org/ccel/s/schaff/anf01/cache/anf01.txt. Retrieved: 2026-09-29T12:55:11Z. Cache: text/ccel-anf01.txt
- Loci read: I.10.1–2; II.2.1–5; II.30.3–9; II.32.4–5; III.8.1–3; III.23.3; IV.7.4; IV.16.2; IV.20.1; IV.36.4; IV.37.1; IV.40.1–3; IV.41.1–3; V.21.1–3; V.23.1–2; V.24.1–4.
- Quoted: all loci listed except II.30.4 and V.24.1 (read, not quoted in final text).
- Rights: public domain.
- Ceiling: English from the Latin and Greek fragments as ANF prints them; chapter titles are ANF editorial and not quoted as Irenaeus.

### Clement of Alexandria, Stromata
- Witness: ANF vol. 2.
- Repository ids: none registered; the entry cites the edition directly.
- URL / Retrieved / Cache: as ANF 2.
- Loci read: VI.3 (angel mentions), VI.7, VI.13, VI.16, VI.17; VII.1, VII.2, VII.7, VII.12, VII.13.
- Quoted: VI.7, 13, 16, 17; VII.1, 2 (block and inline), 7, 12, 13.
- Rights: public domain. Ceiling: English only.

### Origen, De principiis (Rufinus's Latin, tr. Crombie)
- Witness: ANF vol. 4 (Crombie's translation of Rufinus, with Jerome fragments from the Letter to Avitus).
- Repository ids: `work.origen.de-principiis` (existing).
- URL: https://ccel.org/ccel/s/schaff/anf04/cache/anf04.txt
- Retrieved: 2026-09-29T12:55:15Z. Cache: text/ccel-anf04.txt
- Loci read: preface 1–10 with notes [1919]–[1932]; I.5.1–5; I.6.1–4; I.8.1–4 and the two Jerome fragments; II.9.1–7; III.2.1–4; III.3.1–3.
- Quoted: preface 5, 6, 10; I.5.1, 2, 4, 5; I.6.1, 2, 3; I.8.1 (block and inline), 3, 4; Jerome fragment after I.8; II.9.1, 2, 3, 6; III.2.1, 2, 3, 4; III.3.2.
- Rights: public domain.
- Ceiling: English of Rufinus's Latin; Greek fragments not consulted beyond the Jerome fragment in ANF.

### Origen, Contra Celsum
- Witness: ANF vol. 4 (tr. Crombie).
- Repository ids: `work.origen.contra-celsum` (existing).
- URL / Retrieved / Cache: as ANF 4.
- Loci read: V.1–6, V.29–32; VIII.13, 25–27, 34–36, 57, 60, 64.
- Quoted: V.4 (block), 5, 29, 30, 32; VIII.13, 25, 27, 34 (block and inline), 36 (block), 57, 60, 64 (block).
- Rights: public domain. Ceiling: English only.

### Origen, Commentary on Matthew, Book XIII
- Witness: ANF vol. 9 (1896 additional volume; tr. Patrick).
- Repository ids: `work.origen.commentarium-in-matthaeum` (registered with this publication); `work.ante-nicene-fathers.volume-9` (existing).
- URL: https://ccel.org/ccel/s/schaff/anf09/cache/anf09.txt
- Retrieved: 2026-09-29T13:24:25Z. Cache: text/ccel-anf09.txt
- Loci read: XIII.26, 27, 28.
- Quoted: XIII.26, 27, 28.
- Rights: public domain. Ceiling: English only; complements the treatment in 70-disputed-questions.tex (sec:disputed), which covers XIII.27–28 for q. 113 a. 5.

### Gregory Thaumaturgus, Oration and Panegyric Addressed to Origen
- Witness: ANF vol. 6 (with introductory notice: native of Neocaesarea in Pontus, journey toward Berytus for law, Panegyric as valedictory at Caesarea, later bishop of Neocaesarea).
- Repository ids: `work.ante-nicene-fathers.volume-6` (existing).
- URL: https://ccel.org/ccel/s/schaff/anf06/cache/anf06.txt
- Retrieved: 2026-09-30T14:09:50Z (fetched by this lane). Cache: text/ccel-anf06.txt
- Loci read: Arguments IV, V, XIX; introductory notice.
- Quoted: IV (block and inline), V, XIX.
- Rights: public domain. Ceiling: English only.

### Methodius of Olympus, Banquet of the Ten Virgins; Discourse on the Resurrection (with Photius's synopsis and the Damascene fragment)
- Witness: ANF vol. 6.
- Repository ids: none registered; the entry cites the edition directly.
- URL / Retrieved / Cache: as ANF 6.
- Loci read: Symp. I.4 (angels mention), II.6, III.4, III.6, VIII.10; De res. I.9–12; Part II (Damascene fragment); Part III.1–9 (Photius, cod. 234, with notes [2894]–[2897]); introductory notice (bishop of Olympus and Patara in Lycia).
- Quoted: Symp. II.6, III.6, VIII.10; De res. I.10 (block and inline), I.12; Part II fragment; Photius synopsis 7.
- Rights: public domain.
- Ceiling: English only; Part III is Photius's précis, cited as such.

### Augustine, De civitate Dei XV.23, XVI.29
- Witness: NPNF series 1 vol. 2 (tr. Dods).
- Repository ids: `work.augustine.de-civitate-dei` (existing); `work.nicene-and-post-nicene-fathers.series-1-volume-2` (existing).
- URL: https://ccel.org/ccel/s/schaff/npnf102/cache/npnf102.txt
- Retrieved: 2026-09-29T12:55:19Z. Cache: text/ccel-npnf102.txt
- Loci read: XV.23 (whole chapter), XVI.29.
- Quoted: XVI.29 only; XV.23 cited for position (sons of God = Sethites; holy angels could not so fall).
- Rights: public domain. Ceiling: English only.

### John Chrysostom, Homiliae in Genesim 22
- Witness: Migne, PG 53 (Paris 1862), Greek text, archive.org OCR.
- Repository ids: none registered; the entry cites the edition directly.
- URL: https://archive.org/download/patrologiae_cursus_completus_gr_vol_053/patrologiae_cursus_completus_gr_vol_053_djvu.txt
- Retrieved: 2026-09-30T14:20:51Z (fetched by this lane). Cache: text/ia-pg53-djvu.txt (lines ~25765–25900).
- Loci read: Hom. 22.2–3 (Greek): refutes the angel reading of Gen 6:2 (angels are never called sons of God; the devil fell before man's creation; the bodiless nature is incapable of such desire, Matt 22:30) and identifies the sons of God with the line of Seth and Enos.
- Quoted: nothing (position only, own reading of the Greek; no English rendering printed).
- Rights: public domain (1862 text).
- Ceiling: noisy Greek OCR; section numbers and PG columns not verified against the page image, so the body cites "Hom. in Gen. 22" without column.

### Thomas Aquinas, Summa theologiae (English Dominican 1920, New Advent; Latin Corpus Thomisticum)
- Witness: ST I qq. 45 (Latin), 47, 50, 51, 59, 61, 62, 63, 64, 106, 108, 110, 111, 113, 114.
- Repository ids: `work.thomas-aquinas.summa-theologiae` (existing).
- URL: https://www.newadvent.org/summa/1047.htm (and 1050, 1051, 1059, 1061–1064, 1106, 1108, 1110, 1111, 1113, 1114); https://www.corpusthomisticum.org/sth1044.html
- Retrieved: 2026-09-29 (12:53–12:54Z; ct-sth1044 12:54:28Z).
- SHA-256 of the bytes read: 41c6edfab20faec48a4181d11d3dbde6549398127633854b20c60bce9f3c5b9c (176483 bytes)
- Loci read: I q. 45 a. 5 (s.c., corpus, Latin); q. 47 a. 2 corpus and ad 3; q. 50 a. 3 s.c.; q. 51 aa. 1–3 (obj. 1 and ad 1; a. 2 s.c.; a. 3 ad 5, ad 6); q. 59 titles; q. 61 a. 1 title; q. 62 a. 6 s.c.; q. 63 aa. 2 (corpus), 3 (s.c.), 5 (corpus), 6 (obj. 2 and ad 2), 7 (obj. 1, ad 1), 8 (s.c.); q. 64 a. 1 ad 4, a. 2 corpus, a. 4; q. 106 titles; q. 108 aa. 5–6, 8; q. 110 a. 1 corpus; q. 111 aa. 1–3 corpus; q. 113 aa. 5, 7 obj. 4, 8 corpus; q. 114 aa. 1, 3.
- Quoted: q. 51 a. 3 ad 5 ("in whom, nevertheless, he worshipped God"); q. 63 a. 5 ("under the figure of the prince of Babylon"; "in the person of the King of Tyre"); q. 63 a. 7 ad 1; q. 110 a. 1 (Origen's Hom. in Num. as quoted by Aquinas).
- Rights: public domain (1920).
- Ceiling: New Advent transcription; Latin checked only for q. 45 a. 5.

### Denzinger (Constantinople 543, DS 403–411); Lateran IV (DS 800)
- Witness: Denzinger Latin (patristica.net); Lateran IV Latin as quoted in the CDF 1975 study (vatican.va, Italian page, Latin quotation with COD n. 800).
- Repository ids: `work.denzinger.enchiridion-symbolorum` (existing).
- URL: https://patristica.net/denzinger/enchiridion-symbolorum.html; https://www.vatican.va/roman_curia/congregations/cfaith/documents/rc_con_cfaith_doc_19750626_fede-cristiana-demonologia_it.html
- Retrieved: 2026-09-29T12:56:36Z; 2026-09-29T13:10:47Z
- SHA-256 of the bytes read: 604f24c46e0bc71c2018f25dc787a9ab421d4b2e9cf7d1cee1f43e910ef2708f (2333435 bytes); c3ebeb93cc0b27dcd02a6b98e4021f44c49b1c37e913d7a9425d5c62613036aa (85871 bytes)
- Loci read: DS 403–411; DS 800 (Latin sentence "Diabolus enim et daemones alii ...").
- Quoted: nothing verbatim in the body (paraphrase of DS 403, 411, 800).
- Rights: Latin public domain; English paraphrase only. Ceiling: web transcriptions.

### Catechism of the Catholic Church 328–336
- Witness: CCC English, vatican.va.
- Repository ids: `work.catholic-church.catechism` (existing).
- URL: https://www.vatican.va/archive/ENG0015/__P1A.HTM. Retrieved: 2026-09-29T12:56:38Z. Cache: text/ccc-en-P1A.txt
- Loci read: 328–336.
- Quoted: 328 (two short phrases).
- Rights: Vatican-site document; short quotation with attribution. Ceiling: web text.

### Douay–Rheims (Challoner), Project Gutenberg 1581
- Witness: edition `edition.english-college-of-douay.douay-rheims-bible.challoner-gutenberg-1581`.
- URL: https://www.gutenberg.org/cache/epub/1581/pg1581.txt. Retrieved: 2026-09-29T12:58:58Z. Cache: text/gut-douay-rheims-1581.txt
- Loci read: Gen 6:2; 48:16; Deut 32:8; Job 40:20; Ps 33:8; 90:11; Wis 11:21; Dan 6:22; 7:10; 10:13; Zach 1:14; Matt 18:10; Luke 10:18; Acts 12:15; Apoc 12:4.
- Quoted: Deut 32:8; Matt 18:10 (Douay wording).
- Rights: public domain.

## The Celestial Hierarchy, the nine orders, and Dionysius in the treatise

### Witness 1
- Witness: Pseudo-Dionysius the Areopagite, *De caelesti hierarchia*, English translation by John Parker, *The Works of Dionysius the Areopagite*, Part II (London and Oxford: James Parker and Co., 1899), web transcription at tertullian.org.
- Repository ids: `work.pseudo-dionysius-the-areopagite.de-caelesti-hierarchia` (registered with this publication).
- URL: https://www.tertullian.org/fathers/areopagite_13_heavenly_hierarchy.htm (also areopagite_01_intro.htm, areopagite_11_objections.htm, areopagite_12_introduction.htm)
- Retrieved: 2026-09-29T12:55:02Z
- SHA-256 of the bytes read: ae7608cea7b9f874f2b8ebdabfbe9cfae8b74285fec914aeca3d87cd9089104d (114110 bytes)
- Loci read: entire treatise, chapters 1–15, dedication and colophon; Parker's introductions and "Objections".
- Quoted: CH 1.1–3; 2.1–5; 3.1–3; 4.1–4; 5; 6; 7.1–4; 8.1–2; 9.1–4; 10.1–3; 11.1–2; 12.1–3; 13.1–4; 14; 15.1–9 (verbatim phrases in section 15 file, cited by Parker section).
- Rights: public domain (published 1899; Parker died 1917; US pre-1930 publication).
- Ceiling: web transcription of a print translation; not collated with print; Parker defends the Areopagite authorship (rejected by modern scholarship — not quoted on that point). Note: Parker's ch. 6 has no section division; Migne divides it into §§1–2.

### Witness 2
- Witness: Gregory the Great, *Homiliae in Evangelia* 34, Latin text (Wikisource transcription of a Migne-based text), read for the nine orders, the names, and the citation of Dionysius.
- Repository ids: `work.gregory-the-great.homiliae-in-evangelia` (existing); `edition.gregory-the-great.homiliae-in-evangelia.wikisource-web-2026-09-17` (existing).
- URL: https://la.wikisource.org/wiki/Homiliae_in_Evangelia_(Gregorius_Magnus)
- Retrieved: 2026-09-17 (edition registered 2026-09-17; text extracted to lane scratch 2026-09-29)
- Loci read: Hom. 34 §§1–16 (full homily); §§7–14 read closely.
- Quoted: 34.7 (novem ordines; Ezek 28:12); 34.8 (nomen officii non naturae); 34.9 (minima/summa nuntiant); 34.10 (per-order characterizations, quoted in appendices); 34.12 (Fertur vero Dionysius Areopagita, antiquus videlicet et venerabilis Pater).
- Rights: PD text (PL 76); CC-BY-SA-3.0 for the Wikisource transcription layer.
- Ceiling: web transcription of a Migne-based Latin text; not collated with CCSL/Étaix.

### Witness 3
- Witness: Migne, *Patrologia Graeca* 3 (Dionysius), Corderius edition — scanned page images used only to verify chapter incipit columns for the Celestial Hierarchy.
- Repository ids: none registered; the entry cites the edition directly.
- URL: https://archive.org/details/patrologiae_cursus_completus_gr_vol_003_dionysius_areopagita
- Retrieved: 2026-09-29T13:12:05Z
- Loci read: CH incipits at cols 120B (ch. 1 §1), 136D (ch. 2), 164D (ch. 3), 177C (ch. 4), 196B (ch. 5), 200C (ch. 6 §1), 205B (ch. 7 §1), 237B (ch. 8), 257B (ch. 9 §1; heading 257A), 272D (ch. 10 §1; heading 272C), 284B (ch. 11), 292C (ch. 12), 300B (ch. 13), 321A (ch. 14), 325D (ch. 15 heading); Corderius note on ch. 14 citing ST I q. 50 a. 3.
- Quoted: none (columns only).
- Rights: PD (1865 printing).
- Ceiling: columns for ch. 5/6/7 letters assigned by quarter-page pattern from leaf layout (letter position inferred from page structure, not from a printed letter on the crop); chapter numbers and column numbers read from images directly.

### Witness 4
- Witness: Thomas Aquinas, *Summa theologiae*, New Advent English (Fathers of the English Dominican Province).
- Repository ids: `work.thomas-aquinas.summa-theologiae` (existing).
- URL: https://www.newadvent.org/summa/ (files 1047, 1050–1064, 1106–1114, 3008, 3030, 3059)
- Retrieved: 2026-09-29T12:53:50Z–12:54:25Z
- Loci read: I q. 108 aa. 5–6 read in full; programmatic extraction of every "Dionysius" mention and every "(Coel. Hier.|Div. Nom.|Eccl. Hier.|Myst. Theol.|Hier. Ang.|De Div. Nom.)" parenthetical in the listed files; contexts of all 98 citations inspected.
- Quoted: short phrases from the translation in the section 15 Reception fields and in appendix 05 glosses.
- Rights: translation 1920, PD (US); New Advent HTML used as transcription.
- Ceiling: English translation only; not collated with the Leonine Latin. Note: na-summa-3008 is **II-II q. 8** (gift of understanding), not III q. 8 — New Advent 3xxx series is Secunda Secundae. New Advent prints "Hom. xxiv in Ev." in I q. 108 a. 6 where the homily is xxxiv (their typographical slip or their edition's).

### Witness 5
- Witness: Benedict XVI, General Audience "Pseudo-Dionysius, the Areopagite", 14 May 2008 (vatican.va English).
- Repository ids: `work.benedict-xvi.general-audience-2008-05-14` (registered with this publication).
- URL: https://www.vatican.va/content/benedict-xvi/en/audiences/2008/documents/hf_ben-xvi_aud_20080514.html
- Retrieved: 2026-09-29T13:10:55Z
- SHA-256 of the bytes read: 29c715514923e6bf32cb09bc7264de8b522ef11aaeebfde6d2588391dac6a0f0 (45874 bytes)
- Loci read: whole audience.
- Quoted: "a sixth-century theologian whose name is unknown and who wrote under the pseudonym of Dionysius the Areopagite"; Proclus "who died in Athens in 485"; "did not want to glorify his own name"; "truly to serve the Gospel, to create an ecclesial theology"; "symphony of the cosmos that goes from the Seraphim to the Angels and Archangels"; "virtually rediscovered in the 13th century, especially by St Bonaventure".
- Rights: © Libreria Editrice Vaticana; brief quotation with attribution.
- Ceiling: official English translation; not collated with the Italian.

### Witness 6
- Witness: J. Stiglmayr, "Dionysius the Pseudo-Areopagite", *Catholic Encyclopedia* V (1909); J. P. Kirsch, "Hilduin, Abbot of St-Denis", *Catholic Encyclopedia* VII (1910).
- Repository ids: `work.catholic-encyclopedia.volume-5` (existing); `work.catholic-encyclopedia.volume-7` (existing).
- URL: https://www.newadvent.org/cathen/05013a.htm ; https://www.newadvent.org/cathen/07354a.htm
- Retrieved: 2026-09-29T13:10:56Z / 13:10:58Z
- SHA-256 of the bytes read: a704ad6ccc98d22749dce0515c081c40a973bcd67993a0db3ad872c9c5aa3433 (61832 bytes); e87ceb104d81f949546dfb4a178e00e8b2ff9b6172651861ae2a90fa9b82ab21 (11365 bytes)
- Loci read: both articles in full (historical portions closely).
- Quoted: none verbatim; facts cited: Severus (512–518, letter to abbot John), 533 conference and Hypatius, Sergius of Resaina (d. 536) Syriac version, Koch and Stiglmayr 1895 on Proclus, Michael II's gift 827, Hilduin translation and Denis identification, Eriugena c. 858 for Charles the Bald, Victorines and scholastics, Valla (1407–1457).
- Rights: PD (1909/1910).
- Ceiling: secondary reference, a century old; used only for reception history.

### Witness 7
- Witness: Douay-Rheims Bible (1581/1609), Project Gutenberg transcription.
- Repository ids: `work.english-college-of-douay.douay-rheims-bible` (existing).
- URL: https://www.gutenberg.org/cache/epub/1581/pg1581.txt
- Retrieved: 2026-09-29T12:58:58Z
- SHA-256 of the bytes read: 7d10da78d8ec97db53b4e2bd8719cc01e16106b44937a673ba34aa534a04c007 (5880580 bytes)
- Loci read: Gen 3:24; 4 Kgs 19:15; Tob 12:15; Ps 9:5; 79:2; 81:6; 102:21; 103:4; Isa 6:2–3, 6; 9:6; 63:2 (see open issue); Ezek 3:12; 9; 10:1, 7, 13, 20; 28:12–13; Dan 7:10; 8:16; 10:13; Zech 1–2; Mal 2:7; Matt 4:11; 18:10; 26:53; Luke 1:19; 1 Cor 3:9; Rom 8:38; Eph 1:21; 3:10; Col 1:16; 1 Thess 4:15; Jude 9; Apoc 4:8; 12:7; 1 Pet 3:22; Ps 21:7.
- Quoted: DR wording in appendix 01 scripture loci.
- Rights: PD.
- Ceiling: Gutenberg transcription; verses verified by direct string match.

## Angelic substance; bodies, place, and motion (ST I qq. 50-53)

### Aquinas, Summa theologiae, English
- Witness: Thomas Aquinas, *Summa theologiae* I qq. 50–53, trans. Fathers of the English Dominican Province, 2nd rev. ed. 1920, New Advent online edition.
- Repository ids: `work.thomas-aquinas.summa-theologiae` (existing).
- URL: https://www.newadvent.org/summa/1050.htm, 1051.htm, 1052.htm, 1053.htm
- Retrieved: 2026-09-29T12:53:51Z–12:53:55Z
- SHA-256 of the bytes read: 61ff4ab95cc9d06e45d5026da5c0071ed658d5d324eaf661d205faa3371df5be (50349 bytes); 912322a94acf2906d08fafcb71b69b0aabe61693222de87bd375feb65801088a (31771 bytes)
- Loci read: every article of I qq. 50–53, in full (objections, sed contra, corpus, replies).
- Quoted: q. 50 a. 1 co., ad 1, ad 3; a. 2 co., ad 3, ad 4; a. 3 co., ad 4; a. 4 co., ad 1, ad 3; a. 5 co., ad 1, ad 3; q. 51 a. 1 co., ad 1, ad 3; a. 2 co., ad 1–3; a. 3 co., ad 1, ad 2, ad 4–6; q. 52 a. 1 s.c., co.; a. 2 co., ad obj.; a. 3 co.; q. 53 a. 1 s.c., co., ad 2, ad 3; a. 2 co.; a. 3 co., ad 1, ad 3.
- Rights: public domain (1920 translation); New Advent presentation.
- Ceiling: web transcription, not collated with the 1920 print. New Advent omits the question prologues in English; the prologue of q. 50 is given from the Latin only.

### Aquinas, Summa theologiae, Latin
- Witness: Thomas Aquinas, *Summa theologiae* I qq. 50–64, Leonine text as presented by Corpus Thomisticum.
- Repository ids: `work.thomas-aquinas.summa-theologiae` (existing).
- URL: https://www.corpusthomisticum.org/sth1050.html
- Retrieved: 2026-09-29T12:54:32Z
- SHA-256 of the bytes read: e2cfab53e3a057155f3e241b32c059123265ae7cfe58da04e9d7cb41f3fb0ee7 (402442 bytes)
- Loci read: I q. 50 pr. and all articles of qq. 50–53 (corpus and key replies); prologues of qq. 51, 52, 53, 54, 59, 61.
- Quoted: q. 50 pr.; q. 50 a. 1 co. (hic et nunc), a. 2 co. (secundum modum suum), a. 2 ad 3 (quo est / quod est), a. 5 co.; q. 51 pr., a. 1 co., a. 2 ad 1, a. 3 co.; q. 52 a. 1 s.c., co., a. 2 co. (circumscriptive / definitive), a. 3 co.; q. 53 pr., a. 3 ad 1.
- Rights: Latin text public domain; Corpus Thomisticum presentation.
- Ceiling: web transcription of the Leonine text; not collated with print.

### Aquinas, De spiritualibus creaturis
- Witness: Thomas Aquinas, *Quaestio disputata de spiritualibus creaturis*, Corpus Thomisticum.
- Repository ids: `work.thomas-aquinas.de-spiritualibus-creaturis` (registered with this publication).
- URL: https://www.corpusthomisticum.org/qds.html
- Retrieved: 2026-09-29T12:54:57Z
- SHA-256 of the bytes read: 525438a81d5e92e57ec744e24be08c2a90e64fbe2e4cdc0d4919d6b45c96580f (357192 bytes)
- Loci read: a. 1 title and corpus; a. 8 title and corpus.
- Quoted: a. 1 co. (sed tamen hoc non est proprie dictum secundum communem usum nominum).
- Rights: public domain Latin.
- Ceiling: web transcription.

### Aquinas, De ente et essentia
- Witness: Thomas Aquinas, *De ente et essentia*, Corpus Thomisticum.
- Repository ids: `work.thomas-aquinas.de-ente-et-essentia` (registered with this publication).
- URL: https://www.corpusthomisticum.org/oee.html
- Retrieved: 2026-09-29T12:54:59Z
- SHA-256 of the bytes read: 4fbd17e8136d920cd929f7b67fca45693f15eccdf4db7495bd16f9bcca119bb7 (54615 bytes)
- Loci read: the chapter on separate substances (Leonine c. 4, which Corpus Thomisticum numbers `cap. 3`; paragraph [69874]).
- Quoted: none in the body; cited as a parallel.
- Rights: public domain Latin.
- Ceiling: web transcription. The body cites the Leonine chapter number c. 4.

### Aquinas, De substantiis separatis
- Witness: Thomas Aquinas, *De substantiis separatis*, Corpus Thomisticum.
- Repository ids: `work.thomas-aquinas.de-substantiis-separatis` (registered with this publication).
- URL: https://www.corpusthomisticum.org/ots.html
- Retrieved: 2026-09-29T12:54:53Z
- SHA-256 of the bytes read: 3149f5709dbec16c044723d25f009a4a43caf0d38e965f28a0972b55474c78d9 (167879 bytes)
- Loci read: cc. 5–8 (titles; c. 5 in full; c. 7 conclusions).
- Quoted: none in the body; cited as a parallel.
- Rights: public domain Latin.
- Ceiling: web transcription.

### Aquinas, Summa contra gentiles II
- Witness: Thomas Aquinas, *Summa contra gentiles* II cc. 46–55, Corpus Thomisticum.
- Repository ids: `work.thomas-aquinas.summa-contra-gentiles` (registered with this publication).
- URL: https://www.corpusthomisticum.org/scg2046.html
- Retrieved: 2026-09-29T12:55:01Z
- SHA-256 of the bytes read: 4facc3d0007a2edd8ab7f3bfe103446384124af3b18fa1d856b0a45055f33390 (69826 bytes)
- Loci read: titles of cc. 46–55; c. 46 key sentences; c. 54 nn. 1–3.
- Quoted: none in the body; cited as a parallel.
- Rights: public domain Latin.
- Ceiling: web transcription. The cache stops at c. 55, so SCG II cc. 91–93 (multitude and species of separate substances) were not read.

### John Damascene, De fide orthodoxa II.3
- Witness: John of Damascus, *An Exact Exposition of the Orthodox Faith* II.3 "Concerning angels", trans. S. D. F. Salmond, NPNF series 2 vol. 9 (1899), CCEL plain text.
- Repository ids: `work.john-of-damascus.de-fide-orthodoxa` (registered with this publication).
- URL: https://ccel.org/ccel/s/schaff/npnf209/cache/npnf209.txt
- Retrieved: 2026-09-29T12:55:27Z
- SHA-256 of the bytes read: 859ba34cc5998f2761b801aa5de724b2ea741a54d98e21614faeb89cc40f8ad4 (2606804 bytes)
- Loci read: II.3 entire.
- Quoted: II.3 ("compared with God … dense and material"; "immortal, not by nature but by grace"; "Whether they are equals in essence … alone knoweth"; "They are circumscribed …"; "cannot be present and energise in various places at the same time").
- Rights: public domain (1899).
- Ceiling: CCEL transcription of the NPNF print; English of a Greek text; footnote markers dropped from quotations.

### Ambrose, De Spiritu Sancto I.7
- Witness: Ambrose, *On the Holy Spirit* I.7.81, trans. H. de Romestin, NPNF series 2 vol. 10 (1896), CCEL.
- Repository ids: `work.ambrose.de-spiritu-sancto` (registered with this publication).
- URL: https://ccel.org/ccel/s/schaff/npnf210/cache/npnf210.txt
- Retrieved: 2026-09-29T12:55:29Z
- SHA-256 of the bytes read: 14fa05cc98a67cb1ccf7613e63d5eb80fd48feb3e09dd29210e70f53dfcd7577 (2963575 bytes)
- Loci read: I.7.80–82 (NPNF prints the section number 81 twice).
- Quoted: I.7.81.
- Rights: public domain.
- Ceiling: transcription; not collated with the Latin.

### Dionysius, Divine Names 4
- Witness: Dionysius the Areopagite, *On Divine Names*, trans. John Parker, *Works* (London 1897), tertullian.org transcription.
- Repository ids: `work.pseudo-dionysius-the-areopagite.de-divinis-nominibus` (registered with this publication).
- URL: https://www.tertullian.org/fathers/areopagite_03_divine_names.htm
- Retrieved: 2026-09-29T12:55:07Z
- SHA-256 of the bytes read: 7d89093873b2ea5b8cf88e96c9066ce04907a0231523db3fa363c22039dc4295 (206269 bytes)
- Loci read: DN 4.1.
- Quoted: DN 4.1 ("conceived of as incorporeal and immaterial"; "have their life, continuous and undiminished, purified from all corruption and death and matter, and generation").
- Rights: public domain (1897).
- Ceiling: web transcription of Parker; the Summa's Latin citations ("IV cap. de Div. Nom.") matched to DN 4.1 by content.

### Dionysius, Celestial Hierarchy 10, 14, 15
- Witness: Dionysius, *Celestial Hierarchy*, trans. John Parker, *Works* vol. 2 (London 1899), tertullian.org.
- Repository ids: `work.pseudo-dionysius-the-areopagite.de-caelesti-hierarchia` (registered with this publication).
- URL: https://www.tertullian.org/fathers/areopagite_13_heavenly_hierarchy.htm
- Retrieved: 2026-09-29T12:55:02Z
- SHA-256 of the bytes read: ae7608cea7b9f874f2b8ebdabfbe9cfae8b74285fec914aeca3d87cd9089104d (114110 bytes)
- Loci read: CH 10.1–2; 14; 15.3.
- Quoted: CH 10.2; CH 14; CH 15.3.
- Rights: public domain (1899).
- Ceiling: web transcription. The Summa's "Coel. Hier." at q. 51 a. 3 ad 2 names no chapter; CH 15.3 is the matching passage.

### Augustine, De civitate Dei XV.23, XVI.29
- Witness: Augustine, *City of God*, trans. Marcus Dods, NPNF series 1 vol. 2 (1887), CCEL.
- Repository ids: `work.augustine.de-civitate-dei` (existing).
- URL: https://ccel.org/ccel/s/schaff/npnf102/cache/npnf102.txt
- Retrieved: 2026-09-29T12:55:19Z
- SHA-256 of the bytes read: 5c973feda803f3e58a88ed7df210b42d436f5466741eb8dbeae713ab56dedae4 (3692898 bytes)
- Loci read: XV.23; XVI.29.
- Quoted: XV.23 ("angels have appeared to men in such bodies as could not only be seen, but also touched"; "I dare not determine whether there be some spirits embodied in an aerial substance"; "sons of God, who are also called angels of God", "the sons of Seth", "the daughters of Cain"); XVI.29 ("God appeared again to Abraham … were angels"; "could not doubt that God was in them as He was wont to be in the prophets").
- Rights: public domain.
- Ceiling: transcription.

### Augustine, De Trinitate VI.6.8
- Witness: Augustine, *On the Trinity*, trans. A. W. Haddan rev. W. G. T. Shedd, NPNF series 1 vol. 3 (1887), CCEL.
- Repository ids: `work.augustine.de-trinitate` (registered with this publication).
- URL: https://ccel.org/ccel/s/schaff/npnf103/cache/npnf103.txt
- Retrieved: 2026-09-29T12:55:20Z
- SHA-256 of the bytes read: cc8d3ff7ce4d4ba293f50a06200af03ff0e5abdeb5200db3a59b4dbe2cad7bdb (3357503 bytes)
- Loci read: VI.6.8.
- Quoted: VI.6.8 ("in each body, it is both whole in the whole, and whole in each several part of it").
- Rights: public domain.
- Ceiling: transcription.

### Origen, De principiis I.6.4
- Witness: Origen, *De principiis* (Rufinus's Latin), trans. F. Crombie, ANF vol. 4, CCEL.
- Repository ids: `work.origen.de-principiis` (existing).
- URL: https://ccel.org/ccel/s/schaff/anf04/cache/anf04.txt
- Retrieved: 2026-09-29T12:55:15Z
- SHA-256 of the bytes read: b9f385a048c18158c2f74dcd37062f48a1c68a5d05bdb07270a93692d172da2e (4237225 bytes)
- Loci read: I.6.4.
- Quoted: I.6.4.
- Rights: public domain.
- Ceiling: transcription. The English of Rufinus's Latin; the Greek is not extant here.

### Gregory the Great, Moralia XVI.37.45
- Witness: Gregory the Great, *Morals on the Book of Job*, Library of Fathers vol. 21 (Oxford 1845), vol. II parts III–IV, archive.org OCR of a Google scan.
- Repository ids: `work.gregory-the-great.moralia-in-iob` (registered with this publication).
- URL: https://archive.org/download/21ALibraryOfFathersOfTheHolyCatholicV21/21ALibraryOfFathersOfTheHolyCatholicV21_djvu.txt
- Retrieved: 2026-09-29T13:13:13Z
- SHA-256 of the bytes read: f13861be5715cabe5283d5bd7f38cb35c2a1332bd6dc04cf049475b88da5c493 (1916422 bytes)
- Loci read: XVI.37.45–46 (on Job 23:13), pp. 253–254.
- Quoted: XVI.37.45 ("For all things were made out of nothing … by the hand of governance"). Hyphenation removed.
- Rights: public domain (1845).
- Ceiling: OCR, checked by reading; not checked against page images. The chapter number xxxvii comes from the OCR's margin.

### Bonaventure, In II Sententiarum d. 3
- Witness: Bonaventure, *Commentaria in quatuor libros Sententiarum* II, *Opera omnia* t. 2 (Quaracchi 1885), archive.org OCR.
- Repository ids: `work.bonaventure.opera-omnia-quaracchi` (existing).
- URL: https://archive.org/download/doctorisseraphic02bona/doctorisseraphic02bona_djvu.txt
- Retrieved: 2026-09-29T13:13:16Z
- SHA-256 of the bytes read: da25d3f5fb7742367bfae54874c647148b1a96a8b89f2023b65d25bdce6d36dd (6785166 bytes)
- Loci read: the preface's index of the points on which Bonaventure and Thomas disagree (from a late 13th-century Borghese codex, as the editors describe it), nos. 9 and 11; d. 3 p. 1 a. 1 q. 1 respondeo, ad 1, ad 3; a. 1 q. 2 respondeo, first part.
- Quoted: a. 1 q. 1 respondeo (two Latin sentences, OCR errors silently corrected: "iila" → "illa", "coiiipositio" → "compositio", "Angeli-" → "Angeli"); ad 1 (the word *appropriate*); preface index no. 11.
- Rights: public domain (1885).
- Ceiling: OCR. **Pages 97–104 are missing from the OCR** (only their footnotes survive), so d. 3 p. 1 a. 2 q. 1 (whether there are several angels in one species) was **not read**. The body cites only the preface index for that question.

### Lateran IV, Firmiter (DS 800–801)
- Witness: Denzinger, *Enchiridion symbolorum*, Latin, patristica.net presentation; English cross-check at papalencyclicals.net (Tanner translation, not quoted).
- Repository ids: `work.fourth-lateran-council.firmiter-credimus` (existing); `work.denzinger.enchiridion-symbolorum` (existing).
- URL: https://patristica.net/denzinger/enchiridion-symbolorum.html ; https://www.papalencyclicals.net/councils/ecum12-2.htm
- Retrieved: 2026-09-29T12:56:36Z; 12:56:39Z
- SHA-256 of the bytes read: 604f24c46e0bc71c2018f25dc787a9ab421d4b2e9cf7d1cee1f43e910ef2708f (2333435 bytes); b93f45cd1f95cd2b5c994110637699fc665e207040d813107fe4c38c342bef45 (228156 bytes)
- Loci read: DS 800, 801.
- Quoted: DS 800 (utramque de nihilo condidit creaturam, spiritualem et corporalem, angelicam videlicet et mundanam); DS 801 (descendit ad infernos … sed descendit in anima).
- Rights: Latin public domain; the English translation is under copyright and is not quoted.
- Ceiling: web Denzinger; not collated with print.

### Vatican I, Dei Filius ch. 1
- Witness: *Dei Filius* ch. 1, Latin (vatican.va); English (papalencyclicals.net).
- Repository ids: `work.first-vatican-council.dei-filius` (existing).
- URL: https://www.vatican.va/archive/hist_councils/i-vatican-council/documents/vat-i_const_18700424_dei-filius_la.html ; https://www.papalencyclicals.net/councils/ecum20.htm
- Retrieved: 2026-09-29T12:56:42Z; 12:56:40Z
- SHA-256 of the bytes read: cdb6433e97aaa0fd31cd148d513392324c39779f0137402208ad66d19e8d7016 (29192 bytes); 80e25e52ffe10ebb389c1fdc2a9caf44cfca125fc0e75c92d481f2e9c89d242f (155629 bytes)
- Loci read: ch. 1, the creation paragraph (cites Lateran IV *Firmiter*).
- Quoted: none; cited in the dossier as renewing DS 800.
- Rights: official text.
- Ceiling: web.

### Catechism of the Catholic Church 328–330
- Witness: CCC (English, vatican.va).
- Repository ids: `work.catholic-church.catechism` (existing).
- URL: https://www.vatican.va/archive/ENG0015/__P1A.HTM
- Retrieved: 2026-09-29T12:56:38Z
- SHA-256 of the bytes read: f5d0972215f47a1bc22e768aa4e51f454db80f32dcbc4e3dd52b4a40ae5254d3 (22605 bytes)
- Loci read: 328–330.
- Quoted: 328 ("a truth of faith"); 330 ("personal and immortal creatures"; "purely spiritual creatures"). Short quotations with attribution.
- Rights: Vatican English, copyrighted; short quotation.
- Ceiling: official web presentation.

### Douay–Rheims
- Witness: Douay–Rheims (Challoner), Project Gutenberg eBook 1581.
- Repository ids: `work.english-college-of-douay.douay-rheims-bible` (existing); `edition.english-college-of-douay.douay-rheims-bible.challoner-gutenberg-1581` (existing).
- URL: https://www.gutenberg.org/cache/epub/1581/pg1581.txt
- Retrieved: 2026-09-29T12:58:58Z
- SHA-256 of the bytes read: 7d10da78d8ec97db53b4e2bd8719cc01e16106b44937a673ba34aa534a04c007 (5880580 bytes)
- Loci read: Ps 103:4; 148:2, 5; Dan 7:10; Gen 6:4; 18:2, 8, 9, 16; 19:1, 3; Tob 5:7–8; 12:19; Heb 1:14; Acts 23:8.
- Quoted: Ps 103:4; Dan 7:10; Gen 18:9, 18:16; Tob 5:8; 12:19; Heb 1:14.
- Rights: public domain.
- Ceiling: Gutenberg transcription.

## Intellect and knowledge (ST I qq. 54-58)

### Aquinas, Summa theologiae, English
- Witness: Thomas Aquinas, *Summa theologiae* I qq. 54–58, trans. Fathers of the English Dominican Province, 2nd rev. ed. 1920, New Advent online edition.
- Repository ids: `work.thomas-aquinas.summa-theologiae` (existing).
- URL: https://www.newadvent.org/summa/1054.htm … 1058.htm
- Retrieved: 2026-09-29T12:53:56Z–12:54:02Z
- SHA-256 of the bytes read: 1f5d59d040c4c3da01f7d56432fe17ea332fcaf39d2eafd47cdb7d23fb6816d7 (36725 bytes); 786bdc9bb69673651d57e161e7e27b07a0d6b0edde58d57748d6d8b3eaea8fe6 (53086 bytes)
- Loci read: every article of I qq. 54–58 in full (prologues, objections, sed contra, corpus, replies) — all 23 articles.
- Quoted: q. 54 a. 1 co., ad 1–3; a. 2 s.c., co., ad 2; a. 3 s.c., co., ad 1–2; a. 4 co., ad 2; a. 5 s.c., co.; q. 55 a. 1 s.c., co., ad 1–3; a. 2 s.c., co., ad 1–3; a. 3 s.c., co., ad 1–3; q. 56 a. 1 s.c., co., ad 1–3; a. 2 s.c., co., ad 1–4; a. 3 s.c., co., ad 1, ad 3; q. 57 a. 1 co., ad 1–3; a. 2 s.c., co., ad 2; a. 3 s.c., co., ad 2–4; a. 4 s.c., co., ad 1–3; a. 5 s.c., co., ad 1–3; q. 58 a. 1 s.c., co., ad 2; a. 2 s.c., co.; a. 3 s.c., co., ad 1–3; a. 4 s.c., co., ad 1, ad 3; a. 5 s.c., co.; a. 6 s.c., co., ad 1–3; a. 7 s.c., co., ad 1–3.
- Rights: public domain (1920 translation); New Advent presentation.
- Ceiling: web transcription, not collated with the 1920 print.

### Aquinas, Summa theologiae, Latin
- Witness: Thomas Aquinas, *Summa theologiae* I qq. 50–64, Leonine text as presented by Corpus Thomisticum.
- Repository ids: `work.thomas-aquinas.summa-theologiae` (existing).
- URL: https://www.corpusthomisticum.org/sth1050.html
- Retrieved: 2026-09-29T12:54:32Z
- SHA-256 of the bytes read: e2cfab53e3a057155f3e241b32c059123265ae7cfe58da04e9d7cb41f3fb0ee7 (402442 bytes)
- Loci read: prologues of qq. 54–58; corpora and key replies of all articles of qq. 54–58.
- Quoted: q. 54 pr. (procedendum est ad cognitionem ipsius; virtus cognoscitiva; medium cognoscendi; modus cognitionis), a. 1 co. (impossibile est quod actio Angeli … sit eius substantia), a. 3 s.c. (dividuntur in substantiam, virtutem et operationem), a. 5 co. (de viribus animae non possunt eis competere nisi intellectus et voluntas); q. 55 a. 2 co. (species intelligibiles connaturales; non sunt a rebus acceptae, sed eis connaturales; per intelligibilem effluxum); q. 56 a. 1 co. (per suam formam, quae est sua substantia, seipsum intelligat), a. 2 ad 3 (esse intentionale); q. 56 a. 3 co. (ipsa natura angelica est quoddam speculum divinam similitudinem repraesentans); q. 57 a. 3 co. (futura in seipsis; solius Dei est futura cognoscere), a. 4 co. (solus Deus cogitationes cordium et affectiones voluntatum cognoscere potest), a. 5 co. (mysteria gratiae; alia Angelorum cognitio, quae eos beatos facit); q. 58 a. 3 co. (intellectuales … rationales), a. 4 co. (componere et dividere; intelligendo quod quid est), a. 5 co. (intellectus eius quod quid est semper est verus, nisi per accidens), a. 6 co. (cognitio matutina / cognitio vespertina; post vesperam non ponitur nox, sed mane).
- Rights: Latin text public domain; Corpus Thomisticum presentation.
- Ceiling: web transcription of the Leonine text; not collated with print.

### Aquinas, De veritate q. 8
- Witness: Thomas Aquinas, *Quaestiones disputatae de veritate* q. 8 (De cognitione angelorum), Corpus Thomisticum.
- Repository ids: `work.thomas-aquinas.de-veritate` (registered with this publication).
- URL: https://www.corpusthomisticum.org/qdv08.html
- Retrieved: 2026-09-29T12:54:50Z
- SHA-256 of the bytes read: 9b15fb2b63b70db664ba953a6a9a1ea349d3895482cd6a6cdb872dab817a1ec3 (405187 bytes)
- Loci read: q. 8 prologue (17 articles); corpora of aa. 9, 10, 11, 12, 13, 15, 16, 17.
- Quoted: none verbatim in the body; summarized as parallel (a. 11 names Avicenna; a. 17 restricts morning/evening knowledge to the blessed).
- Rights: public domain Latin.
- Ceiling: web transcription.

### Aquinas, De malo q. 16
- Witness: Thomas Aquinas, *Quaestiones disputatae de malo* q. 16, Corpus Thomisticum.
- Repository ids: `work.thomas-aquinas.de-malo` (registered with this publication).
- URL: https://www.corpusthomisticum.org/qdm16.html
- Retrieved: 2026-09-29T12:54:47Z
- SHA-256 of the bytes read: 125185866e21f915d9d469dd101e266842cd4ab6bee62ed7d57c7ad6515dcc62 (322684 bytes)
- Loci read: q. 16 aa. 7–8 corpora and replies (demons' knowledge of the future and of secret thoughts).
- Quoted: a. 8 quotes of Augustine, *Retractationes* II.30 (aut difficillime potest ab hominibus, aut omnino non potest inveniri), reported in the body as quoted by Aquinas.
- Rights: public domain Latin.
- Ceiling: web transcription.

### Aquinas, Summa contra gentiles II
- Witness: Thomas Aquinas, *Summa contra gentiles* II cc. 91–101, Corpus Thomisticum.
- Repository ids: `work.thomas-aquinas.summa-contra-gentiles` (registered with this publication).
- URL: https://www.corpusthomisticum.org/scg2091.html (chunk covering cc. 91–101; the expected scg2096.html returns 404)
- Retrieved: 2026-09-29T13:39:29Z
- SHA-256 of the bytes read: f044d4518ba4eada9fc0ae4539741ad71cd9dfb014730e1d772cd023f952a36e (79602 bytes)
- Loci read: cc. 96 and 97 in full; chapter titles of cc. 96–101.
- Quoted: c. 96 (nisi forte aequivoce, on agent/possible intellect), c. 97 (separate substance's intellect semper intelligens actu).
- Rights: public domain Latin.
- Ceiling: web transcription.

### Aquinas, De substantiis separatis
- Witness: Thomas Aquinas, *De substantiis separatis*, Corpus Thomisticum.
- Repository ids: `work.thomas-aquinas.de-substantiis-separatis` (registered with this publication).
- URL: https://www.corpusthomisticum.org/ots.html
- Retrieved: 2026-09-29T12:54:53Z
- SHA-256 of the bytes read: 3149f5709dbec16c044723d25f009a4a43caf0d38e965f28a0972b55474c78d9 (167879 bytes)
- Loci read: c. 13 (title and argument on the knowledge and providence of spiritual substances); cc. 19–20 (quotations of DN 4 on circular motion and of Augustine, *De Genesi ad litteram* VIII, on the motion of created spirit through time).
- Quoted: none in the body; cited as a parallel.
- Rights: public domain Latin.
- Ceiling: web transcription.

### Dionysius, De divinis nominibus
- Witness: Pseudo-Dionysius, *On the Divine Names*, trans. John Parker, 1897, tertullian.org online edition.
- Repository ids: `work.pseudo-dionysius-the-areopagite.de-divinis-nominibus` (registered with this publication).
- URL: https://www.tertullian.org/fathers/areopagite_03_divine_names.htm
- Retrieved: 2026-09-29T12:55:07Z
- SHA-256 of the bytes read: 7d89093873b2ea5b8cf88e96c9066ce04907a0231523db3fa363c22039dc4295 (206269 bytes)
- Loci read: DN 1.2; 4.5–9, 4.22–23; 7.2.
- Quoted: DN 1.2 (altogether incomprehensible to all …); DN 4.7 (embraced the whole in one); DN 4.8 (moved circularly …); DN 4.22 (a mirror untarnished …); DN 4.23 (an irrational anger …); DN 7.2 (not in portions, or from portions …; intuitively, immaterially and uniformly).
- Rights: public domain translation (Parker, 1897).
- Ceiling: web transcription of Parker; Greek text not consulted.

### Dionysius, De caelesti hierarchia
- Witness: Pseudo-Dionysius, *On the Heavenly Hierarchy*, trans. John Parker, 1899, tertullian.org online edition.
- Repository ids: `work.pseudo-dionysius-the-areopagite.de-caelesti-hierarchia` (registered with this publication).
- URL: https://www.tertullian.org/fathers/areopagite_13_heavenly_hierarchy.htm
- Retrieved: 2026-09-29T12:55:02Z
- SHA-256 of the bytes read: ae7608cea7b9f874f2b8ebdabfbe9cfae8b74285fec914aeca3d87cd9089104d (114110 bytes)
- Loci read: CH 4.2; 6.1; 7.3; 11.2; 12.2.
- Quoted: CH 4.2 (share in the supremely Divine participation …); CH 6.1 (they know their own proper powers); CH 7.3 (questioning Jesus Himself …); CH 11.2 (distributed into three,----into essence, and power, and energy); CH 12.2 (partially … in a lower degree).
- Rights: public domain translation (Parker, 1899).
- Ceiling: web transcription; Greek not consulted.

### Dionysius, De ecclesiastica hierarchia
- Witness: Pseudo-Dionysius, *On the Ecclesiastical Hierarchy*, trans. John Parker, 1899, tertullian.org online edition.
- Repository ids: none registered; the entry cites the edition directly.
- URL: https://www.tertullian.org/fathers/areopagite_14_ecclesiastical_hierarchy.htm
- Retrieved: 2026-09-29T12:55:09Z
- SHA-256 of the bytes read: bf098b8ee8a85ecfa388d3004d389f8176f745e5bc80ff6494765a8bd281790c (152291 bytes)
- Loci read: EH 6.6 (the heavenly orders unequal in the sacred sciences).
- Quoted: EH 6 (all the heavenly Orders are not the same, in all the sacred sciences …).
- Rights: public domain translation.
- Ceiling: web transcription; Greek not consulted.

### Augustine, De Genesi ad litteram
- Witness: Augustine, *De Genesi ad litteram* libri XII, Latin, augustinus.it (Nuova Biblioteca Agostiniana text presentation).
- Repository ids: `work.augustine.de-genesi-ad-litteram` (existing).
- URL: https://www.augustinus.it/latino/genesi_lettera/genesi_lettera_02_libro.htm (and _04, _05, _08)
- Retrieved: 2026-09-29T13:31:53Z–13:32:00Z
- SHA-256 of the bytes read: f8cf26227b12b2f3c5b58dd51c7e84e5e4813c20a45175499fca7ff0a7dc2808 (55987 bytes); 17605bed34870cd80c29f10c8361ce52eeac593961d90cc4e6bb7554c3d9e529 (83034 bytes); 2d8ed3690cecec76bc5a7ce33c1fdb4e6e49e55d4250dfc66caae2b0a12cfa76 (62309 bytes); a024b5abb84bf0eb2a1f254c7262ac585f3df876ae43c478a00f609af99c7f74 (72204 bytes)
- Loci read: II.8.16–19; IV.22.39–25.42; IV.29.46; IV.31.48; IV.32.49–50; V.19.38; VIII.20.39.
- Quoted: II.8.16 (caetera vero quae infra sunt …; in ipsa sua conformatione cognovit …); II.8.17 (ratio qua creatura conditur …; ex quo creati sunt, ipsa Verbi aeternitate …); IV.23.40 (multum quippe interest …); IV.24.41 (non remanet angelica scientia in eo quod creatum est …); IV.29.46 (simul hoc totum possint …); IV.32 (secundum potentiam spiritalem …); V.19.38 (sic ergo fuit hoc absconditum a saeculis in Deo …); VIII.20.39 (per tempus movet conditum spiritum …).
- Rights: Latin text public domain; augustinus.it presentation.
- Ceiling: web transcription; not collated with CSEL 28 or CSEL 28.1 print. Numbering follows the Maurist/NBA division; the Summa's "Gen. ad lit. iv, 24" corresponds to Maurist IV.23.40, and its "iv, 22, 31" to the IV.22.39 and IV.32.49–50 region.

### Augustine, De divinatione daemonum
- Witness: Augustine, *De divinatione daemonum*, Latin, augustinus.it.
- Repository ids: none registered; the entry cites the edition directly.
- URL: https://www.augustinus.it/latino/potere_divinatorio/potere_divinatorio_libro.htm
- Retrieved: 2026-09-29T13:32:03Z
- SHA-256 of the bytes read: 152f2e97c16255ad64191158345f5f220e113de7e86ce1480cf38a5406e7bc4b (30665 bytes)
- Loci read: 5.9 (demons' prevision and reading of dispositions).
- Quoted: 5.9 (non solum voce prolatas, verum etiam cogitatione conceptas … tota facilitate perdiscunt).
- Rights: Latin text public domain.
- Ceiling: web transcription; not collated with CSEL 41 print.

### Augustine, De diversis quaestionibus octoginta tribus
- Witness: Augustine, *De diversis quaestionibus LXXXIII*, Latin, augustinus.it.
- Repository ids: none registered; the entry cites the edition directly.
- URL: https://www.augustinus.it/latino/ottantatre_questioni/ottantatre_questioni_libro.htm
- Retrieved: 2026-09-29T13:31:33Z
- SHA-256 of the bytes read: 60b9fbde7a1bb0bd7e4b28efa445f3ecc04da8459fca9407303464dd9fd68d28 (316081 bytes)
- Loci read: q. 32 (Utrum verum possit falsum videri).
- Quoted: q. 32 (non ergo potest quidquam intellegi nisi ut est).
- Rights: Latin text public domain.
- Ceiling: web transcription. The Summa cites "QQ. 83, qu. 32"; some editions number this question 31 (Renatus); augustinus.it carries it as q. 32, matching the Summa.

### Augustine, De civitate Dei
- Witness: Augustine, *City of God*, trans. Marcus Dods, NPNF 1.2 (Schaff), ccel.org.
- Repository ids: `work.augustine.de-civitate-dei` (existing).
- URL: https://www.ccel.org/ccel/schaff/npnf102.txt
- Retrieved: 2026-09-29T12:55:19Z
- SHA-256 of the bytes read: 5c973feda803f3e58a88ed7df210b42d436f5466741eb8dbeae713ab56dedae4 (3692898 bytes)
- Loci read: XI.7; XI.29.
- Quoted: XI.7 (the knowledge of the creature is, in comparison of the knowledge of the Creator, but a twilight …); XI.29 (a noonday knowledge … a twilight knowledge).
- Rights: public domain translation (1871–87 NPNF).
- Ceiling: web transcription.

### John Damascene, De fide orthodoxa
- Witness: John of Damascus, *Exposition of the Orthodox Faith* II.3, trans. Salmond, NPNF 2.9, ccel.org.
- Repository ids: `work.john-of-damascus.de-fide-orthodoxa` (registered with this publication).
- URL: https://www.ccel.org/ccel/schaff/npnf209.txt
- Retrieved: 2026-09-29T12:55:27Z
- SHA-256 of the bytes read: 859ba34cc5998f2761b801aa5de724b2ea741a54d98e21614faeb89cc40f8ad4 (2606804 bytes)
- Loci read: II.3 (Of angels).
- Quoted: II.3 (an intelligent essence, in perpetual motion, with free-will, incorporeal …; secondary intelligent lights …; they have no need of tongue or hearing …; They behold God according to their capacity …).
- Rights: public domain translation.
- Ceiling: web transcription; Greek not consulted.

### Gregory the Great, Moralia in Iob
- Witness: Gregory the Great, *Morals on the Book of Job*, vol. 2, Library of the Fathers 21 (Oxford, 1844), archive.org.
- Repository ids: `work.gregory-the-great.moralia-in-iob` (registered with this publication).
- URL: https://archive.org/download/21ALibraryOfFathersOfTheHolyCatholicV21/21ALibraryOfFathersOfTheHolyCatholicV21_djvu.txt
- Retrieved: 2026-09-29T13:13:13Z
- SHA-256 of the bytes read: f13861be5715cabe5283d5bd7f38cb35c2a1332bd6dc04cf049475b88da5c493 (1916422 bytes)
- Loci read: Moralia XVIII, on Job 28:17 (§§77–78 in the LF paragraph division).
- Quoted: XVIII (when the countenance of each one is marked his conscience is penetrated along with it …; as now he cannot be distinguishable to himself).
- Rights: public domain translation (1844–50).
- Ceiling: archive.org OCR; not collated with print.

### Gregory the Great, Homiliae in Evangelia
- Witness: Gregory the Great, *XL Homiliarum in Evangelia libri duo*, ed. Wagner, Regensburg 1892, archive.org.
- Repository ids: `work.gregory-the-great.homiliae-in-evangelia` (existing).
- URL: https://archive.org/download/sanctigregoriim00igoog/sanctigregoriim00igoog_djvu.txt
- Retrieved: 2026-09-29T13:48:47Z
- SHA-256 of the bytes read: 4eb8d78cd432816ff08b76b2549b6015fe29637307a22ee1d7ba79884d68e2f1 (701111 bytes)
- Loci read: Homilia XXIX.2.
- Quoted: Hom. XXIX.2 (commune esse cum lapidibus, vivere cum arboribus, sentire cum animalibus, intelligere cum angelis; Angeli autem sunt, vivunt, sentiunt, et discernunt).
- Rights: public domain Latin (1892 edition).
- Ceiling: archive.org OCR of the Wagner edition; not collated with CCSL 141 (Étaix).

### Bonaventure, In II Sententiarum
- Witness: Bonaventure, *Commentaria in II Sententiarum*, Opera omnia t. 2 (Quaracchi, 1885), archive.org.
- Repository ids: `work.bonaventure.opera-omnia-quaracchi` (existing).
- URL: https://archive.org/ (Quaracchi t. 2; cached as ia-bonaventure-qu02)
- Retrieved: 2026-09-29T13:15:31Z
- SHA-256 of the bytes read: da25d3f5fb7742367bfae54874c647148b1a96a8b89f2023b65d25bdce6d36dd (6785166 bytes)
- Loci read: d. 3 p. 2 a. 2 q. 1 (whether angels know by innate species), in full.
- Quoted: none verbatim; summarized as contrary opinion (tertia positio: innate species for all things, possible reception of new species, singulars known by composing innate species while directing the gaze upon the thing).
- Rights: public domain (1885 edition).
- Ceiling: archive.org OCR; not collated with print.

### Douay-Rheims Bible
- Witness: The Holy Bible, Douay-Rheims (NT 1582 / OT 1609–10), Project Gutenberg #1581.
- Repository ids: `work.english-college-of-douay.douay-rheims-bible` (existing).
- URL: https://www.gutenberg.org/files/1581/1581.txt (as cached)
- Retrieved: 2026-09-29T12:58:58Z
- SHA-256 of the bytes read: 7d10da78d8ec97db53b4e2bd8719cc01e16106b44937a673ba34aa534a04c007 (5880580 bytes)
- Loci read: Gen 1:5; Ps 90[91]:11; Ps 118[119]:100; Eccles 5:5; Isa 41:23; Isa 63:1; Jer 17:9–10; Amos 3:7; Matt 18:10; 22:30; 24:36; Rom 1:19–20; 1 Cor 2:10–11; 13:12; Eph 3:10; 5:8; 1 Tim 3:16; Heb 1:14; 1 Pet 1:12; 2 Pet 1:19.
- Quoted: Ps 90[91]:11; Eccles 5:5; Isa 41:23; Jer 17:9–10; 1 Cor 2:11; Matt 24:36; 22:30; 1 Cor 13:12 (short clauses and full verses as given in the body).
- Rights: public domain.
- Ceiling: web transcription of the original Douay-Rheims; not the Challoner revision.

### Catechism of the Catholic Church
- Witness: *Catechism of the Catholic Church*, 2nd ed., English, vatican.va.
- Repository ids: `work.catholic-church.catechism` (existing).
- URL: https://www.vatican.va/archive/ENG0015/_INDEX.HTM (as cached)
- Retrieved: 2026-09-29T12:56:38Z (P1A)
- SHA-256 of the bytes read: f5d0972215f47a1bc22e768aa4e51f454db80f32dcbc4e3dd52b4a40ae5254d3 (22605 bytes)
- Loci read: CCC 328–330.
- Quoted: CCC 330 (As purely spiritual creatures angels have intelligence and will …).
- Rights: fair quotation of a short numbered paragraph in a reference work.
- Ceiling: web transcription.

## Will and love; creation, grace, and glory (ST I qq. 59-62)

### Thomas Aquinas, Summa theologiae I qq. 59–62 (English)

- Witness: Thomas Aquinas, *Summa theologiae*, Fathers of the English
  Dominican Province translation (Benziger, 1947), New Advent web
  transcription.
- Repository ids: `work.thomas-aquinas.summa-theologiae` (existing).
- URL: https://www.newadvent.org/summa/1059.htm (…1060, 1061, 1062)
- Retrieved: 2026-09-29T12:54:03Z–12:54:07Z (manifest `na-summa-1059..1062`)
- Quoted: I q. 59 aa. 1–4; I q. 60 aa. 1–5; I q. 61 aa. 1–4;
  I q. 62 aa. 1–9 (corpora, sed contra, replies as cited in the
  sections); all English Summa quotations in both sections.
- Rights: 1947 Benziger translation, public domain in the US; New
  Advent transcription used under brief's standing cache policy.
- Ceiling: Web transcription; not collated with the Leonine text or a
  print Benziger.

### Thomas Aquinas, Summa theologiae I qq. 50–64 (Latin)

- Witness: Corpus Thomisticum (Leonine text) `sth1050.html`.
- Repository ids: `work.thomas-aquinas.summa-theologiae` (existing).
- URL: https://www.corpusthomisticum.org/sth1050.html
- Retrieved: 2026-09-29T12:54:32Z (manifest `ct-sth1050`)
- Quoted: Latin key terms and phrases for qq. 59–62 (e.g. q. 59 a. 3
  "ubicumque est intellectus, est liberum arbitrium"; q. 61 a. 3 co.
  duplex sententia, "probabilius"; q. 62 a. 3 "in gratia gratum
  faciente"; q. 62 a. 7 "salvari primum in secundo"; q. 62 a. 8 ad 3
  "maior libertas"; q. 62 a. 9 viator/comprehensor).
- Rights: Corpus Thomisticum web text of the public-domain Leonine
  edition; short quotations.
- Ceiling: Web transcription; not collated with print Leonine.

### Augustine, De civitate Dei (English)

- Witness: NPNF I-2, Marcus Dods translation (CCEL text).
- Repository ids: `work.augustine.de-civitate-dei` (existing).
- URL: https://ccel.org/ccel/s/schaff/npnf102/cache/npnf102.txt
- Retrieved: 2026-09-29T12:55:19Z (manifest `ccel-npnf102`)
- Quoted: XI.9 (angels as the light called "Day"; partakers of the
  eternal light); XII.1 (two cities among the angels); XII.9
  ("creating their nature, and endowing it with grace").
- Rights: NPNF (1886–90), public domain.
- Ceiling: CCEL transcription; not collated with CCSL 47–48.

### Augustine, De civitate Dei (Latin)

- Witness: The Latin Library, civ11.shtml / civ12.shtml.
- Repository ids: `work.augustine.de-civitate-dei` (existing).
- URL: https://www.thelatinlibrary.com/augustine/civ11.shtml ,
  https://www.thelatinlibrary.com/augustine/civ12.shtml
- Retrieved: 2026-09-29T13:36:43Z–13:36:45Z (manifest `ll-aug-civ11`,
  `ll-aug-civ12`)
- Quoted: XI.9 "ut ea luce inluminati, qua creati, fierent lux et
  uocarentur dies"; XII.9 "simul eis et condens naturam et largiens
  gratiam".
- Rights: Public-domain Latin text; Latin Library transcription.
- Ceiling: Unattributed web transcription; not collated with CCSL.

### Gregory of Nazianzus, Oration 38 (English)

- Witness: NPNF II-7 (CCEL text), Oration 38.9–10.
- Repository ids: `work.gregory-of-nazianzus.oration-38` (registered with this publication).
- URL: https://ccel.org/ccel/s/schaff/npnf207/cache/npnf207.txt
- Retrieved: 2026-09-29T12:55:25Z (manifest `ccel-npnf207`)
- Quoted: 38.9 ("He first conceived the Heavenly and Angelic Powers…")
  and 38.9–10 (second, material creation after the first).
- Rights: NPNF, public domain.
- Ceiling: CCEL transcription of the English only; Greek not read.

### John of Damascus, De fide orthodoxa (English)

- Witness: NPNF II-9 (CCEL text), II.3.
- Repository ids: `work.john-of-damascus.de-fide-orthodoxa` (registered with this publication).
- URL: https://ccel.org/ccel/s/schaff/npnf209/cache/npnf209.txt
- Retrieved: 2026-09-29T12:55:27Z (manifest `ccel-npnf209`)
- Quoted: II.3 (angelic nature "rational, and intelligent, and endowed
  with free-will"; "Some, indeed, like Gregory the Theologian, say that
  these were before the creation of other things").
- Rights: NPNF, public domain.
- Ceiling: CCEL transcription of the English only.

### Pseudo-Dionysius, De divinis nominibus (English, Parker)

- Witness: John Parker translation (1897), tertullian.org
  transcription.
- Repository ids: `work.pseudo-dionysius-the-areopagite.de-divinis-nominibus` (registered with this publication).
- URL: https://www.tertullian.org/fathers/areopagite_03_divine_names.htm
- Retrieved: 2026-09-29T12:55:07Z (manifest `tert-areopagite_03_divine_names`)
- Quoted: DN §4 in Parker's section numbering: 4.4 (graded aspiration),
  4.12 (love "of a power unifying, and binding together"), 4.23
  (demons: "An irrational anger----a senseless desire----a headlong
  fancy").
- Rights: Parker 1897, public domain.
- Ceiling: Parker's section numbers do not map one-to-one onto modern
  chapter divisions; section cites DN 4 with Parker's sub-numbering.
  Not collated with the Greek or Luibheid.

### Jerome, Commentariorum in epistolam ad Titum (Latin)

- Witness: PL 26 (Migne), archive.org OCR of the volume scan, on
  Titus 1:2.
- Repository ids: `work.jerome.commentariorum-in-epistolam-ad-titum` (registered with this publication).
- URL: https://archive.org/download/patrologiaecurs240unkngoog/patrologiaecurs240unkngoog_djvu.txt
- Retrieved: 2026-09-29T13:24:28Z (manifest `ia-pl26`)
- Quoted: on Titus 1:2 ("Sex milia necdum nostri orbis implentur
  anni…"; "in quibus angeli, throni, dominationes, caeteraeque virtutes
  servierint Deo…").
- Rights: Migne PL 26 (1845), public domain.
- Ceiling: Uncorrected archive.org OCR of the Migne scan; not collated
  with CCSL 77C.

### Peter Lombard, Sententiae II (Latin)

- Witness: Quaracchi 1916 edition, vol. I, archive.org OCR.
- Repository ids: `work.peter-lombard.sententiae` (existing).
- URL: https://archive.org/download/libriivsententia01pete/libriivsententia01pete_djvu.txt
- Retrieved: 2026-09-29T13:46:02Z (manifest
  `ia-quaracchi-lombard-t1_djvu`)
- Quoted: II d. 3 c. 2 (grace and glory proportioned to nature); d. 3
  c. 4 ("non poterant proficere ad meritum vitae, nisi gratia
  superadderetur"); d. 4 unicum (created neither in beatitude nor in
  misery); d. 5 c. 1 ("nunquam est apposita ut converterentur"); d. 5
  c. 4 (cooperating grace given to those who stood).
- Rights: Quaracchi 1916, public domain.
- Ceiling: Uncorrected OCR; not collated with the 1971–81
  Grottaferrata edition. franciscan-archive.org transcriptions of these
  distinctions returned 404.

### Thomas Aquinas, Quaestiones disputatae de potentia (Latin)

- Witness: Corpus Thomisticum `qdp3.html`.
- Repository ids: `work.thomas-aquinas.de-potentia` (registered with this publication).
- URL: https://www.corpusthomisticum.org/qdp3.html
- Retrieved: 2026-09-29T13:36:49Z (manifest `ct-qdp3`)
- Quoted: q. 3 a. 18 co. ("Angeli simul cum creatura corporali sunt
  conditi; tamen sine alterius opinionis praeiudicio") and its
  discussion of Jerome's report; q. 3 a. 17 read for the eternity
  question.
- Rights: Corpus Thomisticum web text; short quotations.
- Ceiling: Web transcription; not collated with a critical edition.

### Thomas Aquinas, Scriptum super libros Sententiarum II (Latin)

- Witness: Corpus Thomisticum `snp2002.html` (dd. 2–4).
- Repository ids: `work.thomas-aquinas.scriptum-super-sententiis` (existing).
- URL: https://www.corpusthomisticum.org/snp2002.html
- Retrieved: 2026-09-29T13:36:53Z (manifest `ct-snp2002`)
- Quoted: d. 2 q. 1 a. 3 ("non est demonstratum, nec fide expressum");
  d. 4 q. 1 a. 3 ("in naturalibus tantum creati sunt; et haec opinio
  est communior"); d. 2 q. 1 a. 1 (aevum) referenced.
- Rights: Corpus Thomisticum web text; short quotations.
- Ceiling: Web transcription; not collated with the Mandonnet/Moos
  edition.

### Thomas Aquinas, Summa contra gentiles II (Latin)

- Witness: Corpus Thomisticum `scg2046.html` (cc. 46–).
- Repository ids: `work.thomas-aquinas.summa-contra-gentiles` (registered with this publication).
- URL: https://www.corpusthomisticum.org/scg2046.html
- Retrieved: 2026-09-29T12:55:01Z (manifest `ct-scg2046`)
- Quoted: read II.46–48 for the q. 59 dossier parallel; nothing quoted
  verbatim in the sections.
- Rights: Corpus Thomisticum web text.
- Ceiling: Web transcription.

### Catechism of the Catholic Church (English)

- Witness: vatican.va archive ENG0015, part one section one page.
- Repository ids: `work.catholic-church.catechism` (existing).
- URL: https://www.vatican.va/archive/ENG0015/__P1A.HTM
- Retrieved: 2026-09-29T12:56:38Z (manifest `ccc-en-P1A`)
- Quoted: CCC 330 ("have intelligence and will: they are personal and
  immortal creatures"); CCC 331–332 (created through and for Christ;
  present since creation).
- Rights: Vatican-site document; short quotations with attribution.
- Ceiling: Official English; Latin typical edition not consulted.

### Denzinger, Enchiridion symbolorum (Latin)

- Witness: patristica.net transcription, DS 800 (Lateran IV, Firmiter).
- Repository ids: `work.denzinger.enchiridion-symbolorum` (existing).
- URL: https://patristica.net/denzinger/enchiridion-symbolorum.html
- Retrieved: 2026-09-29T12:56:36Z (manifest `denz-patristica`)
- Quoted: DS 800 "simul ab initio temporis utramque de nihilo condidit
  creaturam, spiritualem et corporalem, angelicam videlicet et
  mundanam".
- Rights: Conciliar text is public domain; Latin quoted per brief's
  rights caution (Tanner's English not used).
- Ceiling: Web transcription; not collated with the 43rd Denzinger
  edition.

### Vatican I, Dei Filius (Latin)

- Witness: vatican.va, conciliar documents, Latin.
- Repository ids: `work.first-vatican-council.dei-filius` (existing).
- URL: https://www.vatican.va/archive/hist_councils/i-vatican-council/documents/vat-i_const_18700424_dei-filius_la.html
- Retrieved: 2026-09-29T12:56:42Z (manifest `va-dei-filius-la`)
- Quoted: ch. 1, the same "utramque de nihilo condidit creaturam…"
  clause (repeating Lateran IV).
- Rights: Vatican-site document; short Latin quotation with attribution.
- Ceiling: Official Latin text; English paraphrase is mine (Tanner not
  used).

### Douay-Rheims Bible (English)

- Witness: Project Gutenberg #1581 (Douay-Rheims, Challoner).
- Repository ids: `work.english-college-of-douay.douay-rheims-bible` (existing).
- URL: https://www.gutenberg.org/cache/epub/1581/pg1581.txt
- Retrieved: 2026-09-29T12:58:58Z (manifest `gut-douay-rheims-1581`)
- Quoted: Ps 148:2, 5; Sir 13:19.
- Rights: Public domain.
- Ceiling: Gutenberg transcription; other Scripture quotations in the
  sections are as embedded in the Summa text (Benziger), not separately
  verified against the Douay.

## The fall and punishment of the demons (ST I qq. 63-64; De malo q. 16)

### Aquinas, Summa theologiae I qq. 63–64 (English)
- Witness: Thomas Aquinas, *Summa theologiae*, trans. Fathers of the English Dominican Province, 2nd rev. ed. 1920, as presented by New Advent.
- Repository ids: `work.thomas-aquinas.summa-theologiae` (existing).
- URL: https://www.newadvent.org/summa/1063.htm ; https://www.newadvent.org/summa/1064.htm
- Retrieved: 2026-09-29T12:54:08Z ; 2026-09-29T12:54:10Z
- SHA-256 of the bytes read: ec2392cac3741da5f73dcfb70d3a7add91edbd85c06543c174cb470936c0ced8 (79216 bytes); 843a0edc18e7c3bfba1864b089b68c8db0e7fe106c8ee1d8402a05b00a89bc28 (49694 bytes)
- Loci read: q. 63 aa. 1–9 and q. 64 aa. 1–4, every objection, *sed contra*, corpus, and reply.
- Quoted: q. 63 a. 1 co., ad 4; a. 2 s.c., co., ad 1; a. 3 co.; a. 4 co.; a. 5 co., ad 1, ad 4; a. 6 s.c., co., ad 4; a. 7 s.c., co.; a. 8 ad 3; a. 9 s.c., ad 3; q. 64 a. 1 co., ad 4; a. 2 co., ad 2, ad 5; a. 3 s.c., co., ad 3; a. 4 s.c., co., ad 3.
- Rights: 1920 translation in the public domain; New Advent's copyright covers the online presentation only.
- Ceiling: web transcription, not collated with print. New Advent omits the question prologues; the q. 63 prologue is given from the Latin only.

### Aquinas, Summa theologiae I qq. 63–64 (Latin)
- Witness: Thomas Aquinas, *Summa theologiae*, Leonine text as edited by Corpus Thomisticum (Busa, Alarcón).
- Repository ids: `work.thomas-aquinas.summa-theologiae` (existing).
- URL: https://www.corpusthomisticum.org/sth1050.html
- Retrieved: 2026-09-29T12:54:32Z
- SHA-256 of the bytes read: e2cfab53e3a057155f3e241b32c059123265ae7cfe58da04e9d7cb41f3fb0ee7 (402442 bytes)
- Loci read: I q. 63 pr. and aa. 1–9; q. 64 pr. and aa. 1–4.
- Quoted (Latin): q. 63 pr.; a. 2 co., ad 2; a. 3 co.; a. 4 s.c.; a. 5 co.; a. 6 co., ad 4; a. 7 co.; a. 8 co.; a. 9 co.; q. 64 a. 1 s.c., co., ad 3; a. 2 co.; a. 3 co.; a. 4 co.
- Rights: Latin text; short quotations with attribution.
- Ceiling: web edition of the Leonine text; not collated with the printed Leonine volume.

### Aquinas, De malo q. 16
- Witness: Thomas Aquinas, *Quaestiones disputatae de malo*, q. 16, Taurini 1953 text as edited by Corpus Thomisticum.
- Repository ids: `work.thomas-aquinas.de-malo` (registered with this publication).
- URL: https://www.corpusthomisticum.org/qdm16.html
- Retrieved: 2026-09-29T12:54:47Z
- SHA-256 of the bytes read: 125185866e21f915d9d469dd101e266842cd4ab6bee62ed7d57c7ad6515dcc62 (322684 bytes)
- Loci read: prooemium (all twelve article titles); aa. 1–6 corpus; a. 4 arguments.
- Quoted (Latin): a. 1 co. (`non multum refert ad fidei Christianae doctrinam`); a. 3 co.; a. 4 co. (three passages); a. 5 co.
- Rights: Latin text; short quotations.
- Ceiling: web edition of the Marietti text, not the Leonine; not collated with print.

### Aquinas, Scriptum super Sententiis II (parallels)
- Witness: Thomas Aquinas, *Scriptum super libros Sententiarum* II, Parma text as edited by Corpus Thomisticum.
- Repository ids: `work.thomas-aquinas.scriptum-super-sententiis` (existing).
- URL: https://www.corpusthomisticum.org/snp2002.html ; https://www.corpusthomisticum.org/snp2005.html
- Retrieved: 2026-09-29T13:36:53Z ; 2026-09-30T14:25:15Z (snp2005 fetched by another lane today)
- SHA-256 of the bytes read: aa7e232d993331e1651b74086148b7908e90c5825d72764b020ff19f9f14ebfa (224942 bytes); 9f55c793a696b620eb411cd7406b077051ae7a33262c6a5adc1f557458f2d7ce (210163 bytes)
- Loci read: II d. 3 q. 2 a. 1 co.; d. 5 q. 1 aa. 1–3 co.; d. 6 q. 1 aa. 1–3 co.; d. 7 q. 1 a. 2 co.; d. 7 q. 2 a. 1 co.
- Quoted: none in section 40 (parallels only, in the dossier Summa fields).
- Rights: Latin text.
- Ceiling: web text; read for correspondence of determination only.

### Augustine, De civitate Dei XI.13, XI.15, XIV.3
- Witness: Augustine, *The City of God*, trans. Marcus Dods, NPNF series 1 vol. 2 (Schaff, 1887); Latin XI from The Latin Library.
- Repository ids: `work.augustine.de-civitate-dei` (existing).
- URL: https://ccel.org/ccel/s/schaff/npnf102/cache/npnf102.txt ; https://www.thelatinlibrary.com/augustine/civ11.shtml
- Retrieved: 2026-09-29T12:55:19Z ; 2026-09-29T13:36:43Z
- SHA-256 of the bytes read: 5c973feda803f3e58a88ed7df210b42d436f5466741eb8dbeae713ab56dedae4 (3692898 bytes); d39371cdd16d35aff529af05c50c68ba6260fbff76ff33526ddfca81cd3fb2e0 (81384 bytes)
- Loci read: XI.13 (Latin and English), XI.15, XIV.3.
- Quoted: XIV.3 (NPNF: "is exceedingly proud and envious", "is reserved in chains of darkness to everlasting punishment"). The *sed contra* wording of q. 63 a. 2 and the XI.15 phrase "from the beginning of sin" are the Summa's English, attributed as its citations.
- Rights: NPNF public domain; Latin text public domain.
- Ceiling: web transcriptions, not collated with print.

### Augustine, Enchiridion 28–29
- Witness: Augustine, *Enchiridion*, trans. J. F. Shaw, NPNF series 1 vol. 3.
- Repository ids: `work.augustine.enchiridion-ad-laurentium` (existing).
- URL: https://ccel.org/ccel/s/schaff/npnf103/cache/npnf103.txt
- Retrieved: 2026-09-29T12:55:20Z
- SHA-256 of the bytes read: cc8d3ff7ce4d4ba293f50a06200af03ff0e5abdeb5200db3a59b4dbe2cad7bdb (3357503 bytes)
- Loci read: chh. 28–29.
- Quoted: ch. 29.
- Rights: public domain.
- Ceiling: web transcription.

### Augustine, De Genesi ad litteram III.10.15; XI.14.18; XI.23.30; XI.26.33
- Witness: Augustine, *De Genesi ad litteram*, Latin text of augustinus.it (NBA).
- Repository ids: `work.augustine.de-genesi-ad-litteram` (existing).
- URL: https://www.augustinus.it/latino/genesi_lettera/genesi_lettera_03_libro.htm ; https://www.augustinus.it/latino/genesi_lettera/genesi_lettera_11_libro.htm
- Retrieved: 2026-09-29T17:51:12Z ; 2026-09-29T17:51:14Z
- SHA-256 of the bytes read: 09c40f51702e2b82d0abb51201874d54412fc704c6eb3f89235f5c70e0ce51cc (56067 bytes); bb4af4ce50086b4b659056c7c6126dcae4d41d0d3e3af56b57157d98db17cdb0 (87547 bytes)
- Loci read: III.10.15; XI.14.18; XI.23.30; XI.24.31–26.33.
- Quoted (Latin): III.10.15; XI.14.18; XI.26.33 (extended in revision); XI.23.30 cited in the dossier (`superbia tumidus`).
- Rights: Latin text; short quotation.
- Ceiling: web edition; not collated with CSEL 28.

### Gregory the Great, Homiliae in Evangelia 34.7, 34.9
- Witness: Gregory the Great, *XL homiliarum in Evangelia libri duo*, Latin, archive.org scan (Google-digitized edition) with djvu OCR.
- Repository ids: `work.gregory-the-great.homiliae-in-evangelia` (existing).
- URL: https://archive.org/download/sanctigregoriim00igoog/sanctigregoriim00igoog_djvu.txt
- Retrieved: 2026-09-29T13:48:47Z
- SHA-256 of the bytes read: 4eb8d78cd432816ff08b76b2549b6015fe29637307a22ee1d7ba79884d68e2f1 (701111 bytes)
- Loci read: 34.6–34.9.
- Quoted (Latin): 34.7 (`dum cunctis agminibus angelorum praelatus est, ex eorum comparatione clarior fuit`); 34.9 (`ille antiquus hostis, qui Deo esse per superbiam similis concupivit`, added in revision in place of an English rendering).
- Rights: Latin text, public domain.
- Ceiling: very poor OCR; readings regularized by sense (e.g. OCR `agminibua wi-gelonim praelatua` for `agminibus angelorum praelatus`; `antiquua hostis ... super-biaai similis coucupivit`). Not collated with PL 76 or CCSL 141.

### Gregory the Great, Moralia XXXII.23.47; XXXIV.6.11
- Witness: Gregory the Great, *Morals on the Book of Job*, Library of the Fathers (Oxford, 1844–50), as transcribed at lectionarycentral.com.
- Repository ids: `work.gregory-the-great.moralia-in-iob` (registered with this publication).
- URL: https://www.lectionarycentral.com/GregoryMoralia/Book32.html ; https://www.lectionarycentral.com/GregoryMoralia/Book34.html
- Retrieved: 2026-09-29T17:51:08Z ; 2026-09-29T17:51:09Z
- SHA-256 of the bytes read: 426a7d69992a5e03be469291433c135f5520e125db35b53f65d850b927b4dbef (153054 bytes); 01cd003e8190bffcb1c6a15e2cff7cde9c3f0a484c881c9627a3a7bbe5fa637a (139202 bytes)
- Loci read: XXXII.23.47–48; XXXIV.6.11.
- Quoted: XXXII.23.47 (two sentences); XXXIV.6.11.
- Rights: 1844–50 translation, public domain.
- Ceiling: web transcription of the Oxford translation; section numbering as that page prints it.

### John Damascene, De fide orthodoxa II.4
- Witness: John of Damascus, *Exposition of the Orthodox Faith*, trans. S. D. F. Salmond, NPNF series 2 vol. 9.
- Repository ids: `work.john-of-damascus.de-fide-orthodoxa` (registered with this publication).
- URL: https://ccel.org/ccel/s/schaff/npnf209/cache/npnf209.txt
- Retrieved: 2026-09-29T12:55:27Z
- SHA-256 of the bytes read: 859ba34cc5998f2761b801aa5de724b2ea741a54d98e21614faeb89cc40f8ad4 (2606804 bytes)
- Loci read: II.3–4.
- Quoted: II.4 ("was not made wicked in nature but was good"; "of his free choice was changed"; "an innumerable host of angels subject to him were torn away and followed him"; and, added in revision, "what in the case of man is death is a fall in the case of angels ... no repentance").
- Rights: public domain.
- Ceiling: web transcription.

### Origen, De principiis I.6
- Witness: Origen, *De principiis*, Rufinus's Latin as translated by F. Crombie, ANF vol. 4.
- Repository ids: `work.origen.de-principiis` (existing).
- URL: https://ccel.org/ccel/s/schaff/anf04/cache/anf04.txt
- Retrieved: 2026-09-29T12:55:15Z
- SHA-256 of the bytes read: b9f385a048c18158c2f74dcd37062f48a1c68a5d05bdb07270a93692d172da2e (4237225 bytes)
- Loci read: I.6.1–3.
- Quoted: none; I.6.3 paraphrased in the Contrary opinion field (Origen leaves the conversion of the devil's orders to the reader).
- Rights: public domain.
- Ceiling: translation of Rufinus's Latin; the Summa's report of Origen's opinion (q. 64 a. 2) is given as Aquinas's report.

### Dionysius, Divine Names 4.23
- Witness: Dionysius the Areopagite, *Divine Names*, trans. John Parker, *Works* Part I (London, 1897), as transcribed at tertullian.org.
- Repository ids: `work.pseudo-dionysius-the-areopagite.de-divinis-nominibus` (registered with this publication).
- URL: https://www.tertullian.org/fathers/areopagite_03_divine_names.htm
- Retrieved: 2026-09-29T12:55:07Z
- SHA-256 of the bytes read: 7d89093873b2ea5b8cf88e96c9066ce04907a0231523db3fa363c22039dc4295 (206269 bytes)
- Loci read: DN 4.23.
- Quoted: DN 4.23 (extended in revision to the end of Parker's clause).
- Rights: public domain.
- Ceiling: web transcription; section numbering as in Parker.

### Anselm, De casu diaboli c. 4
- Witness: Anselm, *De casu diaboli*, Latin, logicmuseum transcription.
- Repository ids: `work.anselm-of-canterbury.de-casu-diaboli` (registered with this publication).
- URL: https://www.logicmuseum.com/wiki/Authors/Anselm/de_casu
- Retrieved: 2026-09-29T13:24:24Z
- SHA-256 of the bytes read: 289e187e37b0d9cc4428483a07db50be6cf58b5ab46aba8cdc1a0cb283206bf0 (115975 bytes)
- Loci read: c. 4.
- Quoted: none in section 40.
- Rights: Latin text.
- Ceiling: the Summa's words `appetiit illud ad quod pervenisset si stetisset` do not occur verbatim in c. 4; section 40 gives them as Aquinas's citation of Anselm.

### Denzinger (Lateran IV; Braga I; Constantinople 543)
- Witness: Denzinger, *Enchiridion symbolorum* (Latin, with DS and older numbers), patristica.net transcription.
- Repository ids: `work.denzinger.enchiridion-symbolorum` (existing); `work.fourth-lateran-council.firmiter-credimus` (existing).
- URL: https://patristica.net/denzinger/enchiridion-symbolorum.html
- Retrieved: 2026-09-29T12:56:36Z
- SHA-256 of the bytes read: 604f24c46e0bc71c2018f25dc787a9ab421d4b2e9cf7d1cee1f43e910ef2708f (2333435 bytes)
- Loci read: DS 403–411; DS 455–464; DS 800–802.
- Quoted: DS 409 (can. 7), 411 (can. 9), 457 (Braga I can. 7), 800, 801.
- Rights: Latin conciliar text.
- Ceiling: web transcription of Denzinger; not collated with the printed DS.

### Catechism of the Catholic Church 391–395, 414
- Witness: *Catechism of the Catholic Church*, English, vatican.va.
- Repository ids: `work.catholic-church.catechism` (existing).
- URL: https://www.vatican.va/archive/ENG0015/__P1C.HTM
- Retrieved: 2026-09-29T13:10:40Z
- SHA-256 of the bytes read: 3ce4c15f4bdb2cccf0dd788c1ddbe25a7eee2b8c1b35ecb60aa07d509b30c153 (33151 bytes)
- Loci read: 391–395, 414.
- Quoted: 392 (twice), 393, 395.
- Rights: Vatican English; short quotations with attribution.
- Ceiling: official web text.

### Douay–Rheims Bible (Challoner)
- Witness: Douay–Rheims Bible, Challoner revision, Project Gutenberg eBook 1581.
- Repository ids: `work.english-college-of-douay.douay-rheims-bible` (existing); `edition.english-college-of-douay.douay-rheims-bible.challoner-gutenberg-1581` (existing).
- URL: https://www.gutenberg.org/cache/epub/1581/pg1581.txt
- Retrieved: 2026-09-29T12:58:58Z
- SHA-256 of the bytes read: 7d10da78d8ec97db53b4e2bd8719cc01e16106b44937a673ba34aa534a04c007 (5880580 bytes)
- Loci read: every verse listed under Scripture cited.
- Quoted: Job 4:18; 40:14; 41:25; Isa 14:12–14; Ezek 28:13; John 8:44; 1 John 3:8; 2 Pet 2:4, 2:19; Apoc 12:4, 12:9, 18:7; Luke 8:31, 10:18; Matt 25:41; Gen 1:31; Ecclus 10:15; Wis 2:24; Ps 73:23; 4 Kgs 6:16; James 2:19; Eph 6:12.
- Rights: public domain.
- Ceiling: Gutenberg transcription.

## Disputed questions after Aquinas; positions on the first sin

### Aquinas, Summa theologiae, English
- Witness: Thomas Aquinas, *Summa theologiae* I, trans. Fathers of the English Dominican Province, 2nd rev. ed. 1920, New Advent online edition.
- Repository ids: `work.thomas-aquinas.summa-theologiae` (existing).
- URL: https://www.newadvent.org/summa/1050.htm, 1052.htm, 1061.htm, 1062.htm, 1063.htm, 1113.htm
- Retrieved: 2026-09-29 (cache; see manifest.tsv)
- SHA-256 of the bytes read: 61ff4ab95cc9d06e45d5026da5c0071ed658d5d324eaf661d205faa3371df5be (50349 bytes); a9933f3fabd2548737fdb3cbdc535e04f069dbd8fe5b7454954b93269ee7fe9a (19884 bytes); 50aa6317cf29f0ce6cb0a3c7ff5f81afc2387096f0f11f5020e59cd09b338e2c (28841 bytes); b7412a7cf1b4a8ab31c909237e3912e37eb10b3dce9a7fb40a6dffd43f8b267e (71939 bytes); ec2392cac3741da5f73dcfb70d3a7add91edbd85c06543c174cb470936c0ced8 (79216 bytes); 90503352952827b68b50c430f51df5fa977cd4d3404a06934b860fa9d6f2b576 (53327 bytes)
- Loci read: I q. 50 aa. 2, 4; q. 52 aa. 1–3; q. 61 a. 3; q. 62 a. 3; q. 63 aa. 1–9 (corpus of each, aa. 2–3, 5–6 in full); q. 113 a. 5 in full.
- Quoted: q. 50 a. 2 co., a. 4 co.; q. 52 a. 1 co.; q. 61 a. 3 co., ad 1; q. 62 a. 3 co.; q. 63 a. 3 co. (the Anselm clause), a. 5 co., a. 6 co.; q. 113 a. 5 co., ad 3.
- Rights: public domain (1920 translation).
- Ceiling: web transcription, not collated with the 1920 print.

### Aquinas, Summa theologiae, Latin
- Witness: Leonine text as presented by Corpus Thomisticum (I qq. 50–64 page).
- Repository ids: `work.thomas-aquinas.summa-theologiae` (existing).
- URL: https://www.corpusthomisticum.org/sth1050.html
- Retrieved: 2026-09-29 (cache)
- SHA-256 of the bytes read: e2cfab53e3a057155f3e241b32c059123265ae7cfe58da04e9d7cb41f3fb0ee7 (402442 bytes)
- Loci read: prologues and corpora of qq. 50, 52, 61, 62, 63 consulted for Latin terms.
- Quoted: none verbatim in the body (Latin terms cross-checked here).
- Rights: public domain Latin. Ceiling: web transcription.

### Aquinas, De malo q. 16
- Witness: *Quaestiones disputatae de malo*, q. 16, Corpus Thomisticum.
- Repository ids: `work.thomas-aquinas.de-malo` (registered with this publication).
- URL: https://www.corpusthomisticum.org/qdm16.html
- Retrieved: 2026-09-29 (cache)
- SHA-256 of the bytes read: 125185866e21f915d9d469dd101e266842cd4ab6bee62ed7d57c7ad6515dcc62 (322684 bytes)
- Loci read: q. 16 a. 3 co. [63593], a. 4 co. [63645], both in full.
- Quoted: a. 3 co. (`eam consequi voluit per virtutem suae naturae; non tamen sine Deo in naturam operante, sed sine Deo gratiam conferente`); a. 4 co. (`reprobata fuit ab omnibus magistris tunc Parisiis legentibus`).
- Rights: public domain Latin. Ceiling: web transcription.

### Aquinas, De spiritualibus creaturis
- Witness: *Quaestio disputata de spiritualibus creaturis*, Corpus Thomisticum.
- Repository ids: `work.thomas-aquinas.de-spiritualibus-creaturis` (registered with this publication).
- URL: https://www.corpusthomisticum.org/qds.html
- Retrieved: 2026-09-29 (cache)
- SHA-256 of the bytes read: 525438a81d5e92e57ec744e24be08c2a90e64fbe2e4cdc0d4919d6b45c96580f (357192 bytes)
- Loci read: a. 1 co.
- Quoted: a. 1 co. (`sed tamen hoc non est proprie dictum secundum communem usum nominum`).
- Rights: public domain Latin. Ceiling: web transcription.

### Bonaventure, In II Sent. (Quaracchi t. 2)
- Witness: Bonaventure, *Commentaria in quatuor libros Sententiarum* II, in *Opera omnia* t. 2 (Quaracchi; archive.org item doctorisseraphic02bona, item metadata dated 1882), `_djvu.txt` OCR.
- Repository ids: `work.bonaventure.opera-omnia-quaracchi` (existing).
- URL: https://archive.org/details/doctorisseraphic02bona (OCR: https://archive.org/download/doctorisseraphic02bona/doctorisseraphic02bona_djvu.txt)
- Retrieved: 2026-09-29 (cache, this lane's fetch list)
- SHA-256 of the bytes read: da25d3f5fb7742367bfae54874c647148b1a96a8b89f2023b65d25bdce6d36dd (6785166 bytes)
- Loci read: II d. 3 p. 1 a. 1 q. 1 (spiritual matter); d. 3 p. 1 a. 2 q. 1 (one species or many; pp. 102–104); d. 4 a. 1 q. 2 (created in grace; pp. 133–134); d. 5 a. 1 q. 1 (first sin pride; pp. 146–148); d. 9 a. unicus q. 1 (one species; p. 243).
- Quoted: d. 3 p. 1 a. 1 q. 1 concl. (`Si materia large sumitur...`) and resp. (`illa positio videtur verior esse...`); d. 3 p. 1 a. 2 q. 1 concl. (`In Angelis, vel in aliquibus vel in omnibus, est discretio solummodo quoad personalitatem, non quoad speciem`), resp. (`praesumtio`; `positio sobria et catholica`); d. 9 q. 1 concl. (`videtur magis theologica et probabilis positio... quod omnes Angeli sint eiusdem speciei, sicut et omnes homines`); d. 4 a. 1 q. 2 concl. (`Probabilius videtur, Angelos non habuisse gratiam sanctificantem a primo instanti suae creationis`); d. 5 a. 1 q. 1 concl. (`Primum Angeli peccatum fuit superbia; quod initiatum est in praesumtione, consummatum in ambitione, confirmatum in invidiae et odii aversione`) and resp. (`ita quod nulli subesset; hoc est solius Dei, et hoc est aequiparantiae`).
- Rights: public domain print (1882).
- Ceiling: OCR with obvious errors silently corrected; **d. 3 p. 1 a. 2 q. 1 (pp. 102–104) verified against the page images** (BookReaderImages leaves 124–126, scale 2; images kept in `.scratch/lanes/l10b-disputed/pages/`) — this closes the gap l1 flagged. Other loci: OCR only, not collated with page images.

### Scotus, Ordinatio (Opus Oxoniense) II, Vivès tt. 11–12
- Witness: John Duns Scotus, *Opera omnia* (Vivès), t. 11 (1891; item operaomni11duns) and t. 12 (1891; item operaomni12duns), containing the Opus Oxoniense II with Lychetus's commentary; `_djvu.txt` OCR.
- Repository ids: `work.john-duns-scotus.ordinatio` (registered with this publication).
- URL: https://archive.org/details/operaomni11duns , https://archive.org/details/operaomni12duns
- Retrieved: 2026-09-29 (cache)
- SHA-256 of the bytes read: 530a361c48f7fb0ddeb0b6dfc7c7577a6fe7c6e821a3d0f02e29c9035fd81db0 (2304815 bytes); f457700397f55926a4bd9a0f5ee58898b03b86825a9aafbd42f89a9194495b0c (2712272 bytes)
- Loci read: II d. 2 q. 5 (Vivès XI; angel in place — with the Lychetus gloss identifying Aquinas, I q. 52 aa. 1–2); II d. 3 q. 7 (several angels in one species; Vivès XII, pp. 159–163); II d. 6 q. 1 (could the devil will equality; Vivès XII, pp. 333 sqq.) and q. 2 (the first inordinate act; pp. 344 sqq., n. 14).
- Quoted: d. 3 q. 7 (`Tenenda est ergo conclusio simpliciter opposita, quod scilicet simpliciter possibile est plures Angelos esse in eadem specie`); d. 2 q. 5 (`istud videtur esse damnatum, sicut quidam articulus damnatus ab Episcopo Parisiensi et excommunicatus`; `Nec valet dicere, quod excommunicatio non transeat mare, nec dioecesim...`); d. 6 q. 1 (`volitio complacentiae... potest esse impossibilis, et hoc sufficit ad meritum et demeritum`); d. 6 q. 2 (`primum peccatum ejus non fuit superbia proprie dicta, sed propter delectationem quam importabat, magis videtur reduci ad luxuriam`).
- Rights: public domain print (1891).
- Ceiling: OCR; d. 2's two-column interleaving makes the question number uncertain (Vivès running head and index give q. 5; Cajetan cites d. 2 q. 6) — see Open issues. d. 6 q. 2's phrase `immoderata concupiscentia beatitudinis` sits in a block the Vivès editors mark *Additio*; the body quotes only the n. 14 text proper.

### Chartularium Universitatis Parisiensis t. 1 (the 1277 articles)
- Witness: Heinrich Denifle and Émile Chatelain, *Chartularium Universitatis Parisiensis*, t. 1 (Paris 1889; item chartulariumuniv01univuoft), no. 473 (Stephen Tempier's condemnation of 7 March 1277) with the roll of 219 articles and Denifle's apparatus.
- Repository ids: `work.heinrich-denifle.chartularium-universitatis-parisiensis` (registered with this publication).
- URL: https://archive.org/details/chartulariumuniv01univuoft
- Retrieved: 2026-09-29 (cache)
- SHA-256 of the bytes read: 6b34c960627d168ad5ec1ebe0d14dccfc171cd9e13a5281254e86127ed6be586 (2925942 bytes)
- Loci read: no. 473 heading and prefatory letter (pp. 543 sqq.); roll arts. 80–86, 96, 190–206, 217–219 and explicit (pp. 554–556, 558); Denifle's apparatus ad no. 473 (pp. 548–550), including the John of Naples report and the judgment on St. Thomas.
- Quoted: arts. 81, 96, 191, 204, 218, 219 verbatim; the explicit (date clause); Denifle's note (`in condemnatione an. 1277 Parisiis non aperte agitur de S. Thoma`).
- Rights: public domain print (1889).
- Ceiling: OCR; the articles quoted were re-read in situ and are clean.

### Cajetan on the Prima pars (Leonine t. 5)
- Witness: Thomas de Vio, Cardinal Cajetan, *Commentaria* in *Summa theologiae* Ia, printed in the Leonine *Opera omnia* of Aquinas, t. 5 (Romae, Typographia Polyglotta; item operaomniaiussu05thom, item metadata dated 1882).
- Repository ids: `work.thomas-de-vio-cajetan.commentaria-in-summam-theologiae` (registered with this publication).
- URL: https://archive.org/details/operaomniaiussu05thom
- Retrieved: 2026-09-29 (cache)
- SHA-256 of the bytes read: 84fbee0e6b7bf684efc99ff632a75dcae6a2ab40a39829597a07bfb84c5d6fe4 (3986146 bytes)
- Loci read: commentary on I q. 50 a. 4 (nn. 1–2, the doubt on `differunt materialiter` and the note that Scotus follows Aquinas's third recited opinion); commentary on I q. 52 a. 1 (nn. 1–28: the five considerations, Paris art. 219 turned on the opponents, the replies to Scotus's arguments via Capreolus, the Aristotle *De caelo* I and Nazianzen points, the citation of Aquinas, *Quodl.* I q. 3 a. 1).
- Quoted: none verbatim in the body (paraphrase throughout; the Quodlibet distinction is reported as Cajetan's citation).
- Rights: public domain print (1882).
- Ceiling: OCR; question-number references to Scotus are Cajetan's (d. 2 q. 6).

### Suárez, De angelis
- Witness: Francisco Suárez, *De angelis*, in *Opera omnia* (Vivès) t. 2 (Paris 1856; item rpfranciscisuare02su), `_djvu.txt` OCR.
- Repository ids: `work.francisco-suarez.de-angelis` (registered with this publication).
- URL: https://archive.org/details/rpfranciscisuare02su
- Retrieved: 2026-09-29 (cache)
- SHA-256 of the bytes read: f563a3ff080cfc2c73a5634a3278d8c2a5b7a93b6154c4023c3e819f7d652472 (6655674 bytes)
- Loci read: lib. I cap. 3 nn. 1–15 (when the angels were created; the Lateran *simul* controversy, with Ferrariensis, Vázquez, Cajetan, Sixtus of Siena, Bañez); lib. VII cap. 13 nn. 12–14 and 27–31 (the hypostatic-union object; revelation of Christ as head; positive precept).
- Quoted: VII.13 n. 13 (`valde probabilis est sententia credens, Luciferum de facto peccasse per superbiam, appetendo hypostaticam unionem, et a principio adversarium Christi fuisse`); VII.30 (`revelavit a principio Christum, ut caput eorum, ut auctorem gratiae`); I.3 n. 15 paraphrased (`non carere temeritate` — the phrase verified in the text).
- Rights: public domain print (1856).
- Ceiling: OCR; two-column interleaving frequent; quoted phrases re-verified at their lines. Lib. VI on guardianship not read (see Open issues).

### Anselm, De casu diaboli
- Witness: Anselm of Canterbury, *De casu diaboli*, Latin text at logicmuseum.com, transcribed from F. S. Schmitt's edition (vol. 1, Edinburgh 1946, pp. 231–276).
- Repository ids: `work.anselm-of-canterbury.de-casu-diaboli` (registered with this publication).
- URL: https://www.logicmuseum.com/wiki/Authors/Anselm/de_casu
- Retrieved: 2026-09-29T13:24:24Z (manifest)
- SHA-256 of the bytes read: 289e187e37b0d9cc4428483a07db50be6cf58b5ab46aba8cdc1a0cb283206bf0 (115975 bytes)
- Loci read: c. 4 (the sin's object) in full.
- Quoted: c. 4 (`Peccavit ergo volendo aliquod commodum, quod nec habebat nec tunc velle debuit`; `voluit inordinate similis esse deo`; `propria voluntate, quae nulli subdita fuit`).
- Rights: the underlying Latin is medieval; the Schmitt *edition* (1946) is in copyright — used in short focused quotations only (three sentences), rights basis: fair-use-scale quotation of a critical text for identification of the locus; no extended reproduction.
- Ceiling: web transcription of Schmitt; not collated with the print; two obvious scan/transcription slips (`ibi` for `sibi`, `foit` for `fuit`) silently corrected.

### Augustine, De civitate Dei (NPNF)
- Witness: Augustine, *The City of God*, trans. Marcus Dods, NPNF ser. 1 vol. 2, CCEL text.
- Repository ids: `work.augustine.de-civitate-dei` (existing).
- URL: https://www.ccel.org/ccel/schaff/npnf102.html
- Retrieved: 2026-09-29 (cache)
- SHA-256 of the bytes read: 5c973feda803f3e58a88ed7df210b42d436f5466741eb8dbeae713ab56dedae4 (3692898 bytes)
- Loci read: XI.13–15; XII.6–7; XII.9.
- Quoted: XI.15 (`from the beginning of his sin...`); XII.6 (`have forsaken Him who supremely is... what else is it called than pride? For "pride is the beginning of sin"`); XII.9 (`in one and the same act creating their nature, and endowing it with grace`).
- Rights: public domain translation (1886–90).
- Ceiling: web transcription of NPNF.

### Gregory of Nazianzus, Oration 38 (NPNF)
- Witness: Gregory of Nazianzus, *Oration* 38 (*On the Theophany*), trans. Browne–Swallow, NPNF ser. 2 vol. 7, CCEL text.
- Repository ids: `work.gregory-of-nazianzus.oration-38` (registered with this publication).
- URL: https://www.ccel.org/ccel/schaff/npnf207.html
- Retrieved: 2026-09-29 (cache)
- SHA-256 of the bytes read: 56d84cfa94dee313af0139e2d7f3d4b5f7fffca40ce0f34794b5f56264964dfd (3388014 bytes)
- Loci read: Or. 38.9–10.
- Quoted: 38.9 (`He first conceived the Heavenly and Angelic Powers`; `became and is called Darkness through his pride`); 38.10 (`Then when His first creation was in good order, He conceives a second world, material and visible`).
- Rights: public domain translation.
- Ceiling: web transcription of NPNF.

### Basil, Hexaemeron (NPNF)
- Witness: Basil of Caesarea, *Hexaemeron* homily 1, trans. Blomfield Jackson, NPNF ser. 2 vol. 8, CCEL text.
- Repository ids: `work.basil-of-caesarea.homiliae-in-hexaemeron` (existing).
- URL: https://www.ccel.org/ccel/schaff/npnf208.html
- Retrieved: 2026-09-29 (cache)
- SHA-256 of the bytes read: 4f21a589be54f0c160c2a2bf8c316991dae1a0f3d13430466ed2db555018e0e2 (2645735 bytes)
- Loci read: Hex. I.5.
- Quoted: I.5 (`even before this world an order of things existed`; `outstripping the limits of time`).
- Rights: public domain translation.
- Ceiling: web transcription of NPNF.

### John of Damascus, De fide orthodoxa (NPNF)
- Witness: John of Damascus, *Exposition of the Orthodox Faith*, trans. S. D. F. Salmond, NPNF ser. 2 vol. 9, CCEL text.
- Repository ids: `work.john-of-damascus.de-fide-orthodoxa` (registered with this publication).
- URL: https://www.ccel.org/ccel/schaff/npnf209.html
- Retrieved: 2026-09-29 (cache)
- SHA-256 of the bytes read: 859ba34cc5998f2761b801aa5de724b2ea741a54d98e21614faeb89cc40f8ad4 (2606804 bytes)
- Loci read: II.3 (creation of angels; the two opinions), II.4 (the devil and demons) in full.
- Quoted: II.3 (`For myself, I am in harmony with the theologian`); II.4 (`determined to rise in rebellion`; the free-choice change).
- Rights: public domain translation.
- Ceiling: web transcription of NPNF.

### Origen, Commentary on Matthew (ANF)
- Witness: Origen, *Commentary on Matthew*, book XIII, trans. John Patrick, ANF vol. 9 (ANF Additional Volume), CCEL text.
- Repository ids: `work.origen.commentarium-in-matthaeum` (registered with this publication).
- URL: https://www.ccel.org/ccel/schaff/anf09.html
- Retrieved: 2026-09-29 (cache)
- SHA-256 of the bytes read: 3861096b158e12bc13f4516baac913cbd3d921c607862a7eace4f0257b3aefa5 (3047154 bytes)
- Loci read: XIII.27–28 in full.
- Quoted: XIII.27 (`from... the laver of regeneration`; `from birth... according to the foreknowledge and predestination of God`); XIII.28 (`consigns us to a holy angel`).
- Rights: public domain translation.
- Ceiling: web transcription of ANF; the Latin of Rufinus not consulted.

### Jerome, Commentariorum in Matthaeum (PL 26)
- Witness: Jerome, *Commentariorum in evangelium Matthaei* libri IV, Vallarsi–Migne text, PL 26; archive.org OCR of the PL printing (item patrologiaecurs240unkngoog, vol. 26, 1844/45).
- Repository ids: `work.jerome.commentariorum-in-evangelium-matthaei` (existing); `work.jacques-paul-migne.patrologia-latina-volume-26` (existing).
- URL: https://archive.org/details/patrologiaecurs240unkngoog
- Retrieved: 2026-09-29 (cache)
- SHA-256 of the bytes read: 74c5dd24a294e30a8a1de023ef9842b41a79f52410fae49113156b075ce0d046 (4745230 bytes)
- Loci read: lib. III on Matt 18:10 (col. 130 area).
- Quoted: `Magna dignitas animarum, ut unaquaeque habeat ab ortu nativitatis in custodiam sui angelum delegatum`.
- Rights: public domain print (1845).
- Ceiling: OCR; the quoted sentence read clean in situ.

### Peter Lombard, Sententiae II
- Witness: Peter Lombard, *Sententiarum libri quatuor* II, as printed at the head of each distinction in the Quaracchi Bonaventure t. 2 (the same scan as above).
- Repository ids: `work.peter-lombard.sententiae` (existing).
- URL: https://archive.org/details/doctorisseraphic02bona
- Retrieved: 2026-09-29 (cache)
- SHA-256 of the bytes read: da25d3f5fb7742367bfae54874c647148b1a96a8b89f2023b65d25bdce6d36dd (6785166 bytes)
- Loci read: II d. 4 c. 1; d. 5 cc. 1–5.
- Quoted: d. 5 c. 1 (`Invidiae namque mater est superbia, qua voluerunt se parificare Deo`; `Post creationem namque mox quidam conversi sunt... quidam aversi`; `nunquam est apposita, ut converterentur`).
- Rights: public domain print (1882).
- Ceiling: OCR of the Quaracchi printing of the Lombard's text, not the Grottaferrata critical edition.

### Lateran IV, Firmiter; Vatican I, Dei Filius (Denzinger)
- Witness: Lateran IV, *Firmiter* (DS 800), and Vatican I, *Dei Filius* ch. 1 (DS 3002), Latin text in Denzinger, *Enchiridion* (cache file denz-patristica.txt); *Dei Filius* also checked in the vatican.va Latin (va-dei-filius-la.txt).
- Repository ids: `work.fourth-lateran-council.firmiter-credimus` (existing); `work.first-vatican-council.dei-filius` (existing); `work.denzinger.enchiridion-symbolorum` (existing).
- URL: (cache; Denzinger) ; https://www.vatican.va/.../dei-filius (Latin)
- Retrieved: 2026-09-29 (cache)
- SHA-256 of the bytes read: 604f24c46e0bc71c2018f25dc787a9ab421d4b2e9cf7d1cee1f43e910ef2708f (2333435 bytes); cdb6433e97aaa0fd31cd148d513392324c39779f0137402208ad66d19e8d7016 (29192 bytes)
- Loci read: DS 800 creation clause; DS 3002 (ch. 1, the repeated clause with the Lateran citation).
- Quoted: DS 800 (`sua omnipotenti virtute simul ab initio temporis utramque de nihilo condidit creaturam, spiritualem et corporalem, angelicam videlicet et mundanam`).
- Rights: Latin conciliar text, public domain. The papalencyclicals.net English (Tanner) was NOT quoted, per the brief's rights caution; used only as a finding aid.
- Ceiling: Denzinger printing.

### Catechism of the Catholic Church
- Witness: CCC, English, vatican.va, part 1 art. 1 section paragraphs incl. 336.
- Repository ids: `work.catholic-church.catechism` (existing).
- URL: https://www.vatican.va/archive/ENG0015/__P1A.HTM (cache)
- Retrieved: 2026-09-29 (cache)
- SHA-256 of the bytes read: f5d0972215f47a1bc22e768aa4e51f454db80f32dcbc4e3dd52b4a40ae5254d3 (22605 bytes)
- Loci read: 336.
- Quoted: 336 (`From infancy to death human life is surrounded by their watchful care and intercession`) — short quotation, Vatican-site document, attribution in body.
- Rights: short quotation with attribution (brief's Vatican-site rule).
- Ceiling: web text.

### Douay–Rheims Bible
- Witness: Douay–Rheims (Challoner), Project Gutenberg eBook 1581.
- Repository ids: `edition.english-college-of-douay.douay-rheims-bible.challoner-gutenberg-1581` (existing).
- SHA-256 of the bytes read: 7d10da78d8ec97db53b4e2bd8719cc01e16106b44937a673ba34aa534a04c007 (5880580 bytes)
- Loci read: Ecclus 10:14–15 (verification of the pride verse cited by Augustine).
- Quoted: none in body (Ecclus 10:15 is cited through Augustine's quotation; the Douay verse verified).
- Rights: public domain.
