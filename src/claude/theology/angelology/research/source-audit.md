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

## Before the Fathers: Israel's writings outside the canon, the Septuagint, and Philo

### Septuagint (Brenton)
- Witness: L. C. L. Brenton, The Septuagint Version of the Old Testament with an English Translation (London: Bagster, 1851), as presented by eBible.org (eng-Brenton, per-chapter HTML).
- Repository ids: `work.lancelot-brenton.septuagint-english-translation` (existing).
- URL: https://ebible.org/eng-Brenton/{GEN06,DEU32,DEU33,JOB01,JOB02,JOB04,JOB38,PSA008,PSA077,PSA096,PSA137,PSA148,ISA09,ISA63,DAN03,DAN04,DAG03,DAG04,TOB12,TOB03}.htm; copyright page https://ebible.org/eng-Brenton/copyright.htm
- Retrieved: 2026-09-30T14:37:41Z–14:38:05Z
- Loci read: Gen 6:1–11; Deut 32:7–10, 43; 33:2; Job 1:6; 2:1; 4:18; 38:4–10; Ps 8:5–9; 77:23–27; 96:7; 137:1; 148:1–6; Isa 9:5–6 (LXX 9:5 = Vulg 9:6); 63:8–9; Dan 3 (both Greek forms); Dan 4 (Theodotion); Tob 3; 12.
- Quoted: Deut 32:8–9; Deut 32:43 (clause); Deut 33:2 (clause); Job 1:6; Job 38:7; Ps 96:7 (clause); Isa 9:6 (LXX 9:5, clause); Isa 63:9 (clause); Gen 6:2 marginal note "Alex. angels of God" (paraphrased).
- Rights: public domain (1851).
- Ceiling: web transcription, eBible "source files dated 12 Dec 2025"; not collated with the 1851 print. The eBible Tobit and Greek Daniel additions read like the Authorized Version's Apocrypha; Tob 12:15 (Greek) therefore paraphrased only, not quoted. Brenton verse numbering is the Septuagint's (Isa 9:5).

### Douay–Rheims (Challoner)
- Witness: Douay–Rheims Bible, Challoner revision, Project Gutenberg eBook 1581.
- Repository ids: `work.english-college-of-douay.douay-rheims-bible` (existing).
- URL: https://www.gutenberg.org/cache/epub/1581/pg1581.txt
- Retrieved: per manifest (gut-douay-rheims-1581.txt)
- SHA-256 of the bytes read: 7d10da78d8ec97db53b4e2bd8719cc01e16106b44937a673ba34aa534a04c007 (5880580 bytes)
- Loci read: Gen 4:26; 5:24; 6:2; 48:16; Exod 4:22; Deut 32:8, 43; 33:2; Job 1:6; 4:18; 38:7; Ps 8:6; 77:25, 49; 81:6; 95:5; 96:7; 137:1; Wis 2:24; 16:20; Isa 9:6; 63:9; Dan 3:49, 58, 92, 95; 4:10, 14, 20; 10:21; 12:1; Tob 12:12, 15; Matt 18:10; 22:30; John 1:51; Acts 7:53; 1 Cor 10:20; 11:10; Gal 3:19; 1 Tim 2:5; Heb 1:6; 2:2, 7; 2 Pet 2:4; Jude 6, 14–15; Apoc 8:2–4.
- Quoted: all the above that appear in quotation marks in the body.
- Rights: public domain.
- Ceiling: Gutenberg transcription, not collated with print.

### 1 Enoch (Charles 1917)
- Witness: R. H. Charles, The Book of Enoch, with introduction by W. O. E. Oesterley (London: SPCK, 1917), transcribed at archive.sacred-texts.com (J. B. Hare, 2004).
- Repository ids: none registered; the entry cites the edition directly.
- URL: https://archive.sacred-texts.com/bib/boe/boe{000,001,004,009–023,042,043,064,072,074,103,104}.htm (the live sacred-texts.com is now a JS app; archive host serves the original HTML)
- Retrieved: 2026-09-30T14:38:06Z–14:38:40Z
- Loci read: title page; 1; 6–20; 39; 40; 61; 69 (scan); 71; 99; 100.
- Quoted: 1:9; 6:2, 6; 8:1; 9:3; 10:4–6, 12; 12:4; 15:2, 6–8; 16:3; 19:1; 14:22–23; 39:12; 71:7; 61:10; 40:9; 100:5; 20:1–8 (phrases).
- Rights: public domain in the US (published 1917); transcription notice says PD.
- Ceiling: web transcription; Charles's critical signs (⌈ ⌉, 〈 〉, †) omitted in quotation, as the body footnote states; not collated with print. Charles's translation is from the Ethiopic (1912 title page; not asserted in body for 1917).

### Jubilees (Charles 1917)
- Witness: R. H. Charles, The Book of Jubilees or the Little Genesis, translated from the Ethiopic, intro G. H. Box (London: SPCK, 1917), archive.sacred-texts.com.
- Repository ids: none registered; the entry cites the edition directly.
- URL: https://archive.sacred-texts.com/bib/jub/jub{00,01,05,11,12,13,14,17,18,24,25,35,39,40,85}.htm
- Retrieved: 2026-09-30T14:38:42Z–14:39:02Z
- Loci read: title; 1:27–29; 2:1–33 (with Charles's notes); 4:15–24; 5:1–20; 10:1–17; 15:25–34; 17:15–18; 48:1–14; intro "Affinities" (finding aid only).
- Quoted: 1:27; 1:29; 2:2 (with Charles's square brackets kept); 2:3; 2:18/15:27 ("great classes"); 4:15; 4:21–22; 5:6, 10; 10:6, 8–9; 17:16; 48:10; 15:31–32.
- Rights: public domain in the US (1917).
- Ceiling: web transcription; footnote numerals embedded in running text removed.

### Testaments of the Twelve Patriarchs (Sinker, ANF 8)
- Witness: R. Sinker (trans.), Testaments of the Twelve Patriarchs, Ante-Nicene Fathers vol. 8 (American ed. 1886), CCEL plain text.
- Repository ids: none registered; the entry cites the edition directly.
- URL: https://ccel.org/ccel/s/schaff/anf08/cache/anf08.txt
- Retrieved: 2026-09-30T14:39:13Z
- SHA-256 of the bytes read: fc3df54906137039ef2371aa9cf0fb774712d8ad0fd8f08b494cf5bf90817584 (4430805 bytes)
- Loci read: Coxe and Sinker introductions; T. Reuben 1–7 (with notes 39–48); T. Levi 1–9; T. Judah 20–21; T. Dan 6 (note 149); T. Naphtali 3, 8; T. Asher 1, 6–7; T. Benjamin 6.
- Quoted: T. Levi 3, 5; T. Dan 6; T. Judah 20; T. Asher 6; T. Benjamin 6; T. Reuben 2 ("seven spirits of error"), 3, 5; T. Naphtali 3.
- Rights: public domain.
- Ceiling: CCEL text, not collated with print.

### Philo (Yonge)
- Witness: C. D. Yonge (trans.), The Works of Philo Judaeus (London: Bohn, 1854–55), as presented at earlychristianwritings.com (section numbers of the modern editions inserted).
- Repository ids: `work.philo.de-gigantibus` (registered with this publication); `work.philo.de-somniis` (registered with this publication); `work.philo.de-confusione-linguarum` (registered with this publication); `work.philo.de-plantatione` (registered with this publication); `work.philo.de-opificio-mundi` (registered with this publication); `work.philo.quaestiones-in-genesin` (registered with this publication).
- URL: https://www.earlychristianwritings.com/yonge/book{1,9,12,15,21,41}.html (book19, book22 fetched, not used)
- Retrieved: 2026-09-30T14:39:03Z–14:39:11Z; book41 later on 2026-09-30 (list-l13a-israel-2)
- Loci read: De opif. 72–76; De gig. 1–18; De plant. 12–15; De conf. 168–183; De somn. I.1–3, 133–150; QG I.1–2, 92–93.
- Quoted: De gig. 6, 12, 16; De somn. I.141–142; De conf. 171, 174, 175, 179; QG I.92.
- Rights: public domain (Yonge).
- Ceiling: web edition; the site's text may derive from the Hendrickson reprint; De gig. 16 reads "differing indeed in name, but not identical in reality" — apparently a transcription error for "but identical" — not quoted. QG is Yonge's English of Aucher's Latin of the Armenian.

### 1 Clement; Justin; Irenaeus (ANF 1)
- Witness: ANF vol. 1 (1885), CCEL.
- Repository ids: `work.ante-nicene-fathers.volume-1` (existing); `work.justin-martyr.second-apology` (existing); `work.justin-martyr.dialogus-cum-tryphone` (registered with this publication); `work.irenaeus.adversus-haereses` (existing).
- URL: https://ccel.org/ccel/s/schaff/anf01/cache/anf01.txt
- Retrieved: per manifest (ccel-anf01.txt)
- SHA-256 of the bytes read: ee9c7f0ac3f4df08d07ddf81cd7e061e82a35e0d27de611cae06f1e05b2fb991 (3149312 bytes)
- Loci read: 1 Clem. 29; 2 Apol. 5; Dial. 62, 126, 131; Adv. haer. III.12.9, III.20.4, IV.16.2, IV.20.1, IV.36.4.
- Quoted: all listed except 1 Clem. 29 (paraphrased in final text).
- Rights: public domain. Ceiling: CCEL text; footnote markers removed.

### Athenagoras; Clement of Alexandria; Hermas (ANF 2)
- Witness: ANF vol. 2, CCEL.
- Repository ids: none registered; the entry cites the edition directly.
- URL: https://ccel.org/ccel/s/schaff/anf02/cache/anf02.txt
- SHA-256 of the bytes read: ae8e15414a21fe8d54a30fee7c3fbd1ee6a018e624dcd681d030da5c1cabbcac (3768675 bytes)
- Loci read: Legatio 24–25; Strom. I.15; V.1; VI.16; VII.2; Adumbrationes in Iudam; Hermas Mand. VI.2.
- Quoted: Leg. 24, 25; Strom. I.15 (phrase), V.1, VI.16, VII.2; Mand. VI.2. Adumbr. paraphrased (ANF text reads "verities", a transcription error).
- Rights: public domain.

### Tertullian (ANF 3, 4)
- Witness: ANF vols. 3–4, CCEL.
- Repository ids: `work.ante-nicene-fathers.volume-3` (existing); `work.ante-nicene-fathers.volume-4` (existing); `work.tertullian.de-cultu-feminarum` (registered with this publication); `work.tertullian.de-idololatria` (registered with this publication); `work.tertullian.de-virginibus-velandis` (registered with this publication).
- URL: https://ccel.org/ccel/s/schaff/anf03/cache/anf03.txt ; .../anf04/cache/anf04.txt
- Loci read: De idol. 4, 9, 15; De cultu fem. I.2–3; De virg. vel. 7.
- Quoted: De cultu fem. I.2, I.3; De idol. 4, 9; De virg. vel. 7.
- Rights: public domain.

### Origen (ANF 4, ANF 9, GCS 7)
- Witness: ANF 4 (De principiis, Contra Celsum), ANF 9 (Comm. in Io.); W. A. Baehrens, Origenes Werke 7 (GCS 30, Leipzig 1921), archive.org OCR.
- Repository ids: `work.origen.de-principiis` (existing); `work.origen.contra-celsum` (existing); `work.ante-nicene-fathers.volume-9` (existing); `work.origen.commentarii-in-iohannem` (registered with this publication); `work.origen.homiliae-in-iesu-nave` (registered with this publication).
- URL: CCEL anf04, anf09; https://archive.org/download/origeneswerkehrs07origuoft/origeneswerkehrs07origuoft_djvu.txt
- Retrieved: GCS 2026-09-30 (list-l13a-israel-2); others per manifest
- SHA-256 of the bytes read: b9f385a048c18158c2f74dcd37062f48a1c68a5d05bdb07270a93692d172da2e (4237225 bytes); 3861096b158e12bc13f4516baac913cbd3d921c607862a7eace4f0257b3aefa5 (3047154 bytes); 2c72837897b3ace1f5548a9a15563062f5601c563cc566d9fec6712adcdbb290 (2230721 bytes)
- Loci read: De princ. I.3.3; I.5.2; I.8.1; IV.35 (ANF); C. Cels. IV.51; V.4, 29, 53–55; Comm. Io. VI.25 (ANF); Hom. in Ies. Nave 15.5–6 (GCS 7 pp. 389–392).
- Quoted: De princ. I.5.2 (phrase), I.8.1; C. Cels. IV.51, V.4, V.53, V.54, V.55; Comm. Io. VI.25; Hom. Ies. Nave 15.5, 15.6 (Latin).
- Rights: public domain (ANF; GCS 1921 PD in US).
- Ceiling: GCS OCR normalized ("tanien"→"tamen", "fomicationis"→"fornicationis"). PG 12 OCR is Greek-mode and unusable for Latin.

### Cyprian (ANF 5)
- Repository ids: `work.ante-nicene-fathers.volume-5` (existing); `work.cyprian.de-habitu-virginum` (registered with this publication).
- URL: CCEL anf05. Cache: text/ccel-anf05.txt
- Loci read/Quoted: De habitu virginum 14.
- Rights: public domain.

### Julius Africanus (ANF 6)
- Repository ids: `work.ante-nicene-fathers.volume-6` (existing).
- URL: CCEL anf06. Cache: text/ccel-anf06.txt
- Loci read/Quoted: Chronographia frag. 2 (via Syncellus).
- Rights: public domain.

### Lactantius (ANF 7; CSEL 19)
- Witness: ANF 7; S. Brandt, CSEL 19 (1890), archive.org OCR.
- Repository ids: `work.lactantius.divinae-institutiones` (registered with this publication).
- URL: CCEL anf07; archive.org CSEL 19 (see manifest ia-csel19-lactantius.txt)
- Loci read: Div. Inst. II.14 (CSEL numbering; ANF II.15).
- Quoted: English ANF II.15; Latin CSEL II.14.1 phrase "misit angelos ad tutelam cultumque generis humani".
- Rights: public domain.

### Basil (PG 29)
- Witness: Migne PG 29, archive.org OCR (Greek).
- Repository ids: none registered; the entry cites the edition directly.
- URL: https://archive.org/download/patrologiae_cursus_completus_gr_vol_029/patrologiae_cursus_completus_gr_vol_029_djvu.txt
- Loci read: Adv. Eun. III.1 (cols. c. 655–658).
- Quoted: none (paraphrase from the Greek).
- Rights: public domain. Ceiling: Greek OCR; column numbers unclear, cited as PG 29 only.

### Eusebius (Ferrar)
- Witness: W. J. Ferrar (trans.), Eusebius, Demonstratio evangelica (1920), tertullian.org.
- Repository ids: `work.eusebius.demonstratio-evangelica` (registered with this publication).
- URL: https://www.tertullian.org/fathers/eusebius_de_06_book4.htm
- Retrieved: 2026-09-30 (list-l13a-israel)
- SHA-256 of the bytes read: f969714663559f4b0cfc837aab5ac34fae2a2f8c0525b3bc2b10b7afc642975d (129224 bytes)
- Loci read: IV.7–9. Quoted: IV.7.
- Rights: public domain in the US (published 1920).

### Hilary (CSEL 22)
- Witness: A. Zingerle, CSEL 22 (1891), archive.org OCR.
- Repository ids: `work.hilary-of-poitiers.tractatus-super-psalmos` (existing).
- SHA-256 of the bytes read: 0c9712d4bb1cabe200b4acc320feb70c4f0a593f59ba902fc897ae006285eb08 (2320546 bytes)
- Loci read: Tract. in Ps. 2.29–32 (p. 60); 132.6–7 (p. 689).
- Quoted: 2.31 (Latin); 132.6 (Latin).
- Rights: public domain. Ceiling: OCR; section "81" read as 31 from sequence 29, 30, [31], 32.

### Epiphanius (PG 41, PG 43)
- Witness: Migne PG 41 (Panarion), PG 43 (De mensuris et ponderibus), archive.org Greek-mode OCR.
- Repository ids: `work.epiphanius-of-salamis.panarion` (registered with this publication); `work.epiphanius-of-salamis.de-mensuris-et-ponderibus` (registered with this publication).
- URL: https://archive.org/download/patrologiae_cursus_completus_gr_vol_041/..._djvu.txt; .../vol_043/..._djvu.txt
- Retrieved: 2026-09-30T14:39:34Z, 14:39:38Z
- Loci read: Panarion 39.6.1 (Greek); De mensuris 22 (Greek).
- Quoted: Greek transliteration only (ta pneumata ta leitourgounta en\=opion autou; ta I\=ob\=elaia); otherwise paraphrase.
- Rights: public domain. Ceiling: Greek OCR; Latin columns unreadable; no PD English located.

### Chrysostom (PG 53; NPNF 1/10)
- Witness: Migne PG 53 (Hom. in Gen. 22), archive.org Greek OCR; NPNF 1/10 (Hom. in Matt. 76).
- Repository ids: `work.john-chrysostom.homiliae-in-genesim` (registered with this publication); `work.john-chrysostom.homiliae-in-matthaeum` (existing).
- SHA-256 of the bytes read: b6fe7617168ba125d9fa4c2401e2ead351c91c4b508eecc96056e78ddd23dab3 (4609519 bytes); adb8f1c9a988c5050a20fb9fdbf75143dcb227e95e3dad2f560a63b757923648 (3345978 bytes)
- Loci read: Hom. in Gen. 22.1–3 (Greek); Hom. in Matt. 76.
- Quoted: none (paraphrase from Greek; Hom. in Matt. 76 cut from final text).
- Rights: public domain. Ceiling: Greek OCR; section numbers from OCR markers (β′ misread as δ′).

### Jerome (NPNF 2/3; PL 25; PL 22)
- Repository ids: `work.jerome.de-viris-illustribus` (existing); `work.jerome.commentaria-in-danielem` (existing); `work.nicene-and-post-nicene-fathers.series-2-volume-3` (existing).
- URL: https://ccel.org/ccel/s/schaff/npnf203/cache/npnf203.txt (retrieved 2026-09-30T14:39:15Z); PL 25 and PL 22 archive.org (manifest ia-pl25-jerome-1845.txt, ia-pl22-jerome-epist-1845.txt)
- Loci read: De vir. ill. 4, 11; In Dan. 4:10 (PL 25); Ep. 78, 18th station (PL 22).
- Quoted: De vir. ill. 4, 11; In Dan. 4:10 (Latin); Ep. 78 (Latin phrase).
- Rights: public domain. Ceiling: PL OCR normalized ("pernoe-tationibus"→"pernoctationibus", "oflicia"→"officia", "qut a Gracis"→"qui a Graecis"). Jerome's Comm. in Tit. 1:12 on Enoch (PL 26) located via index but OCR illegible — not used.

### Augustine (NPNF 1/2; Latin)
- Repository ids: `work.augustine.de-civitate-dei` (existing); `work.augustine.enarrationes-in-psalmos` (existing); `work.nicene-and-post-nicene-fathers.series-1-volume-2` (existing).
- URL: CCEL npnf102; augustinus.it cdd_15_libro (cached), cdd_11/cdd_18 fetched 2026-09-30; enarr. Ps 103 (cached aug-enarr-ps103-s1-la)
- Loci read: De civ. Dei XI.9; XV.23 (English and Latin XV.23.4); XVIII.38; Enarr. in Ps. 103 s.1.15.
- Quoted: XI.9; XV.23 (English; Latin sentence on Enoch); XVIII.38; Enarr. Ps. 103 s.1.15 (Latin).
- Rights: public domain (Dods; Latin).

### Cassian; Sulpicius Severus (NPNF 2/11)
- Repository ids: `work.nicene-and-post-nicene-fathers.series-2-volume-11` (existing); `work.sulpicius-severus.chronica` (registered with this publication).
- SHA-256 of the bytes read: 8b1206d4e7488c65b5391875fd9570a8a6bcc83270dea35ffe44010c3575d267 (3470230 bytes)
- Loci read: Conl. VIII.7, 17, 20–21; Chron. I.2.
- Quoted: Conl. VIII.7, 17, 21; Chron. I.2 quote cut from final text (cited only).
- Rights: public domain.

### Ambrose (CSEL 32.1)
- Witness: C. Schenkl (ed.), Sancti Ambrosii Opera I, CSEL 32.1 (Vienna 1896/97), archive.org OCR (Google scan).
- Repository ids: `work.ambrose.de-noe` (registered with this publication).
- URL: https://archive.org/download/sanctiambrosiio00ambrgoog/sanctiambrosiio00ambrgoog_djvu.txt
- Retrieved: 2026-09-30 (list-l13a-israel-2)
- SHA-256 of the bytes read: c21ca8f75aa87c1e38f270bf3d39d12e6cb3de8ac8dc04e06dcb7c258d02d651 (1286745 bytes)
- Loci read: De Noe 4.8–9 (pp. 417–418) with Schenkl's source apparatus ("Philo Quaest. I 92").
- Quoted: De Noe 4.8 (Latin), OCR normalized ("ficripturae"→"scripturae", "augelis"→"angelis").
- Rights: public domain.

### Benedict (Latin Library)
- Repository ids: `work.benedict-of-nursia.regula-benedicti` (existing).
- URL: https://www.thelatinlibrary.com/benedict.html (retrieved 2026-09-30)
- SHA-256 of the bytes read: 915d0ea6db9c756d84f0360fa22ed486c71babfa29419ac57de56ba21d85d835 (98415 bytes)
- Loci read/Quoted: Regula 19.
- Rights: public domain text.

### Dionysius, Celestial Hierarchy (Parker)
- Repository ids: `work.pseudo-dionysius-the-areopagite.de-caelesti-hierarchia` (registered with this publication); `work.pseudo-dionysius-the-areopagite.works-part-ii-parker` (registered with this publication).
- SHA-256 of the bytes read: ae7608cea7b9f874f2b8ebdabfbe9cfae8b74285fec914aeca3d87cd9089104d (114110 bytes)
- Loci read/Quoted: CH 9.1–4.
- Rights: public domain (Parker 1899).

### Gregory the Great
- Repository ids: `work.gregory-the-great.homiliae-in-evangelia` (existing).
- SHA-256 of the bytes read: 4eb8d78cd432816ff08b76b2549b6015fe29637307a22ee1d7ba79884d68e2f1 (701111 bytes); dfd661ab607de8517fed4ffabddea2bdb80da2591230cb5b9a73efc62d56147f (35028 bytes)
- Loci read: Hom. in Ev. 34.8–9. Quoted: 34.8 Latin phrase ("apud nos etiam nomina a ministeriis trahunt").
- Rights: public domain.

### Aquinas, Summa theologiae (English Dominican 1920, New Advent)
- Repository ids: `work.thomas-aquinas.summa-theologiae` (existing).
- URL: https://www.newadvent.org/summa/{1045,1051,1061,1063,1064,1075,1091,1103,1108,1110,1112,1113,1114,2098,4026}.htm (1045, 1075, 1091, 2098, 4026, 1068 fetched this lane 2026-09-30)
- Loci read: I q.45 a.5; q.51 a.3 ad 6; q.61 a.3; q.63 aa.2, 4; q.64 a.4; q.75 a.7; q.91 aa.2, 4; q.103 a.6; q.108 aa.5–6; q.110 a.1; q.112 a.3 ad 3; q.113 aa.1–8 (s.c.); q.114 aa.1, 3; I-II q.98 a.3; III q.26 a.1.
- Quoted: all listed except q.45 a.5, q.113 a.1 (cited).
- Rights: public domain (1920).

### Denzinger (Latin)
- Repository ids: `work.denzinger.enchiridion-symbolorum` (existing).
- SHA-256 of the bytes read: 604f24c46e0bc71c2018f25dc787a9ab421d4b2e9cf7d1cee1f43e910ef2708f (2333435 bytes)
- Loci read: DS 403 (Constantinople 543, can. 1); DS 800 (Lateran IV); DS 1502–1503 (Trent).
- Quoted: DS 403 (phrase), DS 800 (two clauses).
- Rights: Latin conciliar texts, public domain.

### Roman synod of 745 (MGH)
- Witness: A. Werminghoff (ed.), MGH Concilia II.1 (1906), archive.org OCR.
- Repository ids: none registered; the entry cites the edition directly.
- SHA-256 of the bytes read: a246239977995d40164f867ff7297f93c5763150115fc2b2d67527d997f1b35a (2099550 bytes)
- Loci read: Concilium Romanum a. 745, pp. 42–43 (Aldebert's prayer and the bishops' answer).
- Quoted: "non plus quam trium angelorum nomina cognoscimus, id est Michael, Gabriel, Raphael".
- Rights: public domain. Ceiling: OCR; the eight names are not quoted because the OCR of two names ("Adiiius") is uncertain.

### Directory on Popular Piety
- Repository ids: `work.congregation-for-divine-worship-and-the-discipline-of-the-sacraments.directory-on-popular-piety-2001` (registered with this publication).
- SHA-256 of the bytes read: a9d30018f650a6854f3f13d3691a068a6519c2ebdb8d1fc9a2418ad13b90ed38 (531807 bytes)
- Loci read/Quoted: no. 217 (one sentence).
- Rights: © Libreria Editrice Vaticana; short quotation with attribution.

### Catechism of the Catholic Church (vatican.va)
- Repository ids: `work.catholic-church.catechism` (existing).
- URL: https://www.vatican.va/archive/ENG0015/__PG.HTM (retrieved 2026-09-30, list-l13a-israel-2)
- SHA-256 of the bytes read: 83fac8941c8c9463f6aa75fa84e5193ba635411be3bc7564dca32368a290e395 (11902 bytes)
- Loci read: CCC 56–58 with notes 9–12 (note 10 cites "Dt (LXX) 32:8").
- Quoted: CCC 57 (short phrase).
- Rights: © LEV; short quotation.

## Before the Fathers: the Greek poets and philosophers

### Hesiod, Works and Days
- Witness: Hesiod, *Works and Days*, tr. H. G. Evelyn-White, *Hesiod, the Homeric Hymns and Homerica* (Loeb 1914), Project Gutenberg eBook 348.
- Repository ids: `work.hesiod.works-and-days` (registered with this publication).
- URL: https://www.gutenberg.org/cache/epub/348/pg348.txt
- Retrieved: 2026-09-30T14:33:47Z
- SHA-256 of the bytes read: ba394b58b5c57fd137af888a20abf3d1c3515c273b0f29da4778484bb15349f2 (547932 bytes)
- Loci read: ll. 106–155 (the races), 248–264.
- Quoted: 121–126 (block ll. 121–139 in the translation); 248–255.
- Rights: public domain (1914; Gutenberg PD US; translator d. 1924).
- Ceiling: Gutenberg transcription; line numbers from the translation's bracketed ranges; not collated with print.

### Plato, dialogues (Jowett)
- Witness: Plato, *Cratylus*, *Apology*, *Symposium*, *Phaedo*, *Republic*, *Timaeus*, *Laws*, *Statesman*, *Phaedrus*, tr. B. Jowett (3rd ed. 1892), Project Gutenberg eBooks 1616, 1656, 1600, 1658, 1497, 1572, 1750, 1738, 1636.
- Repository ids: `work.plato.symposium` (existing); `work.plato.cratylus` (registered with this publication); `work.plato.apologia-socratis` (registered with this publication); `work.plato.phaedo` (registered with this publication); `work.plato.respublica` (registered with this publication); `work.plato.timaeus` (registered with this publication); `work.plato.leges` (registered with this publication); `work.plato.politicus` (registered with this publication); `work.plato.phaedrus` (registered with this publication).
- URL: https://www.gutenberg.org/cache/epub/{1616,1656,1600,1658,1497,1572,1750,1738,1636}/pg{id}.txt
- Retrieved: 2026-09-30T14:33:49Z–14:34:03Z (Phaedrus 14:52:41Z)
- SHA-256 of the bytes read: e5fe819c38e449ac686945b92aca54f3d4917e04ab1d47c576c54c9072e40acc (326450 bytes); f4cc548bd8c8b59e14effdbaab9df97f29bd48f317a466fe8c3c63ad288b964c (107485 bytes); 8b5c599ea734ff0f5e8d83f399dead8c796800897b107c8d53fa909f74a05d6f (200974 bytes); 164533dde5628e7cd2e51442c29367a132fc470271f0d7e77a2ef06170a008ca (257103 bytes); 917c1cb469e1a8eba6083808764d7131da8d79140b575b4214c9d02a73ec4528 (1244164 bytes); 4f839b423198a80be946aeb7d4b0baef30862d12702a6026b2479be9718342d9 (475689 bytes); 9a6ea73161956a622d0aba13d70b82c076feed7d37d257d26e458671b26dc8c9 (1364421 bytes); 171c09697bde2a26ad7cd4775929e780b0bc218ea47c4b4755cabe437610d3f4 (252962 bytes); ce41cbe9eb5750163ef9084d253d7786d13c24968ae7f5079be3abda53114734 (235362 bytes)
- Loci read: Cratylus 397c–398e; Apology 31c–32a, 40a–41d; Symposium 202b–203b; Phaedo 107c–108c, 113d; Republic V 468e–469b, X 617c–621b; Timaeus 40a–42e, 90a–c; Laws IV 713b–714a, X 896d–897b, 906a–b; Statesman 271c–272b; Phaedrus 246e–247a.
- Quoted: Cratylus 397e–398c; Apology 31c–d, 40a–c; Symposium 202d–203a; Phaedo 107d–108b; Republic X 617d–e, 620d–e; Timaeus 40d, 41a–b, 90a; Laws IV 713c–e, X 896e, 906a; Statesman 271d.
- Rights: public domain (Jowett d. 1893).
- Ceiling: the Gutenberg texts carry no Stephanus numbers; Stephanus loci assigned by content, not collated with a paginated edition. Phaedrus 246e read to verify Athenagoras' quotation; not quoted from Jowett.

### Aristotle, Metaphysics XII and De caelo
- Witness: Aristotle, *Metaphysics* XII, tr. W. D. Ross (Oxford 1908); *On the Heavens*, tr. J. L. Stocks (Oxford 1922); Internet Classics Archive.
- Repository ids: `work.aristotle.metaphysica` (registered with this publication); `work.aristotle.de-caelo` (registered with this publication).
- URL: https://classics.mit.edu/Aristotle/metaphysics.12.xii.html ; https://classics.mit.edu/Aristotle/heavens.1.i.html ; https://classics.mit.edu/Aristotle/heavens.2.ii.html
- Retrieved: 2026-09-30T14:40:44Z–14:40:46Z
- SHA-256 of the bytes read: c1902c3f3c37160e057cb8dffb9c565c28724361d695d1ea67d20afc5659882c (62565 bytes); 63448eff6776b62066566a85e472e4463c4a39ae3b7dbfa763ba33ca1be0ee29 (101501 bytes); fe9950b0a7f8ba0045738e098f993e23d9f0b0980feaca3bcec11844b1058b0f (96969 bytes)
- Loci read: Metaph. XII.7–8 entire; De caelo I.3; II.12.
- Quoted: XII.8 1073a, 1074a, 1074b; De caelo I.3 270b; II.12 292a.
- Rights: Ross 1908 public domain; Stocks 1922 public domain in the US (pre-1929) and in the UK (translator d. 1937).
- Ceiling: web transcription without Bekker numbers; Bekker loci assigned by content.

### Plutarch, De defectu oraculorum and De genio Socratis
- Witness: Plutarch, *Why the Oracles Cease to Give Answers* (tr. R. Midgley) and *A Discourse concerning Socrates's Daemon*, in *Plutarch's Essays and Miscellanies*, ed. W. W. Goodwin (Boston, Little, Brown; vols. 2 and 4), Project Gutenberg 78147 and 79588.
- Repository ids: `work.plutarch.de-defectu-oraculorum` (registered with this publication); `work.plutarch.de-genio-socratis` (registered with this publication).
- URL: https://www.gutenberg.org/cache/epub/79588/pg79588.txt ; https://www.gutenberg.org/cache/epub/78147/pg78147.txt
- Retrieved: 2026-09-30T14:40:56Z; 14:40:51Z
- SHA-256 of the bytes read: 844d4c840ea86f90cf2cb6df38efd7905e51ff96e77dca2ee0aba7b0784f9bcb (1133803 bytes); c9593413ce80263cfc44e22e1be06267781e863252336a0cb603809246905ac8 (1107887 bytes)
- Loci read: De def. or. 9–19; De gen. Socr. 20–24.
- Quoted: De def. or. 10, 13, 15, 17; De gen. Socr. 20.
- Rights: public domain (17th-c. translations revised by Goodwin, first ed. 1870s).
- Ceiling: Gutenberg transcription of the Goodwin revision; chapter numbers are Goodwin's.

### Apuleius, De deo Socratis
- Witness: Apuleius, *On the God of Socrates*, anonymous translation in *The Works of Apuleius* (Bohn's Classical Library, London 1853; reprint 1878), archive.org OCR; Latin text from The Latin Library.
- Repository ids: `work.apuleius.de-deo-socratis` (registered with this publication).
- URL: https://archive.org/download/worksapuleiusco00gurngoog/worksapuleiusco00gurngoog_djvu.txt ; https://archive.org/download/worksofapuleiusc00apulrich/worksofapuleiusc00apulrich_djvu.txt ; https://www.thelatinlibrary.com/apuleius/apuleius.deosocratis.shtml
- Retrieved: 2026-09-30T14:41:17Z; 14:49:43Z; 14:49:44Z
- SHA-256 of the bytes read: 413c8e7c78c40da536f001822961e35ae2d0c479bdafc22ac5d283b8189cd728 (1476884 bytes); 2f9560bb0b0dbe7254e014605afe8a78c99e1722cf2dd7dedc29c6cce522b62a (1434536 bytes); e0173182c21a0d01a1bd79137c9398bf2832e666c40ff786837c23d1c4fa21b3 (34353 bytes)
- Loci read: De deo Socr. 1–6, 13–17 (English and Latin).
- Quoted: 4 (Latin), 6 (English), 13 (English and Latin), 16 (English); 15 paraphrased.
- Rights: public domain (1853).
- Ceiling: OCR; the 1853 OCR has errors in ch. 6 ("asjaessengers", "Itey"), so the quoted text is collated against the 1878 OCR of the same Bohn setting; chapter numbers checked against The Latin Library headings.

### Plotinus, Enneads III.4, III.5; Porphyry, Life of Plotinus
- Witness: Plotinus, *Complete Works*, tr. K. S. Guthrie (1918), vols. 1 and 4, Project Gutenberg 42930 and 42933 (vol. 1 includes Porphyry's *Life*).
- Repository ids: `work.plotinus.enneades` (registered with this publication); `work.porphyry.vita-plotini` (registered with this publication).
- URL: https://www.gutenberg.org/cache/epub/42930/pg42930.txt ; https://www.gutenberg.org/cache/epub/42933/pg42933.txt
- Retrieved: 2026-09-30T14:40:59Z; 14:41:04Z
- SHA-256 of the bytes read: f4ef8a36b1fc21dd615e307e65b18aad6841d6f2c39eb336f51fc80a611c66a2 (521117 bytes); af75f5796e71afd86554bf300543811bdd22f41b2aaae5f77eceb918ef8ac703 (865752 bytes)
- Loci read: Enn. III.4 (entire, Guthrie's "Of Our Individual Guardian"); III.5.1–6; Life 10.
- Quoted: III.4.3; III.5.6; Life 10.
- Rights: public domain in the US (1918); translator d. 1940.
- Ceiling: Guthrie renders daimon as "guardian"; section numbers are Guthrie's; not collated with Henry–Schwyzer.

### Porphyry, De abstinentia II
- Witness: Porphyry, *On Abstinence from Animal Food*, book II, tr. T. Taylor, *Select Works of Porphyry* (London 1823), archive.org OCR.
- Repository ids: `work.porphyry.de-abstinentia` (registered with this publication).
- URL: https://archive.org/download/selectworksporp00taylgoog/selectworksporp00taylgoog_djvu.txt
- Retrieved: 2026-09-30T14:41:21Z
- SHA-256 of the bytes read: 8aa0167ea2e6a4a943440e7092e74caecf7b9e170bf159ffcb15b1a0b728747f (607119 bytes)
- Loci read: II.36–43.
- Quoted: II.38 (Taylor); II.38–42 quoted through Eusebius (Gifford).
- Rights: public domain (1823).
- Ceiling: noisy OCR; one silent correction in a quotation ("maderate" → "moderate"); the evil-daemon sentences are quoted from Gifford's Eusebius, where Gifford's notes identify them as De abst. II.38–42.

### Iamblichus, De mysteriis
- Witness: Iamblichus, *On the Mysteries of the Egyptians, Chaldeans, and Assyrians*, tr. T. Taylor (2nd ed. 1895), archive.org OCR.
- Repository ids: `work.iamblichus.de-mysteriis` (registered with this publication).
- URL: https://archive.org/download/b24884170/b24884170_djvu.txt
- Retrieved: 2026-09-30T14:51:36Z
- SHA-256 of the bytes read: ab16f1f084301058f6b31518b6e80bbbc6724302fc59c8b1ff97c8de5c5e7996 (625203 bytes)
- Loci read: II.2–4.
- Quoted: II.3.
- Rights: public domain (Taylor 1821; 1895 reprint).
- Ceiling: OCR; Porphyry's question is Taylor's italic, and two OCR errors in it are corrected in the quotation ("hy" → "by", "he hnownr" → "be known").

### Justin Martyr, Apologies
- Witness: Justin, *First Apology* and *Second Apology*, ANF 1 (Schaff edition), CCEL text.
- Repository ids: `work.justin-martyr.first-apology` (existing); `work.justin-martyr.second-apology` (existing); `work.ante-nicene-fathers.volume-1` (existing).
- URL: https://ccel.org/ccel/s/schaff/anf01/cache/anf01.txt
- Retrieved: 2026-09-29T12:55:11Z
- SHA-256 of the bytes read: ee9c7f0ac3f4df08d07ddf81cd7e061e82a35e0d27de611cae06f1e05b2fb991 (3149312 bytes)
- Loci read: 1 Apol. 5, 44, 59–60; 2 Apol. 10, 13.
- Quoted: all these.
- Rights: public domain (ANF 1885).
- Ceiling: CCEL plain text; not collated with a Greek edition.

### Athenagoras, Legatio; Clement of Alexandria, Stromata
- Witness: Athenagoras, *A Plea for the Christians*; Clement, *Stromata*; ANF 2, CCEL text.
- Repository ids: `work.clement-of-alexandria.stromata` (registered with this publication).
- URL: https://ccel.org/ccel/s/schaff/anf02/cache/anf02.txt
- Retrieved: 2026-09-29T12:55:12Z
- SHA-256 of the bytes read: ae8e15414a21fe8d54a30fee7c3fbd1ee6a018e624dcd681d030da5c1cabbcac (3768675 bytes)
- Loci read: Leg. 23–24; Strom. I.5, I.17, I.21 (opening), V.14 (passages on Plato), VI.3, VI.17, VII.2.
- Quoted: Leg. 23, 24; Strom. I.5, I.17, I.21, V.14, VI.17, VII.2.
- Rights: public domain.
- Ceiling: CCEL plain text; ANF chapter titles are editorial and are not quoted as Clement's words.

### Tertullian, Apologeticum; De anima
- Witness: Tertullian, *Apology* and *A Treatise on the Soul*, ANF 3 (CCEL); Latin of *Apologeticum* 22 from The Latin Library.
- Repository ids: `work.tertullian.apologeticum` (existing); `work.tertullian.de-anima` (registered with this publication); `work.ante-nicene-fathers.volume-3` (existing).
- URL: https://ccel.org/ccel/s/schaff/anf03/cache/anf03.txt ; https://www.thelatinlibrary.com/tertullian/tertullian.apol.shtml
- Retrieved: 2026-09-29T12:55:14Z; 2026-09-30T14:14:43Z
- SHA-256 of the bytes read: 9299f3fae7c08024ea918e70d25433b7b110cc2b851d030cb22f3b1f080800c8 (4427171 bytes); 04410aeeabcd7f2ef832b41b28469ee2cdf87d06a2898afccb8d2e3dcb0bbe01 (148723 bytes)
- Loci read: Apol. 22–23; De anima 1, 37, 39, 53.
- Quoted: Apol. 22.1–2 (English and Latin); De anima 1, 37, 39, 53.
- Rights: public domain.
- Ceiling: web transcriptions.

### Minucius Felix, Octavius; Origen, Contra Celsum
- Witness: Minucius Felix, *Octavius*; Origen, *Against Celsus*; ANF 4 (CCEL).
- Repository ids: `work.minucius-felix.octavius` (registered with this publication); `work.origen.contra-celsum` (existing); `work.ante-nicene-fathers.volume-4` (existing).
- URL: https://ccel.org/ccel/s/schaff/anf04/cache/anf04.txt
- Retrieved: 2026-09-29T12:55:15Z
- SHA-256 of the bytes read: b9f385a048c18158c2f74dcd37062f48a1c68a5d05bdb07270a93692d172da2e (4237225 bytes)
- Loci read: Oct. 26–27; C. Cels. V.2–6; VII.68–70; VIII.24, 31–36, 60–64.
- Quoted: Oct. 26; C. Cels. V.4, V.5, VII.69, VIII.31, 32, 34, 64.
- Rights: public domain.
- Ceiling: CCEL plain text.

### Lactantius, Divinae institutiones II
- Witness: Lactantius, *Divine Institutes*, ANF 7 (CCEL; ANF numbers the chapters II.15–16); Latin, ed. S. Brandt, CSEL 19 (1890), archive.org OCR (numbers them II.14–15).
- Repository ids: `work.lactantius.divinae-institutiones` (registered with this publication).
- URL: https://ccel.org/ccel/s/schaff/anf07/cache/anf07.txt ; https://archive.org/download/CorpusScriptorumEcclesiasticorumLatinorum19/Corpus_scriptorum_ecclesiasticorum_Latinorum_19_djvu.txt
- Retrieved: 2026-09-29T12:55:17Z; 2026-09-30T14:24:31Z
- SHA-256 of the bytes read: b69327af0a84dd247c8e32848ad158b038125b534fa6333bba734c5de22e261c (3986919 bytes); c9cab1f595d738f66287faf45407805b62bb73459952f4381905499e2a8eb286 (2788107 bytes)
- Loci read: II.14–15 Brandt (ANF II.15–16).
- Quoted: II.14.7–8 (English); II.14.6, 8, 12 (Latin phrases).
- Rights: public domain.
- Ceiling: CSEL OCR; Brandt section numbers read from the page margins; the apparatus note tying the grammarians' etymology to Cratylus 398b is a finding aid only.

### Eusebius, Praeparatio evangelica
- Witness: Eusebius of Caesarea, *Preparation for the Gospel*, tr. E. H. Gifford (Oxford 1903), books IV, V, VII, XI, XIII, transcribed by Roger Pearse at tertullian.org.
- Repository ids: `work.eusebius.praeparatio-evangelica` (registered with this publication).
- URL: https://www.tertullian.org/fathers/eusebius_pe_{04_book4,05_book5,07_book7,11_book11,13_book13}.htm
- Retrieved: 2026-09-30T14:34:08Z–14:34:14Z
- SHA-256 of the bytes read: 554dd61a56a7b96a1d1a02cbc0b412e1cf93d5b64967f13dabcc7659c1c84ddf (118032 bytes)
- Loci read: IV contents, 17, 22–23 with Gifford's notes; V.1–7, 15–17; VII.15–16; XI.26–27; XIII preface, 1–2, 11–15.
- Quoted: IV.17, 22; V.1, 3, 4, 17; VII.15, 16; XI.26; XIII preface, 1, 14, 15.
- Rights: public domain (Gifford 1903; the transcription is marked public domain).
- Ceiling: web transcription; Gifford's page references kept only in the notes read.

### Augustine, De civitate Dei VIII–X; De doctrina christiana II.40
- Witness: Augustine, *City of God*, NPNF 1.2 (Book VIII tr. J. J. Smith; Books IX–X tr. M. Dods); *On Christian Doctrine*, tr. J. F. Shaw, NPNF 1.2; Latin of VIII–IX from augustinus.it (NBA).
- Repository ids: `work.augustine.de-civitate-dei` (existing); `work.augustine.de-doctrina-christiana` (existing); `work.nicene-and-post-nicene-fathers.series-1-volume-2` (existing).
- URL: https://ccel.org/ccel/s/schaff/npnf102/cache/npnf102.txt ; https://www.augustinus.it/latino/cdd/cdd_08_libro.htm ; https://www.augustinus.it/latino/cdd/cdd_09_libro.htm
- Retrieved: 2026-09-29T12:55:19Z; 2026-09-30T14:15:01Z; 14:15:03Z
- SHA-256 of the bytes read: 5c973feda803f3e58a88ed7df210b42d436f5466741eb8dbeae713ab56dedae4 (3692898 bytes); bd8ed7a5c387c8a52d501258bbecb724e6dae8833c816822a5bb79925ef2d1aa (100585 bytes); 464d82ad37e9313a7e4c8181f2518d39ec487cb1453fb504e8bcc70280058076 (66915 bytes)
- Loci read: VIII.5, 9, 11, 13–16, 18, 22; IX.15, 19–23; X.1–2, 9–11, 26–27, 29; De doctr. chr. II.40.60–61; the NPNF note naming Smith as translator of Book VIII.
- Quoted: VIII.5, 9, 11, 14, 16, 18 (English and Latin), 20 (Latin), 22; IX.15, 19, 20 (English and Latin), 23 (English and Latin phrase); X.2, 9, 10, 11, 26, 29; De doctr. chr. II.40.60.
- Rights: public domain.
- Ceiling: CCEL and augustinus.it transcriptions; subsection numbers within chapters not used.

### Isidore, Etymologiae VIII.11
- Witness: Isidore of Seville, *Etymologiae* VIII, The Latin Library.
- Repository ids: `work.isidore.etymologiae` (existing).
- URL: https://www.thelatinlibrary.com/isidore/8.shtml
- Retrieved: 2026-09-30T14:49:33Z
- SHA-256 of the bytes read: 96480a05bcaa0360188cf5970c0d02914ee2df2e65b62f9ea4d89288d0034439 (65576 bytes)
- Loci read: VIII.11.1–18.
- Quoted: VIII.11.16 (Latin phrase); VIII.11.15 cited.
- Rights: public domain text.
- Ceiling: web transcription (Lindsay text).

### Thomas Aquinas, Summa theologiae (English and Latin)
- Witness: *ST*, English Dominican translation, 2nd rev. ed. 1920, New Advent.
- Repository ids: `work.thomas-aquinas.summa-theologiae` (existing).
- URL: https://www.newadvent.org/summa/{1022,1050,1051,1063,1064,1103,1110,1111,1112,1113,3094}.htm
- Retrieved: 2026-09-29/30 (see manifest; 3094 fetched 2026-09-30T14:34:15Z)
- SHA-256 of the bytes read: a1a20aa7d29ce6cbcfc7a9dd60dcdad0edb7f39594e2f99f9c865b048952a3ea (42227 bytes)
- Loci read: I q.22 a.3; q.50 aa.2–3, 5; q.51 a.1; q.63 a.7; q.64 a.4; q.103 a.6; q.110 aa.1–3; q.111 a.1; q.112 a.4; q.113 aa.2, 5; II-II q.94 aa.1, 4.
- Quoted: all of these except q.110 aa.2–3.
- Rights: public domain (1920).
- Ceiling: New Advent HTML; the objections' citations of Damascene, Origen, Augustine (Gen. ad litt., De div. qq. 83), Jerome and Nemesius are reported as the *Summa*'s.

### Thomas Aquinas, De substantiis separatis; SCG II.92; In Metaph. XII; In De causis; In De div. nom.
- Witness: Corpus Thomisticum (Leonine 1968 for De sub. sep.; Leonine/Marietti for SCG; Marietti 1950 for In Metaph. and In DN; Saffrey 1954 for In De causis).
- Repository ids: `work.thomas-aquinas.de-substantiis-separatis` (registered with this publication); `work.thomas-aquinas.summa-contra-gentiles` (registered with this publication); `work.thomas-aquinas.sententia-libri-metaphysicae` (registered with this publication); `work.thomas-aquinas.super-librum-de-causis` (registered with this publication); `work.thomas-aquinas.super-de-divinis-nominibus` (registered with this publication).
- URL: https://www.corpusthomisticum.org/ots.html ; scg2091.html ; cmp12.html ; cdc00.html ; cdn00.html
- Retrieved: ots 2026-09-29T12:54:53Z; scg2091 2026-09-29T13:39:29Z; cmp12, cdc00, cdn00 2026-09-30T14:41:06Z–14:41:11Z
- SHA-256 of the bytes read: 3149f5709dbec16c044723d25f009a4a43caf0d38e965f28a0972b55474c78d9 (167879 bytes); f044d4518ba4eada9fc0ae4539741ad71cd9dfb014730e1d772cd023f952a36e (79602 bytes); 58a349313eea934ec0f245f40754207a798b7b6f567d38690dc6dc7a4b0d19bc (216417 bytes); 3eda0e782b143d595ba3ddb6e933a6abf592c5f3b44325e288189fff5f9124b0 (7552 bytes); c5688a430f217569300187345cdf3e7abecd2e36c9d676725dafc79518aa7908 (9523 bytes)
- Loci read: De sub. sep. prooem., 1–4, openings of 9–11, 18–20; SCG II.92 entire; In Metaph. XII lect. 8 n. 6–7, lect. 10 n. 31–33; In De causis prooem.; In DN prooem.
- Quoted (Latin, with English marked "our translation"): De sub. sep. prooem., 2, 3, 4, 18, 20; SCG II.92 n. 7 (English only); In Metaph. XII lect. 10 n. 31; In De causis prooem.; In DN prooem.
- Rights: the Latin text is public domain; the Corpus Thomisticum digital edition carries "© 2019 Fundación Tomás de Aquino quoad hanc editionem", so only short excerpts are quoted.
- Ceiling: web edition; not collated with the Leonine print.

### Magisterium and Scripture
- Witness: Lateran IV, *Firmiter* (DS 800), Denzinger via patristica.net; CCC 329–331 (vatican.va English); Douay–Rheims (Challoner), Gutenberg 1581.
- Repository ids: `work.fourth-lateran-council.firmiter-credimus` (existing); `work.denzinger.enchiridion-symbolorum` (existing); `work.catholic-church.catechism` (existing); `edition.english-college-of-douay.douay-rheims-bible.challoner-gutenberg-1581` (existing).
- URL: https://patristica.net/denzinger/enchiridion-symbolorum.html ; https://www.vatican.va/archive/ENG0015/__P1A.HTM ; https://www.gutenberg.org/cache/epub/1581/pg1581.txt
- Retrieved: 2026-09-29T12:56:36Z; 12:56:38Z; 12:58:58Z
- SHA-256 of the bytes read: 604f24c46e0bc71c2018f25dc787a9ab421d4b2e9cf7d1cee1f43e910ef2708f (2333435 bytes); f5d0972215f47a1bc22e768aa4e51f454db80f32dcbc4e3dd52b4a40ae5254d3 (22605 bytes); 7d10da78d8ec97db53b4e2bd8719cc01e16106b44937a673ba34aa534a04c007 (5880580 bytes)
- Loci read: DS 800; CCC 329–331; the Douay verses listed below.
- Quoted: DS 800 (Latin); CCC 329 and 331 (short phrases); Douay verses.
- Rights: DS Latin public domain; CCC English is Vatican copyright, used in two short phrases with attribution; Douay public domain.
- Ceiling: web transcriptions.

## The Greek Fathers before Nicaea

### Clement of Rome, First Epistle to the Corinthians
- Witness: Clement of Rome, *1 Clement*, tr. in ANF vol. 1 (Roberts/Donaldson/Coxe, 1885), CCEL plain text.
- Repository ids: `work.ante-nicene-fathers.volume-1` (existing); `work.clement-of-rome.first-epistle-to-the-corinthians` (registered with this publication).
- URL: https://ccel.org/ccel/s/schaff/anf01/cache/anf01.txt
- Retrieved: 2026-09-29T12:55:11Z
- SHA-256 of the bytes read: ee9c7f0ac3f4df08d07ddf81cd7e061e82a35e0d27de611cae06f1e05b2fb991 (3149312 bytes)
- Loci read: chs. 29, 34, 36 (and chapter scan for all angel mentions, chs. 1–59).
- Quoted: 29; 34 (block); 36.
- Rights: public domain (1885 translation).
- Ceiling: CCEL e-text of ANF; not collated with print or with the Greek.

### Ignatius of Antioch, Letters to the Trallians, Smyrnaeans, Ephesians
- Witness: Ignatius, *Trall.*, *Smyrn.*, *Eph.*, shorter and longer Greek recensions in parallel, ANF vol. 1.
- Repository ids: `work.ignatius-of-antioch.letter-to-the-smyrnaeans` (existing); `work.ignatius-of-antioch.letter-to-the-trallians` (registered with this publication); `work.ignatius-of-antioch.letter-to-the-ephesians` (registered with this publication).
- URL: https://ccel.org/ccel/s/schaff/anf01/cache/anf01.txt
- Retrieved: 2026-09-29T12:55:11Z
- SHA-256 of the bytes read: ee9c7f0ac3f4df08d07ddf81cd7e061e82a35e0d27de611cae06f1e05b2fb991 (3149312 bytes)
- Loci read: Trall. 5 (both recensions), Smyrn. 6, Eph. 13, 19 (both recensions); ANF introductory note on the recensions.
- Quoted: Trall. 5 (shorter; and longer recension marked as such); Smyrn. 6; Eph. 13, 19 (shorter).
- Rights: public domain.
- Ceiling: English only; the longer recension identified as an interpolated expansion on the ANF introductory note's authority.

### Epistle of Barnabas; Epistle to Diognetus; Martyrdom of Polycarp
- Witness: ANF vol. 1 translations.
- Repository ids: `work.ante-nicene-fathers.volume-1` (existing); `work.anonymous.epistle-of-barnabas` (registered with this publication); `work.anonymous.epistle-to-diognetus` (registered with this publication).
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
- Repository ids: `work.athenagoras.legatio-pro-christianis` (registered with this publication).
- URL: https://ccel.org/ccel/s/schaff/anf02/cache/anf02.txt
- Retrieved: 2026-09-29T12:55:12Z. Cache: text/ccel-anf02.txt
- Loci read: Leg. 10, 24–28.
- Quoted: 10 (block), 24 (block and inline), 25, 26, 27.
- Rights: public domain. Ceiling: English only.

### Tatian, Address to the Greeks
- Witness: ANF vol. 2 (with the ANF introductory note on Tatian's later Encratism).
- Repository ids: `work.tatian.oratio-ad-graecos` (registered with this publication).
- URL / Retrieved / Cache: as ANF 2 above.
- Loci read: Or. 7–9, 12–16, 20; introductory note.
- Quoted: 7, 12, 14, 15, 16. Greek term `angelos protogonos` from the American editor's note [441] at ch. 7.
- Rights: public domain. Ceiling: English only.

### Theophilus of Antioch, To Autolycus
- Witness: ANF vol. 2.
- Repository ids: `work.theophilus-of-antioch.ad-autolycum` (registered with this publication).
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
- Repository ids: `work.clement-of-alexandria.stromata` (registered with this publication).
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
- Repository ids: `work.methodius-of-olympus.symposium` (registered with this publication); `work.methodius-of-olympus.de-resurrectione` (registered with this publication).
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
- Repository ids: `work.john-chrysostom.homiliae-in-genesim` (registered with this publication).
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

## The Greek Fathers from Athanasius to Chrysostom

### Athanasius, Orationes contra Arianos I–III
- Witness: Athanasius, *Four Discourses against the Arians* (Newman's translation as revised by A. Robertson), NPNF2 4 (New York: Christian Literature Publishing Co., 1892), CCEL plain text; New Advent HTML of the same translation used only to restore the opening quotation marks that CCEL's text conversion drops.
- Repository ids: `work.athanasius-of-alexandria.orationes-contra-arianos` (registered with this publication).
- URL: https://ccel.org/ccel/s/schaff/npnf204/cache/npnf204.txt ; https://www.newadvent.org/fathers/28161.htm , 28162.htm , 28163.htm
- Retrieved: 2026-09-30 (CCEL 14:09:25Z; New Advent 14:32Z)
- SHA-256 of the bytes read: d2f362ce989db6955bb7d900c619543c581beceaca52acd8359510551c85f124 (4570263 bytes); c7af95bd78890b292ac48db06c4401bafc431d64693afab2cd0460e14752b900 (220200 bytes)
- Loci read: I.53–62; II.18–30; III.10–15
- Quoted: I.55, 56, 61, 62; II.19, 20, 21, 23, 26, 27, 29; III.10, 12, 14
- Rights: public domain (1892 translation)
- Ceiling: web transcription; not collated with print or Greek; New Advent modernizes scriptural pronouns, so wording was taken from CCEL and only punctuation from New Advent.

### Athanasius, De incarnatione Verbi
- Witness: Athanasius, *On the Incarnation of the Word* (A. Robertson), NPNF2 4 (1892), CCEL.
- Repository ids: none registered; the entry cites the edition directly.
- URL: https://ccel.org/ccel/s/schaff/npnf204/cache/npnf204.txt
- Retrieved: 2026-09-30T14:09:25Z
- SHA-256 of the bytes read: d2f362ce989db6955bb7d900c619543c581beceaca52acd8359510551c85f124 (4570263 bytes)
- Loci read: 25 (with §§23–24 headings)
- Quoted: 25.5, 25.6
- Rights: public domain
- Ceiling: web transcription; not collated.

### Athanasius, Vita Antonii
- Witness: Athanasius, *Life of Antony* (H. Ellershaw), NPNF2 4 (1892), CCEL.
- Repository ids: `work.athanasius-of-alexandria.vita-antonii` (existing).
- URL: https://ccel.org/ccel/s/schaff/npnf204/cache/npnf204.txt
- Retrieved: 2026-09-30T14:09:25Z
- SHA-256 of the bytes read: d2f362ce989db6955bb7d900c619543c581beceaca52acd8359510551c85f124 (4570263 bytes)
- Loci read: 16, 20–44, 59–66
- Quoted: 21, 22, 23, 24, 25, 26, 28, 29, 30, 31, 33, 34, 35, 36, 37, 38, 40, 41, 42, 43, 65
- Rights: public domain
- Ceiling: web transcription; translator named in the NPNF2 4 preface ("the Rev. H. Ellershaw, jun.").

### Cyril of Jerusalem, Catecheses and Mystagogical Catecheses
- Witness: Cyril of Jerusalem, *Catechetical Lectures* (E. H. Gifford), NPNF2 7 (New York, 1893), CCEL.
- Repository ids: `work.cyril-of-jerusalem.catechetical-lectures` (existing).
- URL: https://ccel.org/ccel/s/schaff/npnf207/cache/npnf207.txt
- Retrieved: 2026-09-29T12:55:25Z
- SHA-256 of the bytes read: 56d84cfa94dee313af0139e2d7f3d4b5f7fffca40ce0f34794b5f56264964dfd (3388014 bytes)
- Loci read: Cat. II.3–4; III.3, 16; IV.1; VI.5–6; VIII.3–5; XI.11–13, 21–23; XV.21–25; XVI.13–17, 20–24; Myst. V.4–9 (with the NPNF notes 2045, 2483–2486)
- Quoted: II.4; III.3; III.16; IV.1; VI.6; VIII.4; XI.11, 12, 13, 21, 23; XV.22, 23, 24; XVI.13, 15, 16, 23; Myst. V.6
- Rights: public domain
- Ceiling: web transcription; not collated with Greek.

### Basil, De Spiritu Sancto
- Witness: Basil, *On the Spirit* (Blomfield Jackson), NPNF2 8 (Edinburgh: T&T Clark, 1895), CCEL.
- Repository ids: `work.basil-of-caesarea.de-spiritu-sancto` (existing).
- URL: https://ccel.org/ccel/s/schaff/npnf208/cache/npnf208.txt
- Retrieved: 2026-09-29T12:55:26Z
- SHA-256 of the bytes read: 4f21a589be54f0c160c2a2bf8c316991dae1a0f3d13430466ed2db555018e0e2 (2645735 bytes)
- Loci read: 13.29–30; 16.37–40; 23.54
- Quoted: 13.29, 13.30, 16.38 (several sentences), 23.54
- Rights: public domain
- Ceiling: web transcription; Greek not collated (so the Greek behind "powers/authorities" in 16.38 is not verified).

### Basil, Hexaemeron
- Witness: Basil, *Hexaemeron* (Blomfield Jackson), NPNF2 8 (1895), CCEL.
- Repository ids: `work.basil-of-caesarea.homiliae-in-hexaemeron` (existing).
- URL: https://ccel.org/ccel/s/schaff/npnf208/cache/npnf208.txt
- Retrieved: 2026-09-29T12:55:26Z
- SHA-256 of the bytes read: 4f21a589be54f0c160c2a2bf8c316991dae1a0f3d13430466ed2db555018e0e2 (2645735 bytes)
- Loci read: I.1, I.5–6; II.4–5; V.5–6
- Quoted: I.5; II.5; V.6
- Rights: public domain
- Ceiling: web transcription.

### Basil, Adversus Eunomium III (Greek, PG 29)
- Witness: Basil, *Adversus Eunomium* III.1–2, Greek text in Migne, *Patrologia Graeca* 29 (Paris, 1857), archive.org OCR; English rendering made for this edition.
- Repository ids: `work.jacques-paul-migne.patrologia-graeca-volume-29` (existing).
- URL: https://archive.org/download/patrologiae_cursus_completus_gr_vol_029/patrologiae_cursus_completus_gr_vol_029_djvu.txt
- Retrieved: 2026-09-29T17:52:47Z
- SHA-256 of the bytes read: f4b52a32d8e2a8e33c0532df6224976b63896f8f6276358b207f9297730f1c8e (8499613 bytes)
- Loci read: III.1–2 (PG 29, 655–658; column headers 655/656 and 657/658 legible)
- Quoted: III.1 (own rendering, block quotation, PG 29, 656B–657A); III.2 (own rendering, one sentence); transliterated terms paidag\=ogos, nomeus, archistrat\=egos
- Rights: Migne Greek public domain; English is the edition's own rendering (marked by footnote in the body).
- Ceiling: OCR of the Greek column read and rendered; the Latin column is OCR'd in Greek glyphs and is illegible; not collated with a critical edition. CCC 336 note 203 independently gives "PG 29, 656B".

### Basil, Homiliae in Psalmos 33 and 48 (Greek, PG 29)
- Witness: Basil, *Homilia in Psalmum 33* and *Homilia in Psalmum 48*, Greek text in PG 29, archive.org OCR; English renderings made for this edition.
- Repository ids: `work.basil-of-caesarea.homilia-in-psalmum-33` (existing); `work.basil-of-caesarea.homiliae-in-psalmos` (existing); `work.jacques-paul-migne.patrologia-graeca-volume-29` (existing).
- URL: https://archive.org/download/patrologiae_cursus_completus_gr_vol_029/patrologiae_cursus_completus_gr_vol_029_djvu.txt
- Retrieved: 2026-09-29T17:52:47Z
- SHA-256 of the bytes read: f4b52a32d8e2a8e33c0532df6224976b63896f8f6276358b207f9297730f1c8e (8499613 bytes)
- Loci read: Hom. in Ps. 33.5 (on v. 8), 33.8 (on v. 12), 33 on vv. 16–17 (section number not legible in OCR), Hom. in Ps. 48.9 (on v. 15)
- Quoted: all as own renderings: 33.5 (block + two sentences), 33.8 (one sentence), 33 on vv. 16–17 (two sentences), 48.9 (two sentences)
- Rights: Migne Greek public domain; English is the edition's own rendering.
- Ceiling: OCR Greek read; section numbers inferred from OCR markers ("5.", "8.", "9."); PG column numbers for these homilies are not legible in the OCR and are not printed in the body.

### Gregory of Nazianzus, Orations 2, 28, 31, 38, 40, 41, 42, 45
- Witness: Gregory Nazianzen, *Select Orations* (C. G. Browne and J. E. Swallow), NPNF2 7 (1893), CCEL.
- Repository ids: `work.gregory-of-nazianzus.oration-38` (registered with this publication); `work.gregory-of-nazianzus.oration-40` (existing); `work.gregory-of-nazianzus.oration-2` (registered with this publication).
- URL: https://ccel.org/ccel/s/schaff/npnf207/cache/npnf207.txt
- Retrieved: 2026-09-29T12:55:25Z
- SHA-256 of the bytes read: 56d84cfa94dee313af0139e2d7f3d4b5f7fffca40ce0f34794b5f56264964dfd (3388014 bytes)
- Loci read: Or. 2.67–73; 28.8–9, 30–31; 31.15, 29; 38.4, 7–12, 16–17; 40.4–7, 36; 41.10–11; 42 heading, 8–9, 27; 45.1–2, 5
- Quoted: 2.73; 28.31 (two blocks and several phrases); 31.15; 31.29; 38.9 (block); 38.10; 38.11; 38.17; 40.5 (block); 40.7; 41.11; 42.9; 42.27; 45.2
- Rights: public domain
- Ceiling: web transcription; not collated with Greek (so the Greek of "Splendours, Ascents, Intelligences" is not given).

### Gregory of Nyssa, Oratio catechetica
- Witness: Gregory of Nyssa, *The Great Catechism* (W. Moore and H. A. Wilson), NPNF2 5 (1892), CCEL.
- Repository ids: `work.gregory-of-nyssa.oratio-catechetica-magna` (existing).
- URL: https://ccel.org/ccel/s/schaff/npnf205/cache/npnf205.txt
- Retrieved: 2026-09-29T17:32:27Z
- SHA-256 of the bytes read: cef974043e48a52d1b6d4ce3bdfb538fa5be2c3af8b53e3bb75181760d614484 (3490499 bytes)
- Loci read: 6 (whole); 24; 26 (first half)
- Quoted: 6 (block and phrases); 24; 26
- Rights: public domain
- Ceiling: web transcription.

### Gregory of Nyssa, De hominis opificio
- Witness: *On the Making of Man*, NPNF2 5 (1892), CCEL.
- Repository ids: `work.gregory-of-nyssa.de-hominis-opificio` (existing).
- URL: as above
- Retrieved: 2026-09-29T17:32:27Z
- SHA-256 of the bytes read: cef974043e48a52d1b6d4ce3bdfb538fa5be2c3af8b53e3bb75181760d614484 (3490499 bytes)
- Loci read: 17.1–4
- Quoted: 17.2 (block), 17.3, 17.4
- Rights: public domain
- Ceiling: web transcription.

### Gregory of Nyssa, Contra Eunomium
- Witness: *Against Eunomius*, NPNF2 5 (1892), CCEL, NPNF book numbering.
- Repository ids: `work.gregory-of-nyssa.contra-eunomium` (registered with this publication).
- URL: as above
- Retrieved: 2026-09-29T17:32:27Z
- SHA-256 of the bytes read: cef974043e48a52d1b6d4ce3bdfb538fa5be2c3af8b53e3bb75181760d614484 (3490499 bytes)
- Loci read: NPNF Book IV §§2–3 (lines c. 13880–14010)
- Quoted: IV.3 (two sentences)
- Rights: public domain
- Ceiling: NPNF division only; not reconciled with Jaeger's numbering.

### Gregory of Nyssa, De vita Moysis II (Greek, PG 44)
- Witness: Gregory of Nyssa, *De vita Moysis*, Greek text in Migne, PG 44 (Paris, 1863), archive.org OCR (full-text stream); English rendering made for this edition.
- Repository ids: `work.gregory-of-nyssa.de-vita-moysis` (registered with this publication).
- URL: https://archive.org/stream/patrologiae_cursus_completus_gr_vol_044/patrologiae_cursus_completus_gr_vol_044_djvu.txt (the /download/ djvu.txt URL returned HTTP 500 twice; the stream endpoint serves the same OCR text inside HTML)
- Retrieved: 2026-09-30T14:27:50Z
- SHA-256 of the bytes read: aa9d6d88c7b49eff6b0b40b80c5986228356ccc3418127cdc6d72625d9410c7d (7884554 bytes)
- Loci read: PG 44, 337D–340B
- Quoted: 337D–340A (block, own rendering); 340 (one sentence, own rendering); 340 (paraphrase of the objector's concession)
- Rights: Migne Greek public domain; English is the edition's own rendering.
- Ceiling: OCR Greek read; column numbers inferred from garbled running heads (337/338, 339/340) and margin letters; modern section numbering (Musurillo/Daniélou) not verified, so the body cites book II and PG columns only.

### Ephrem the Syrian, Hymns
- Witness: Ephrem, *Hymns on the Nativity* (I–XIII J. B. Morris, revised; XIV–XIX A. E. Johnston), *Hymns for the Epiphany* (A. E. Johnston), *Nisibene Hymns* (J. T. S. Stopford and others), NPNF2 13, CCEL.
- Repository ids: `work.ephrem-the-syrian.hymni-de-nativitate` (registered with this publication); `work.ephrem-the-syrian.hymni-de-epiphania` (registered with this publication); `work.ephrem-the-syrian.carmina-nisibena` (registered with this publication).
- URL: https://ccel.org/ccel/s/schaff/npnf213/cache/npnf213.txt
- Retrieved: 2026-09-29T12:55:32Z
- SHA-256 of the bytes read: 02dd51a2aff1cabf92e80a0ab5f8d88872f2185613c92acd9d1a90431169285f (1921581 bytes)
- Loci read: translators' preface; Nat. I (prose portion near note 377–378), XIV (whole), XV.35–37, XVI.7–8, XVIII.1–2; Epiph. IV.7–12, VI.5–9, 19–20, VIII.18–20; Nis. XXXVI.1, 14–16
- Quoted: Nat. I; XIV.3–4, 21, 23; XV.37; XVI.8; Epiph. IV.10; VI.7, 8, 20; VIII.19; Nis. XXXVI.15
- Rights: public domain
- Ceiling: English only; Syriac not read ("Watchers" as Ephrem's usual name for the angels rests on the NPNF note 378); Nat. I is cited by hymn only (NPNF prints no stanza number there).

### John Chrysostom, Homilies on Hebrews
- Witness: Chrysostom, *Homilies on Hebrews* (Oxford translation revised by F. Gardiner), NPNF1 14, CCEL.
- Repository ids: `work.john-chrysostom.homilies-on-hebrews` (registered with this publication).
- URL: https://ccel.org/ccel/s/schaff/npnf114/cache/npnf114.txt
- Retrieved: 2026-09-29T12:55:23Z
- SHA-256 of the bytes read: e26f55f8d0739c07d73d5b664e42efbd923a43230a22d93d55261c808e9cd458 (3943878 bytes)
- Loci read: Hom. 3.1–5; 5.1; 6 (passage at line 37968)
- Quoted: 3.1; 3.4 (block and several sentences); 5.1
- Rights: public domain
- Ceiling: web transcription; reviser named in the volume ("rev. frederic gardiner, d.d.").

### John Chrysostom, Homilies on John
- Witness: *Homilies on the Gospel of St. John*, NPNF1 14, CCEL.
- Repository ids: `work.john-chrysostom.homilies-on-john` (existing).
- URL: as above
- Retrieved: 2026-09-29T12:55:23Z
- SHA-256 of the bytes read: e26f55f8d0739c07d73d5b664e42efbd923a43230a22d93d55261c808e9cd458 (3943878 bytes)
- Loci read: Hom. 15.1–2
- Quoted: 15.1
- Rights: public domain
- Ceiling: NPNF numbers this homily 15; the Summa (I q. 12 a. 1 obj. 1) cites it as "Hom. xiv in Joan."

### John Chrysostom, Homilies on Colossians
- Witness: *Homilies on Colossians*, NPNF1 13, CCEL.
- Repository ids: `work.john-chrysostom.homilies-on-colossians` (existing).
- URL: https://ccel.org/ccel/s/schaff/npnf113/cache/npnf113.txt
- Retrieved: 2026-09-29T12:55:22Z
- SHA-256 of the bytes read: 54274dd9aa73ca36e4da9e763e4a27d1818b09e42ffc73795529afec703a4210 (3933882 bytes)
- Loci read: Hom. 3 (on Col 1:15–20, lines 24321–24570); Hom. 5 (lines 25255–25290); Hom. 6 (on Col 2:13–15); Hom. 7 (on Col 2:16–19)
- Quoted: Hom. 3 (two blocks, three phrases); Hom. 5; Hom. 6; Hom. 7
- Rights: public domain
- Ceiling: NPNF gives no section numbers; cited by homily.

### John Chrysostom, Homilies on Ephesians
- Witness: *Homilies on Ephesians*, NPNF1 13, CCEL.
- Repository ids: `work.john-chrysostom.homilies-on-ephesians` (existing).
- URL: as above
- Retrieved: 2026-09-29T12:55:22Z
- SHA-256 of the bytes read: 54274dd9aa73ca36e4da9e763e4a27d1818b09e42ffc73795529afec703a4210 (3933882 bytes)
- Loci read: Hom. 3 (moral part, lines 6340–6395); Hom. 7 (on Eph 3:8–11); Hom. 22 (on Eph 6:10–13)
- Quoted: Hom. 3; Hom. 7; Hom. 22
- Rights: public domain
- Ceiling: cited by homily.

### John Chrysostom, Homilies on Matthew 59
- Witness: *Homilies on Matthew* (G. Prevost, rev. M. B. Riddle), NPNF1 10; read in CCEL and in the New Advent page cached by an earlier lane.
- Repository ids: `work.john-chrysostom.homiliae-in-matthaeum` (existing).
- URL: https://ccel.org/ccel/s/schaff/npnf110/cache/npnf110.txt ; https://www.newadvent.org/fathers/200159.htm (local copy .scratch/aquinas-ministry/chrysostom-matt59.txt, accessed 2026-09-29 per artifact-receipts.json)
- Retrieved: 2026-09-29T17:54:08Z (CCEL)
- SHA-256 of the bytes read: adb8f1c9a988c5050a20fb9fdbf75143dcb227e95e3dad2f560a63b757923648 (3345978 bytes)
- Loci read: Hom. 59.1–5
- Quoted: 59.4
- Rights: public domain
- Ceiling: two web witnesses of the same translation agree; New Advent mislabels 1 Cor 11:10 as "1 Corinthians 10:10".

### John Chrysostom, Homilies on Acts 26
- Witness: *Homilies on the Acts of the Apostles*, NPNF1 11, CCEL.
- Repository ids: `work.john-chrysostom.homilies-on-acts` (existing).
- URL: https://ccel.org/ccel/s/schaff/npnf111/cache/npnf111.txt
- Retrieved: 2026-09-30T14:09:28Z
- SHA-256 of the bytes read: 8bdb50c6fd132a9558cbd16808ae05000ddcc7059cfd6c1d282f4f734e539c15 (4443151 bytes)
- Loci read: Hom. 26 (on Acts 12:12–17) with note 629
- Quoted: Hom. 26
- Rights: public domain
- Ceiling: web transcription.

### John Chrysostom, Homilies on 1 and 2 Corinthians
- Witness: *Homilies on the Epistles of Paul to the Corinthians*, NPNF1 12 (Edinburgh, 1889), CCEL.
- Repository ids: `work.john-chrysostom.homilies-on-first-corinthians` (existing).
- URL: https://ccel.org/ccel/s/schaff/npnf112/cache/npnf112.txt
- Retrieved: 2026-09-30T14:09:29Z
- SHA-256 of the bytes read: 10a3454d6c08d52088837132f06ca07c5a1ec9d7264d909fa92c48aa3b2ddddc (2897359 bytes)
- Loci read: 1 Cor Hom. 26 (on 1 Cor 11:2–10); 2 Cor Hom. 2 (litany for the catechumens, with the NPNF note giving the reconstructed prayer)
- Quoted: 1 Cor Hom. 26; 2 Cor Hom. 2
- Rights: public domain
- Ceiling: web transcription.

### John Chrysostom, De sacerdotio; Ad Theodorum lapsum; De diabolo tentatore
- Witness: *On the Priesthood* (translations new or revised by W. R. W. Stephens, per Schaff's preface), *Exhortation to Theodore after his Fall*, *Three Homilies concerning the Power of Demons*, NPNF1 9 (New York, 1886), CCEL.
- Repository ids: `work.john-chrysostom.de-sacerdotio` (registered with this publication); `work.john-chrysostom.ad-theodorum-lapsum` (registered with this publication); `work.john-chrysostom.de-diabolo-tentatore` (registered with this publication).
- URL: https://ccel.org/ccel/s/schaff/npnf109/cache/npnf109.txt
- Retrieved: 2026-09-30T14:09:26Z
- SHA-256 of the bytes read: d6a51d22d996e02c47b88462f7222737b26d2363212f24e34834cfc6b580da57 (2752950 bytes)
- Loci read: De sac. III.4–5; VI.1–4; Ad Theod. I.11–12; De diab. I.4–6; II.1–2
- Quoted: De sac. III.4 (block), III.5, VI.4 (block and phrase); Ad Theod. I.11, I.12; De diab. I.6, II.1, II.2
- Rights: public domain
- Ceiling: web transcription.

### Thomas Aquinas, Summa theologiae (loci cited for reception)
- Witness: English Dominican translation (2nd rev. ed. 1920) as presented by New Advent; Latin (Leonine) from Corpus Thomisticum for I q. 45 a. 5 and q. 113 prologue.
- Repository ids: `work.thomas-aquinas.summa-theologiae` (existing).
- URL: https://www.newadvent.org/summa/1012.htm , 4083.htm (fetched by this lane); 1050, 1051, 1052, 1057, 1061, 1062, 1063, 1064, 1108, 1113, 1114 (shared cache); Corpus Thomisticum per manifest (ct-sth1044, ct-sth1103)
- Retrieved: 2026-09-30T14:23:55Z (1012, 4083); others 2026-09-29 per manifest
- SHA-256 of the bytes read: ee3e9358de1bb9f43597737f2bdb483742666ca7235053084982853630bd8118 (107866 bytes); 9cc4a4ca7eb43fb062493b171f02284957e4627af226ea6c1e51c1d0659a9a62 (124815 bytes); 41c6edfab20faec48a4181d11d3dbde6549398127633854b20c60bce9f3c5b9c (176483 bytes); 5736abad11534d6a5ebb3fa0c76ff5df228d6558cbb69163f5f437523f2c2ed1 (476518 bytes)
- Loci read: I q. 12 a. 1 (obj. 1, ad 1), a. 7 title; I q. 45 a. 5 (Latin s.c., corpus); I q. 50 a. 3; q. 51 aa. 1–2; q. 52 aa. 1–2 (corpus); q. 57 aa. 3, 5; q. 61 a. 3 (obj. 1, s.c., corpus, ad 1); q. 62 aa. 3, 6, 8 (titles and corpus of 3, 6); q. 63 aa. 2, 7 (corpus); q. 64 aa. 2, 4 (corpus); q. 108 aa. 4, 5 (s.c.), 6 (s.c., corpus); q. 113 aa. 1–6, 8; q. 114 aa. 1, 4; III q. 83 a. 4 (corpus, ad 9)
- Quoted: I q. 12 a. 1 ad 1; q. 50 a. 3; q. 51 a. 2 ad 1; q. 57 a. 3; q. 61 a. 3 (obj. 1); q. 62 aa. 3, 6; q. 63 aa. 2, 7; q. 64 a. 4; q. 108 aa. 4, 6; q. 113 aa. 3, 6; q. 114 a. 1; III q. 83 a. 4 and ad 9
- Rights: public domain translation
- Ceiling: web transcription.

### Denzinger (DS 411, 800, 801)
- Witness: Denzinger, *Enchiridion symbolorum*, Latin, patristica.net transcription.
- Repository ids: none registered; the entry cites the edition directly.
- URL: https://patristica.net/denzinger/enchiridion-symbolorum.html
- Retrieved: 2026-09-29T12:56:36Z
- SHA-256 of the bytes read: 604f24c46e0bc71c2018f25dc787a9ab421d4b2e9cf7d1cee1f43e910ef2708f (2333435 bytes)
- Loci read: DS 403–411; 800–801
- Quoted: DS 800 (Latin phrase)
- Rights: Latin conciliar text
- Ceiling: web transcription.

### Catechism of the Catholic Church 331–336
- Witness: CCC, English, vatican.va.
- Repository ids: none registered; the entry cites the edition directly.
- URL: https://www.vatican.va/archive/ENG0015/__P1A.HTM
- Retrieved: 2026-09-29T12:56:38Z
- SHA-256 of the bytes read: f5d0972215f47a1bc22e768aa4e51f454db80f32dcbc4e3dd52b4a40ae5254d3 (22605 bytes)
- Loci read: 331, 333, 334, 335, 336 and notes 202–203
- Quoted: 335 (one sentence), 336 (two phrases)
- Rights: Vatican copyright; short quotations with attribution.
- Ceiling: web text.

### Douay–Rheims (Challoner)
- Witness: Project Gutenberg eBook 1581.
- Repository ids: `edition.english-college-of-douay.douay-rheims-bible.challoner-gutenberg-1581` (existing).
- URL: https://www.gutenberg.org/cache/epub/1581/pg1581.txt
- Retrieved: 2026-09-29T12:58:58Z
- SHA-256 of the bytes read: 7d10da78d8ec97db53b4e2bd8719cc01e16106b44937a673ba34aa534a04c007 (5880580 bytes)
- Loci read: all verses listed under Scripture cited that are quoted in English
- Quoted: Heb 1:4; 2:2; 2:16; 1 Tim 5:21; Ps 33:8; 48:15; Ezek 28:15; Dan 10:13, 20; Matt 26:53; Acts 12:15; Col 2:18; 1 Cor 11:10
- Rights: public domain
- Ceiling: Gutenberg transcription.

## The Latin Fathers before Dionysius

### Witness: Tertullian, *Apologeticum* 22–23 (ANF 3, S. Thelwall trans.; Latin: The Latin Library)

- Repository ids: `work.tertullian.apologeticum` (existing); `work.ante-nicene-fathers.volume-3` (existing).
- URL: https://ccel.org/ccel/s/schaff/anf03/cache/anf03.txt ; Latin https://www.thelatinlibrary.com/tertullian/tertullian.apol.shtml
- Retrieved: 2026-09-29T12:55:14Z (ANF 3); 2026-09-30T14:14:43Z (Latin)
- SHA-256 of the bytes read: 9299f3fae7c08024ea918e70d25433b7b110cc2b851d030cb22f3b1f080800c8 (4427171 bytes); 04410aeeabcd7f2ef832b41b28469ee2cdf87d06a2898afccb8d2e3dcb0bbe01 (148723 bytes)
- Loci read: chs. 22–23 entire in both
- Quoted: 22.3 (fall of certain angels, demon-brood), 22.5 (*subtilitas et tenuitas*; English phrase), 22.8 (block; Latin *Omnis spiritus ales est: hoc angeli et daemones*), further 22 phrases (prophets, clouds, cures), 23.4, 23.15–16 (block), 23 ("your very gods kindle up faith")
- Rights: public domain (ANF 1885–87; Latin text PD)
- Ceiling: web transcriptions; section numbers from the Latin Library; ANF not collated with CCSL; Latin Library edition not identified on the page

### Witness: Tertullian, *Adversus Marcionem* II.10 (ANF 3, P. Holmes trans.)

- Repository ids: `work.tertullian.adversus-marcionem` (existing).
- URL: https://ccel.org/ccel/s/schaff/anf03/cache/anf03.txt
- Retrieved: 2026-09-29T12:55:14Z
- SHA-256 of the bytes read: 9299f3fae7c08024ea918e70d25433b7b110cc2b851d030cb22f3b1f080800c8 (4427171 bytes)
- Loci read: II.10 entire
- Quoted: II.10 (six phrases/sentences: made good, wisest of creatures, "by creation good and by choice corrupt", the gloss on the archangel, the holy mountain, free will, room for a conflict)
- Rights: public domain
- Ceiling: English only; Latin not consulted for this chapter

### Witness: Tertullian, *De patientia* 5 (ANF 3, S. Thelwall; Latin: The Latin Library)

- Repository ids: `work.tertullian.de-patientia` (registered with this publication).
- URL: ANF 3 as above; https://www.thelatinlibrary.com/tertullian/tertullian.patientia.shtml
- Retrieved: 2026-09-29T12:55:14Z; 2026-09-30T14:14:47Z
- SHA-256 of the bytes read: 9299f3fae7c08024ea918e70d25433b7b110cc2b851d030cb22f3b1f080800c8 (4427171 bytes); c78f0f82c911f7c4bd9741f3707916d7edaa2d00e352b82378e4e86cbdcd3baf (42947 bytes)
- Loci read: ch. 5 entire (English and Latin)
- Quoted: 5 (block, 5.5–6), phrases "that angel of perdition", "grew up indivisible in one paternal bosom"; Latin 5.5 *natales inpatientiae in ipso diabolo deprehendo*
- Rights: public domain
- Ceiling: web transcription

### Witness: Tertullian, *De carne Christi* 3, 6 (ANF 3, P. Holmes; Latin: The Latin Library)

- Repository ids: `work.tertullian.de-carne-christi` (registered with this publication).
- URL: ANF 3; https://www.thelatinlibrary.com/tertullian/tertullian.carne.shtml
- Retrieved: 2026-09-29T12:55:14Z; 2026-09-30T14:14:44Z
- SHA-256 of the bytes read: 9299f3fae7c08024ea918e70d25433b7b110cc2b851d030cb22f3b1f080800c8 (4427171 bytes); 3ae0ac81fcb94bc545c96a46061178e787b157e4028dc26a4b85c24d411919a2 (75987 bytes)
- Loci read: chs. 3 and 6 entire
- Quoted: 3 (angels changed into human form; "there was solidity in their bodily substance"); 6 ("Never did any angel descend…", block on the angelic nature); Latin 6.9 *substantiae spiritalis—etsi corporis alicuius, sui tamen generis*, 6.10 *proprium angelicae potestatis, ex nulla materia corpus sibi sumere*
- Rights: public domain
- Ceiling: web transcription

### Witness: Tertullian, *De oratione* 3, 16, 22, 29 (ANF 3, S. Thelwall; Latin: The Latin Library)

- Repository ids: `work.tertullian.de-oratione` (registered with this publication).
- URL: ANF 3; https://www.thelatinlibrary.com/tertullian/tertullian.oratione.shtml
- Retrieved: 2026-09-29T12:55:14Z; 2026-09-30T14:14:46Z
- SHA-256 of the bytes read: 9299f3fae7c08024ea918e70d25433b7b110cc2b851d030cb22f3b1f080800c8 (4427171 bytes); 36524829732d2399f488fde647ced44383eea570aa9e7f7503f7a7238a7049ce (33407 bytes)
- Loci read: chs. 3, 16, 22 (passage on 1 Cor 11:10), 29
- Quoted: 3.3 (circle of angels, "candidates for angelhood"; Latin *angelorum … candidati*), 16 ("the angel of prayer is still standing by"), 22 ("on account of 'the daughters of men' angels revolted"), 29 ("The angels, likewise, all pray"; Latin *Orant etiam angeli omnes*)
- Rights: public domain
- Ceiling: web transcription; ANF chapter 22 heading "Answer to the Foregoing Arguments"

### Witness: Tertullian, *De anima* (ANF 3, P. Holmes)

- Repository ids: `work.tertullian.de-anima` (registered with this publication).
- URL: ANF 3
- Retrieved: 2026-09-29T12:55:14Z
- SHA-256 of the bytes read: 9299f3fae7c08024ea918e70d25433b7b110cc2b851d030cb22f3b1f080800c8 (4427171 bytes)
- Loci read: chapter headings 1–58; chs. 37, 39, 53 (end), 57 entire
- Quoted: 37, 39, 53, 57 (one sentence each)
- Rights: public domain
- Ceiling: English only; the body's statement that Tertullian holds the soul corporeal rests on the ANF chapter titles of chs. 5 and 7

### Witness: Tertullian, *De idololatria* 9 (ANF 3) and *De cultu feminarum* I.2 (ANF 4)

- Repository ids: `work.tertullian.de-idololatria` (registered with this publication); `work.tertullian.de-cultu-feminarum` (registered with this publication); `work.ante-nicene-fathers.volume-3` (existing); `work.ante-nicene-fathers.volume-4` (existing).
- URL: ANF 3; https://ccel.org/ccel/s/schaff/anf04/cache/anf04.txt
- Retrieved: 2026-09-29T12:55:14Z; 2026-09-29T12:55:15Z
- SHA-256 of the bytes read: 9299f3fae7c08024ea918e70d25433b7b110cc2b851d030cb22f3b1f080800c8 (4427171 bytes); b9f385a048c18158c2f74dcd37062f48a1c68a5d05bdb07270a93692d172da2e (4237225 bytes)
- Loci read: *De idol.* 9 (opening); *De cultu fem.* I.2
- Quoted: *De idol.* 9 (two phrases); *De cultu fem.* I.2 (two phrases)
- Rights: public domain
- Ceiling: English only

### Witness: Minucius Felix, *Octavius* 26–27 (ANF 4, R. E. Wallis trans.)

- Repository ids: `work.minucius-felix.octavius` (registered with this publication).
- URL: https://ccel.org/ccel/s/schaff/anf04/cache/anf04.txt
- Retrieved: 2026-09-29T12:55:15Z
- SHA-256 of the bytes read: b9f385a048c18158c2f74dcd37062f48a1c68a5d05bdb07270a93692d172da2e (4237225 bytes)
- Loci read: chs. 26–27 entire
- Quoted: 26 (block; "the very source of error"), 27 (four phrases/sentences)
- Rights: public domain
- Ceiling: English only; ANF names the magus "Sosthenes (otherwise Hostanes)" — the sentence using it was removed

### Witness: Cyprian, *De zelo et livore* 4; *Quod idola dii non sint* 6–7; *Ad Demetrianum* 15; *De habitu virginum* 14 (ANF 5, R. E. Wallis trans.)

- Repository ids: `work.cyprian.de-zelo-et-livore` (registered with this publication); `work.cyprian.quod-idola-dii-non-sint` (registered with this publication); `work.cyprian.ad-demetrianum` (registered with this publication); `work.cyprian.de-habitu-virginum` (registered with this publication); `work.ante-nicene-fathers.volume-5` (existing).
- URL: https://ccel.org/ccel/s/schaff/anf05/cache/anf05.txt
- Retrieved: 2026-09-30T14:11:58Z
- SHA-256 of the bytes read: a02b61c36f07edd406a08138b9797151d6e808cb1618f1cc282fe9db5f6a87f8 (4302686 bytes)
- Loci read: De zelo 1–5; Quod idola 1–15 (headings) and 6–7 entire; Ad Demetr. 15; De hab. virg. 12–15
- Quoted: De zelo 4 (block and one sentence; "at the very beginnings of the world"; "they who are on his side imitate him"); Quod idola 6, 7 (phrases); Ad Demetr. 15 (one sentence); De hab. virg. 14 (two phrases)
- Rights: public domain
- Ceiling: English only; ANF prints *On the Vanity of Idols* among Cyprian's treatises; its authorship was not examined. ANF 5 introduction used for Cyprian's martyrdom (a.d. 258)

### Witness: Lactantius, *Divinae institutiones* II.8, II.14–16 and *Epitome* 22–23 (ANF 7, W. Fletcher trans.; Latin and numbering: Brandt, CSEL 19, 1890)

- Repository ids: `work.lactantius.divinae-institutiones` (registered with this publication); `work.lactantius.epitome-divinarum-institutionum` (registered with this publication).
- URL: https://ccel.org/ccel/s/schaff/anf07/cache/anf07.txt ; https://archive.org/download/CorpusScriptorumEcclesiasticorumLatinorum19/Corpus_scriptorum_ecclesiasticorum_Latinorum_19_djvu.txt
- Retrieved: 2026-09-29T12:55:17Z; 2026-09-30T14:24:31Z
- SHA-256 of the bytes read: b69327af0a84dd247c8e32848ad158b038125b534fa6333bba734c5de22e261c (3986919 bytes); c9cab1f595d738f66287faf45407805b62bb73459952f4381905499e2a8eb286 (2788107 bytes)
- Loci read: ANF II.9, II.14–17, Epitome 27–28; CSEL II.8.3–7, II.13–14 (pages 162–163), Epit. 22–23
- Quoted: II.8.4–5 (block), II.8.6; II.14.1 (English and Latin *misit angelos ad tutelam cultumque generis humani*), II.14.2–8 (several sentences), II.14 ("insinuate themselves"); II.15 (two sentences); II.16 (block, one sentence); Epit. 22.9–11; Latin II.8.5 *cunctorum malorum fontem esse liuorem*
- Rights: public domain (ANF; CSEL 1890)
- Ceiling: CSEL read in OCR; numbering taken from CSEL running heads and margin numbers; ANF numbers book II chapters one higher (ANF II.9 = CSEL II.8; ANF II.15–17 = CSEL II.14–16) and the Epitome 27–28 = CSEL 22–23 (CSEL prints "23 (28)"). ANF 7 introduction used for Lactantius's biography (rhetoric, Nicomedia, education of Crispus)

### Witness: Hilary of Poitiers, *Tractatus super Psalmos* (CSEL 22, ed. A. Zingerle, 1891)

- Repository ids: `work.hilary-of-poitiers.tractatus-super-psalmos` (existing).
- URL: https://archive.org/download/shilariiepiscopi22hila/shilariiepiscopi22hila_djvu.txt
- Retrieved: 2026-09-30T14:12:47Z
- SHA-256 of the bytes read: 0c9712d4bb1cabe200b4acc320feb70c4f0a593f59ba902fc897ae006285eb08 (2320546 bytes)
- Loci read: Ps 118 Aleph 5–9 (lines 21800–21960), Vau 7–9 (24880–24935); Ps 124.4–6 (35655–35730); Ps 129.6–8 (38600–38720); Ps 134.9, 12, 16–18 (41255–41600); Ps 137.4–6 (43370–43430)
- Quoted (Latin; English the lane's own): 118 Aleph 7 (*plena sunt … incolat*), Aleph 8 (*metuimus … mundum*; *puncto temporis … obeuntem*; *instigare ad peccandum et arguere peccantes*); Vau 8 (*leges angelorum*, *indefessa uoce*, *tamquam lege officii proprioris*, *pusillorum angelos … conspicere*); 124.4–6 (*ecclesia angelorum multitudinis frequentium*, *angelorum munitiones*, *qui ecclesiam quadam custodia circumsaepiunt*, *bonum quidem praesidium angeli, sed melius domini*); 129.7 (block; *intercessione itaque horum non natura dei eget, sed infirmitas nostra*); 134.9 (list), 134.12 (list), 134.17 (block); 137.5 (*scit enim se sub specula … adsistere*)
- Rights: public domain (1891 edition)
- Ceiling: archive.org OCR of a critical edition; readings checked against the printed apparatus where OCR was doubtful (e.g., *Raphael* for OCR "Eaphael"); CSEL orthography (u for v) kept; section numbers from the edition

### Witness: Ambrose, *De Spiritu Sancto* (NPNF2 10, H. de Romestin trans.)

- Repository ids: `work.ambrose.de-spiritu-sancto` (registered with this publication).
- URL: https://ccel.org/ccel/s/schaff/npnf210/cache/npnf210.txt
- Retrieved: 2026-09-29T12:55:29Z
- SHA-256 of the bytes read: 14fa05cc98a67cb1ccf7613e63d5eb80fd48feb3e09dd29210e70f53dfcd7577 (2963575 bytes)
- Loci read: I.5.62–66; I.7.80–88; I.10.112–115; I.11.116–117; I.16.177–179; II.5.36–38
- Quoted: I.7 (the circumscription sentence; NPNF prints two paragraphs numbered 81 — the first is cited as "I.7"), I.7.82 (phrase), I.7.83 (block), I.7.84; I.5.62–63 (two phrases); I.10.115; I.11.116 (block); I.16.178
- Rights: public domain (NPNF 1896)
- Ceiling: English only; II.5.37 read but no longer quoted

### Witness: Ambrose, *De fide* I.10, III.3, IV.1 (NPNF2 10)

- Repository ids: `work.ambrose.de-fide` (registered with this publication).
- URL: NPNF2 10 as above
- Retrieved: 2026-09-29T12:55:29Z
- SHA-256 of the bytes read: 14fa05cc98a67cb1ccf7613e63d5eb80fd48feb3e09dd29210e70f53dfcd7577 (2963575 bytes)
- Loci read: I.10.63–66; III.3.14–20; IV.1.1–11
- Quoted: I.10.64–65 (two phrases), III.3.19 (one sentence), IV.1.6 (block), IV.1.9–10 (one sentence; "Who is the King of glory?")
- Rights: public domain
- Ceiling: English only

### Witness: Ambrose, *De viduis* 9.52–58 (NPNF2 10)

- Repository ids: `work.ambrose.de-viduis` (registered with this publication).
- URL: NPNF2 10 as above
- Retrieved: 2026-09-29T12:55:29Z
- SHA-256 of the bytes read: 14fa05cc98a67cb1ccf7613e63d5eb80fd48feb3e09dd29210e70f53dfcd7577 (2963575 bytes)
- Loci read: ch. 9 (52–58)
- Quoted: 9.55 (block)
- Rights: public domain
- Ceiling: English only; Latin not consulted

### Witness: Jerome, *Commentarii in Matthaeum* III, on Matt 18:10 (PL 26)

- Repository ids: `work.jerome.commentariorum-in-evangelium-matthaei` (existing).
- URL: https://archive.org/download/patrologiaecurs240unkngoog/patrologiaecurs240unkngoog_djvu.txt
- Retrieved: 2026-09-29T13:24:28Z
- SHA-256 of the bytes read: 74c5dd24a294e30a8a1de023ef9842b41a79f52410fae49113156b075ce0d046 (4745230 bytes)
- Loci read: on Matt 18:6–12
- Quoted: *Quia angeli eorum … angelum delegatum* (block; English the lane's own)
- Rights: public domain
- Ceiling: Google-scan OCR, heavily corrupted; normalized (e.g., OCR *dignilas*, *ui*, *nativitaiis* read as *dignitas*, *ut*, *nativitatis*); not collated with CCSL 77; Aquinas's English (*ST* I q. 113 a. 2 s.c.) used only as a control, not quoted as Jerome

### Witness: Jerome, *Epistula* 18 to Damasus (PL 22, Vallarsi text; NPNF2 6 introductory summary as control)

- Repository ids: `work.jerome.letter-18` (registered with this publication).
- URL: https://archive.org/download/bim_early-english-books-1641-1700_patrologiae-cursus-completus-_1845_22/bim_early-english-books-1641-1700_patrologiae-cursus-completus-_1845_22_djvu.txt ; control https://ccel.org/ccel/s/schaff/npnf206/cache/npnf206.txt
- Retrieved: 2026-09-30T14:14:41Z; control 2026-09-29T17:32:29Z
- SHA-256 of the bytes read: afb07d6ae696c65680ea0feba64e541dbcfaa7526304c293f469370014dd5e95 (4268197 bytes); 53fb977f33ea3d92276eca7c0d2fa2e86f654499855ea74bef1c0721706724e1 (3559723 bytes)
- Loci read: §§6–11, 16–17 (Vallarsi sections) and the editor's notes
- Quoted (Latin; English the lane's own): 18.6 etymology, *cum per ea Dominus ipse discatur*; 18.7 *Velabant faciem … condiderit?*; 18.9 *virtutes quasdam in caelis*, *et in diversa ministeria mittantur, maximeque ad eos qui purgatione indigent*; 18.17 *Quotidie ad nos mittitur Seraphim …*, *Nec putandum sexum esse in Virtutibus Dei*
- Rights: public domain
- Ceiling: OCR of PL 22 (1845) corrected by reading; not collated with CSEL 54; NPNF gives only a summary of this letter (used for the date, Constantinople 381), none of it quoted as Jerome

### Witness: Jerome, *Commentarii in Danielem* on 10:7–21 (PL 25)

- Repository ids: `work.jerome.commentaria-in-danielem` (existing).
- URL: https://archive.org/download/bim_early-english-books-1641-1700_patrologiae-cursus-completus-_1845_25/bim_early-english-books-1641-1700_patrologiae-cursus-completus-_1845_25_djvu.txt
- Retrieved: 2026-09-30T14:14:38Z
- SHA-256 of the bytes read: 116c5a253abdc00fd0882e5e102d38d9266b263e4096d0b720b062194cbb4bb9 (4968383 bytes)
- Loci read: on Dan 10:7–21 (two-column OCR re-ordered by reading)
- Quoted (Latin; English the lane's own): on 10:13 (block: *Videtur mihi … dimitteretur*), *enumerans peccata populi Judaeorum …*, *angelus Michael qui praeest populo Israel*, *Principes autem primos, archangelos intelligimus*; on 10:20–21 *ut accusaret et Persarum principem atque Medorum*, *Et revera mira sacramenta Dei*
- Rights: public domain
- Ceiling: OCR with interleaved columns; the order of sentences reconstructed by reading; not collated with CCSL 75A. (A second scan, `text/ia-pl25-jerome-1857.txt`, proved to be PG 25 and was not used.)

### Witness: Jerome, *Commentarii in epistulam ad Titum* on 1:2 and *in epistulam ad Ephesios* I on 1:21 (PL 26)

- Repository ids: `work.jerome.commentariorum-in-epistolam-ad-titum` (registered with this publication); `work.jerome.commentariorum-in-epistolam-ad-ephesios` (registered with this publication).
- URL: PL 26 as above; control for Titus: PL 22 Vallarsi note to Ep. 18.7
- Retrieved: 2026-09-29T13:24:28Z; 2026-09-30T14:14:41Z
- SHA-256 of the bytes read: 74c5dd24a294e30a8a1de023ef9842b41a79f52410fae49113156b075ce0d046 (4745230 bytes); afb07d6ae696c65680ea0feba64e541dbcfaa7526304c293f469370014dd5e95 (4268197 bytes)
- Loci read: on Titus 1:2; on Eph 1:20–23
- Quoted (Latin; English the lane's own): Titus *Sex mille necdum … servierint Deo* (two OCR witnesses agree: PL 26 text and the PL 22 note); Eph *quod scilicet in caelestibus … vocabula*; *et putamus Deum … contentum?*
- Rights: public domain
- Ceiling: OCR normalized; not collated with CCSL

### Witness: John Cassian, *Conlationes* VII–VIII (Abbot Serenus) (NPNF2 11, E. C. S. Gibson trans.)

- Repository ids: `work.john-cassian.conlationes` (registered with this publication); `work.nicene-and-post-nicene-fathers.series-2-volume-11` (existing).
- URL: https://ccel.org/ccel/s/schaff/npnf211/cache/npnf211.txt
- Retrieved: 2026-09-30T14:11:59Z
- SHA-256 of the bytes read: 8b1206d4e7488c65b5391875fd9570a8a6bcc83270dea35ffe44010c3575d267 (3470230 bytes)
- Loci read: Conferences VII and VIII entire; prolegomena on Cassian's life (Bethlehem, Scete, Marseilles; composition 426–428)
- Quoted: VII.8, 10, 12, 13, 15, 16 (block), 17, 19, 20, 21, 22, 23, 28, 30, 32; VIII.6, 7 (block), 8, 10, 12, 13, 14, 15, 16, 17, 19, 21, 25
- Rights: public domain (NPNF 1894)
- Ceiling: English only; Latin (CSEL 13, Petschenig) not consulted

### Witness: Leo the Great, *Sermones* 2, 73, 74 (NPNF2 12, C. L. Feltoe trans.); Letter 15 to Turibius via Denzinger

- Repository ids: `work.nicene-and-post-nicene-fathers.series-2-volume-12` (existing); `work.denzinger.enchiridion-symbolorum` (existing).
- URL: https://ccel.org/ccel/s/schaff/npnf212/cache/npnf212.txt ; https://patristica.net/denzinger/enchiridion-symbolorum.html
- Retrieved: 2026-09-29T12:55:30Z; 2026-09-29T12:56:36Z
- SHA-256 of the bytes read: 7bb1db6e2f6814b58dd13a7b85f17f37f80c22ac979c3298793db1fa909b5b5a (2906681 bytes); 604f24c46e0bc71c2018f25dc787a9ab421d4b2e9cf7d1cee1f43e910ef2708f (2333435 bytes)
- Loci read: Serm. 2.1–2, 26 (angel passages), 73.1–4, 74.1–5; DS 286
- Quoted: Serm. 73.4, 74.4 (two passages); DS 286 Latin clause *diabolus bonus esset, si in eo quod factus est permaneret*
- Rights: public domain
- Ceiling: English only for the sermons; Serm. 2.2 read but its sentence was cut from the final text

### Witness: Gennadius of Marseilles, *Liber de ecclesiasticis dogmatibus* (PL 58, Elmenhorst text)

- Repository ids: none registered; the entry cites the edition directly.
- URL: https://archive.org/download/patrologiae_cursus_completus_lat_vol_058/patrologiae_cursus_completus_lat_vol_058_djvu.txt (primary); https://archive.org/download/patrologiaecur58mign/patrologiaecur58mign_djvu.txt (second scan; Baronius's testimony on attribution)
- Retrieved: 2026-09-30T14:20:54Z; 2026-09-30T14:12:54Z
- SHA-256 of the bytes read: b73b4a2773a18ab3b7a690c5b20817b86c82ea361358c2b9792e201bde99d004 (4389677 bytes); 722ef703cc9374a049f0fea1642b4c341a426bffd5482ea272580b00b4505cb9 (4731021 bytes)
- Loci read: chs. 1–13, 55–65, 80–86 (Elmenhorst numbering)
- Quoted (Latin; English the lane's own): 9 (*in angelicam qua creati sunt redeant dignitatem*), 10 (*In principio … bonitas*), 12 (*Creatura omnis corporea est … circumscribuntur*), 57 (*non est a Deo creata … creatus est*), 59 (block), 60 (*bonus esset …*), 81, 82, 83 (clauses)
- Rights: public domain
- Ceiling: OCR normalized (e.g., *caeteris* for OCR *cxiei is*; *et* for *ei*); chs. 61–62 only paraphrased because the OCR of ch. 62 is badly garbled; chapter numbers differ from those the *Summa* cites (see footnote in the body). NPNF2 11 prolegomena used for Gennadius's date (a.d. 495) and Marseilles

### Witness: Thomas Aquinas, *Summa theologiae* (English Dominican 1920, New Advent; Latin, Corpus Thomisticum)

- Repository ids: `work.thomas-aquinas.summa-theologiae` (existing).
- URL: https://www.newadvent.org/summa/ (1050, 1051, 1056, 1057, 1061, 1062, 1063, 1064, 1108, 1109, 1110, 1113, 1114, 3083, 4008, 4080); https://www.corpusthomisticum.org/sth1050.html , sth1103.html
- Retrieved: 2026-09-29 (1xxx files, 4008), 2026-09-30T14:20:56Z (4080), 2026-09-30T14:26:30Z (3083)
- SHA-256 of the bytes read: fdad93a169263562e04f4d85c8466d04f65115af75b1d398f9f616fd8875b2fe (123249 bytes); 53ca9130d490807df26e7b801dcf7bd79beb8e36dc591a7509b7d1bca53a18e2 (137359 bytes); e2cfab53e3a057155f3e241b32c059123265ae7cfe58da04e9d7cb41f3fb0ee7 (402442 bytes); 5736abad11534d6a5ebb3fa0c76ff5df228d6558cbb69163f5f437523f2c2ed1 (476518 bytes)
- Loci read: I q. 50 a. 1 (obj. 3, ad 3); q. 51 aa. 1–3 (a. 2 corpus and ad 3; a. 3 obj. 6, ad 6); q. 56 a. 2 obj. 3 (Latin); q. 57 aa. 3–5; q. 61 a. 3 (obj. 1, corpus, ad 1); q. 62 aa. 1 (obj. 1, Latin and English), 2, 6, 8, 9; q. 63 aa. 2, 6, 7 (and ad 1); q. 64 a. 4; q. 108 aa. 5 (s.c., ad 5, ad 6), 7 (obj. 1, corpus, ad 1); q. 109 aa. 1–2; q. 110 a. 1; q. 113 aa. 2–5, 8; q. 114 aa. 1, 3 (s.c.), 4; II-II q. 83 a. 4; III q. 8 a. 8 (obj. 2, ad 1); III q. 80 a. 9 ad 2
- Quoted: q. 50 a. 1 ad 3 (phrase); q. 51 a. 2 ad 3 (phrase); q. 57 a. 4 (phrase); q. 61 a. 3 ad 1 (phrase); q. 63 a. 7 ad 1 (phrase); q. 113 a. 5 ("and with reason"); q. 113 a. 3 ("one of the princes"); q. 114 a. 1 (sentence); II-II q. 83 a. 4 (sentence); III q. 8 a. 8 ad 1 (phrase)
- Rights: public domain translation (1920); New Advent presentation
- Ceiling: web transcription; Leonine Latin consulted only for q. 56 a. 2, q. 62 a. 1, q. 114 a. 3

### Witness: Denzinger (DS 286, 411, 800)

- Repository ids: `work.denzinger.enchiridion-symbolorum` (existing).
- URL: https://patristica.net/denzinger/enchiridion-symbolorum.html
- Retrieved: 2026-09-29T12:56:36Z
- SHA-256 of the bytes read: 604f24c46e0bc71c2018f25dc787a9ab421d4b2e9cf7d1cee1f43e910ef2708f (2333435 bytes)
- Loci read: DS 286, 403–411, 800
- Quoted: DS 286 (Latin clause); DS 800 and 411 cited, not quoted
- Rights: public-domain Latin acta
- Ceiling: web transcription

### Witness: Catechism of the Catholic Church, 331–336 (vatican.va English)

- Repository ids: `work.catholic-church.catechism` (existing).
- URL: https://www.vatican.va/archive/ENG0015/__P1A.HTM
- Retrieved: 2026-09-29T12:56:38Z
- SHA-256 of the bytes read: f5d0972215f47a1bc22e768aa4e51f454db80f32dcbc4e3dd52b4a40ae5254d3 (22605 bytes)
- Loci read: 331–336
- Quoted: 333 (phrase), 336 (sentence); 335 paraphrased
- Rights: Vatican English; short quotations with attribution
- Ceiling: web text

### Witness: Douay–Rheims Bible (Challoner), Project Gutenberg 1581

- Repository ids: `work.english-college-of-douay.douay-rheims-bible` (existing); `edition.english-college-of-douay.douay-rheims-bible.challoner-gutenberg-1581` (existing).
- URL: https://www.gutenberg.org/cache/epub/1581/pg1581.txt
- Retrieved: 2026-09-29T12:58:58Z
- SHA-256 of the bytes read: 7d10da78d8ec97db53b4e2bd8719cc01e16106b44937a673ba34aa534a04c007 (5880580 bytes)
- Loci read: every verse quoted in the body (Gen 6:2; Exod 23:20; Ps 33:8; 103:4; 118:2, 44; 129:2; 134:7; 137:1; Dan 10:13, 20; 4 Kgs 6:17; 3 Kgs 8:39; Matt 18:10; 25:41; 1 Cor 2:8; 8:5; 11:10; Eph 1:21; 1 Tim 5:21; Titus 1:2; Heb 1:14), plus Deut 32:8, Tob 12:12, 15, Isa 6:2–3, Ezek 28:12, 14, Isa 14:12–13, Eph 6:12, Jude 6, Apoc 12:4, Luke 10:18, 12:49, Acts 12:15, Job 38:7
- Quoted: the verses listed first above
- Rights: public domain
- Ceiling: web transcription; Deut 32:8 in the Douay reads "children of Israel"; the body notes that Hilary and Jerome cite the Septuagint form "angels of God"

### Witness: editors' introductions (finding aids for dates only)

- Repository ids: none registered; the entry cites the edition directly.
- Loci read: ANF 3 intro (Tertullian d. about a.d. 220, lines 164–301); ANF 5 intro (Cyprian, martyrdom a.d. 258, lines 26954–26966); ANF 7 intro (Lactantius, lines 331–353); NPNF2 6 (Jerome d. 420; Letter 18 written 381); NPNF2 9 (Hilary d. 367, line 3632); NPNF2 10 (Ambrose d. 397); NPNF2 11 prolegomena (Cassian; Gennadius a.d. 495)
- Quoted: none
- Rights: public domain
- Ceiling: secondary; used only for dates and biographical placement stated without quotation

## Augustine

### Augustine, De civitate Dei, English (NPNF)
- Witness: Augustine, *The City of God*, trans. Marcus Dods, in *Nicene and Post-Nicene Fathers*, first series, vol. 2, ed. Philip Schaff (CCEL print basis: New York: Christian Literature Publishing Co., 1890); CCEL plain-text edition.
- Repository ids: `work.augustine.de-civitate-dei` (existing).
- URL: https://ccel.org/ccel/s/schaff/npnf102/cache/npnf102.txt
- Retrieved: 2026-09-29T12:55:19Z (manifest)
- SHA-256 of the bytes read: 5c973feda803f3e58a88ed7df210b42d436f5466741eb8dbeae713ab56dedae4 (3692898 bytes)
- Loci read: VIII.14–27 in full; IX.1–2, 5, 13–23 in full; X.1–9, 12–16, 19–22 in full; XI.1–23, 29–34 in full; XII.1–10 in full; XIV.3 (paragraph on the devil); XV.22–23 in full; XXI.10 in full; XXII.1, 29 (first half), 30 (paragraph on degrees).
- Quoted: VIII.15 (paraphrase), 16, 18, 22, 25, 27; IX.5, 15, 19, 20, 21, 23; X.1, 3, 6, 7, 12, 13, 15, 16, 19, 20, 21, 22; XI.9, 11, 15, 16, 17, 19, 20, 29, 32, 33, 34; XII.1, 6, 7, 8, 9; XIV.3; XV.22, 23; XXI.10; XXII.1, 29, 30.
- Rights: public domain (Dods translation; CCEL print basis 1890).
- Ceiling: web transcription, not collated with the print; the NPNF editor's footnotes were read but no position is taken from them. The GPT scratch copies (`.scratch/christ-liturgy/augustine-cityxi.txt`, `.scratch/source-library/augustine-cdg12.txt`, `augustine-cdg14.txt`) were not used; the CCEL text was used instead.

### Augustine, De civitate Dei, Latin
- Witness: Latin text of books XI and XII at The Latin Library; Latin text of books X, XV, XXII at augustinus.it (books VIII, IX fetched, not quoted).
- Repository ids: `work.augustine.de-civitate-dei` (existing).
- URL: https://www.thelatinlibrary.com/augustine/civ11.shtml ; https://www.thelatinlibrary.com/augustine/civ12.shtml ; https://www.augustinus.it/latino/cdd/cdd_10_libro.htm ; …/cdd_15_libro.htm ; …/cdd_22_libro.htm (also cdd_08, cdd_09)
- Retrieved: civ11 2026-09-29T13:36:43Z, civ12 13:36:45Z; cdd_08/09/10/15/22 2026-09-30T14:15:01Z–14:15:09Z (this lane)
- SHA-256 of the bytes read: d39371cdd16d35aff529af05c50c68ba6260fbff76ff33526ddfca81cd3fb2e0 (81384 bytes); eaa02a7032e27db9eba0d007aafd450017b5b0260f7718d7a28ce968de4b9f7e (72904 bytes)
- Loci read: XI.9, XI.29; XII.1, 7, 9; X.7; XV.23 (opening); XXII.1, 29, 30.
- Quoted: XI.9 (`ut ea luce inluminati, qua creati, fierent lux`; `Mali enim nulla natura est; sed amissio boni mali nomen accepit`); XI.29 (`tamquam in diurna cognitione`; `in se ipsis autem tamquam in uespertina`); XII.7 (`non enim est efficiens sed deficiens, quia nec illa effectio sed defectio`); XII.9 (`simul eis et condens naturam et largiens gratiam`; `aut minorem acceperunt diuini amoris gratiam … illi amplius adiuti`); X.7 (`nobiscum`; `geritur namque ibi cura de nobis`); XV.23 (`iniungendo eis officium nuntiandi`); XXII.1 (`tantum populum gratia sua … ut inde suppleat et instauret partem, quae lapsa est angelorum`).
- Rights: public domain Latin.
- Ceiling: web transcriptions; underlying editions not stated on the pages; not collated with CCL 47–48.

### Augustine, De Genesi ad litteram, Latin
- Witness: Latin text at augustinus.it, books II, III, IV, V, VIII, XI.
- Repository ids: `work.augustine.de-genesi-ad-litteram` (existing).
- URL: https://www.augustinus.it/latino/genesi_lettera/genesi_lettera_02_libro.htm (and _03_, _04_, _05_, _08_, _11_libro.htm)
- Retrieved: 2026-09-29 (02/04/05/08 13:31:53Z–13:32:00Z; 03/11 17:51:12Z–17:51:14Z; manifest)
- Loci read: II.8.16–19; III.10.14–15; IV.20.37–35.56 in full; V.4.10, V.19.37–39; VIII.20.39, VIII.24.45–26.48; XI.13.17–28.35 in full.
- Quoted: II.8.16 (two passages), II.8.17 (three phrases); III.10.14 (`aeria … animalia`; `nunc diabolo, tunc archangelo`; `nonnulli nostri`), III.10.15 (`quasi carcer … usque ad tempus iudicii`); IV.22.39 (`ita et post vesperam fiat mane`; `qua non est quod Deus`; `a sua quadam informitate ad Creatorem conversa atque formata`), IV.23.40 (`aequales Angelis facti`), IV.24.41 (three phrases), IV.25.42, IV.26.43, IV.28.45, IV.30.47, IV.32.49, IV.32.50, IV.33.52 (`creavit omnia simul`), IV.35.56; V.19.37; VIII.20.39, VIII.24.45 (two passages); XI.13.17, XI.14.18 (block), XI.15.19, XI.15.20, XI.16.21 (block and phrase), XI.17.22, XI.19.26, XI.21.28, XI.22.29, XI.23.30 (block and phrase), XI.26.33 (`complexio`, `tamquam archangelus`), XI.27.34.
- Rights: public domain Latin. No public-domain English exists (J. H. Taylor, ACW 41–42, 1982, is in copyright); every English rendering of this work in the body is the drafter's own gloss, set unquoted after the Latin.
- Ceiling: web transcription (augustinus.it; underlying edition not identified on the page); not collated with CSEL 28.1.

### Augustine, De Trinitate
- Witness: Augustine, *On the Holy Trinity*, trans. Arthur West Haddan, rev. W. G. T. Shedd, NPNF first series vol. 3, ed. Schaff (CCEL print basis 1890); Latin book III at augustinus.it.
- Repository ids: `work.augustine.de-trinitate` (registered with this publication).
- URL: https://ccel.org/ccel/s/schaff/npnf103/cache/npnf103.txt ; https://www.augustinus.it/latino/trinita/trinita_03_libro.htm
- Retrieved: 2026-09-29T12:55:20Z (NPNF); 2026-09-30T14:15:11Z (Latin, this lane)
- SHA-256 of the bytes read: cc8d3ff7ce4d4ba293f50a06200af03ff0e5abdeb5200db3a59b4dbe2cad7bdb (3357503 bytes); b2b06936a08717dd5aa48a284827d500e8b632eb700c0779d457b133749e7f51 (68630 bytes)
- Loci read: III.1.4–11.27 (English, in full); Latin III.4.9, III.8.13.
- Quoted: III.1.5; III.4.9 (block and sentences); III.6.11; III.7.12; III.8.13 (block and phrase); III.9.16; III.11.22, 23, 24–25 (Gen 22:16 as quoted), 26; Latin III.4.9 (`de interiore invisibili atque intellegibili aula summi Imperatoris`), III.8.13 (`occulta quaedam semina in istis corporeis mundi huius elementis latent`).
- Rights: public domain.
- Ceiling: web transcription; NPNF numbering is book.chapter with running section numbers (e.g. III.4.9); Shedd's bracketed notes not used.

### Augustine, Enchiridion ad Laurentium
- Witness: *The Enchiridion*, trans. J. F. Shaw, NPNF first series vol. 3 (CCEL); Latin at augustinus.it.
- Repository ids: `work.augustine.enchiridion-ad-laurentium` (existing).
- URL: https://ccel.org/ccel/s/schaff/npnf103/cache/npnf103.txt ; https://www.augustinus.it/latino/enchiridion/enchiridion_libro.htm
- Retrieved: 2026-09-29T12:55:20Z; Latin 2026-09-30T14:14:59Z (this lane)
- SHA-256 of the bytes read: cc8d3ff7ce4d4ba293f50a06200af03ff0e5abdeb5200db3a59b4dbe2cad7bdb (3357503 bytes); 221eeda9e4d2fa2a46cffb067cf140d3b02dc1a5d8baac6bba1d4eacbcd3f1e0 (203208 bytes)
- Loci read: 27–29; 56–63 (English and Latin).
- Quoted: 28; 29 (block and sentence); 56 (block and phrase); 58 (block; Latin `dicant qui possunt, si tamen possunt probare quod dicunt: Ego me ista ignorare confiteor`, `Virtutes`); 59; 61; 62; 63.
- Rights: public domain.
- Ceiling: web transcriptions; chapter numbers as NPNF (= second number of the Latin 9.28, 15.56, etc.).

### Augustine, Enarrationes in Psalmos, Ps 103, sermo 1
- Witness: Latin at augustinus.it (page titled "In Psalmum 103 enarratio I").
- Repository ids: `work.augustine.enarrationes-in-psalmos` (existing).
- URL: https://www.augustinus.it/latino/esposizioni_salmi/esposizione_salmo_125_testo.htm (the site's sequential file number; the page is Ps 103 s. 1)
- Retrieved: 2026-09-29T13:16:09Z
- SHA-256 of the bytes read: c09f35f1aea0164d253248d7975fa0b8184a000566ca740f929de651fc603b3e (60734 bytes)
- Loci read: s. 1.1, 9, 15, 16.
- Quoted: s. 1.15 (block and four phrases); s. 1.16 (`tamquam angelus de coelo ad terram`; `fervens spiritu, ignis ardens est omnis minister Dei`).
- Rights: public domain Latin.
- Ceiling: web transcription. NPNF first series vol. 8 (text/ccel-npnf108.txt, "Psalm CIV … Lat. CIII") was checked: it is an abridged exposition that does not contain s. 1.15, so no public-domain English was available; the English of the key sentence is quoted from CCC 329 (Vatican English, short quotation with attribution), and the rest is the drafter's gloss.

### Augustine, De divinatione daemonum
- Witness: Latin at augustinus.it.
- Repository ids: `work.augustine.de-divinatione-daemonum` (registered with this publication).
- URL: https://www.augustinus.it/latino/potere_divinatorio/potere_divinatorio_libro.htm
- Retrieved: 2026-09-29T13:32:03Z
- SHA-256 of the bytes read: 152f2e97c16255ad64191158345f5f220e113de7e86ce1480cf38a5406e7bc4b (30665 bytes)
- Loci read: 1.1–7.11 in full.
- Quoted: 3.7 (block); 5.9 (`per illam subtilitatem suorum corporum … miscendo`); 6.10 (`quam Deus per sanctos Angelos suos et Prophetas operatur`; `ab Angelis Deo summo pie servientibus alia dispositione ignota daemonibus`).
- Rights: public domain Latin; English glosses are the drafter's own.
- Ceiling: web transcription; not collated with CSEL 41.

### Augustine, Retractationes, book II
- Witness: Latin at augustinus.it.
- Repository ids: `work.augustine.retractationes` (registered with this publication).
- URL: https://www.augustinus.it/latino/ritrattazioni/ritrattazioni_2_libro.htm
- Retrieved: 2026-09-30T14:14:57Z (this lane)
- SHA-256 of the bytes read: 683b581f9430763fb9ddada2aaebb7ee92e924599a8f43f9010bb15f896be3ab (105653 bytes)
- Loci read: II.6.1–2 (Confessions); II.30 (De divinatione daemonum).
- Quoted: II.6.2 (`non satis considerate dictum est; res autem in abdito est valde`); II.30 (`rem dixi occultissimam audaciore asseveratione quam debui`).
- Rights: public domain Latin.
- Ceiling: web transcription. Chapter number II.30 as printed there (the site also gives "LVII" in the running count).

### Augustine, De vera religione
- Witness: Latin at augustinus.it.
- Repository ids: `work.augustine.de-vera-religione` (registered with this publication).
- URL: https://www.augustinus.it/latino/vera_religione/vera_religione_libro.htm
- Retrieved: 2026-09-30T14:14:55Z (this lane)
- SHA-256 of the bytes read: c52fe9053d2b1d51483ea96baea08f09f9755ef97e77c4feacd92121fcc6fc5b (162988 bytes)
- Loci read: 55.107–113.
- Quoted: 55.110 (block and phrase `Quod ergo colit summus angelus, id colendum est etiam ab homine ultimo`); 55.112 (two sentences).
- Rights: public domain Latin; English glosses are the drafter's own (Burleigh's LCC translation, 1953, is in copyright and was not used).
- Ceiling: web transcription; not collated with CCL 32.

### Augustine, De diversis quaestionibus octoginta tribus
- Witness: Latin at augustinus.it.
- Repository ids: `work.augustine.de-diversis-quaestionibus-octoginta-tribus` (registered with this publication).
- URL: https://www.augustinus.it/latino/ottantatre_questioni/ottantatre_questioni_libro.htm
- Retrieved: 2026-09-29T13:31:33Z
- SHA-256 of the bytes read: 60b9fbde7a1bb0bd7e4b28efa445f3ecc04da8459fca9407303464dd9fd68d28 (316081 bytes)
- Loci read: q. 79.1–5.
- Quoted: q. 79.1 (`unaquaeque res visibilis … testatur`); q. 79.4 (`magi per privatos contractus … publicae iustitiae`).
- Rights: public domain Latin.
- Ceiling: web transcription.

### Aquinas, Summa theologiae (English and Latin)
- Witness: English Dominican translation, 2nd rev. ed. 1920, New Advent; Leonine Latin at Corpus Thomisticum.
- Repository ids: `work.thomas-aquinas.summa-theologiae` (existing).
- URL: https://www.newadvent.org/summa/1050.htm … 1064.htm, 1106.htm … 1114.htm; https://www.corpusthomisticum.org/sth1050.html, sth1103.html
- Retrieved: 2026-09-29 (cache; manifest)
- SHA-256 of the bytes read: e2cfab53e3a057155f3e241b32c059123265ae7cfe58da04e9d7cb41f3fb0ee7 (402442 bytes); 5736abad11534d6a5ebb3fa0c76ff5df228d6558cbb69163f5f437523f2c2ed1 (476518 bytes)
- Loci read: every Augustine citation in I qq. 50–64, 106–114 (located by script, then read in context); in full: q. 51 a. 2 s.c., a. 3 ad 6; q. 54 a. 5 co.; q. 55 a. 2 co., ad 1; q. 56 a. 1 s.c., a. 2 co.; q. 57 a. 4 co., a. 5 obj. 1; q. 58 a. 1 s.c.; q. 59 a. 4 ad 2; q. 60 a. 5 obj. 4; q. 61 a. 1 ad 1, a. 2 ad 2, a. 3 (whole), a. 4 obj. 2 and ad 2; q. 62 a. 3 obj. 1, s.c., co., ad 1; q. 63 a. 1 ad 4, a. 2 s.c., a. 5 obj. 2, co., ad 1–2, a. 6 co., a. 7 co., a. 9 ad 3; q. 64 a. 1 obj. 3–5, ad 4–5, a. 4 s.c.; q. 108 a. 1 co., a. 5 ad 1 (Latin), a. 6 co. (English and Latin), a. 8 (whole); q. 109 a. 4 s.c. (English and Latin); q. 110 a. 1 s.c. and co., a. 2 s.c. (Latin), a. 3 s.c., a. 4 obj. 2–3; q. 114 a. 4 s.c., co., ad 2–3.
- Quoted: q. 61 a. 3 co. (`The more probable`; `is not to be deemed erroneous`; `In the beginning`/`In the Son`); q. 62 a. 3 co. (`more probable, and more in keeping with the sayings of holy men`); q. 63 a. 1 ad 4 (`not according to proper measure or rule`), a. 5 co. (`was reasonably rejected by the masters as erroneous`), a. 6 co. (`more probable`), a. 9 ad 3 (`just as men are taken up into every order to supply for the angelic ruin`); q. 54 a. 5 co. (`often makes use of this opinion in his books, although he does not mean to assert it`); q. 61 a. 4 obj. 2 (`upper atmosphere`); Latin q. 108 a. 5 ad 1 (`Angelus nuntius dicitur`).
- Rights: public domain.
- Ceiling: web transcriptions. New Advent's locus labels for Augustine are sometimes wrong (see Open issues); the Leonine labels were checked where they differ.

### Denzinger, Lateran IV, Firmiter (DS 800)
- Witness: Denzinger, *Enchiridion symbolorum*, as transcribed at patristica.net.
- Repository ids: `work.fourth-lateran-council.firmiter-credimus` (existing); `work.denzinger.enchiridion-symbolorum` (existing).
- URL: https://patristica.net/denzinger/enchiridion-symbolorum.html
- Retrieved: 2026-09-29T12:56:36Z
- SHA-256 of the bytes read: 604f24c46e0bc71c2018f25dc787a9ab421d4b2e9cf7d1cee1f43e910ef2708f (2333435 bytes)
- Loci read: DS 800 (old 428) in full.
- Quoted: `simul ab initio temporis utramque de nihilo condidit creaturam, spiritualem et corporalem, angelicam videlicet et mundanam`. The devil's creation in goodness (same locus) is paraphrased, not quoted.
- Rights: public domain Latin conciliar text.
- Ceiling: web transcription of Denzinger.

### Catechism of the Catholic Church (English)
- Witness: CCC, English, vatican.va archive.
- Repository ids: `work.catholic-church.catechism` (existing).
- URL: https://www.vatican.va/archive/ENG0015/__P1A.HTM ; https://www.vatican.va/archive/ENG0015/__P1C.HTM
- Retrieved: 2026-09-29T12:56:38Z; 2026-09-29T13:10:40Z
- SHA-256 of the bytes read: f5d0972215f47a1bc22e768aa4e51f454db80f32dcbc4e3dd52b4a40ae5254d3 (22605 bytes); 3ce4c15f4bdb2cccf0dd788c1ddbe25a7eee2b8c1b35ecb60aa07d509b30c153 (33151 bytes)
- Loci read: 328–336; 391–395.
- Quoted: 329 (Augustine's sentence as the Catechism renders it); 330 (`purely spiritual creatures`); 332 (`communicated the law by their ministry`); 393 (`There is no repentance for the angels after their fall`). 335 paraphrased.
- Rights: Libreria Editrice Vaticana copyright; short quotations with attribution.
- Ceiling: official web text.

### Paul VI, Solemni hac liturgia (Credo of the People of God)
- Witness: Paul VI, motu proprio *Solemni hac liturgia*, 30 June 1968, English, vatican.va.
- Repository ids: `work.paul-vi.solemni-hac-liturgia` (existing).
- URL: https://www.vatican.va/content/paul-vi/en/motu_proprio/documents/hf_p-vi_motu-proprio_19680630_credo.html
- Retrieved: 2026-09-29T13:10:44Z
- SHA-256 of the bytes read: 8108a76f218bc8f70f8dbefd1606d070de70506467abeb287cde6ddcfcec6598 (58147 bytes)
- Loci read: n. 23.
- Quoted: n. 23 (`the sole mediator and way of salvation`).
- Rights: Vatican copyright; short quotation with attribution.
- Ceiling: official web text.

### Directory on Popular Piety and the Liturgy (2001)
- Witness: Congregation for Divine Worship and the Discipline of the Sacraments, *Directory on Popular Piety and the Liturgy*, English, vatican.va.
- Repository ids: `work.congregation-for-divine-worship-and-the-discipline-of-the-sacraments.directory-on-popular-piety-2001` (registered with this publication).
- URL: https://www.vatican.va/roman_curia/congregations/ccdds/documents/rc_con_ccdds_doc_20020513_vers-direttorio_en.html
- Retrieved: 2026-09-29T12:56:46Z
- SHA-256 of the bytes read: a9d30018f650a6854f3f13d3691a068a6519c2ebdb8d1fc9a2418ad13b90ed38 (531807 bytes)
- Loci read: nn. 213–217.
- Quoted: n. 215 (`has recourse to their prompt intercession`); the preceding words are paraphrased because the web text misprints "spirts".
- Rights: Vatican copyright; short quotation with attribution.
- Ceiling: official web text.

### Douay–Rheims Bible (Challoner)
- Witness: Project Gutenberg eBook 1581.
- Repository ids: `edition.english-college-of-douay.douay-rheims-bible.challoner-gutenberg-1581` (existing); `work.english-college-of-douay.douay-rheims-bible` (existing).
- URL: https://www.gutenberg.org/cache/epub/1581/pg1581.txt
- Retrieved: 2026-09-29T12:58:58Z
- SHA-256 of the bytes read: 7d10da78d8ec97db53b4e2bd8719cc01e16106b44937a673ba34aa534a04c007 (5880580 bytes)
- Loci read: every verse in the Scripture table below that the body quotes in its own voice.
- Quoted: Ps 103:4; Rom 11:34; 2 Pet 2:4; John 8:44; Gen 1:31 (phrase); Matt 25:41 (phrase); 1 Tim 6:10 (phrase); Exod 8:19 (phrase); Heb 1:14; Gal 3:19 (phrase); Acts 7:53 (phrase); Eph 3:10 (phrase); Col 1:16 (phrase); Zach 1:9 (phrase); Luke 20:36 (phrase); Apoc 19:10 (two phrases); Mark 1:24; 1 Cor 8:1; Gen 6:2. Scripture inside quoted Augustine keeps the NPNF translator's wording.
- Rights: public domain.
- Ceiling: Gutenberg transcription.

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

## Gregory the Great, Isidore, and Bede

### Gregory the Great, Homiliae XL in Evangelia (Latin)
- Witness: Gregory the Great, *Homiliae in Evangelia*, Latin text transcribed on Latin Wikisource (print base not identified by Wikisource), checked against H. Hurter, *Sanctorum Patrum opuscula selecta*, series altera, t. VI (Innsbruck: Wagner, 1892), archive.org OCR.
- Repository ids: `work.gregory-the-great.homiliae-in-evangelia` (existing).
- URL: https://la.wikisource.org/w/index.php?title=Homiliarum_in_Evangelia/I-VIII&action=raw ; .../I-X ; .../XXIX ; .../XXXIV (also .scratch/aquinas-ministry/gregory-34.txt, EPUB-derived); Hurter: https://archive.org/download/sanctigregoriim00igoog/sanctigregoriim00igoog_djvu.txt
- Retrieved: 2026-09-30T14:47Z (Wikisource); 2026-09-29T13:48:47Z (Hurter)
- SHA-256 of the bytes read: d11ae8b729f667794b6719fa6504d74fd8a4c392d62b5f61330b9ad584e46a52 (5719 bytes); 4eb8d78cd432816ff08b76b2549b6015fe29637307a22ee1d7ba79884d68e2f1 (701111 bytes)
- Loci read: Hom. 8 (whole); 10.1; 29.1--10 (whole homily scanned; 29.2, 29.5, 29.9 read closely); 34.1--18 (whole). Hurter OCR compared at 8.2, 34.4--8, 34.11--15.
- Quoted: 8.1, 8.2 (four passages); 10.1; 29.2; 29.9; 34.3 (four phrases); 34.6 (two); 34.7 (four); 34.8 (three); 34.9 (three); 34.10 (six); 34.11 (four, incl. Deut 32:8 as Gregory reads it); 34.12 (four); 34.13 (four); 34.14 (five); 34.15. All English renderings of the Latin are this lane's own close paraphrases (marked as such in the section's first footnote), not a published translation.
- Rights: Latin text public domain; renderings are lane-authored.
- Ceiling: web transcription of unidentified print base; spot-collated with Hurter OCR (agreement at every quoted phrase checked, incl. "cuncta ibi singulorum sunt"); editorial Scripture/source parentheses of the web text (e.g. "(De Coel. Hierarch. cap. 7, 9, 13)" in 34.12) are omitted from quotations without ellipsis; PL 76 not checked (see Open issues).

### Gregory the Great, Moralia in Iob (English, Library of the Fathers)
- Witness: *Morals on the Book of Job by S. Gregory the Great*, Library of the Fathers 18, 21, 23, 31 (Oxford: Parker, 1844--1850): vol. I (Books I--X), vol. II (XI--XXII), vol. III pt 1 (XXIII--XXIX), vol. III pt 2 (XXX--XXXV); Books XXXII and XXXIV also in the lectionarycentral.com transcription of the same translation.
- Repository ids: `work.gregory-the-great.moralia-in-iob` (registered with this publication).
- URL: https://archive.org/download/moralsonbookofj01greg/moralsonbookofj01greg_djvu.txt ; https://archive.org/download/21ALibraryOfFathersOfTheHolyCatholicV21/21ALibraryOfFathersOfTheHolyCatholicV21_djvu.txt ; https://archive.org/download/23ALibraryOfFathersOfTheHolyCatholicV23/23ALibraryOfFathersOfTheHolyCatholicV23_djvu.txt ; https://archive.org/download/31ALibraryOfFathersOfTheHolyCatholicV31/31ALibraryOfFathersOfTheHolyCatholicV31_djvu.txt ; https://www.lectionarycentral.com/GregoryMoralia/Book32.html ; .../Book34.html
- Retrieved: 2026-09-29T17:54:46Z (vol. I); 2026-09-29T13:13:13Z (vol. II); 2026-09-30T14:47:14Z (III.1); 2026-09-30T14:47:08Z (III.2); 2026-09-29T17:51Z (lectionarycentral)
- SHA-256 of the bytes read: 96e0f3706c7a9a427bb3dffa578be87bd66ac96617fc90a7266ce7f241264ad2 (1806303 bytes); f13861be5715cabe5283d5bd7f38cb35c2a1332bd6dc04cf049475b88da5c493 (1916422 bytes); 84884416006c106a32ef20b8a574d9c06b1ce7db6b4814a73397d25c0356c824 (1027584 bytes); e57596ba2cedfc47ab9ff599c660b172262d9e25c33782c87419544a925f32be (2108312 bytes); 426a7d69992a5e03be469291433c135f5520e125db35b53f65d850b927b4dbef (153054 bytes); 01cd003e8190bffcb1c6a15e2cff7cde9c3f0a484c881c9627a3a7bbe5fa637a (139202 bytes)
- Loci read: Epistle to Leander (opening and note); II.1--12; IV.3.8--IV.7.12; IV.29.55; V.38.68--69; XVII.12.15--XVII.16.22; XXVIII.14.34--XXVIII.15.35; XXXII.22.45--XXXII.24.51; XXXIV.6--XXXIV.7.16; XXXIV.19.38--XXXIV.23.47; index s.v. Isidore (vol. III.2).
- Quoted: II.3.3 (block and three phrases); II.4.4; II.4.5; IV.3.8 (three phrases); IV.7.12; IV.29.55 (four phrases); V.38.68 (block, one phrase); XVII.12.17 (block, one phrase); XVII.13.18 (two); XVII.13.19; XXVIII.14.34 (three); XXXII.23.47 (block, four phrases); XXXII.23.48 (block, eight phrases); XXXII.23.49; XXXII.24.50 (two); XXXIV.7.12 (block); XXXIV.7.13; XXXIV.20.39; XXXIV.21.40 (block, one phrase); XXXIV.23.47.
- Rights: public domain (1844--1850).
- Ceiling: archive.org OCR, silently corrected for evident scanning errors ("tlie" > "the", "hght" > "light", "}" > "?", superscript/marginal debris removed); lectionarycentral transcription collated against the LF 31 scan at XXXII.23.47--48, XXXIV.7.12--13, XXXIV.23.47 (agreement). Chapter numbers taken from the LF marginal chapter marks; the speech passage (II.7.8--12) was read but not quoted because its chapter division is not legible in the OCR. Latin Moralia not read.

### Gregory the Great, Dialogues IV (English)
- Witness: *The Dialogues of Saint Gregory ... Translated into our English Tongue by P.W. and printed at Paris in 1608*, re-edited by Edmund G. Gardner (London: Philip Lee Warner, 1911), Book IV, pp. 177--258, transcribed by Roger Pearse (2004) at tertullian.org.
- Repository ids: `work.gregory-the-great.dialogi` (registered with this publication).
- URL: https://www.tertullian.org/fathers/gregory_04_dialogues_book4.htm ; edition details from https://www.tertullian.org/fathers/gregory_00_dialogues_intro.htm
- Retrieved: 2026-09-30T14:22:02Z (Book IV cache); intro page read by WebFetch 2026-09-30.
- SHA-256 of the bytes read: c0fcbac5f0d6cbf6a192398f793368cf85d2e26253db4a40d0edd116c43698b1 (202560 bytes)
- Loci read: IV.1--20; 25--29; 36--38; 58--59; editor's notes 1--23, 83--89.
- Quoted: IV.1 (three phrases); IV.3; IV.5 (two); IV.7; IV.14 (two); IV.15 (three); IV.19 (two); IV.29; IV.36 (three); IV.58 (block).
- Rights: public domain (1608 translation; 1911 edition; transcription declared public domain).
- Ceiling: web transcription, not collated with the 1911 print; chapter numbers are the 1911 edition's (Aquinas, ST I q. 110 a. 1 s.c., cites the IV.5 passage as "Dial. iv, 6"); Latin not read.

### Isidore of Seville, Etymologiae VII.5 (Latin)
- Witness: Isidore, *Etymologiarum sive Originum liber VII*, ch. 5 "De angelis", The Latin Library transcription.
- Repository ids: `work.isidore.etymologiae` (existing).
- URL: https://www.thelatinlibrary.com/isidore/7.shtml
- Retrieved: 2026-09-29T17:50:49Z
- SHA-256 of the bytes read: 44312348f815c0af0ed00ecb532cbe327d3dc6a50f32ef78726b3d8abe37b150 (80402 bytes)
- Loci read: VII.1 (opening), VII.5.1--33 (whole chapter), VII.8.22.
- Quoted: VII.5.1--2 (block); 5.4; 5.6; 5.8; 5.10--11 (two phrases); 5.12; 5.15 (gloss); 5.24; 5.23; 5.28 (two); 5.29; 5.31 (block); 5.33; Gen 1:6, 8 as Isidore cites it.
- Rights: public domain Latin; English renderings lane-authored.
- Ceiling: web transcription; print base (presumably Lindsay 1911) not verified; the site's orthography (V for initial U) kept where quoted.

### Isidore of Seville, Sententiae I.10 (Latin)
- Witness: Isidore, *Sententiarum libri tres* I.10 "De angelis", Arevalo's text (Rome 1797--1803) in Migne, PL 83 (Paris), two archive.org scans (patrologiae83unknuoft; bim ... 1850_83).
- Repository ids: `work.isidore.sententiae` (registered with this publication).
- URL: https://archive.org/download/patrologiae83unknuoft/patrologiae83unknuoft_djvu.txt ; https://archive.org/download/bim_early-english-books-1641-1700_1850_83/bim_early-english-books-1641-1700_1850_83_djvu.txt
- Retrieved: 2026-09-30T14:47:25Z; 2026-09-30T14:50:58Z
- SHA-256 of the bytes read: e59b2eb652ece1ccf2f4cea6c0a35112dff950a7868c7e97034ee25ede7c0930 (5023656 bytes); 9201ea42ceb36f1bfca2e1ffe9c1719326a650fc5b9f8e4ce1e208d78f07cc9c (4053165 bytes)
- Loci read: I.10.1--29 (PL 83, 553--560) with the notes of Loaisa and Arevalo (sources in Gregory Hom. 34, Moralia V, XXVIII, Augustine).
- Quoted: I.10.2 (three phrases); 10.3; 10.4; 10.13; 10.14 (block); 10.16; 10.17; 10.19; 10.20; 10.24; 10.26.
- Rights: public domain.
- Ceiling: Latin reconstructed from two poor OCR scans read against each other (normalized to Migne orthography: coelum, charitas, j); no page-image check; column range approximate from running heads.

### Bede, In Lucae evangelium expositio I (Latin)
- Witness: Bede, *In Lucae evangelium expositio*, book I, in Migne, PL 92 (Paris, 1850), archive.org OCR.
- Repository ids: `work.bede.in-lucae-evangelium-expositio` (existing).
- URL: https://archive.org/download/bim_early-english-books-1641-1700_1850_92/bim_early-english-books-1641-1700_1850_92_djvu.txt
- Retrieved: 2026-09-30T14:47:37Z
- SHA-256 of the bytes read: 891f98ed5b5ee2ed3c71bcef4ad32ea67580e71e01e9ac2654fbbc5296a3e550 (3120643 bytes)
- Loci read: on Luke 1:5--28 (PL 92, 313--318); on Luke 2:8--14 (PL 92, 332--334).
- Quoted: on Luke 1:26 (two phrases, PL 92, 315--316); on Luke 2:13--14 (block and three phrases, PL 92, 333).
- Rights: public domain; renderings lane-authored.
- Ceiling: reconstructed from OCR (single scan); wording identical to Gregory Hom. 34.8--9 where Bede copies it, which confirms the reconstruction there.

### Bede, Homiliae evangelii I.1 (Latin)
- Witness: Bede, homily "In festo Annuntiationis beatae Mariae" (PL numbering Hom. I.1, "Homiliae genuinae"), Migne, PL 94 (Paris, 1850), archive.org OCR.
- Repository ids: `work.bede.homiliae-evangelii` (registered with this publication).
- URL: https://archive.org/download/bim_early-english-books-1641-1700_1850_94/bim_early-english-books-1641-1700_1850_94_djvu.txt
- Retrieved: 2026-09-30T14:47:33Z
- SHA-256 of the bytes read: eb888073ed25a141a81b55c90bc447e829babb03ab702a76171633012aadfec5 (3827054 bytes)
- Loci read: PL 94, 9--12 (homily opening through the Ave); also PL 94 Hom. "In feria IV Quatuor Temporum" (Gregory 34.8--9 copied) noted, not used.
- Quoted: PL 94, 9 (block); 9--10 (two phrases).
- Rights: public domain; renderings lane-authored.
- Ceiling: reconstructed from interleaved two-column OCR; CCSL numbering (I.3) not verified.

### Bede, Explanatio Apocalypsis (English)
- Witness: *The Explanation of the Apocalypse by Venerable Beda*, trans. Edward Marshall (Oxford and London: James Parker, 1878), archive.org OCR; Fordham Medieval Sourcebook page (preface only).
- Repository ids: `work.bede.explanatio-apocalypsis` (registered with this publication).
- URL: https://archive.org/download/explanationapoc00bedegoog/explanationapoc00bedegoog_djvu.txt ; https://sourcebooks.web.fordham.edu/source/bede-apoc.asp
- Retrieved: 2026-09-30T14:49:33Z; 2026-09-30T14:47:20Z
- SHA-256 of the bytes read: 738afa825b4646d27ad35508904a679993301c51b97f4842bc7f410ebb7b72a6 (364008 bytes); 840e32eb2c7a02b0b7d09eefee0de06908afec03fe9249024c543dd26a98bf80 (37752 bytes)
- Loci read: book II on Apoc 7:11--13, 12:1--14; book III on 19:9--11, 22:8--10.
- Quoted: on 12:7 (block); on 12:7 (lemma "fought", one phrase); on 12:10; on 12:12; on 19:10.
- Rights: public domain (1878).
- Ceiling: OCR corrected for evident errors ("jmned" > "joined", "citizensi" > "citizens,"); Latin (PL 93, cached as ia-pl93-bede.txt) not collated.

### Bede, Historia ecclesiastica gentis Anglorum (English)
- Witness: *Bede's Ecclesiastical History of England*, a revised translation by A. M. Sellar (London: George Bell, 1907), incl. Sellar's Life of Bede and Cuthbert's letter on Bede's death; Project Gutenberg eBook 38326.
- Repository ids: `work.bede.historia-ecclesiastica-gentis-anglorum` (registered with this publication).
- URL: https://www.gutenberg.org/cache/epub/38326/pg38326.txt
- Retrieved: 2026-09-30T14:47:15Z
- SHA-256 of the bytes read: 977da0babf070c825befb0a5db65a9cc2440d9ab45aa869a959c1bab911be2c8 (1093654 bytes)
- Loci read: Life of Bede (dates; Cuthbert's letter); II.1; III.8; III.19; IV.3; IV.23; V.12; V.13; V.14; V.19; notes 332--333, 547, 706, 926.
- Quoted: Cuthbert's letter (two phrases); II.1 (two); III.8 (two); III.19 (six); IV.3 (block, three phrases); IV.23 (two); V.12 (four); V.13 (three); V.19.
- Rights: public domain in the US (1907); translator's death date not verified for life+70 jurisdictions.
- Ceiling: e-text of the 1907 print, not collated with page images; Latin (Plummer) not read (thelatinlibrary URLs 404).

### Rabanus Maurus, De universo I.5 (Latin)
- Witness: Rabanus Maurus, *De universo libri XXII*, I.5 "De angelis", Migne, PL 111 (Paris, 1852; running head OCR "CXIl"), archive.org OCR.
- Repository ids: `work.rabanus-maurus.de-universo` (registered with this publication).
- URL: https://archive.org/download/bim_early-english-books-1641-1700_patrologiae-cursus-completus-_1852_111/bim_early-english-books-1641-1700_patrologiae-cursus-completus-_1852_111_djvu.txt
- Retrieved: 2026-09-30T14:47:28Z
- SHA-256 of the bytes read: 388452e9eac45018b493be159eeaa67fff350b298b2682db021e5bf80abe5bf2 (4995841 bytes)
- Loci read: I.5 whole (PL 111, c. 27--32); title page.
- Quoted: I.5 (Gregory's sentence "Sed quid prodest..."; "Quod nomen non per naturam, sed per officium ministrationis sortiti sunt").
- Rights: public domain.
- Ceiling: OCR; "Quod" reconstructed from "Quo"; column range approximate.

### Thomas Aquinas, Summa theologiae (English and Latin)
- Witness: *Summa theologiae*, Fathers of the English Dominican Province, 2nd rev. ed. 1920, New Advent.
- Repository ids: `work.thomas-aquinas.summa-theologiae` (existing).
- URL: https://www.newadvent.org/summa/1050.htm ... 1064.htm, 1106.htm ... 1114.htm
- Retrieved: 2026-09-29 (manifest, e.g. 1108 at 12:54:13Z)
- Loci read: I q. 51 aa. 1--2; q. 54 a. 5; q. 58 a. 3; q. 61 a. 3; q. 62 a. 8; q. 63 aa. 2--3, 7; q. 64 aa. 2, 4; q. 106 a. 3; q. 108 aa. 5--8; q. 109 a. 4; q. 110 aa. 1, 4; q. 111 a. 2; q. 112 aa. 1--4; q. 113 aa. 3, 8; name counts over I qq. 50--64, 106--114 (Gregory 52, Augustine 110, Damascene 18, Jerome 9, Isidore 4, Ambrose 3, Bede 1).
- Quoted: q. 51 a. 1 ad 2; q. 58 a. 3 ad 3; q. 51 a. 2 ad 3; q. 63 a. 7 (s.c. paraphrase, co. "the more probable view", ad 1); q. 64 a. 2 ad 4; q. 108 a. 5 co. and ad 3 (paraphrase), a. 6 co. (three phrases), a. 8 co.; q. 111 a. 2 obj. 2; q. 112 a. 2 s.c. and co.; a. 3 obj. 1, ad 3; q. 113 a. 3 co., a. 8 co.
- Rights: public domain translation.
- Ceiling: New Advent presentation; the English edition misprints Gregory's homily as "Hom. xxiv" in q. 108; Latin not consulted for these loci.

### Douay--Rheims Bible (Challoner), with notes
- Witness: Douay--Rheims (Challoner revision), Project Gutenberg eBook 1581.
- Repository ids: `work.english-college-of-douay.douay-rheims-bible` (existing); `edition.english-college-of-douay.douay-rheims-bible.challoner-gutenberg-1581` (existing).
- URL: https://www.gutenberg.org/cache/epub/1581/pg1581.txt
- Retrieved: 2026-09-29T12:58:58Z
- SHA-256 of the bytes read: 7d10da78d8ec97db53b4e2bd8719cc01e16106b44937a673ba34aa534a04c007 (5880580 bytes)
- Loci read: all verses listed under Scripture cited; notes on Ezek 28:12 and Apoc 19:10.
- Quoted: Luke 15:10; Ezek 28:12, 13; Eph 1:21; Col 1:16; Ps 103:4; Isa 14:13--14; Apoc 12:7; Ps 23:8, 10; Ps 9:5; Deut 32:8; Exod 7:1; Rom 13:10; Isa 6:6--7; Dan 7:10; Zach 2:3--4; Ps 79:2; Apoc 22:9; Job 1:6; 4:18; 25:2, 3; 40:14; 41:16, 24, 25; Dan 10:13; 12:1; Matt 18:10; Acts 12:15; Heb 1:14 (as quoted by Gregory/Isidore); Mal 3:1; Job 41:16; notes on Ezek 28:12 and Apoc 19:10.
- Rights: public domain.
- Ceiling: e-text; not collated with print.

### Catechism of the Catholic Church
- Witness: CCC (English, vatican.va), Part One, section on heaven and earth.
- Repository ids: `work.catholic-church.catechism` (existing).
- URL: https://www.vatican.va/archive/ENG0015/__P1A.HTM
- Retrieved: 2026-09-29T12:56:38Z
- SHA-256 of the bytes read: f5d0972215f47a1bc22e768aa4e51f454db80f32dcbc4e3dd52b4a40ae5254d3 (22605 bytes)
- Loci read: 329--336.
- Quoted: none verbatim beyond the single words "angel"/"spirit" (CCC 329); 332, 333, 335, 336 cited by paraphrase.
- Rights: Vatican copyright; no extended quotation.
- Ceiling: official web text.

### Directory on Popular Piety and the Liturgy (2001)
- Witness: Congregation for Divine Worship and the Discipline of the Sacraments, *Directory on Popular Piety and the Liturgy* (Vatican City, December 2001), English, vatican.va.
- Repository ids: `work.congregation-for-divine-worship-and-the-discipline-of-the-sacraments.directory-on-popular-piety-2001` (registered with this publication).
- URL: https://www.vatican.va/roman_curia/congregations/ccdds/documents/rc_con_ccdds_doc_20020513_vers-direttorio_en.html
- Retrieved: 2026-09-29T12:56:46Z
- SHA-256 of the bytes read: a9d30018f650a6854f3f13d3691a068a6519c2ebdb8d1fc9a2418ad13b90ed38 (531807 bytes)
- Loci read: 215--217; title page.
- Quoted: none (no. 217 paraphrased).
- Rights: Vatican copyright; paraphrase only.
- Ceiling: official web text.

### Catholic Encyclopedia, "Dionysius the Pseudo-Areopagite" (Stiglmayr, 1909)
- Witness: J. Stiglmayr, "Dionysius the Pseudo-Areopagite", *Catholic Encyclopedia* V (1909), New Advent.
- Repository ids: `work.catholic-encyclopedia.volume-5` (existing).
- URL: https://www.newadvent.org/cathen/05013a.htm
- Retrieved: 2026-09-29T13:10:56Z
- SHA-256 of the bytes read: a704ad6ccc98d22749dce0515c081c40a973bcd67993a0db3ad872c9c5aa3433 (61832 bytes)
- Loci read: paragraphs on Michael II's gift (827), Hilduin, Eriugena (c. 858, for Charles the Bald).
- Quoted: none.
- Rights: public domain.
- Ceiling: finding aid for one historical fact in the Rabanus subsection; no position attributed from it.

## The medieval Doctors to Peter Lombard; comparative orderings

### Anselm, De casu diaboli (PL 158)
- Witness: Anselm of Canterbury, *De casu diaboli*, Gerberon's text as reprinted in Migne, PL 158:325–360 (page images of the Migne volume as served by Documenta Catholica Omnia); archive.org OCR of PL 158 (patrologiaecursu0158mign_f7g5) for location; F. S. Schmitt's text (Edinburgh 1946) at logicmuseum.com read as a finding aid only.
- Repository ids: `work.anselm-of-canterbury.de-casu-diaboli` (registered with this publication).
- URL: http://www.documentacatholicaomnia.eu/02m/1033-1109,_Anselmus_Cantuariensis,_De_Casu_Diaboli,_MLT.pdf ; https://archive.org/download/patrologiaecursu0158mign_f7g5/patrologiaecursu0158mign_f7g5_djvu.txt ; https://www.logicmuseum.com/wiki/Authors/Anselm/de_casu
- Retrieved: 2026-09-30 (DCO, archive.org); 2026-09-29 (logicmuseum)
- SHA-256 of the bytes read: fe79468c7052228d498bec193f97c0d58f02dab8794dd0c6eb65746560af4d05 (6778 bytes); 90c8383a5312d57171dbb9020ac0095d433952ccb805ed2bb70753c51241640f (3653321 bytes); 289e187e37b0d9cc4428483a07db50be6cf58b5ab46aba8cdc1a0cb283206bf0 (115975 bytes)
- Loci read: cc. 1–28 entire (Schmitt); PL cols 331–336, 341–350, 355–360 on page images
- Quoted: c. 3 (col. 331, "sponte dimisit voluntatem quam habebat"); c. 4 (col. 333, three passages); c. 6 (col. 334, two); c. 14 (col. 346); c. 17 (col. 349); c. 18 (col. 350); c. 24 PL division = c. 25 Schmitt (col. 357); c. 27 (col. 360)
- Rights: Migne 1853 public domain; Schmitt 1946 text not quoted (in copyright).
- Ceiling: every Latin quotation checked against the Migne page image; not collated with Schmitt except where noted (PL c. 4 reads "ad augmentum beatitudinis esse illi poterat", Schmitt "ad augmentum ibi beatitudinis esse poterat"; PL ends c. 24 with the "praemium justitiae" sentence that Schmitt prints in c. 25). Chapters cited by Migne's numbering.

### Anselm, Cur Deus homo I.16–18 (Deane 1903)
- Witness: Anselm, *Cur Deus homo*, tr. Sidney Norton Deane, *St. Anselm: Proslogium; Monologium; … and Cur Deus Homo* (Chicago: Open Court, 1903), pp. 210–222.
- Repository ids: `work.anselm-of-canterbury.cur-deus-homo` (registered with this publication).
- URL: https://archive.org/download/stanselmeproslog00anseuoft/stanselmeproslog00anseuoft_djvu.txt
- Retrieved: 2026-09-30T14:58:11Z
- SHA-256 of the bytes read: 5a578093b4b8c6a8042b8d695bda68df4e22d112f1774590c552d6851fee976a (642892 bytes)
- Loci read: I.16, I.17, I.18, I.19 (opening)
- Quoted: I.16 (one passage), I.17 (two), I.18 (three short passages)
- Rights: published Chicago 1903; public domain in the US (pre-1931).
- Ceiling: archive.org OCR of the printed volume; wording checked by reading; not compared with page images; Latin (PL 158:359–432) not collated.

### Bernard, De consideratione V (PL 182; Lewis 1908)
- Witness: Bernard of Clairvaux, *De consideratione* V.3.6–5.12: Latin PL 182:791–795 (DCO page images; archive.org OCR patrologiaecursu0182mign); English, George Lewis, *St. Bernard On Consideration* (Oxford: Clarendon Press, 1908), pp. 135–144.
- Repository ids: `work.bernard-of-clairvaux.de-consideratione` (registered with this publication).
- URL: http://www.documentacatholicaomnia.eu/02m/1090-1153,_Bernardus_Claraevallensis_Abbas,_De_Consideratione_Libri_Quinque_Ad_Eugenium_Tertium,_MLT.pdf ; https://archive.org/download/onconsideration00bern/onconsideration00bern_djvu.txt
- Retrieved: 2026-09-30
- SHA-256 of the bytes read: 83f2b090410f16d495b1e83878b5cff5c07b7a8bd4f931e2b47f80b59d1c0655 (7064 bytes); 57e5cb80e805369053a638f31e47e7f4ef94dcf488c1983c226814f727e2b970 (3621335 bytes); 23dacc2ca0c5f0244fe9c456afbdb2a2745767b2281d7553d07899d93416f49e (306976 bytes)
- Loci read: V.3.5–6.13 (Lewis); PL cols 791–796 on page images
- Quoted: English V.3.6, V.4.7 (block and three phrases), V.4.8 (seven phrases), V.4.9 (two), V.4.10 (two plus block), V.5.11, V.5.12 (two); Latin V.4.8 (col. 792, Thrones), V.5.11 (col. 795, "Adsunt Angeli…"), V.5.12 (col. 795, two sentences)
- Rights: Lewis 1908, public domain (US; pre-1931). Migne public domain.
- Ceiling: Lewis's section numbers are printed "4." for PL 7 (OCR or printing); loci cited in PL numbering. Latin checked on page images at 60 dpi, legible.

### Bernard, Sermons on Psalm 90 (Qui habitat) 11–13 (PL 183; Mount Melleray 1921)
- Witness: Latin PL 183:225–236 (DCO page images; archive.org OCR patrologiaecursu0183mign); English, *St. Bernard's Sermons for the Seasons & Principal Festivals of the Year*, tr. a Priest of Mount Melleray, vol. 1 (Dublin: Browne and Nolan, 1921), pp. 231–260.
- Repository ids: `work.bernard-of-clairvaux.sermones-in-psalmum-qui-habitat` (registered with this publication).
- URL: http://www.documentacatholicaomnia.eu/02m/1090-1153,_Bernardus_Claraevallensis_Abbas,_Sermones_De_Tempore._In_Psalmum_XC,_MLT.pdf ; https://archive.org/download/stbernardssermon0001prie_y4z3/stbernardssermon0001prie_y4z3_djvu.txt
- Retrieved: 2026-09-30
- SHA-256 of the bytes read: 937b7aae2d2821a3c9cc562dcd1995394d072dc94466347bbdd07011d0effba4 (7766 bytes); 449957346cf138812697c9f27b12dfec40b699b327b0b00ddb937fbdae61b39a (4127764 bytes); a66ad9a360627d988ff526cf20de3615d4b67c7c82157f69ff51340a84d1263e (807286 bytes)
- Loci read: serm. 11 entire; serm. 12 entire; serm. 13.1–3 (English); PL cols 225–236 (page images of 225–226, 233–236)
- Quoted: English 11.4, 11.6 (block), 12.3, 12.4 (two), 12.6 (three), 12.7 (three), 12.10, 13.1 (two); Latin 12.6 (col. 233, block), 12.8 (col. 234), 12.10 (col. 235)
- Rights: 1921 Dublin publication, anonymous translator; public domain in the US (pre-1931); EU/Irish status depends on the translator's identity (not established). Quotations kept focused.
- Ceiling: English from archive.org OCR, read; Latin checked on page images; section numbers from PL.

### Bernard, Sermons for the feast of St Michael 1–2 (PL 183; Mount Melleray 1925)
- Witness: Latin PL 183:447–454 (DCO page images; archive.org OCR); English, *St. Bernard's Sermons for the Seasons*, vol. 3 (Dublin, 1925), pp. 315–329.
- Repository ids: `work.bernard-of-clairvaux.sermones-in-festo-sancti-michaelis` (registered with this publication).
- URL: http://www.documentacatholicaomnia.eu/02m/1090-1153,_Bernardus_Claraevallensis_Abbas,_Sermones_De_Sanctis._In_Festo_Sancti_Michaelis,_MLT.pdf ; https://archive.org/download/stbernardssermon0003prie_s9b1/stbernardssermon0003prie_s9b1_djvu.txt
- Retrieved: 2026-09-30
- SHA-256 of the bytes read: 1c0bfe0eff6719fa2cf3beefaaee22676c1049ac38e05d77612440b200f5bc57 (7294 bytes); b216b78d046e34fe56d463bf53eb6ca48a7dd8c7be7a1c08ccca2b39180df89a (964870 bytes)
- Loci read: serm. 1 entire, serm. 2 entire (English); PL col. 449 on page image; cols 447–452 in OCR
- Quoted: English 1.1, 1.2 (three), 1.3 (three), 1.5 (two); Latin 1.4 (col. 449)
- Rights: as for the Mount Melleray volume 1 (1925; US public domain).
- Ceiling: section numbers from PL OCR (1.4 funiculus triplex; 1.5–6 concord and discord; 2.2 three reasons).

### Bernard, Sermons on the Song of Songs 5, 7, 19, 27 (Eales 1896)
- Witness: *Life and Works of Saint Bernard*, ed. Mabillon, tr. Samuel J. Eales, vol. 4, *Cantica Canticorum* (London: John Hodges, 1896).
- Repository ids: `work.bernard-of-clairvaux.sermones-super-cantica-canticorum` (registered with this publication).
- URL: https://archive.org/download/LifeWorksOfSBernardClairvauxV4/LifeWorksOfSBernardClairvauxV4_djvu.txt (also DCO PDF of PL 183:785–1198 fetched, not used for quotation)
- Retrieved: 2026-09-30T14:58:08Z
- SHA-256 of the bytes read: 26d3f6378ee7b171dc0d6e4c0be0de6d7eedc27a813c296a1dea9b4283b4e287 (2087239 bytes); 05a4ae4546150b33e035d9900b9d393812df00896ca0a2ac92f6321787694964 (7009 bytes)
- Loci read: serm. 5 entire; 7.1–7; 19 entire; 27.1–10
- Quoted: 5.2, 5.4, 5.7, 5.8; 7.4 (three); 19.2–7 (seven, one block); 27.5 (two); 27.6 (block)
- Rights: 1896, public domain.
- Ceiling: English OCR read; Latin not collated. Eales's Psalm numbering is Hebrew; the body cites Vulgate with Hebrew in brackets. Aquinas's citation of sermon 6 (ST I q. 51 a. 1 obj. 1) reported as a claim about the Summa; sermon 6 not read.

### Hugh of St Victor, De sacramentis I.5 (PL 176)
- Witness: Hugh of Saint Victor, *De sacramentis christianae fidei* I, pars 5, cc. 1–34, PL 176:245–264 (DCO page images; archive.org OCR patrologiaecursu0176mign).
- Repository ids: `work.hugh-of-saint-victor.de-sacramentis-christianae-fidei` (registered with this publication).
- URL: http://www.documentacatholicaomnia.eu/02m/1096-1141,_Hugo_De_S_Victore,_De_Sacramentis_Christianae_Fidei,_MLT.pdf ; https://archive.org/download/patrologiaecursu0176mign/patrologiaecursu0176mign_djvu.txt
- Retrieved: 2026-09-30
- SHA-256 of the bytes read: bdff1cbacd432932a543cbeaa815a34b1abe47e7f879ecfe53dadb0390733800 (7210 bytes); 45aa2541b54393f64578761a1c3cc1a64f80575c750dc16f3bee454953348134 (3673923 bytes)
- Loci read: I.5.1–34 entire (OCR); page images of cols 247–254, 257–262
- Quoted: I.5.3 (col. 247), I.5.4 (cols 248, 249), I.5.5 (col. 249), I.5.7 (col. 250, two), I.5.8 (col. 250), I.5.10, I.5.12 (col. 251), I.5.13 (col. 252), I.5.18 (col. 253), I.5.24 (col. 257), I.5.26, I.5.27 (col. 258), I.5.30 (col. 260, block; col. 261), I.5.31, I.5.32 (col. 261)
- Rights: Migne, public domain; English glosses are the lane's own, unquoted.
- Ceiling: checked on page images; c. 28's list paraphrased because the print has a typographical error ("aus" for "aut").

### Hugh of St Victor, Commentaria in Hierarchiam caelestem VI (PL 175)
- Witness: PL 175:1037–1038 (DCO page image; archive.org OCR patrologiaecursu175mign).
- Repository ids: `work.hugh-of-saint-victor.commentaria-in-hierarchiam-caelestem` (registered with this publication).
- URL: http://www.documentacatholicaomnia.eu/02m/1096-1141,_Hugo_De_S_Victore,_Commentariorum_In_Hierarchiam_Coelestem_S_Dionysii_Areopagitae,_MLT.pdf
- Retrieved: 2026-09-30T14:56:33Z
- SHA-256 of the bytes read: 8b94178c65af38ddec2a9bd5f89ea94bc588638e67bd4313f1d29b4d7f1d2812 (7247 bytes); 2707405f16b87cf12bf9e3432922d7c75f093ba6391a55d0d3bc758b506abe3d (4568494 bytes)
- Loci read: book VI, cols 1037–1038
- Quoted: VI (col. 1038, block)
- Rights: Migne, public domain.
- Ceiling: page image at 120 dpi.

### Honorius Augustodunensis, Elucidarium (PL 172)
- Witness: *Elucidarium* I.6–11 and II.28–29, PL 172:1113–1116, 1154–1155 (DCO page images; archive.org OCR patrologiaecursu0172mign).
- Repository ids: `work.honorius-augustodunensis.elucidarium` (registered with this publication).
- URL: http://www.documentacatholicaomnia.eu/02m/1080-1137,_Honorius_Augustodunensis,_Elucidarium_Sive_Dialogus_De_Summa_Totius_Christianae_Theologiae,_MLT.pdf
- Retrieved: 2026-09-30T14:56:06Z
- SHA-256 of the bytes read: 120fff9f38815abbd8ef962b4eda31123df36db044ef40179be4edac17f0ddc7 (7067 bytes); 2ebfcb5ff3c527820036fe06be730b45d544eb1024dd5cb1980ef9c5a59444b1 (4174594 bytes)
- Loci read: I.5–11; II.28–29
- Quoted: I.6 (six short passages, col. 1113), I.7 (col. 1114), I.9, I.10 (cols 1115–1116, four), I.11, II.28 (col. 1154, block)
- Rights: Migne, public domain.
- Ceiling: page images at 60–80 dpi.

### Hildegard of Bingen, Scivias I.6 (PL 197)
- Witness: *Scivias* I, visio 6, PL 197:437–441 (DCO page images; archive.org OCR patrologiaecursu0197mign).
- Repository ids: `work.hildegard-of-bingen.scivias` (registered with this publication).
- URL: http://www.documentacatholicaomnia.eu/02m/1098-1179,_Hildegardis_(Hildegard_von_Bingen),_Scivias_Sive_Visionum_Ac_Revelationum_Libri_Tres,_MLT.pdf
- Retrieved: 2026-09-30T14:56:03Z
- SHA-256 of the bytes read: 3b891785a90d123b17a8f1827cfa01319ba52ef9dce1360d3dd8940d9c174f16 (6993 bytes); af5a03a74331e07219121e74ff58685a55d83702bfdb6044ea202a3ecbd82cd5 (4056084 bytes)
- Loci read: I.6 entire (cols 437–441)
- Quoted: col. 437 (block; two phrases), col. 438 (two), col. 440 (one)
- Rights: Migne, public domain; English glosses are the lane's own, unquoted.
- Ceiling: page images; PL prints no chapter numbers within the vision, so loci are by column.

### Peter Lombard, Sententiae II dd. 1–11 (Quaracchi 1916)
- Witness: *Libri IV Sententiarum*, 2nd ed., t. 1 (Ad Claras Aquas: Collegium S. Bonaventurae, 1916), pp. 309–357.
- Repository ids: `work.peter-lombard.sententiae` (existing).
- URL: https://archive.org/download/libriivsententia01pete/libriivsententia01pete_djvu.txt ; https://archive.org/download/libriivsententia01pete/libriivsententia01pete_bw.pdf
- Retrieved: 2026-09-29 (OCR); 2026-09-30T15:15:34Z (PDF)
- SHA-256 of the bytes read: 4cc27eb3178d204a0d8727cb8bdfad2bcd0180a1ded0b9cc9d605b33b59c4cf8 (1592526 bytes)
- Loci read: II d. 1 c. 5 – d. 12 c. 1 entire
- Quoted: d. 2 c. 1; d. 2 c. 3; d. 3 c. 1; d. 3 c. 4; d. 4; d. 5 c. 1 (block); d. 5 c. 6; d. 6 c. 1 (two); d. 7 c. 4; d. 8 c. 3; d. 9 c. 1 (two); d. 9 c. 2 (three); d. 9 c. 3; d. 9 c. 6; d. 11 c. 1 (block; Jerome); d. 11 c. 2
- Rights: 1916 edition, public domain (US; editors' text of a medieval work).
- Ceiling: every quotation checked on page images (PDF pp. 397–440 = printed pp. 313–356).

### Bonaventure, Breviloquium II.6–8 (Quaracchi 1911)
- Witness: *Tria opuscula S. Bonaventurae: Breviloquium, Itinerarium, De reductione artium*, 3rd ed. (Ad Claras Aquas, 1911), pp. 74–82.
- Repository ids: `work.bonaventure.breviloquium` (registered with this publication).
- URL: https://archive.org/download/triaopusculaseraphici3ed/triaopusculaseraphici3ed.pdf ; …_djvu.txt
- Retrieved: 2026-09-30
- SHA-256 of the bytes read: 354278e155b269ba486c804cbfee9345a2903cc8f1f10c887aff872a58d431bf (673514 bytes)
- Loci read: II.5.8 – II.9.2
- Quoted: II.6.2 (two), II.7.1, II.7.3, II.8.1 (block), II.8.2, II.8.3
- Rights: 1911, public domain.
- Ceiling: page images (PDF pp. 85, 87–89, 91).

### Thomas Aquinas, Summa theologiae I (English Dominican 1920; Leonine Latin)
- Witness: New Advent English (Fathers of the English Dominican Province, 2nd rev. ed. 1920); Corpus Thomisticum Latin for q. 108 a. 6.
- Repository ids: `work.thomas-aquinas.summa-theologiae` (existing).
- URL: https://www.newadvent.org/summa/1108.htm (and 1051, 1062, 1063, 1106, 1111, 1112, 1113 as cached); https://www.corpusthomisticum.org (cache ct-sth1103.txt)
- Retrieved: 2026-09-29
- SHA-256 of the bytes read: 5736abad11534d6a5ebb3fa0c76ff5df228d6558cbb69163f5f437523f2c2ed1 (476518 bytes)
- Loci read: q. 51 a. 1; q. 62 aa. 2, 6; q. 63 aa. 1, 3, 9; q. 106 aa. 2, 4; q. 108 aa. 4–6, 8; q. 111 a. 2; q. 112 a. 1; q. 113 aa. 1–2
- Quoted: q. 63 a. 3 co. (Anselm); q. 108 a. 6 co. (six phrases) and ad 4 (one)
- Rights: 1920 English, public domain.
- Ceiling: New Advent presentation; Leonine Latin of q. 108 a. 6 read (it gives no homily number for Gregory; New Advent adds "Hom. xxiv").

### Dionysius, Celestial Hierarchy 6–9 (Parker 1899)
- Witness: John Parker, *The Works of Dionysius the Areopagite*, pt. 2 (London, 1899), as transcribed at tertullian.org.
- Repository ids: `work.pseudo-dionysius-the-areopagite.de-caelesti-hierarchia` (registered with this publication).
- URL: https://www.tertullian.org/fathers/areopagite_13_heavenly_hierarchy.htm
- Retrieved: 2026-09-29
- SHA-256 of the bytes read: ae7608cea7b9f874f2b8ebdabfbe9cfae8b74285fec914aeca3d87cd9089104d (114110 bytes)
- Loci read: CH 5–9
- Quoted: CH 7.1 ("warmth, and keenness")
- Rights: 1899, public domain.
- Ceiling: web transcription; not collated with print.

### Gregory the Great, Hom. in Evang. 34; Moralia XXXII.48
- Witness: Latin *Homiliae in Evangelia* 34 (la.wikisource, PL 76 text); *Morals on the Book of Job*, Library of the Fathers vol. 31 (vol. III pt. 2, Oxford 1850), and lectionarycentral transcription.
- Repository ids: `work.gregory-the-great.homiliae-in-evangelia` (existing); `work.gregory-the-great.moralia-in-iob` (registered with this publication).
- URL: https://la.wikisource.org/w/index.php?title=Homiliarum_in_Evangelia/XXXIV&action=raw ; https://archive.org/download/31ALibraryOfFathersOfTheHolyCatholicV31/31ALibraryOfFathersOfTheHolyCatholicV31_djvu.txt ; https://www.lectionarycentral.com/GregoryMoralia/Book32.html
- Retrieved: 2026-09-29/30
- SHA-256 of the bytes read: dfd661ab607de8517fed4ffabddea2bdb80da2591230cb5b9a73efc62d56147f (35028 bytes); e57596ba2cedfc47ab9ff599c660b172262d9e25c33782c87419544a925f32be (2108312 bytes); 426a7d69992a5e03be469291433c135f5520e125db35b53f65d850b927b4dbef (153054 bytes)
- Loci read: Hom. 34.7–13; Moralia XXXII.47–48
- Quoted: none in prose (lists in appendix table)
- Rights: public domain.
- Ceiling: web transcription (Wikisource) and OCR; lists agree across LF OCR and lectionarycentral.

### Isidore, Etymologiae VII.5
- Witness: Latin text at The Latin Library.
- Repository ids: `work.isidore.etymologiae` (existing).
- URL: https://www.thelatinlibrary.com/isidore/7.shtml
- Retrieved: 2026-09-29T17:50:49Z
- SHA-256 of the bytes read: 44312348f815c0af0ed00ecb532cbe327d3dc6a50f32ef78726b3d8abe37b150 (80402 bytes)
- Loci read: VII.5.1–33
- Quoted: VII.5.4 (list, appendix)
- Rights: public domain text.
- Ceiling: web transcription.

### Cyril of Jerusalem; Gregory Nazianzen; Ambrose; John Damascene (NPNF)
- Witness: *Myst. Cat.* V.6 and *Or.* 28.31 (NPNF2 7); Ambrose *De fide* V.13.166 and *De Spiritu Sancto* I.16.178 (NPNF2 10); Damascene *De fide orth.* II.3, tr. Salmond (NPNF2 9).
- Repository ids: `work.cyril-of-jerusalem.catechetical-lectures` (existing); `work.gregory-of-nazianzus.oration-28` (registered with this publication); `work.ambrose.de-fide` (registered with this publication); `work.john-of-damascus.de-fide-orthodoxa` (registered with this publication).
- URL: https://ccel.org/ccel/s/schaff/npnf207/cache/npnf207.txt ; …npnf210… ; …npnf209…
- Retrieved: 2026-09-29
- SHA-256 of the bytes read: 56d84cfa94dee313af0139e2d7f3d4b5f7fffca40ce0f34794b5f56264964dfd (3388014 bytes); 14fa05cc98a67cb1ccf7613e63d5eb80fd48feb3e09dd29210e70f53dfcd7577 (2963575 bytes); 859ba34cc5998f2761b801aa5de724b2ea741a54d98e21614faeb89cc40f8ad4 (2606804 bytes)
- Loci read: as named
- Quoted: lists only (appendix)
- Rights: public domain.
- Ceiling: CCEL plain text.

### Dante, Paradiso XXVIII (Longfellow)
- Witness: *Divine Comedy*, tr. H. W. Longfellow, *Paradiso*, Project Gutenberg eBook 1003.
- Repository ids: `work.dante-alighieri.divina-commedia` (registered with this publication).
- URL: https://www.gutenberg.org/cache/epub/1003/pg1003.txt
- Retrieved: 2026-09-30T14:58:13Z
- SHA-256 of the bytes read: 1d3caefa714846480a0ce44067396bc755b23ac78de41772c6d6bc98aa24095a (249847 bytes)
- Loci read: Par. XXVIII entire (vv. counted: 139)
- Quoted: XXVIII.133–135
- Rights: public domain.
- Ceiling: Gutenberg text; verse numbers counted from the canto text.

### Fourth Lateran Council (Denzinger)
- Witness: *Firmiter* and c. 2, Latin as in the Denzinger text cached for the leaf.
- Repository ids: `work.fourth-lateran-council.firmiter-credimus` (existing); `work.denzinger.enchiridion-symbolorum` (existing).
- URL: see manifest (denz-patristica)
- Retrieved: 2026-09-29
- SHA-256 of the bytes read: 604f24c46e0bc71c2018f25dc787a9ab421d4b2e9cf7d1cee1f43e910ef2708f (2333435 bytes)
- Loci read: DS 800–804
- Quoted: DS 800 (two clauses), DS 804 ("cum Petro Lombardo")
- Rights: public domain Latin.
- Ceiling: Denzinger transcription.

### Douay–Rheims (Challoner)
- Witness: Project Gutenberg eBook 1581.
- Repository ids: `work.english-college-of-douay.douay-rheims-bible` (existing).
- URL: https://www.gutenberg.org/cache/epub/1581/pg1581.txt
- Retrieved: 2026-09-29
- SHA-256 of the bytes read: 7d10da78d8ec97db53b4e2bd8719cc01e16106b44937a673ba34aa534a04c007 (5880580 bytes)
- Loci read and quoted: 1 Cor 4:7; Gen 1:1; Ps 90:11–12; Ps 117:15; Ps 137:1; Isa 14:13–14; Job 40:14; Ezek 28:12–13; 4 Kgs 6:16; Eph 1:21; Col 1:16; Eph 6:12
- Rights: public domain.
- Ceiling: Gutenberg text.

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
- Repository ids: `work.pseudo-dionysius-the-areopagite.de-ecclesiastica-hierarchia` (registered with this publication).
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
- Repository ids: `work.augustine.de-divinatione-daemonum` (registered with this publication).
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

## Illumination and speech; hierarchies and orders; the order of the universe (ST I qq. 106-109)

### Aquinas, Summa theologiae, English
- Witness: Thomas Aquinas, *Summa theologiae*, tr. Fathers of the English Dominican Province, 2nd rev. ed. 1920, as presented by New Advent.
- Repository ids: `work.thomas-aquinas.summa-theologiae` (existing).
- URL: https://www.newadvent.org/summa/1047.htm, /1050.htm, /1103.htm, /1022.htm, /1106.htm, /1107.htm, /1108.htm, /1109.htm
- Retrieved: 2026-09-29 (1047, 1050, 1106-1109); 2026-09-30 (1103, 1022)
- Loci read: I q. 47 aa. 1-3; q. 50 a. 1; q. 103 a. 6; qq. 106-109 entire (every objection, s.c., corpus, reply).
- Quoted: I q. 47 aa. 1-3 co.; q. 50 a. 1 co.; q. 103 a. 6 co., s.c.; q. 106 aa. 1-4 (co., s.c., replies); q. 107 aa. 1-5; q. 108 aa. 1-8; q. 109 aa. 1-4.
- Rights: public domain (1920 translation).
- Ceiling: web transcription; not collated with print. New Advent prints "Hom. xxiv in Evang." at q. 108 a. 5 ad 3-4 and a. 6 (Latin has only "Gregorius"); treated as Hom. 34. New Advent typos kept where quoted ("more perfect that what", q. 108 a. 2 ad 2); avoided where possible ("consummae end", q. 106 a. 2 ad 1, replaced by the Latin).

### Aquinas, Summa theologiae, Latin
- Witness: Leonine text as presented by Corpus Thomisticum (E. Alarcón).
- Repository ids: `work.thomas-aquinas.summa-theologiae` (existing).
- URL: https://www.corpusthomisticum.org/sth1103.html; https://www.corpusthomisticum.org/sth1044.html
- Retrieved: 2026-09-29
- SHA-256 of the bytes read: 5736abad11534d6a5ebb3fa0c76ff5df228d6558cbb69163f5f437523f2c2ed1 (476518 bytes); 41c6edfab20faec48a4181d11d3dbde6549398127633854b20c60bce9f3c5b9c (176483 bytes)
- Loci read: I qq. 106-109 entire; q. 47 aa. 1-3.
- Quoted: key Latin terms and sentences at q. 106 pr., aa. 1-4; q. 107 aa. 1, 4, 5; q. 108 pr., aa. 2, 4, 5, 6; q. 109 a. 1.
- Rights: Leonine Latin, public domain; CT presentation used for short quotation.
- Ceiling: digital text; not collated with Leonine print.

### Aquinas, De veritate
- Witness: *Quaestiones disputatae de veritate*, Leonine text (1972) as presented by Corpus Thomisticum.
- Repository ids: `work.thomas-aquinas.de-veritate` (registered with this publication).
- URL: https://www.corpusthomisticum.org/qdv08.html
- Retrieved: 2026-09-29
- SHA-256 of the bytes read: 9b15fb2b63b70db664ba953a6a9a1ea349d3895482cd6a6cdb872dab817a1ec3 (405187 bytes)
- Loci read: q. 9 aa. 1-7 (corpora; a. 6 ad 1-2; a. 7 ad 1).
- Quoted: q. 9 a. 1 co.; a. 2 co.; a. 3 co.; a. 4 co.; a. 5 co.; a. 6 ad 2 (paraphrase); a. 7 co. (Latin only; English is paraphrase).
- Rights: public domain Latin.
- Ceiling: digital text.

### Aquinas, Scriptum super Sententiis II
- Witness: *Scriptum super libros Sententiarum*, Parma 1856 text as presented by Corpus Thomisticum.
- Repository ids: `work.thomas-aquinas.scriptum-super-sententiis` (existing).
- URL: https://www.corpusthomisticum.org/snp2009.html (d. 9-11); https://www.corpusthomisticum.org/snp2005.html (d. 5-8)
- Retrieved: 2026-09-29 (snp2009); 2026-09-30 (snp2005)
- SHA-256 of the bytes read: 1df33e5b7ce0687c4d9a80c3b172ec4252734260d7259db445dbf8e1bb33560a (218939 bytes); 9f55c793a696b620eb411cd7406b077051ae7a33262c6a5adc1f557458f2d7ce (210163 bytes)
- Loci read: II d. 9 q. 1 aa. 1-8 (corpora and most replies); d. 10 q. 1 a. 1 co.; d. 11 q. 2 aa. 2-6 (s.c. and co.); d. 6 q. 1 a. 1 (s.c., co.), a. 4 (entire).
- Quoted (Latin): d. 9 q. 1 a. 1 co.; a. 3 co., ad 3, ad 7; a. 4 ad 2, ad 5; a. 5 co., s.c. 2; a. 7 co.; a. 8 co., ad 2, ad 4; d. 11 q. 2 a. 2 co., a. 3 co., a. 4 co., a. 5 co., a. 6 co.; d. 6 q. 1 a. 1 co., a. 4 co., ad 3.
- Rights: public domain Latin.
- Ceiling: Parma text (not Leonine; the Leonine is not published for this book); digital text. The d. 6 a. 4 s.c. cites "Job 61" (Parma typo); body cites Job 41:7-8.

### Aquinas, Summa contra gentiles
- Witness: *Summa contra gentiles*, Leonine manual text (Turin 1961) as presented by Corpus Thomisticum.
- Repository ids: `work.thomas-aquinas.summa-contra-gentiles` (registered with this publication).
- URL: https://www.corpusthomisticum.org/scg2046.html; https://www.corpusthomisticum.org/scg3064.html
- Retrieved: 2026-09-29
- SHA-256 of the bytes read: 4facc3d0007a2edd8ab7f3bfe103446384124af3b18fa1d856b0a45055f33390 (69826 bytes); b3be14fbe2b9597f2ca9cb482c009c33a133fcc73ff9190c836011a4cdb8bf1b (393598 bytes)
- Loci read: II.46 entire; III.77-80 entire.
- Quoted (Latin): II.46 tit., nn. 1, 2, 3, 5, 7; III.77 nn. 4, 6; III.78 n. 1; III.80 nn. 5-7, 10-11, 14-15, 17, 19.
- Rights: public domain Latin.
- Ceiling: digital text.

### Dionysius, Celestial Hierarchy (Parker)
- Witness: *The Works of Dionysius the Areopagite*, Part II, tr. John Parker (London and Oxford: James Parker, 1899), transcribed at tertullian.org.
- Repository ids: `work.pseudo-dionysius-the-areopagite.de-caelesti-hierarchia` (registered with this publication); `work.pseudo-dionysius-the-areopagite.works-part-ii-parker` (registered with this publication).
- URL: https://www.tertullian.org/fathers/areopagite_13_heavenly_hierarchy.htm
- Retrieved: 2026-09-29
- SHA-256 of the bytes read: ae7608cea7b9f874f2b8ebdabfbe9cfae8b74285fec914aeca3d87cd9089104d (114110 bytes)
- Loci read: CH 1.2-1.3; 3.1-3; 4.1-4; 5; 6; 7.1-4; 8.1-2; 9.1-4; 10.1-3; 11.1-2; 12.1-3; 14; 15.3.
- Quoted: CH 1.2; 3.1; 3.2; 4.1; 4.2; 4.3; 5; 6; 7.2; 7.3; 7.4; 8.1; 10.1; 10.2; 11.2; 15.3.
- Rights: public domain (1899).
- Ceiling: web transcription; Parker's section numbers; not collated with print; PG columns not checked by this lane.

### Dionysius, Ecclesiastical Hierarchy (Parker)
- Witness: same volume, EH, tertullian.org.
- Repository ids: `work.pseudo-dionysius-the-areopagite.works-part-ii-parker` (registered with this publication); `work.pseudo-dionysius-the-areopagite.de-ecclesiastica-hierarchia` (registered with this publication).
- URL: https://www.tertullian.org/fathers/areopagite_14_ecclesiastical_hierarchy.htm
- Retrieved: 2026-09-29
- SHA-256 of the bytes read: bf098b8ee8a85ecfa388d3004d389f8176f745e5bc80ff6494765a8bd281790c (152291 bytes)
- Loci read: EH 5.6-7.
- Quoted: EH 5.7.
- Rights: public domain.
- Ceiling: web transcription. EH 6 (cited by Aquinas at q. 106 a. 2 ad 1) not read; attributed as "Aquinas cites".

### Dionysius, Divine Names (Parker)
- Witness: *The Works of Dionysius the Areopagite*, Part I, tr. John Parker (1897), tertullian.org.
- Repository ids: `work.pseudo-dionysius-the-areopagite.de-divinis-nominibus` (registered with this publication).
- URL: https://www.tertullian.org/fathers/areopagite_03_divine_names.htm
- Retrieved: 2026-09-29
- SHA-256 of the bytes read: 7d89093873b2ea5b8cf88e96c9066ce04907a0231523db3fa363c22039dc4295 (206269 bytes)
- Loci read: DN 4.1-4, 4.13-17, 4.23.
- Quoted: DN 4.1; 4.2; 4.13; 4.14; 4.15; 4.23.
- Rights: public domain.
- Ceiling: web transcription. DN 12 (q. 108 a. 5 ad 2) not read; attributed via Aquinas.

### Gregory the Great, Homiliae in Evangelia
- Witness: H. Hurter (ed.), *Sanctorum Patrum opuscula selecta*, series altera, t. VI (Gregory, XL homiliae in Evangelia), Google scan at archive.org; OCR corrected against the Latin Wikisource transcription of *Homiliarum in Evangelia* (Migne-derived) held at .scratch/aquinas-ministry/gregory-34.txt (EPUB member c36; source https://la.wikisource.org/wiki/Homiliarum_in_Evangelia).
- Repository ids: `work.gregory-the-great.homiliae-in-evangelia` (existing).
- URL: https://archive.org/download/sanctigregoriim00igoog/sanctigregoriim00igoog_djvu.txt; https://la.wikisource.org/wiki/Homiliarum_in_Evangelia
- Retrieved: 2026-09-29 (archive.org); Wikisource copy date not recorded in the GPT-edition receipts
- SHA-256 of the bytes read: 4eb8d78cd432816ff08b76b2549b6015fe29637307a22ee1d7ba79884d68e2f1 (701111 bytes)
- Loci read: Hom. 29.2; Hom. 34.6-15.
- Quoted (Latin): 29.2; 34.6; 34.8; 34.10; 34.11; 34.12; 34.13; 34.14; 34.15. Orthography follows Hurter (caritas, majora, nunciantur, coelestis). English glosses are the lane's own renderings, printed as paraphrase, not as quotation.
- Rights: public domain Latin.
- Ceiling: OCR witness, spot-collated at every quoted sentence against the Wikisource transcription; not collated with PL 76 print.

### Gregory the Great, Moralia (Library of the Fathers)
- Witness: *Morals on the Book of Job*, Library of the Fathers, vol. 1 (Oxford 1844), vol. 2 (1845), vol. 3 (1850, via lectionarycentral transcription).
- Repository ids: `work.gregory-the-great.moralia-in-iob` (registered with this publication).
- URL: https://archive.org/download/moralsonbookofj01greg/moralsonbookofj01greg_djvu.txt; https://archive.org/download/21ALibraryOfFathersOfTheHolyCatholicV21/21ALibraryOfFathersOfTheHolyCatholicV21_djvu.txt; https://www.lectionarycentral.com/GregoryMoralia/Book32.html; https://www.lectionarycentral.com/GregoryMoralia/Book34.html
- Retrieved: 2026-09-29
- SHA-256 of the bytes read: 96e0f3706c7a9a427bb3dffa578be87bd66ac96617fc90a7266ce7f241264ad2 (1806303 bytes); f13861be5715cabe5283d5bd7f38cb35c2a1332bd6dc04cf049475b88da5c493 (1916422 bytes); 426a7d69992a5e03be469291433c135f5520e125db35b53f65d850b927b4dbef (153054 bytes); 01cd003e8190bffcb1c6a15e2cff7cde9c3f0a484c881c9627a3a7bbe5fa637a (139202 bytes)
- Loci read: II.7-12 (LF sections 7-12); XVIII.77-78; XXXII.23.47-48; XXXIV.23.47-48.
- Quoted: II.8, II.9, II.10, II.11; XVIII.77-78; XXXII.23.48; XXXIV.23.47.
- Rights: public domain (1844-50).
- Ceiling: OCR (vols 1-2) and web transcription (vol. 3); cited by book and LF section number (the chapter numbers of books II and XVIII were not legible in the OCR); one transcription typo ("nine; orders", XXXII.23.48) avoided by paraphrase.

### Augustine, De civitate Dei
- Witness: tr. Marcus Dods, NPNF series 1 vol. 2 (1887), CCEL plain text; Latin, The Latin Library.
- Repository ids: `work.augustine.de-civitate-dei` (existing).
- URL: https://ccel.org/ccel/s/schaff/npnf102/cache/npnf102.txt; https://www.thelatinlibrary.com/augustine/civ12.shtml
- Retrieved: 2026-09-29
- SHA-256 of the bytes read: 5c973feda803f3e58a88ed7df210b42d436f5466741eb8dbeae713ab56dedae4 (3692898 bytes); eaa02a7032e27db9eba0d007aafd450017b5b0260f7718d7a28ce968de4b9f7e (72904 bytes)
- Loci read: XII.1; XII.9; XII.21 (NPNF numbering; Latin Library [XXII]).
- Quoted: XII.1; XII.9; XII.21.
- Rights: public domain.
- Ceiling: CCEL proofed text; not collated with print.

### Augustine, De Trinitate III
- Witness: tr. A. W. Haddan, NPNF series 1 vol. 3, as presented by New Advent (130103); Latin, augustinus.it.
- Repository ids: `work.augustine.de-trinitate` (registered with this publication).
- URL: https://www.newadvent.org/fathers/130103.htm; https://www.augustinus.it/latino/trinita/trinita_03_libro.htm
- Retrieved: 2026-09-29 (New Advent copy at .scratch/aquinas-ministry/augustine-trin3.txt, GPT-edition receipt); 2026-09-30 (Latin)
- SHA-256 of the bytes read: b2b06936a08717dd5aa48a284827d500e8b632eb700c0779d457b133749e7f51 (68630 bytes)
- Loci read: III.4.9 (English and Latin).
- Quoted: III.4.9.
- Rights: public domain.
- Ceiling: web transcription.

### Augustine, Enchiridion; De cura pro mortuis gerenda
- Witness: tr. J. F. Shaw (Enchiridion) and H. Browne (De cura), NPNF series 1 vol. 3, CCEL.
- Repository ids: `work.augustine.enchiridion-ad-laurentium` (existing); `work.augustine.de-cura-pro-mortuis-gerenda` (registered with this publication).
- URL: https://ccel.org/ccel/s/schaff/npnf103/cache/npnf103.txt
- Retrieved: 2026-09-29
- SHA-256 of the bytes read: cc8d3ff7ce4d4ba293f50a06200af03ff0e5abdeb5200db3a59b4dbe2cad7bdb (3357503 bytes)
- Loci read: Enchiridion 29, 58-63; De cura 19-20 (NPNF sections; Migne ch. 16).
- Quoted: Enchiridion 29, 58, 61, 62, 63; De cura 16.19.
- Rights: public domain.
- Ceiling: CCEL proofed text.

### Augustine, De diversis quaestionibus LXXXIII
- Witness: Latin text, augustinus.it (NBA).
- Repository ids: `work.augustine.de-diversis-quaestionibus-octoginta-tribus` (registered with this publication).
- URL: https://www.augustinus.it/latino/ottantatre_questioni/ottantatre_questioni_libro.htm
- Retrieved: 2026-09-29
- SHA-256 of the bytes read: 60b9fbde7a1bb0bd7e4b28efa445f3ecc04da8459fca9407303464dd9fd68d28 (316081 bytes)
- Loci read: q. 51.2-4.
- Quoted: q. 51.2, 51.4 (Latin).
- Rights: Latin text public domain; site presentation used for short quotation only.
- Ceiling: web text.

### John Chrysostom, Homilies on Matthew
- Witness: tr. G. Prevost, rev. M. B. Riddle, NPNF series 1 vol. 10, CCEL.
- Repository ids: `work.john-chrysostom.homiliae-in-matthaeum` (existing).
- URL: https://ccel.org/ccel/s/schaff/npnf110/cache/npnf110.txt
- Retrieved: 2026-09-29
- SHA-256 of the bytes read: adb8f1c9a988c5050a20fb9fdbf75143dcb227e95e3dad2f560a63b757923648 (3345978 bytes)
- Loci read: Hom. 28.3.
- Quoted: Hom. 28.3.
- Rights: public domain.
- Ceiling: CCEL text.

### John of Damascus, De fide orthodoxa
- Witness: tr. S. D. F. Salmond, NPNF series 2 vol. 9, CCEL.
- Repository ids: `work.john-of-damascus.de-fide-orthodoxa` (registered with this publication).
- URL: https://ccel.org/ccel/s/schaff/npnf209/cache/npnf209.txt
- Retrieved: 2026-09-29
- SHA-256 of the bytes read: 859ba34cc5998f2761b801aa5de724b2ea741a54d98e21614faeb89cc40f8ad4 (2606804 bytes)
- Loci read: I.13 (section on the place of angels).
- Quoted: I.13.
- Rights: public domain.
- Ceiling: CCEL text.

### Isidore, Etymologiae VII
- Witness: Latin (Lindsay text) at The Latin Library.
- Repository ids: `work.isidore.etymologiae` (existing).
- URL: https://www.thelatinlibrary.com/isidore/7.shtml
- Retrieved: 2026-09-29
- SHA-256 of the bytes read: 44312348f815c0af0ed00ecb532cbe327d3dc6a50f32ef78726b3d8abe37b150 (80402 bytes)
- Loci read: VII.5.1-33.
- Quoted: VII.5.2, 5.8, 5.20, 5.33 (Latin).
- Rights: public domain Latin.
- Ceiling: web transcription.

### Peter Lombard, Sententiae II
- Witness: *Libri IV Sententiarum*, 2nd Quaracchi ed. (1916), t. I, archive.org OCR.
- Repository ids: `work.peter-lombard.sententiae` (existing).
- URL: https://archive.org/download/libriivsententia01pete/libriivsententia01pete_djvu.txt
- Retrieved: 2026-09-29
- SHA-256 of the bytes read: 4cc27eb3178d204a0d8727cb8bdfad2bcd0180a1ded0b9cc9d605b33b59c4cf8 (1592526 bytes)
- Loci read: II d. 9 cc. 1-7; d. 11 c. 2.
- Quoted (Latin): d. 9 cc. 1, 2, 3, 4, 5, 6, 7; d. 11 c. 2.
- Rights: public domain (Latin text; 1916 apparatus not quoted).
- Ceiling: OCR, read against the page; apparatus letters removed from quotations. The Quaracchi note at d. 9 c. 1 states that the triad list is verbatim from Hugh, *Summa sententiarum* tr. 2 c. 5 (not read).

### Bernard of Clairvaux, De consideratione
- Witness: *Saint Bernard On Consideration*, tr. George Lewis (Oxford: Clarendon Press, 1908), archive.org OCR.
- Repository ids: `work.bernard-of-clairvaux.de-consideratione` (registered with this publication).
- URL: https://archive.org/download/onconsideration00bern/onconsideration00bern_djvu.txt
- Retrieved: 2026-09-30
- SHA-256 of the bytes read: 23dacc2ca0c5f0244fe9c456afbdb2a2745767b2281d7553d07899d93416f49e (306976 bytes)
- Loci read: V.4.7-10; V.5.11-12 (Lewis's section numbers).
- Quoted: V.4.8; V.4.10; V.5.11.
- Rights: public domain in the United States (published 1908); translator's death date not verified (see Open issues).
- Ceiling: OCR; the section number printed before the first paragraph of ch. IV reads "4." in the OCR (probably 7); the quoted passage is Lewis's §8.

### Douay-Rheims Bible
- Witness: Douay-Rheims (Challoner), Project Gutenberg eBook 1581.
- Repository ids: `work.english-college-of-douay.douay-rheims-bible` (existing); `edition.english-college-of-douay.douay-rheims-bible.challoner-gutenberg-1581` (existing).
- URL: https://www.gutenberg.org/cache/epub/1581/pg1581.txt
- Retrieved: 2026-09-29
- SHA-256 of the bytes read: 7d10da78d8ec97db53b4e2bd8719cc01e16106b44937a673ba34aa534a04c007 (5880580 bytes)
- Loci read and quoted: see ## Scripture cited.
- Rights: public domain.
- Ceiling: Gutenberg text.

## Government, mission, and the assaults of demons (ST I qq. 110-112, 114); the demons' powers and limits

### Aquinas, Summa theologiae I qq. 110–112, 114 (with q. 57 aa. 3–4, q. 64 aa. 1 and 4, q. 103 a. 6, q. 106 pr.)
- Witness: English Dominican translation, 2nd rev. ed. 1920, as presented by New Advent; Latin Leonine text as presented by Corpus Thomisticum.
- Repository ids: `work.thomas-aquinas.summa-theologiae` (existing).
- URL: https://www.newadvent.org/summa/1110.htm, 1111.htm, 1112.htm, 1114.htm, 1057.htm, 1064.htm; https://www.corpusthomisticum.org/sth1103.html
- Retrieved: 2026-09-29 (manifest)
- SHA-256 of the bytes read: 5736abad11534d6a5ebb3fa0c76ff5df228d6558cbb69163f5f437523f2c2ed1 (476518 bytes)
- Loci read: I q. 110 pr., aa. 1–4 entire; q. 111 pr., aa. 1–4 entire; q. 112 pr., aa. 1–4 entire; q. 114 pr., aa. 1–5 entire; q. 57 aa. 3–4 corpora and ad 1; q. 64 a. 1 corpus and ad 4, a. 4 corpus; q. 103 a. 6 co. (Latin only); q. 106 pr. (Latin).
- Quoted: every article of qq. 110–112 and 114 (English and key Latin); q. 103 a. 6 co. (Latin); q. 106 pr. and qq. 110–112, 114 prologues (Latin).
- Rights: English Dominican 1920, public domain; Latin text public domain.
- Ceiling: web presentations; not collated with the Leonine print. New Advent's typographical slip "form some corporeal agent" (q. 110 a. 2) avoided by quoting the Latin.

### Aquinas, Summa contra gentiles III.78–81, 103
- Witness: Latin (Leonine manual) as presented by Corpus Thomisticum.
- Repository ids: `work.thomas-aquinas.summa-contra-gentiles` (registered with this publication).
- URL: https://www.corpusthomisticum.org/scg3064.html
- Retrieved: 2026-09-29
- SHA-256 of the bytes read: b3be14fbe2b9597f2ca9cb482c009c33a133fcc73ff9190c836011a4cdb8bf1b (393598 bytes)
- Loci read: III.78 nn. 1–6; III.79 nn. 1–5; III.80 nn. 1–19; III.81 n. 1; III.103 nn. 1–9.
- Quoted: III.78 n. 1; III.80 nn. 10–11 (phrases); III.103 nn. 6–7.
- Rights: Latin, public domain.
- Ceiling: web transcription; English not used.

### Aquinas, Quaestiones disputatae de potentia q. 6
- Witness: Latin (Marietti) as presented by Corpus Thomisticum.
- Repository ids: `work.thomas-aquinas.de-potentia` (registered with this publication).
- URL: https://www.corpusthomisticum.org/qdp5.html (the page carrying qq. 5–6; qdp6.html returned 404)
- Retrieved: 2026-09-30T14:22:35Z
- SHA-256 of the bytes read: f470797614277976e9a030aaa1b33238a8853b30bd4f52443cbde09bcc449d70 (424769 bytes)
- Loci read: q. 6 pr.; aa. 3, 4, 5, 10 corpora.
- Quoted: a. 3 (absque assertione et sententiae melioris praeiudicio; unde Augustinus dicit ... ad nutum materia corporalis; per modum miraculi ... per modum artis); a. 5 (si Daemonibus ... non decet; per modum artis).
- Rights: Latin, public domain.
- Ceiling: web transcription. a. 3 cites Augustine "in II Lib. de Trinitate" for a passage that stands in De Trin. III.10.21. The gloss on Gen 6:4 in a. 3 is not used.

### Aquinas, Quaestiones disputatae de malo q. 16
- Witness: Latin (Leonine) as presented by Corpus Thomisticum.
- Repository ids: `work.thomas-aquinas.de-malo` (registered with this publication).
- URL: https://www.corpusthomisticum.org/qdm16.html
- Retrieved: 2026-09-29
- SHA-256 of the bytes read: 125185866e21f915d9d469dd101e266842cd4ab6bee62ed7d57c7ad6515dcc62 (322684 bytes)
- Loci read: a. 6 co. (end), a. 7 co. (opening), aa. 8–12 corpora.
- Quoted: a. 9 co. (spiritual substances cannot transform bodies formally); a. 12 co. (good angels strengthen the light, demons do not).
- Rights: Latin, public domain.
- Ceiling: web transcription.

### Augustine, De Trinitate III
- Witness: English of A. W. Haddan (1873), revised W. G. T. Shedd, NPNF series 1 vol. 3 (1887), CCEL plain text; Latin as presented by augustinus.it (NBA text).
- Repository ids: `work.augustine.de-trinitate` (registered with this publication).
- URL: https://ccel.org/ccel/s/schaff/npnf103/cache/npnf103.txt; https://www.augustinus.it/latino/trinita/trinita_03_libro.htm
- Retrieved: 2026-09-29 (English); 2026-09-30T14:15:11Z (Latin)
- SHA-256 of the bytes read: cc8d3ff7ce4d4ba293f50a06200af03ff0e5abdeb5200db3a59b4dbe2cad7bdb (3357503 bytes); b2b06936a08717dd5aa48a284827d500e8b632eb700c0779d457b133749e7f51 (68630 bytes)
- Loci read: III.pref.1–3, III.1.4–11.27 entire.
- Quoted: III.1.4, 1.6, 3.8, 4.9 (block), 5.11, 6.11, 7.12, 8.13 (block and Latin), 9.16, 9.18 (block), 10.19, 10.20, 10.21, 11.22, 11.23, 11.27; Latin 4.9, 8.13.
- Rights: NPNF public domain; Latin public domain (web presentation).
- Ceiling: web transcriptions; not collated with CCSL 50. Shedd's bracketed notes not used.

### Augustine, De Genesi ad litteram VIII.24.45
- Witness: Latin as presented by augustinus.it.
- Repository ids: `work.augustine.de-genesi-ad-litteram` (existing).
- URL: https://www.augustinus.it/latino/genesi_lettera/genesi_lettera_08_libro.htm
- Retrieved: 2026-09-29
- SHA-256 of the bytes read: a024b5abb84bf0eb2a1f254c7262ac585f3df876ae43c478a00f609af99c7f74 (72204 bytes)
- Loci read: VIII.23.44–27.50.
- Quoted: VIII.24.45 (two Latin phrases).
- Rights: Latin, public domain.
- Ceiling: web transcription; not collated with CSEL 28.

### Augustine, De diversis quaestionibus octoginta tribus q. 79
- Witness: Latin as presented by augustinus.it.
- Repository ids: `work.augustine.de-diversis-quaestionibus-octoginta-tribus` (registered with this publication).
- URL: https://www.augustinus.it/latino/ottantatre_questioni/ottantatre_questioni_libro.htm
- Retrieved: 2026-09-29
- SHA-256 of the bytes read: 60b9fbde7a1bb0bd7e4b28efa445f3ecc04da8459fca9407303464dd9fd68d28 (316081 bytes)
- Loci read: q. 79.1–5.
- Quoted: q. 79.1, 79.4, 79.5 (Latin).
- Rights: Latin, public domain.
- Ceiling: web transcription.

### Augustine, De divinatione daemonum
- Witness: Latin as presented by augustinus.it.
- Repository ids: `work.augustine.de-divinatione-daemonum` (registered with this publication).
- URL: https://www.augustinus.it/latino/potere_divinatorio/potere_divinatorio_libro.htm
- Retrieved: 2026-09-29
- SHA-256 of the bytes read: 152f2e97c16255ad64191158345f5f220e113de7e86ce1480cf38a5406e7bc4b (30665 bytes)
- Loci read: entire (1.1–10.14).
- Quoted: 3.7, 5.9, 6.10 (Latin phrases).
- Rights: Latin, public domain. No public-domain English located; none quoted.
- Ceiling: web transcription.

### Augustine, Retractationes II.30
- Witness: Latin as presented by augustinus.it.
- Repository ids: `work.augustine.retractationes` (registered with this publication).
- URL: https://www.augustinus.it/latino/ritrattazioni/ritrattazioni_2_libro.htm
- Retrieved: 2026-09-30T14:14:57Z
- SHA-256 of the bytes read: 683b581f9430763fb9ddada2aaebb7ee92e924599a8f43f9010bb15f896be3ab (105653 bytes)
- Loci read: II.30 (LVII).
- Quoted: II.30 (two Latin phrases).
- Rights: Latin, public domain.
- Ceiling: web transcription.

### Augustine, De civitate Dei XVIII.18, XX.19
- Witness: English of Marcus Dods, NPNF series 1 vol. 2 (1887), CCEL.
- Repository ids: `work.augustine.de-civitate-dei` (existing).
- URL: https://ccel.org/ccel/s/schaff/npnf102/cache/npnf102.txt
- Retrieved: 2026-09-29
- SHA-256 of the bytes read: 5c973feda803f3e58a88ed7df210b42d436f5466741eb8dbeae713ab56dedae4 (3692898 bytes)
- Loci read: XVIII.18 entire; XX.19 (passage on the lying wonders and Job).
- Quoted: XVIII.18 (three sentences); XX.19 (two sentences).
- Rights: public domain.
- Ceiling: web transcription. The transformation narratives of XVIII.18 are not used.

### Gregory the Great, Moralia in Iob II and XVII
- Witness: Library of the Fathers, Morals on the Book of Job, vol. 1 (Oxford 1844) and vol. 2 (Oxford 1845), archive.org OCR.
- Repository ids: `work.gregory-the-great.moralia-in-iob` (registered with this publication).
- URL: https://archive.org/download/moralsonbookofj01greg/moralsonbookofj01greg_djvu.txt; https://archive.org/download/21ALibraryOfFathersOfTheHolyCatholicV21/21ALibraryOfFathersOfTheHolyCatholicV21_djvu.txt
- Retrieved: 2026-09-29
- SHA-256 of the bytes read: 96e0f3706c7a9a427bb3dffa578be87bd66ac96617fc90a7266ce7f241264ad2 (1806303 bytes); f13861be5715cabe5283d5bd7f38cb35c2a1332bd6dc04cf049475b88da5c493 (1916422 bytes)
- Loci read: II.2.2–13.22 (Job 1:6–15); XVII.12.17–14.20 (Job 25:2–4).
- Quoted: II.3.3, II.4.4–5, II.10.16–17 (block), II.11.19, II.12.21, II.13.22; XVII.13.18–19.
- Rights: LF translation, public domain.
- Ceiling: OCR; obvious OCR errors corrected in quotation ("gb"→"go", "tlie/tlic"→"the", "hght"→"light"); passages with garbled quotation marks quoted only in their clean parts. Not collated with print or CCSL 143.

### Gregory the Great, Homiliae in Evangelia 34
- Witness: Latin, Wikisource transcription of a Migne-based text (repository edition).
- Repository ids: `work.gregory-the-great.homiliae-in-evangelia` (existing); `edition.gregory-the-great.homiliae-in-evangelia.wikisource-web-2026-09-17` (existing).
- URL: https://la.wikisource.org/wiki/Homiliae_in_Evangelia_(Gregorius_Magnus)
- Retrieved: 2026-09-17 (edition registration); read through the l7-ch extract .scratch/lanes/l7-ch/greg-h34-wrapped.txt
- Loci read: 34.7–14.
- Quoted: 34.8, 34.10, 34.12, 34.13 (Latin).
- Rights: PL 76 text public domain; Wikisource layer CC BY-SA.
- Ceiling: web transcription; no public-domain English located; none quoted in English.

### Gregory the Great, Dialogues IV
- Witness: English of 1608 (P. W.), ed. Edmund G. Gardner (London 1911), transcribed at tertullian.org.
- Repository ids: `work.gregory-the-great.dialogi` (registered with this publication).
- URL: https://www.tertullian.org/fathers/gregory_04_dialogues_book4.htm
- Retrieved: 2026-09-30T14:22:02Z
- SHA-256 of the bytes read: c0fcbac5f0d6cbf6a192398f793368cf85d2e26253db4a40d0edd116c43698b1 (202560 bytes)
- Loci read: IV.1–6.
- Quoted: IV.5 (one sentence, the source of the sed contra of I q. 110 a. 1).
- Rights: public domain.
- Ceiling: web transcription. Chapter numbering of the 1911 English (ch. 5) differs from Aquinas's citation (iv, 6); footnoted in the body.

### Dionysius, Celestial Hierarchy 1, 4, 8, 13, 14
- Witness: John Parker, The Works of Dionysius the Areopagite, part II (London 1899), tertullian.org transcription.
- Repository ids: `work.pseudo-dionysius-the-areopagite.de-caelesti-hierarchia` (registered with this publication); `work.pseudo-dionysius-the-areopagite.works-part-ii-parker` (registered with this publication).
- URL: https://www.tertullian.org/fathers/areopagite_13_heavenly_hierarchy.htm
- Retrieved: 2026-09-29
- SHA-256 of the bytes read: ae7608cea7b9f874f2b8ebdabfbe9cfae8b74285fec914aeca3d87cd9089104d (114110 bytes)
- Loci read: CH 1.2–3; 4.1–4; 8.1–2; 13.1–4; 14; 15.1 (opening).
- Quoted: 1.2; 4.2, 4.3; 8.1; 13.2, 13.3, 13.4; 14.
- Rights: public domain.
- Ceiling: web transcription; stray period in 13.2 ("same name. as") avoided by quoting around it. CH 7 cited only as Aquinas cites it.

### Dionysius, Divine Names 4 and 7
- Witness: John Parker, Works of Dionysius, part I (London 1897), tertullian.org transcription.
- Repository ids: `work.pseudo-dionysius-the-areopagite.de-divinis-nominibus` (registered with this publication).
- URL: https://www.tertullian.org/fathers/areopagite_03_divine_names.htm
- Retrieved: 2026-09-29
- SHA-256 of the bytes read: 7d89093873b2ea5b8cf88e96c9066ce04907a0231523db3fa363c22039dc4295 (206269 bytes)
- Loci read: DN 4.1–3, 4.18–23; 7.2–3.
- Quoted: 4.2; 4.18; 4.23; 7.3.
- Rights: public domain.
- Ceiling: web transcription.

### John of Damascus, De fide orthodoxa II.3–4
- Witness: S. D. F. Salmond, NPNF series 2 vol. 9 (1899), CCEL.
- Repository ids: `work.john-of-damascus.de-fide-orthodoxa` (registered with this publication).
- URL: https://ccel.org/ccel/s/schaff/npnf209/cache/npnf209.txt
- Retrieved: 2026-09-29
- SHA-256 of the bytes read: 859ba34cc5998f2761b801aa5de724b2ea741a54d98e21614faeb89cc40f8ad4 (2606804 bytes)
- Loci read: II.3–4 entire.
- Quoted: II.3 (five sentences); II.4 (four sentences).
- Rights: public domain.
- Ceiling: English only; Salmond's rendering of the sentence Aquinas cites in I q. 111 a. 2 obj. 2 and q. 114 a. 3 obj. 1 differs from the Latin Aquinas used; both are given as such.

### Origen, De principiis III.2
- Witness: F. Crombie's English of Rufinus's Latin, ANF vol. 4, CCEL.
- Repository ids: `work.origen.de-principiis` (existing).
- URL: https://ccel.org/ccel/s/schaff/anf04/cache/anf04.txt
- Retrieved: 2026-09-29
- SHA-256 of the bytes read: b9f385a048c18158c2f74dcd37062f48a1c68a5d05bdb07270a93692d172da2e (4237225 bytes)
- Loci read: III.2.1–7 entire.
- Quoted: III.2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7.
- Rights: public domain.
- Ceiling: translation of Rufinus's Latin; not collated.

### Origen, Contra Celsum I.6
- Witness: F. Crombie, ANF vol. 4, CCEL.
- Repository ids: `work.origen.contra-celsum` (existing).
- URL: as above
- Retrieved: 2026-09-29
- SHA-256 of the bytes read: b9f385a048c18158c2f74dcd37062f48a1c68a5d05bdb07270a93692d172da2e (4237225 bytes)
- Loci read: I.6.
- Quoted: I.6 (one sentence, appendix).
- Rights: public domain.
- Ceiling: web transcription.

### Athanasius, Vita Antonii 16–43
- Witness: English of H. Ellershaw, NPNF series 2 vol. 4 (ed. A. Robertson, 1892), CCEL.
- Repository ids: `work.athanasius-of-alexandria.vita-antonii` (existing).
- URL: https://ccel.org/ccel/s/schaff/npnf204/cache/npnf204.txt
- Retrieved: 2026-09-30T14:09:25Z
- SHA-256 of the bytes read: d2f362ce989db6955bb7d900c619543c581beceaca52acd8359510551c85f124 (4570263 bytes)
- Loci read: 16–43 entire.
- Quoted: 21, 22, 23, 24, 28, 29, 30, 31, 35, 38, 41, 42.
- Rights: public domain.
- Ceiling: web transcription. Ch. 43 (the questioning of apparitions) deliberately not used under the profile's fallen-angel bounds.

### Athanasius, De incarnatione 47.2
- Witness: A. Robertson, NPNF series 2 vol. 4 (1892), CCEL.
- Repository ids: none registered; the entry cites the edition directly.
- URL: as above
- Retrieved: 2026-09-30T14:09:25Z
- SHA-256 of the bytes read: d2f362ce989db6955bb7d900c619543c581beceaca52acd8359510551c85f124 (4570263 bytes)
- Loci read: 47.1–4; 55.1–3.
- Quoted: 47.2 (appendix).
- Rights: public domain.
- Ceiling: web transcription.

### John Chrysostom, Three Homilies concerning the Power of Demons
- Witness: English of T. P. Brandram, NPNF series 1 vol. 9, CCEL.
- Repository ids: none registered; the entry cites the edition directly.
- URL: https://ccel.org/ccel/s/schaff/npnf109/cache/npnf109.txt
- Retrieved: 2026-09-30T14:09:26Z
- SHA-256 of the bytes read: d6a51d22d996e02c47b88462f7222737b26d2363212f24e34834cfc6b580da57 (2752950 bytes)
- Loci read: hom. 1 entire; hom. 2 entire; hom. 3.1–5.
- Quoted: 1.6; 2.1, 2.2, 2.4, 2.5; 3.1, 3.2, 3.4.
- Rights: public domain.
- Ceiling: web transcription; a stray period in 3.4 ("wickedness. of") avoided by quoting around it. The editor's introduction is not used as a source.

### John Chrysostom, Homilies on John 46
- Witness: English of G. T. Stupart, NPNF series 1 vol. 14, CCEL.
- Repository ids: `work.john-chrysostom.homilies-on-john` (existing).
- URL: https://ccel.org/ccel/s/schaff/npnf114/cache/npnf114.txt
- Retrieved: 2026-09-29
- SHA-256 of the bytes read: e26f55f8d0739c07d73d5b664e42efbd923a43230a22d93d55261c808e9cd458 (3943878 bytes)
- Loci read: hom. 46 (Eucharistic passage).
- Quoted: one sentence (appendix).
- Rights: public domain.
- Ceiling: web transcription.

### John Cassian, Conferences VII–VIII
- Witness: English of E. C. S. Gibson, NPNF series 2 vol. 11, CCEL.
- Repository ids: none registered; the entry cites the edition directly.
- URL: https://ccel.org/ccel/s/schaff/npnf211/cache/npnf211.txt
- Retrieved: 2026-09-30T14:11:59Z
- SHA-256 of the bytes read: 8b1206d4e7488c65b5391875fd9570a8a6bcc83270dea35ffe44010c3575d267 (3470230 bytes)
- Loci read: VII.1–3, 6–23; VIII.1–3, 12–20.
- Quoted: VII.8, 10, 15, 16, 17, 19, 20, 22; VIII.19.
- Rights: public domain.
- Ceiling: web transcription. VIII.16 (narrative about an identified monk's fall) not used.

### Denzinger–Schönmetzer: Trent, Sess. V can. 1 (DS 1511), Sess. VI ch. 1 (DS 1521); Braga I can. 8 (DS 458)
- Witness: Enchiridion symbolorum, Latin, patristica.net presentation.
- Repository ids: `work.denzinger.enchiridion-symbolorum` (existing); `work.council-of-trent.canones-et-decreta` (existing).
- URL: https://patristica.net/denzinger/enchiridion-symbolorum.html
- Retrieved: 2026-09-29
- SHA-256 of the bytes read: 604f24c46e0bc71c2018f25dc787a9ab421d4b2e9cf7d1cee1f43e910ef2708f (2333435 bytes)
- Loci read: DS 457–460; 1511–1512; 1521.
- Quoted: DS 1511, 1521 (Latin phrases); DS 458 paraphrased.
- Rights: Latin conciliar texts, public domain; no copyrighted English used.
- Ceiling: web transcription of DS.

### Catechism of the Catholic Church 391–395, 2846–2854
- Witness: English, vatican.va archive.
- Repository ids: `work.catholic-church.catechism` (existing).
- URL: https://www.vatican.va/archive/ENG0015/__P1C.HTM; https://www.vatican.va/archive/ENG0015/__PAC.HTM
- Retrieved: 2026-09-29 (P1C); 2026-09-30T14:22:36Z (PAC)
- SHA-256 of the bytes read: 3ce4c15f4bdb2cccf0dd788c1ddbe25a7eee2b8c1b35ecb60aa07d509b30c153 (33151 bytes); 42f886d8140924ace0ef510b3443096b88f74bfd2b9757080e684c854c112197 (15476 bytes)
- Loci read: 391–395; 2846–2854 with notes 150–175.
- Quoted: 395, 2846, 2849, 2851, 2852 (with Ambrose as cited), 2853, 2854 — short quotations.
- Rights: Libreria Editrice Vaticana English, copyrighted; short focused quotations with attribution.
- Ceiling: official web text.

### Paul VI, general audience of 15 November 1972
- Witness: Italian, vatican.va.
- Repository ids: `work.paul-vi.general-audience-1972-11-15` (registered with this publication).
- URL: https://www.vatican.va/content/paul-vi/it/audiences/1972/documents/hf_p-vi_aud_19721115.html
- Retrieved: 2026-09-29
- SHA-256 of the bytes read: ade46aabccf08b76fcb0ea47f159fe252585939feb0db6d1f649a6be8eb589fe (50375 bytes)
- Loci read: entire.
- Quoted: short Italian phrases (per eccellenza; per via dei sensi, della fantasia, della concupiscenza; Non è detto che ogni peccato ...; tutto ciò che ci difende ... La grazia è la difesa decisiva).
- Rights: Holy See text; short quotations with attribution.
- Ceiling: official web text. The printed reference "S. TH. 1, 104, 3" attached to the sentence on every sin evidently intends I q. 114 a. 3; the body says only "with a reference to the Summa".

### Douay–Rheims Bible (Challoner)
- Witness: Project Gutenberg eBook 1581.
- Repository ids: `edition.english-college-of-douay.douay-rheims-bible.challoner-gutenberg-1581` (existing).
- URL: https://www.gutenberg.org/cache/epub/1581/pg1581.txt
- Retrieved: 2026-09-29
- SHA-256 of the bytes read: 7d10da78d8ec97db53b4e2bd8719cc01e16106b44937a673ba34aa534a04c007 (5880580 bytes)
- Loci read and quoted: see Scripture cited.
- Rights: public domain.
- Ceiling: Gutenberg transcription.

### Patrologia Latina 58 (contents)
- Witness: PL 58, archive.org OCR.
- Repository ids: none registered; the entry cites the edition directly.
- URL: https://archive.org/download/patrologiaecur58mign/patrologiaecur58mign_djvu.txt
- Retrieved: 2026-09-30T14:12:54Z
- SHA-256 of the bytes read: 722ef703cc9374a049f0fea1642b4c341a426bffd5482ea272580b00b4505cb9 (4731021 bytes)
- Loci read: volume contents (Gennadius Massiliensis, Liber de Ecclesiasticis Dogmatibus).
- Quoted: nothing.
- Rights: public domain.
- Ceiling: the chapter quoted by Aquinas (De eccl. dogm. 49, sed contra of I q. 114 a. 3) could not be located in the OCR; the body quotes it only as the Summa gives it and does not name Gennadius.

## The guardian angels (ST I q. 113)

### Aquinas, Summa theologiae I q. 113
Witness: Thomas Aquinas, *Summa theologiae*, English Dominican Province 2nd rev. ed. 1920 (New Advent); Latin Leonine text (Corpus Thomisticum).
Repository id: work.thomas-aquinas.summa-theologiae
URL: https://www.newadvent.org/summa/1113.htm ; https://www.corpusthomisticum.org/sth1103.html
Retrieved: 2026-09-29 (manifest)
SHA-256 of the bytes read: 90503352952827b68b50c430f51df5fa977cd4d3404a06934b860fa9d6f2b576 (53327 bytes); 5736abad11534d6a5ebb3fa0c76ff5df228d6558cbb69163f5f437523f2c2ed1 (476518 bytes)
Loci read: I q. 113 pr., aa. 1–8 entire (obj., s.c., co., ad) in both languages.
Quoted: pr. (Latin); every article, English and key Latin phrases.
Rights: 1920 English public domain; Latin text quoted in short phrases.
Ceiling: web transcriptions; not collated with Leonine print. New Advent's "Tract. v, super Matt." (a. 5) is its own reference; Leonine has "super Matthaeum".

### Aquinas, Scriptum super Sententiis II d. 11
Witness: Thomas Aquinas, *In II Sent.* d. 11 q. 1 aa. 1–5, expositio textus; q. 2 a. 5 (Corpus Thomisticum, Parma text).
Repository id: work.thomas-aquinas.scriptum-super-sententiis
URL: https://www.corpusthomisticum.org/snp2009.html
Retrieved: 2026-09-29
SHA-256 of the bytes read: 1df33e5b7ce0687c4d9a80c3b172ec4252734260d7259db445dbf8e1bb33560a (218939 bytes)
Loci read: d. 11 q. 1 pr., aa. 1–5 entire, expositio; q. 2 pr., a. 1, a. 5 entire.
Quoted: q. 1 a. 1 ad 1, ad 5, ad 6; a. 2 co. (phrase); a. 3 co., ad 3, ad 5; a. 4 ad 1, ad 5; a. 5 ad 2, ad 3; expositio; q. 2 a. 5 co. (Latin, with glosses).
Rights: Latin, short quotation.
Ceiling: web text; a. 5 co. reading "etiam impossibile erat" paraphrased by sense only.

### Aquinas, Summa contra gentiles III.80
Witness: *SCG* III.78–80, Leonine text (Corpus Thomisticum).
Repository id: work.thomas-aquinas.summa-contra-gentiles
URL: https://www.corpusthomisticum.org/scg3064.html
Retrieved: 2026-09-29
SHA-256 of the bytes read: b3be14fbe2b9597f2ca9cb482c009c33a133fcc73ff9190c836011a4cdb8bf1b (393598 bytes)
Loci read: III.78–80 entire.
Quoted: III.80 nn. 14, 16 (Latin phrases).
Rights: Latin, short quotation.
Ceiling: web text.

### Aquinas, De veritate q. 8 a. 11
Witness: *Quaestiones disputatae de veritate* q. 8 a. 11 (Corpus Thomisticum).
Repository id: work.thomas-aquinas.de-veritate
URL: https://www.corpusthomisticum.org/qdv08.html
Retrieved: 2026-09-29
SHA-256 of the bytes read: 9b15fb2b63b70db664ba953a6a9a1ea349d3895482cd6a6cdb872dab817a1ec3 (405187 bytes)
Loci read: q. 8 a. 11 s.c. 1, co.; a. 12 arg. 5.
Quoted: a. 11 co. (one Latin phrase).
Rights: Latin, short quotation.
Ceiling: web text.

### Douay–Rheims Bible
Witness: Douay–Rheims (Challoner), Project Gutenberg eBook 1581.
Repository id: work.english-college-of-douay.douay-rheims-bible
URL: https://www.gutenberg.org/cache/epub/1581/pg1581.txt
Retrieved: 2026-09-29
SHA-256 of the bytes read: 7d10da78d8ec97db53b4e2bd8719cc01e16106b44937a673ba34aa534a04c007 (5880580 bytes)
Loci read: every verse in "Scripture cited" below.
Quoted: all English Scripture outside the Summa's own quotations.
Rights: public domain.
Ceiling: Gutenberg transcription.

### Hermas, Shepherd
Witness: *Shepherd of Hermas*, ANF 2 (Crombie).
Repository id: NEW work.hermas.pastor — title "The Shepherd"; responsible Hermas; work_type apocalyptic-parenesis; languages grc, la, en; locus Vis./Mand./Sim. book.chapter.
URL: https://ccel.org/ccel/s/schaff/anf02/cache/anf02.txt
Retrieved: 2026-09-29
SHA-256 of the bytes read: ae8e15414a21fe8d54a30fee7c3fbd1ee6a018e624dcd681d030da5c1cabbcac (3768675 bytes)
Loci read: Mand. VI.1–2; Vis. V.
Quoted: Mand. VI.2.
Rights: public domain (ANF 1885).
Ceiling: ANF translation.

### Clement of Alexandria, Stromata VI.17
Witness: *Stromata* VI.17, ANF 2 (Wilson).
Repository id: NEW work.clement-of-alexandria.stromata — responsible Clement of Alexandria; work_type miscellany; languages grc, en; locus book.chapter.
URL: as ANF 2 above
Retrieved: 2026-09-29
SHA-256 of the bytes read: ae8e15414a21fe8d54a30fee7c3fbd1ee6a018e624dcd681d030da5c1cabbcac (3768675 bytes)
Loci read: VI.17 (passage on providence and angels).
Quoted: VI.17 ("regiments of angels ... assigned to individuals").
Rights: public domain.
Ceiling: ANF translation. Eclogae 41, 48 (ANF 8) read but not used (they cite the apocryphal Apocalypse of Peter).

### Origen, Commentary on Matthew XIII.26–28
Witness: Origen, *Comm. in Matt.* XIII.26–28, ANF 9 (Patrick).
Repository id: work.origen.commentarium-in-matthaeum
URL: https://ccel.org/ccel/s/schaff/anf09/cache/anf09.txt
Retrieved: 2026-09-29
SHA-256 of the bytes read: 3861096b158e12bc13f4516baac913cbd3d921c607862a7eace4f0257b3aefa5 (3047154 bytes)
Loci read: XIII.26–28 entire.
Quoted: XIII.26, 27, 28 (short).
Rights: public domain.
Ceiling: ANF translation.

### Origen, De principiis II.10.7
Witness: *De principiis* II.10.7, Rufinus's Latin in ANF 4 (Crombie).
Repository id: work.origen.de-principiis
URL: https://ccel.org/ccel/s/schaff/anf04/cache/anf04.txt
Retrieved: 2026-09-29
SHA-256 of the bytes read: b9f385a048c18158c2f74dcd37062f48a1c68a5d05bdb07270a93692d172da2e (4237225 bytes)
Loci read: II.10.7–8.
Quoted: II.10.7.
Rights: public domain.
Ceiling: ANF translation.

### Origen, Homilies on Numbers XI.3–4
Witness: Origen, *Hom. in Num.* XI.3–4, Rufinus's Latin, ed. W. A. Baehrens, GCS 30 (Origenes Werke 7), Leipzig 1921, pp. 80–82.
Repository id: NEW work.origen.homiliae-in-numeros — responsible Origen (Rufinus trans.); work_type homilies; languages la; locus homily.section.
URL: https://archive.org/download/origeneswerkehrs07origuoft/origeneswerkehrs07origuoft_djvu.txt
Retrieved: 2026-09-30 (manifest)
SHA-256 of the bytes read: 2c72837897b3ace1f5548a9a15563062f5601c563cc566d9fec6712adcdbb290 (2230721 bytes)
Loci read: XI.2–4.
Quoted: XI.3 (one sentence), XI.4 (two sentences), Latin with gloss.
Rights: ancient text; 1921 edition, US public domain.
Ceiling: OCR normalized (e.g. "consunimatione" → consummatione, "angeii" → angeli); not collated with print.

### Gregory the Wonderworker, Panegyric on Origen
Witness: *Oratio panegyrica* 4–5, ANF 6 (Salmond).
Repository id: NEW work.gregory-thaumaturgus.oratio-panegyrica-in-origenem — responsible Gregory Thaumaturgus; work_type oration; languages grc, en; locus section.
URL: https://ccel.org/ccel/s/schaff/anf06/cache/anf06.txt
Retrieved: 2026-09-30
SHA-256 of the bytes read: cd739171090895364bad7600ebdebe824f995e696e75a3894c28ebdc671d68fb (3439156 bytes)
Loci read: Pan. Or. 4, 5.
Quoted: 4 ("that holy angel of God who fed me from my youth").
Rights: public domain.
Ceiling: ANF translation.

### Basil, Adversus Eunomium III.1
Witness: Basil, *Adversus Eunomium* III.1, Greek, Migne PG 29, 656B–657A.
Repository id: NEW work.basil-of-caesarea.adversus-eunomium (textual control work.jacques-paul-migne.patrologia-graeca-volume-29)
URL: https://archive.org/download/patrologiae_cursus_completus_gr_vol_029/patrologiae_cursus_completus_gr_vol_029_djvu.txt
Retrieved: 2026-09-29
SHA-256 of the bytes read: f4b52a32d8e2a8e33c0532df6224976b63896f8f6276358b207f9297730f1c8e (8499613 bytes)
Loci read: III.1–2.
Quoted: III.1 (Greek in transliteration, unquoted gloss).
Rights: public domain.
Ceiling: Greek OCR; column from running head (656/657).

### Basil, Homily on Psalm 33
Witness: *Hom. in Ps.* 33.5, Greek, PG 29.
Repository id: work.basil-of-caesarea.homilia-in-psalmum-33
URL: as PG 29 above
Retrieved: 2026-09-29
SHA-256 of the bytes read: f4b52a32d8e2a8e33c0532df6224976b63896f8f6276358b207f9297730f1c8e (8499613 bytes)
Loci read: 33.5 (on v. 8) to start of 33.6.
Quoted: 33.5 (two transliterated phrases, glossed).
Rights: public domain.
Ceiling: OCR; PG column not fixed (running heads garbled).

### Gregory of Nyssa, Life of Moses II
Witness: *De vita Moysis* II, Greek, Migne PG 44, 337–340.
Repository id: NEW work.gregory-of-nyssa.de-vita-moysis — responsible Gregory of Nyssa; work_type spiritual treatise; languages grc; locus book.section (PG column).
URL: https://archive.org/stream/patrologiae_cursus_completus_gr_vol_044/patrologiae_cursus_completus_gr_vol_044_djvu.txt
Retrieved: 2026-09-30
SHA-256 of the bytes read: aa9d6d88c7b49eff6b0b40b80c5986228356ccc3418127cdc6d72625d9410c7d (7884554 bytes)
Loci read: the Aaron-meets-Moses passage (Exod 4:27) entire.
Quoted: three transliterated phrases, glossed.
Rights: public domain.
Ceiling: Greek OCR; modern section numbers (II.45–47) not verified, so not printed.

### Chrysostom, Homilies on Matthew 59
Witness: *Hom. in Matt.* 59.4, NPNF 1.10 (Prevost).
Repository id: work.john-chrysostom.homiliae-in-matthaeum
URL: https://ccel.org/ccel/s/schaff/npnf110/cache/npnf110.txt
Retrieved: 2026-09-29
SHA-256 of the bytes read: adb8f1c9a988c5050a20fb9fdbf75143dcb227e95e3dad2f560a63b757923648 (3345978 bytes)
Loci read: Hom. 59.3–4.
Quoted: 59.4.
Rights: public domain.
Ceiling: NPNF translation.

### Chrysostom, Homilies on Acts 26
Witness: *Hom. in Act.* 26, NPNF 1.11.
Repository id: work.john-chrysostom.homilies-on-acts
URL: https://ccel.org/ccel/s/schaff/npnf111/cache/npnf111.txt
Retrieved: 2026-09-30
SHA-256 of the bytes read: 8bdb50c6fd132a9558cbd16808ae05000ddcc7059cfd6c1d282f4f734e539c15 (4443151 bytes)
Loci read: Hom. 26 on Acts 12:12–17.
Quoted: "This is a truth, that each man has an Angel."
Rights: public domain.
Ceiling: NPNF translation.

### Chrysostom, Homilies on Colossians 3
Witness: *Hom. in Col.* 3, NPNF 1.13.
Repository id: work.john-chrysostom.homilies-on-colossians
URL: https://ccel.org/ccel/s/schaff/npnf113/cache/npnf113.txt
Retrieved: 2026-09-29
SHA-256 of the bytes read: 54274dd9aa73ca36e4da9e763e4a27d1818b09e42ffc73795529afec703a4210 (3933882 bytes)
Loci read: Hom. 3 on Col 1:20.
Quoted: the passage on the angels of believers.
Rights: public domain.
Ceiling: NPNF translation.

### Hilary, Tractatus super Psalmos 124, 134
Witness: Hilary, *Tract. in Ps.* 124.6, 134.17, ed. Zingerle, CSEL 22 (1891).
Repository id: work.hilary-of-poitiers.tractatus-super-psalmos
URL: https://archive.org/download/shilariiepiscopi22hila/shilariiepiscopi22hila_djvu.txt
Retrieved: 2026-09-30
SHA-256 of the bytes read: 0c9712d4bb1cabe200b4acc320feb70c4f0a593f59ba902fc897ae006285eb08 (2320546 bytes)
Loci read: 124.5–6; 134.17.
Quoted: 124.6, 134.17 (Latin, glossed).
Rights: public domain.
Ceiling: OCR.

### Ambrose, De viduis 9.55
Witness: *De viduis* 9.55, NPNF 2.10 (de Romestin).
Repository id: NEW work.ambrose.de-viduis — responsible Ambrose; work_type treatise; languages la, en; locus chapter.section.
URL: https://ccel.org/ccel/s/schaff/npnf210/cache/npnf210.txt
Retrieved: 2026-09-29
SHA-256 of the bytes read: 14fa05cc98a67cb1ccf7613e63d5eb80fd48feb3e09dd29210e70f53dfcd7577 (2963575 bytes)
Loci read: 9.54–56.
Quoted: 9.55 (one sentence).
Rights: public domain.
Ceiling: English only; Latin not read.

### Jerome, In Matthaeum III on 18:10
Witness: Jerome, *Commentariorum in Matthaeum* III, Migne PL 26.
Repository id: work.jerome.commentariorum-in-evangelium-matthaei
URL: https://archive.org/download/patrologiaecurs240unkngoog/patrologiaecurs240unkngoog_djvu.txt
Retrieved: 2026-09-29
SHA-256 of the bytes read: 74c5dd24a294e30a8a1de023ef9842b41a79f52410fae49113156b075ce0d046 (4745230 bytes)
Loci read: on Matt 18:7–12.
Quoted: "Magna dignitas animarum ..." (Latin, glossed).
Rights: public domain.
Ceiling: OCR; column not fixed.

### Jerome, In Danielem on 10:13
Witness: Jerome, *Commentaria in Danielem*, PL 25 (1845).
Repository id: work.jerome.commentaria-in-danielem
URL: see manifest `ia-pl25-jerome-1845.txt`
Retrieved: 2026-09-30
SHA-256 of the bytes read: 116c5a253abdc00fd0882e5e102d38d9266b263e4096d0b720b062194cbb4bb9 (4968383 bytes)
Loci read: on 10:13–20.
Quoted: two Latin phrases.
Rights: public domain.
Ceiling: OCR, interleaved columns.

### Cassian, Conferences VIII.13, 17
Witness: Cassian, *Conlationes* VIII.13, 17, NPNF 2.11 (Gibson).
Repository id: work.nicene-and-post-nicene-fathers.series-2-volume-11 (or NEW work.john-cassian.conlationes)
URL: https://ccel.org/ccel/s/schaff/npnf211/cache/npnf211.txt
Retrieved: 2026-09-30
SHA-256 of the bytes read: 8b1206d4e7488c65b5391875fd9570a8a6bcc83270dea35ffe44010c3575d267 (3470230 bytes)
Loci read: VIII.13; VIII.17.
Quoted: VIII.13 (one sentence), VIII.17.
Rights: public domain.
Ceiling: NPNF translation.

### Gregory the Great, Homilies on the Gospels 34
Witness: *Hom. in Ev.* 34.8, 10, Latin (la.wikisource from PL 76).
Repository id: work.gregory-the-great.homiliae-in-evangelia
URL: https://la.wikisource.org/w/index.php?title=Homiliarum_in_Evangelia/XXXIV&action=raw
Retrieved: 2026-09-30
SHA-256 of the bytes read: dfd661ab607de8517fed4ffabddea2bdb80da2591230cb5b9a73efc62d56147f (35028 bytes)
Loci read: 34.7–11.
Quoted: 34.8, 34.10 (Latin phrases, glossed).
Rights: public domain.
Ceiling: Wikisource transcription.

### Gregory the Great, Moralia III and XVII
Witness: *Moralia in Iob*, Library of the Fathers (Oxford 1844–50), vols. 1 and 2.
Repository id: work.gregory-the-great.moralia-in-iob
URL: see manifest `ia-gregory-morals-lf-v1_djvu.txt`, `ia-lf21-gregory-morals-vol2`
Retrieved: 2026-09-29
SHA-256 of the bytes read: 96e0f3706c7a9a427bb3dffa578be87bd66ac96617fc90a7266ce7f241264ad2 (1806303 bytes); f13861be5715cabe5283d5bd7f38cb35c2a1332bd6dc04cf049475b88da5c493 (1916422 bytes)
Loci read: III §§5–7 (on Job 2:6); XVII.12.16–17 (on Job 25:2–3).
Quoted: III §6; XVII.12.17.
Rights: public domain.
Ceiling: OCR; chapter number of III §6 not fixed, so cited by book and section.

### Isidore, Sententiae I.10
Witness: Isidore, *Sententiae* I.10.18–23, PL 83.
Repository id: NEW work.isidore.sententiae — responsible Isidore of Seville; work_type sentences; languages la; locus book.chapter.section.
URL: https://archive.org/download/patrologiae83unknuoft/patrologiae83unknuoft_djvu.txt
Retrieved: 2026-09-30
SHA-256 of the bytes read: e59b2eb652ece1ccf2f4cea6c0a35112dff950a7868c7e97034ee25ede7c0930 (5023656 bytes)
Loci read: I.10.18–23.
Quoted: none (paraphrase).
Rights: public domain.
Ceiling: OCR.

### Bernard, Sermons on Psalm 90 (Qui habitat) 11–13
Witness: Bernard of Clairvaux, *In Psalmum XC Qui habitat sermones XVII*, Migne PL 183, cols. 225–237.
Repository id: NEW work.bernard-of-clairvaux.sermones-in-psalmum-qui-habitat — responsible Bernard of Clairvaux; work_type sermons; languages la; locus sermon.section.
URL: https://archive.org/download/patrologiaecur183mign/patrologiaecur183mign_djvu.txt
Retrieved: 2026-09-30T14:58:15Z
SHA-256 of the bytes read: 05858281218a7e910ff33ea618309ed47106e3588ebe0e4b5589485022f08491 (4631784 bytes)
Loci read: series title; Sermo XI entire; Sermo XII entire; Sermo XIII §1.
Quoted: XI.2, 6, 10; XII.3, 4, 6, 7, 8, 9, 10 (Latin, glossed).
Rights: public domain.
Ceiling: OCR normalized (e.g. "vultum", "nutum", "gloriae", "coheredes", "Habetote"); doubtful readings avoided ("Tunc/Tune audeas", "ab opera/opere", "adjutorem tuum [in] opportunitatibus").

### Bernard, De consideratione V.4.8
Witness: Bernard, *On Consideration*, trans. G. Lewis (Oxford 1908).
Repository id: NEW work.bernard-of-clairvaux.de-consideratione
URL: https://archive.org/download/onconsideration00bern/onconsideration00bern_djvu.txt
Retrieved: 2026-09-30
SHA-256 of the bytes read: 23dacc2ca0c5f0244fe9c456afbdb2a2745767b2281d7553d07899d93416f49e (306976 bytes)
Loci read: V.4.7–8.
Quoted: V.4.8 (one clause).
Rights: public domain (1908).
Ceiling: OCR of translation.

### Honorius Augustodunensis, Elucidarium II.28–29
Witness: *Elucidarium* II.28–29, Migne PL 172, 1154–1155.
Repository id: NEW work.honorius-augustodunensis.elucidarium
URL: https://archive.org/download/patrologiaecur172mign/patrologiaecur172mign_djvu.txt
Retrieved: 2026-09-30T14:59:21Z
SHA-256 of the bytes read: 1c684f8a4792074e498a0a5f41c59092d03c6beac181457c78275e61f8c55a52 (4786925 bytes)
Loci read: II.26–29.
Quoted: II.28 (three Latin sentences), II.29 (one clause).
Rights: public domain.
Ceiling: OCR normalized.

### Peter Lombard, Sententiae II d. 11
Witness: Lombard, *Sententiae* II d. 11 c. 1–2, Quaracchi 1916, pp. 353–355.
Repository id: work.peter-lombard.sententiae
URL: https://archive.org/download/libriivsententia01pete/libriivsententia01pete_djvu.txt
Retrieved: 2026-09-29
SHA-256 of the bytes read: 4cc27eb3178d204a0d8727cb8bdfad2bcd0180a1ded0b9cc9d605b33b59c4cf8 (1592526 bytes)
Loci read: d. 11 c. 1 entire; c. 2 opening.
Quoted: chapter title; two sentences (Latin, glossed).
Rights: public domain (1916).
Ceiling: OCR. The attribution to Gregory is the Master's; Gregory's own locus not read.

### Suárez, De angelis VI.17–19
Witness: Suárez, *De angelis* VI.17–19, Opera omnia t. 2 (Vivès, Paris 1856), pp. 746–765.
Repository id: work.francisco-suarez.de-angelis
URL: https://archive.org/download/rpfranciscisuare02su/rpfranciscisuare02su_djvu.txt
Retrieved: 2026-09-29
SHA-256 of the bytes read: f563a3ff080cfc2c73a5634a3278d8c2a5b7a93b6154c4023c3e819f7d652472 (6655674 bytes)
Loci read: VI.17.1–22; VI.18.1–6; VI.19.1–9, 12; index s.v. Custodia.
Quoted: VI.17.6, 8, 10, 14, 18; VI.19.9 (Latin phrases, glossed); Origen as quoted at VI.17.9.
Rights: public domain.
Ceiling: OCR; chapter heading of VI.17 lost in OCR (running head only).

### Catechism of the Catholic Church 336
Witness: CCC (English, vatican.va).
Repository id: work.catholic-church.catechism
URL: https://www.vatican.va/archive/ENG0015/__P1A.HTM
Retrieved: 2026-09-29
SHA-256 of the bytes read: f5d0972215f47a1bc22e768aa4e51f454db80f32dcbc4e3dd52b4a40ae5254d3 (22605 bytes)
Loci read: 333–336 and n. 202–203.
Quoted: 336.
Rights: Libreria Editrice Vaticana; short quotation with attribution.
Ceiling: web text.

### John Paul II, general audience of 6 August 1986
Witness: Italian text, vatican.va (the English page carries no text).
Repository id: work.john-paul-ii.general-audience-1986-08-06
URL: https://www.vatican.va/content/john-paul-ii/it/audiences/1986/documents/hf_jp-ii_aud_19860806.html
Retrieved: 2026-09-29
SHA-256 of the bytes read: 537f0d3d9e86424b0d34ef5b1248e1993bac6544074fc4b185975953b2cd537f (53326 bytes)
Loci read: nn. 1–8.
Quoted: n. 7 (one sentence), n. 8 (one clause), Italian with gloss.
Rights: LEV; short quotation with attribution.
Ceiling: web text.

### Directory on Popular Piety and the Liturgy (2001)
Witness: CDWDS, English, vatican.va.
Repository id: work.congregation-for-divine-worship-and-the-discipline-of-the-sacraments.directory-on-popular-piety-2001
URL: https://www.vatican.va/roman_curia/congregations/ccdds/documents/rc_con_ccdds_doc_20020513_vers-direttorio_en.html
Retrieved: 2026-09-29
SHA-256 of the bytes read: a9d30018f650a6854f3f13d3691a068a6519c2ebdb8d1fc9a2418ad13b90ed38 (531807 bytes)
Loci read: nn. 213–217.
Quoted: nn. 215, 216, 217 (short).
Rights: Vatican; short quotation with attribution.
Ceiling: web text.

### John Damascene, De fide orthodoxa II.3
Witness: NPNF 2.9 (Salmond).
Repository id: work.john-of-damascus.de-fide-orthodoxa
URL: https://ccel.org/ccel/s/schaff/npnf209/cache/npnf209.txt
Retrieved: 2026-09-29
SHA-256 of the bytes read: 859ba34cc5998f2761b801aa5de724b2ea741a54d98e21614faeb89cc40f8ad4 (2606804 bytes)
Loci read: II.3; II.4 opening.
Quoted: II.3 (guardians of the divisions of the earth).
Rights: public domain.
Ceiling: NPNF translation.

### Augustine, De civitate Dei XIV.6, 15
Witness: NPNF 1.2 (Dods).
Repository id: work.augustine.de-civitate-dei
URL: https://ccel.org/ccel/s/schaff/npnf102/cache/npnf102.txt
Retrieved: 2026-09-29
SHA-256 of the bytes read: 5c973feda803f3e58a88ed7df210b42d436f5466741eb8dbeae713ab56dedae4 (3692898 bytes)
Loci read: XIV.6; XIV.15 (end).
Quoted: XIV.15.
Rights: public domain.
Ceiling: English only.

### Dionysius, Celestial Hierarchy 4, 5, 9, 10
Witness: Parker translation (1899), tertullian.org.
Repository id: work.pseudo-dionysius-the-areopagite.works-part-ii-parker
URL: https://www.tertullian.org/fathers/areopagite_13_heavenly_hierarchy.htm
Retrieved: 2026-09-29
SHA-256 of the bytes read: ae7608cea7b9f874f2b8ebdabfbe9cfae8b74285fec914aeca3d87cd9089104d (114110 bytes)
Loci read: CH 4.3–4, 5, 9.1–4, 10.1–3.
Quoted: 4.4, 9.2 (short).
Rights: public domain.
Ceiling: web transcription.

### Fetched, not used
`ia-bernard-sermons-seasons-v1-1921_djvu.txt` (St. Bernard's Sermons for the Seasons, vol. 1, Dublin 1921): contains no Qui habitat sermon; not used.

## Christ, Mary, and the angels; the Byzantine line

### Aquinas, Summa theologiae, English
- Witness: Thomas Aquinas, *Summa theologiae*, trans. Fathers of the English Dominican Province, 2nd rev. ed. 1920, New Advent online edition.
- Repository ids: `work.thomas-aquinas.summa-theologiae` (existing).
- URL: https://www.newadvent.org/summa/4008.htm, 4030.htm, 4059.htm, 1057.htm, 1064.htm, 1108.htm, 1050.htm, 1052.htm, 1061.htm, 1062.htm, 1063.htm, 1093.htm, 1110.htm, 1012.htm, 4083.htm, 1106.htm, 1113.htm (titles)
- Retrieved: 2026-09-29T12:53:51Z–13:47:25Z; 1093 on 2026-09-30T15:27:55Z; 1012 and 4083 on 2026-09-30T14:23:55Z
- SHA-256 of the bytes read: 40e150ece1b236f941f1322562aedfc70cab94a964c87328f94e7adfc99106bd (62188 bytes)
- Loci read: III q. 8 a. 4 entire; III q. 30 aa. 1–4 entire; III q. 59 a. 6 entire; I q. 57 a. 5 entire; I q. 64 a. 1 obj. 4 and ad 4; I q. 108 a. 8 entire, aa. 5–6 (Gregory citations); I q. 50 a. 1 obj. 1–2, ad 1–2, a. 5 obj. 1, ad 1; I q. 52 a. 2 s.c.; I q. 61 a. 3 obj. 1, co., ad 1; I q. 62 a. 1 co., article titles; I q. 63 aa. 7 (co., ad 1) and 8 (obj. 1); I q. 64 a. 2 (Damascene citation); I q. 93 a. 3 entire; I q. 110 a. 1 co. (Damascene citation); I q. 12 a. 5 co.; III q. 83 a. 4 ad 9; titles of I qq. 106, 113.
- Quoted: III q. 8 a. 4 s.c., co., ad 1–3; III q. 30 a. 1 co., ad 1–2; a. 2 co., ad 1, ad 3 (paraphrase), ad 4; a. 3 s.c., co., ad 3; a. 4 co., ad 1, ad 2; III q. 59 a. 6 obj. 2, s.c., co., ad 2, ad 3; I q. 57 a. 5 co., ad 1; I q. 64 a. 1 ad 4; I q. 108 a. 8 co.; I q. 50 a. 1 ad 1–2, a. 5 ad 1; I q. 61 a. 3 co., ad 1; I q. 63 a. 7 co.; I q. 93 a. 3 co.
- Rights: 1920 translation public domain; New Advent presentation.
- Ceiling: web transcription, not collated with print. New Advent's I q. 93 a. 3 co. contains a duplicated clause ("as God from God; and also in the fact that the whole human soul is in the whole body"); the Latin was quoted for that clause. Aquinas's citations of pseudo-Augustine, pseudo-Jerome, Origen, Maximus, Augustine (*De vera rel.* 31, *De civ. Dei* IX.21, *De sancta virg.* 3) are reported as his citations, not read at their loci.

### Aquinas, Summa theologiae, Latin
- Witness: Leonine text as presented by Corpus Thomisticum.
- Repository ids: `work.thomas-aquinas.summa-theologiae` (existing).
- URL: https://www.corpusthomisticum.org/sth4002.html (III qq. 2ff., for q. 8), sth4027.html (III q. 30), sth4053.html (III q. 59), sth1090.html (I q. 93)
- Retrieved: 2026-09-30T14:53:29Z–14:53:38Z; sth1090 2026-09-30T15:27:58Z
- SHA-256 of the bytes read: 3c6e8783bd7c396063261f33dd7b2d1f4b6356466eca5e07464f202e6401956e (513039 bytes); 5194d64c15bb57bb77bf0c769a4a0c04c646651006837b96b5725ab65290fa26 (436659 bytes); 4d96bdb03adcc441d962b6cbf978fce93293325be47d4a99cf4236f809c132ef (203855 bytes); 6dd5bd042610f3d689584ddfa14ab2245f63e49deea42432ce114219e94c9ad8 (279820 bytes)
- Loci read: III q. 8 a. 4 arg., s.c., co.; III q. 30 pr., aa. 1–4 co., a. 2 ad 1, ad 4; III q. 59 a. 6 s.c., co.; I q. 93 a. 3 co.
- Quoted: III q. 8 a. 4 co. (corpus Ecclesiae mysticum …); III q. 30 a. 1 co. (loco totius humanae naturae), a. 2 ad 1, a. 2 ad 4 (de ordine Archangelorum), a. 3 co. (visione angelica refovendi); I q. 93 a. 3 co. (inquantum … sicut Deus se habet ad mundum; simpliciter / secundum quid).
- Rights: public-domain Latin.
- Ceiling: web transcription of the Leonine text.

### Douay–Rheims (Challoner)
- Witness: Douay–Rheims Bible, Challoner revision, Project Gutenberg eBook 1581.
- Repository ids: `work.english-college-of-douay.douay-rheims-bible` (existing).
- URL: https://www.gutenberg.org/cache/epub/1581/pg1581.txt
- Retrieved: 2026-09-29T12:58:58Z
- SHA-256 of the bytes read: 7d10da78d8ec97db53b4e2bd8719cc01e16106b44937a673ba34aa534a04c007 (5880580 bytes)
- Loci read: every verse listed under Scripture cited.
- Quoted: see Scripture cited (all English Scripture quotations are Douay except Deut 32:8 and Isa 9:6 in the Septuagint, from Brenton).
- Rights: public domain.
- Ceiling: Gutenberg transcription.

### Brenton, Septuagint in English
- Witness: L. C. L. Brenton, *The Septuagint Version of the Old Testament* (English), ebible.org.
- Repository ids: `work.lancelot-brenton.septuagint-english-translation` (existing).
- URL: https://ebible.org/eng-Brenton/ISA09.htm; https://ebible.org/eng-Brenton/DEU32.htm
- Retrieved: 2026-09-30T14:37:43Z–14:37:56Z (fetched by another lane)
- SHA-256 of the bytes read: b411669dc694e59c082ab593d3e3fb64e74a35adf4a4e55c2d347a1d20252540 (6669 bytes); d5709ff7c85ab52d9538e4aaed3b4fbddb3d1a60932c7b7ffcf853ce855516f9 (13928 bytes)
- Loci read: Isa 9:5 (LXX numbering; Vulgate 9:6); Deut 32:8.
- Quoted: Isa 9:6 "the Messenger of great counsel"; Deut 32:8 "set the bounds of the nations according to the number of the angels of God".
- Rights: public domain (19th-c. translation).
- Ceiling: web transcription.

### Dionysius, Celestial Hierarchy (Parker)
- Witness: *Celestial Hierarchy*, John Parker trans., Works vol. 2 (London 1899), tertullian.org transcription.
- Repository ids: `work.pseudo-dionysius-the-areopagite.de-caelesti-hierarchia` (registered with this publication).
- URL: https://www.tertullian.org/fathers/areopagite_13_heavenly_hierarchy.htm
- Retrieved: 2026-09-29T12:55:02Z
- SHA-256 of the bytes read: ae7608cea7b9f874f2b8ebdabfbe9cfae8b74285fec914aeca3d87cd9089104d (114110 bytes)
- Loci read: CH 4.4; CH 7.3.
- Quoted: CH 4.4 (Angels first were initiated … God-formation); CH 7.3 (even the first of the Beings in Heaven …; immediately, and shewing to them …).
- Rights: public domain.
- Ceiling: web transcription; not collated with print.

### Catechism of the Catholic Church
- Witness: CCC, English, vatican.va.
- Repository ids: `work.catholic-church.catechism` (existing).
- URL: https://www.vatican.va/archive/ENG0015/__P1A.HTM
- Retrieved: 2026-09-29T12:56:38Z
- SHA-256 of the bytes read: f5d0972215f47a1bc22e768aa4e51f454db80f32dcbc4e3dd52b4a40ae5254d3 (22605 bytes)
- Loci read: CCC 330–336.
- Quoted: 331 ("Christ is the centre of the angelic world"); 333 (three short phrases).
- Rights: Libreria Editrice Vaticana copyright; short quotations with attribution.
- Ceiling: official web text.

### Irenaeus, Against Heresies
- Witness: ANF vol. 1 (Edinburgh trans., American ed. 1885), CCEL text.
- Repository ids: `work.irenaeus.adversus-haereses` (existing).
- URL: https://ccel.org/ccel/s/schaff/anf01/cache/anf01.txt
- Retrieved: 2026-09-29T12:55:11Z
- SHA-256 of the bytes read: ee9c7f0ac3f4df08d07ddf81cd7e061e82a35e0d27de611cae06f1e05b2fb991 (3149312 bytes)
- Loci read: III.16.6–7.
- Quoted: III.16.6.
- Rights: public domain.
- Ceiling: CCEL transcription.

### John Chrysostom, Homilies on Matthew, Ephesians, Hebrews
- Witness: NPNF series 1 vols 10, 13, 14 (Schaff), CCEL text.
- Repository ids: `work.john-chrysostom.homiliae-in-matthaeum` (existing); `work.john-chrysostom.homilies-on-ephesians` (existing); `work.john-chrysostom.homilies-on-hebrews` (registered with this publication).
- URL: https://ccel.org/ccel/s/schaff/npnf110/cache/npnf110.txt; npnf113; npnf114
- Retrieved: 2026-09-29T17:54:08Z (110); 2026-09-29T12:55:22Z–12:55:23Z (113, 114)
- SHA-256 of the bytes read: adb8f1c9a988c5050a20fb9fdbf75143dcb227e95e3dad2f560a63b757923648 (3345978 bytes); 54274dd9aa73ca36e4da9e763e4a27d1818b09e42ffc73795529afec703a4210 (3933882 bytes); e26f55f8d0739c07d73d5b664e42efbd923a43230a22d93d55261c808e9cd458 (3943878 bytes)
- Loci read: Hom. in Matt. 4.1–10, 13.5, 83.1; Hom. in Eph. 3 (on Eph 1:15–23 and moral part); Hom. in Heb. 3.1–4, 5.1.
- Quoted: Hom. in Matt. 4.10, 13.5, 83.1; Hom. in Eph. 3 (two passages); Hom. in Heb. 3.1, 5.1.
- Rights: public domain.
- Ceiling: CCEL transcription; Hom. in Eph. 3 has no section numbers in this edition.

### Gregory Nazianzen, Orations 38 and 45
- Witness: NPNF series 2 vol. 7, CCEL text.
- Repository ids: `work.gregory-of-nazianzus.oration-38` (registered with this publication); `work.gregory-of-nazianzus.oration-45` (registered with this publication).
- URL: https://ccel.org/ccel/s/schaff/npnf207/cache/npnf207.txt
- Retrieved: 2026-09-29T12:55:25Z
- SHA-256 of the bytes read: 56d84cfa94dee313af0139e2d7f3d4b5f7fffca40ce0f34794b5f56264964dfd (3388014 bytes)
- Loci read: Or. 38 entire (I–XVIII); Or. 45.24–26.
- Quoted: Or. 38.2, 38.11, 38.14, 38.16, 38.17; Or. 45.24, 45.25.
- Rights: public domain.
- Ceiling: CCEL transcription.

### Cyril of Jerusalem, Catechetical Lectures
- Witness: NPNF series 2 vol. 7, CCEL text.
- Repository ids: `work.cyril-of-jerusalem.catechetical-lectures` (existing).
- URL: as above (npnf207)
- Retrieved: 2026-09-29T12:55:25Z
- SHA-256 of the bytes read: 56d84cfa94dee313af0139e2d7f3d4b5f7fffca40ce0f34794b5f56264964dfd (3388014 bytes)
- Loci read: Cat. 14.22–30; Cat. 15.1–33.
- Quoted: Cat. 14.22, 14.24; 15.1, 15.10, 15.21, 15.22, 15.24.
- Rights: public domain.
- Ceiling: CCEL transcription.

### Hilary of Poitiers, On the Trinity
- Witness: NPNF series 2 vol. 9 (Watson and Pullan), CCEL text.
- Repository ids: none registered; the entry cites the edition directly.
- URL: https://ccel.org/ccel/s/schaff/npnf209/cache/npnf209.txt
- Retrieved: 2026-09-29T12:55:27Z
- SHA-256 of the bytes read: 859ba34cc5998f2761b801aa5de724b2ea741a54d98e21614faeb89cc40f8ad4 (2606804 bytes)
- Loci read: De Trin. X.40–41.
- Quoted: X.40 (short), X.41.
- Rights: public domain.
- Ceiling: CCEL transcription.

### Leo the Great, Sermons
- Witness: NPNF series 2 vol. 12 (Feltoe), CCEL text.
- Repository ids: none registered; the entry cites the edition directly.
- URL: https://ccel.org/ccel/s/schaff/npnf212/cache/npnf212.txt
- Retrieved: 2026-09-29T12:55:30Z
- SHA-256 of the bytes read: 7bb1db6e2f6814b58dd13a7b85f17f37f80c22ac979c3298793db1fa909b5b5a (2906681 bytes)
- Loci read: Serm. 21, 26 (Nativity), 73, 74 (Ascension) entire.
- Quoted: Serm. 21.1, 21.2, 26.1, 26.3, 73.4, 74.1, 74.4.
- Rights: public domain.
- Ceiling: CCEL transcription.

### Ambrose, Exposition of Luke
- Witness: *Expositio evangelii secundum Lucam*, Latin Wikisource reproduction of the Corpus Corporum transcription of Migne PL 15.
- Repository ids: `work.ambrose.expositio-evangelii-secundum-lucam` (existing).
- URL: https://la.wikisource.org/w/index.php?title=Expositio_evangelii_secundum_Lucam/II&action=raw; …/X&action=raw
- Retrieved: 2026-09-30T14:57:38Z–14:57:40Z
- SHA-256 of the bytes read: 54d176a8f39bf9ae0703523cd23b0e4e5b0c615a40c6837819d057006443b970 (85898 bytes); d9776febe006764afbd835cfabd0602395fdc6607d1b45d939a5044b93d30e07 (112946 bytes)
- Loci read: II.1–19, 50–53; X.65, 180–181.
- Quoted (Latin, with unquoted gloss): II.8, II.15, II.19, II.50, II.51, II.52, II.53; X.65, X.181.
- Rights: public-domain Latin.
- Ceiling: web transcription of Migne; not collated with CSEL 32.4.

### Bede, Homilies
- Witness: Bede, *Homiliae* I.1 (In festo Annuntiationis), Migne PL 94 (1850), archive.org OCR.
- Repository ids: `work.bede.homiliae-evangelii` (registered with this publication).
- URL: https://archive.org/download/bim_early-english-books-1641-1700_1850_94/bim_early-english-books-1641-1700_1850_94_djvu.txt
- Retrieved: 2026-09-30T14:47:33Z (fetched by another lane)
- SHA-256 of the bytes read: eb888073ed25a141a81b55c90bc447e829babb03ab702a76171633012aadfec5 (3827054 bytes)
- Loci read: Hom. I.1, opening sections (Luke 1:26–28).
- Quoted: two sentences (Aptum profecto … decipiendam; Illa a diabolo … edidit) and one clause (jure angelico … imitari), orthography normalized.
- Rights: public-domain Latin.
- Ceiling: OCR, not checked on page images; PL column not given in the body.

### Gregory the Great, Homilies on the Gospels
- Witness: *Homiliae in Evangelia* 34, Latin Wikisource.
- Repository ids: `work.gregory-the-great.homiliae-in-evangelia` (existing).
- URL: https://la.wikisource.org/w/index.php?title=Homiliarum_in_Evangelia/XXXIV&action=raw
- Retrieved: 2026-09-30T14:47:04Z (fetched by another lane)
- SHA-256 of the bytes read: dfd661ab607de8517fed4ffabddea2bdb80da2591230cb5b9a73efc62d56147f (35028 bytes)
- Loci read: 34.1–12.
- Quoted (Latin with gloss): 34.3, 34.6, 34.11.
- Rights: public-domain Latin.
- Ceiling: web transcription.

### Augustine, Enchiridion
- Witness: NPNF series 1 vol. 3 (Shaw), CCEL text.
- Repository ids: `work.augustine.enchiridion-ad-laurentium` (existing).
- URL: https://ccel.org/ccel/s/schaff/npnf103/cache/npnf103.txt
- Retrieved: 2026-09-29T12:55:20Z
- SHA-256 of the bytes read: cc8d3ff7ce4d4ba293f50a06200af03ff0e5abdeb5200db3a59b4dbe2cad7bdb (3357503 bytes)
- Loci read: Enchir. 29, 62.
- Quoted: 29, 62 (one phrase each).
- Rights: public domain.
- Ceiling: CCEL transcription.

### Bernard of Clairvaux, Homilies Super Missus est
- Witness: *Sermons of St. Bernard on Advent and Christmas, including the famous treatise on the Incarnation called "Missus est"*, compiled and translated at St. Mary's Convent from the 1508 edition, introd. J. C. Hedley (London: R. & T. Washbourne; New York: Benziger, 1909); imprimatur 25 Oct. 1909.
- Repository ids: `work.bernard-of-clairvaux.homiliae-super-missus-est` (registered with this publication).
- URL: https://archive.org/download/sermonsofstberna00bernuoft/sermonsofstberna00bernuoft_djvu.txt
- Retrieved: 2026-09-30T14:54:05Z
- SHA-256 of the bytes read: 15cf43944c2024f84839994bf3294a6820d9080b5a1e959ac70897b10dd3c659 (288038 bytes)
- Loci read: Missus est preface and homm. 1–4 (pp. 22–74).
- Quoted: hom. 1 (pp. 25–26, 30–31), hom. 2 (one phrase), hom. 3 (pp. 48–49), hom. 4 (pp. 68–69).
- Rights: published London 1909, before 1931: public domain in the United States.
- Ceiling: OCR, checked for sense; not collated with the page images or with the Latin (PL 183; Leclercq).

### John Damascene, Exposition of the Orthodox Faith
- Witness: *De fide orthodoxa*, trans. S. D. F. Salmond, NPNF series 2 vol. 9 (CCEL); Greek of Migne PG 94 (archive.org PatrologiaGraeca item, OCR).
- Repository ids: `work.john-of-damascus.de-fide-orthodoxa` (registered with this publication).
- URL: https://ccel.org/ccel/s/schaff/npnf209/cache/npnf209.txt; https://archive.org/download/PatrologiaGraeca/Patrologia%20Graeca%20Vol.%20094_djvu.txt
- Retrieved: 2026-09-29T12:55:27Z; 2026-09-30T14:53:44Z
- SHA-256 of the bytes read: 859ba34cc5998f2761b801aa5de724b2ea741a54d98e21614faeb89cc40f8ad4 (2606804 bytes); 20425e6a8263f916adfcd75dfe76c6f12abdc9bb5c0487691a07a0b15c2dfa5f (9824524 bytes)
- Loci read: II.3 and II.4 entire (English); Greek of II.3 definition, the triads, and the death/fall sentence of II.4; the NPNF prolegomenon on Burgundio's translation; translator's name (Salmond).
- Quoted: II.3 (definition and most sentences on nature, lights, place, ministry, orders, time of creation, creators); II.4 (opening block and the sentences on evil, power, attack, death/fall); Greek transliterated for the definition, the triads, and the death/fall sentence.
- Rights: public domain (1899 translation; Migne).
- Ceiling: PG column numbers inferred from OCR column headers (865; 873–874; 877–878), not checked on page images.

### John Damascene, On Holy Images; Homilies on the Dormition
- Witness: *St John Damascene on Holy Images, followed by Three Sermons on the Assumption*, trans. Mary H. Allies (London 1898; imprimatur 12 Aug. 1898), Project Gutenberg eBook 49917.
- Repository ids: `work.john-of-damascus.homilies-on-the-dormition` (existing); `work.john-of-damascus.contra-imaginum-calumniatores` (registered with this publication).
- URL: https://www.gutenberg.org/cache/epub/49917/pg49917.txt
- Retrieved: 2026-09-30T14:54:06Z
- SHA-256 of the bytes read: a0ba4890b6c020d446f469ea9cb6bf0daebe13f0e24a02a3f58b7bb3dda96de1 (358782 bytes)
- Loci read: Apologies I and III (angel passages); Sermons I and II on the Assumption (angel passages).
- Quoted: De imag. I (one sentence), III (block and several sentences); Hom. in Dorm. I (several sentences), II (two passages).
- Rights: 1898 London publication; public domain in the United States.
- Ceiling: Gutenberg transcription with transcriber's minor emendations; no page numbers; Allies's Greek parentheses omitted with ellipsis.

### Maximus the Confessor, Mystagogia
- Witness: *Mystagogia*, Greek text of Migne PG 91 (archive.org PatrologiaGraeca, Vol. 091).
- Repository ids: `work.maximus-the-confessor.mystagogia` (registered with this publication).
- URL: https://archive.org/download/PatrologiaGraeca/Patrologia%20Graeca%20Vol.%20091_djvu.txt; page images via the item's jp2.zip (leaves 367, 369, 380)
- Retrieved: 2026-09-30T14:53:41Z (OCR); page images 2026-09-30
- SHA-256 of the bytes read: e4e1c1926ec2dfd9fd71f276ca125866230230507d7727455e66cf40d3fca85c (7890188 bytes)
- Loci read: chs. 13, 19, 24 (Greek), 20–21 incipits; Migne's Latin of ch. 24 on the page image (col. 710).
- Quoted (Greek transliterated, own rendering unquoted): ch. 13 (PG 91, 692C–D; checked on page image); ch. 19 (696C; checked on page image); ch. 24 phrase (709; OCR, consistent with the Latin read on the image).
- Rights: public domain.
- Ceiling: OCR plus page-image checks as stated.

### Theodore the Studite, Orations 5 and 6
- Witness: Migne PG 99 (archive.org PatrologiaGraeca Vol. 099): Or. 5 In dormitionem Deiparae; Or. 6 In sanctos angelos (Εἰς τὴν σύναξιν τῶν οὐρανίων ταγμάτων), from A. Mai's *Nova Patrum Bibliotheca*.
- Repository ids: none registered; the entry cites the edition directly.
- URL: https://archive.org/download/PatrologiaGraeca/Patrologia%20Graeca%20Vol.%20099_djvu.txt; page images via jp2.tar (leaves 365–368)
- Retrieved: 2026-09-30T14:53:50Z (OCR); images 2026-09-30
- SHA-256 of the bytes read: af55f76d4179c09f4f808d2de05c9a4400a4fd45c0fa665aae1fb5cf437a00bb (9580329 bytes)
- Loci read: Or. 5.5 (col. 728); Or. 6.1–3 (cols. 729–736) with Mai's note (col. 730).
- Quoted (Greek transliterated): Or. 5.5 (checked on image); Or. 6.1 and 6.2 phrases (checked on images, cols. 729, 732, 733); Or. 6.3 phrase ton trisagion tēs Triados mēnyonta thesmon (OCR only).
- Rights: public domain.
- Ceiling: attribution of Or. 6 is Mai's; Mai notes an altered excerpt printed among Chrysostom's spuria.

### Andrew of Caesarea, Commentary on the Apocalypse
- Witness: Migne PG 106 (archive.org PatrologiaGraeca Vol. 106), Greek with Latin.
- Repository ids: `work.andrew-of-caesarea.commentarius-in-apocalypsin` (registered with this publication).
- URL: https://archive.org/download/PatrologiaGraeca/Patrologia%20Graeca%20Vol.%20106_djvu.txt
- Retrieved: 2026-09-30T14:53:53Z
- SHA-256 of the bytes read: 7b0567d128f8a25a8d1f3380bfb05c8b791b0704d5647898eb26ac2031b0c530 (7148801 bytes)
- Loci read: ch. 21 (on Apoc 8:3–4); ch. 34 (on Apoc 12:7–9) with the Papias fragment.
- Quoted (Greek transliterated): ch. 21 one sentence; ch. 34 two phrases.
- Rights: public domain.
- Ceiling: OCR only; not checked on page images; PG column numbers not established (no hOCR index for this volume), so the body cites "PG 106" without column.

### Gregory Palamas, One Hundred and Fifty Chapters
- Witness: *Capita physica, theologica, moralia et practica CL*, Migne PG 150 (archive.org PatrologiaGraeca Vol. 150).
- Repository ids: `work.gregory-palamas.capita-150` (registered with this publication).
- URL: https://archive.org/download/PatrologiaGraeca/Patrologia%20Graeca%20Vol.%20150_djvu.txt; page images via jp2.zip (leaves 596–597, 601, 610–611)
- Retrieved: 2026-09-30T14:53:57Z (OCR); images 2026-09-30
- SHA-256 of the bytes read: 4a5d98a2a7645b490dcc9e8500a060231e10dbc5c6441f54cb68280feebb09e5 (6994915 bytes)
- Loci read: Cap. 27–28, 38–40, 60–66.
- Quoted (Greek transliterated, checked on page images): Cap. 27 (1140A), 39 (1148B), 62 (1165A), 62 phrase, 63 phrase (1165D), 64 (1168A), 65 (1168C, with DN 4.8).
- Rights: public domain (Migne). English translations (Sinkewicz 1988) are in copyright and were not used.
- Ceiling: page images for every quoted phrase; paraphrase elsewhere from OCR.

### Denzinger (Nicaea II; Constantinople IV)
- Witness: Denzinger, *Enchiridion symbolorum*, Latin, patristica.net.
- Repository ids: `work.denzinger.enchiridion-symbolorum` (existing).
- URL: https://patristica.net/denzinger/enchiridion-symbolorum.html
- Retrieved: 2026-09-29T12:56:36Z
- SHA-256 of the bytes read: 604f24c46e0bc71c2018f25dc787a9ab421d4b2e9cf7d1cee1f43e910ef2708f (2333435 bytes)
- Loci read: DS 600–603 (Nicaea II, definition on images, 13 Oct. 787); DS 655–656 (Constantinople IV, can. 3; heading "oecum. VIII", 870).
- Quoted: DS 600 (sequentesque … Ecclesiae; tam videlicet … Sanctorum), DS 601 (veram latriam …; Imaginis enim honor …), DS 656 (insuper et iconas …).
- Rights: public-domain Latin text.
- Ceiling: web transcription; source typo "honrobiliumque" normalized to "honorabiliumque".

### Second Vatican Council, Lumen gentium
- Witness: Latin and English, vatican.va.
- Repository ids: `work.second-vatican-council.lumen-gentium` (existing).
- URL: https://www.vatican.va/archive/hist_councils/ii_vatican_council/documents/vat-ii_const_19641121_lumen-gentium_lt.html; English at https://www.vatican.va/archive/hist_councils/ii_vatican_council/documents/vat-ii_const_19641121_lumen-gentium_en.html (local copy .scratch/christ-liturgy/lg.txt)
- Retrieved: Latin 2026-09-30T14:59:02Z; English copy 2026-09-29 (christ-liturgy scratch)
- SHA-256 of the bytes read: 0a828abb4be1de13b600bbc9bbae32832ed5ce4dad940629f57aae54c679fe23 (192411 bytes)
- Loci read: LG 49–50, 53, 56, 59, 66, 69.
- Quoted (Latin with gloss): 56, 66, 69.
- Rights: Vatican text; short quotations with attribution.
- Ceiling: official web text.

### Pius XII, Ad caeli Reginam; Munificentissimus Deus
- Witness: vatican.va Latin and English.
- Repository ids: `work.pius-xii.ad-caeli-reginam` (registered with this publication); `work.pius-xii.munificentissimus-deus` (existing).
- URL: https://www.vatican.va/content/pius-xii/la/encyclicals/documents/hf_p-xii_enc_11101954_ad-caeli-reginam.html (and /en/); https://www.vatican.va/content/pius-xii/la/apost_constitutions/documents/hf_p-xii_apc_19501101_munificentissimus-deus.html (and /en/)
- Retrieved: 2026-09-30T14:59:04Z–14:59:10Z
- SHA-256 of the bytes read: 56079ef76d8496821ead5fdf4d0c0f6e9bdd82281b1e89e70ae3ec1d5e671b80 (67390 bytes); 2c84ef30841b66359d28d526a3aed585d6aa6aafbed3054fd564cf907d6a371f (74564 bytes)
- Loci read: ACR 3, 30, 31, 41–42, 46–47, notes 55, 56, 61; MD definition and the paragraphs citing the angels (Albert the Great).
- Quoted: ACR Latin 3, 41, 42, 46; MD Latin definition; MD English two short phrases; MD Latin Albert phrase.
- Rights: Vatican texts; short quotations with attribution.
- Ceiling: Pius IX's *Ineffabilis Deus* read only as quoted in ACR 41–42; ACR paragraph numbers follow the English edition.

### Missale Romanum 1962
- Witness: *Missale Romanum*, editio typica 1962 (CMAA facsimile PDF), text layer extracted with pdftotext.
- Repository ids: `work.catholic-church.missale-romanum` (existing).
- URL: https://media.churchmusicassociation.org/pdf/missale62.pdf (local copy .scratch/christ-liturgy/missale62.pdf, sha256 648fdb8f…)
- Retrieved: 2026-09-29 (christ-liturgy scratch)
- Loci read: 31 May B.M.V. Reginae (II cl.), Introit n. 2681; 16 July Introit n. 3054; 15 Aug. Assumption (I cl.), Alleluia n. 3382; 29 Sept. Dedication of St Michael (I cl.), nn. 3726–3731; Paschal preface; Canon, Supplices.
- Quoted (Latin with gloss): n. 2681 Introit; n. 3382 Alleluia; n. 3727 collect (incipit); preface ending; Supplices clause.
- Rights: Latin liturgical text; quoted briefly.
- Ceiling: text layer only, not checked on page images.

### Manual of Prayers (Baltimore, 1889)
- Witness: *A Manual of Prayers for the Use of the Catholic Laity* (New York: Catholic Publication Society; London: Burns & Oates, 1889), archive.org manualofprayersf00wood.
- Repository ids: `work.third-plenary-council-of-baltimore.manual-of-prayers` (existing).
- URL: https://archive.org/download/manualofprayersf00wood/manualofprayersf00wood_djvu.txt; page images page/n62, n63, n74, n84, n85
- Retrieved: 2026-09-30T14:54:08Z (OCR); images 2026-09-30
- SHA-256 of the bytes read: eada18d4949720fcef1f031d067136c3dba908d2d3142c62f15bcfe54fc0c33f (1379047 bytes)
- Loci read: pp. 55–56 (Angelus), 67 (Litany of Loreto), 77–78 (Ave Regina caelorum).
- Quoted: Angelus versicle and collect (p. 55–56); Regina Angelorum / Queen of Angels (p. 67); Ave Regina caelorum, first two lines, Latin and English (p. 77). All checked on page images.
- Rights: 1888 US copyright expired; public domain.
- Ceiling: verified on page images.

### Hapgood, Service Book (1906)
- Witness: Isabel F. Hapgood, *Service Book of the Holy Orthodox-Catholic Apostolic (Greco-Russian) Church* (1906; printed by H. O. Houghton & Co.), Cornell copy, archive.org cu31924029363128.
- Repository ids: `work.isabel-florence-hapgood.service-book` (registered with this publication).
- URL: https://archive.org/download/cu31924029363128/cu31924029363128_djvu.txt; page numbers via the item's hOCR page index and page_numbers.json
- Retrieved: 2026-09-30T14:54:01Z
- SHA-256 of the bytes read: 2b9e6ed4cb7d488c88fa5a17fb96479c3f3c0360fb81f78190654682f1d3f650 (1883883 bytes)
- Loci read: calendar p. xiv; table p. xxiv; Vespers dismissal p. 14; weekday hymns p. 61; Divine Liturgy pp. 83–102, 126; Annunciation pp. 201–202; Falling-asleep pp. 264–266.
- Quoted: pp. xiv, 14, 61, 83, 85, 86, 94, 95, 101, 102, 201, 202, 264, 266.
- Rights: 1906 US publication; public domain.
- Ceiling: OCR text layer; page numbers from the hOCR index; not checked on page images.

### Synaxarium Ecclesiae Constantinopolitanae (Delehaye 1902)
- Witness: *Synaxarium Ecclesiae Constantinopolitanae e codice Sirmondiano*, ed. H. Delehaye, Propylaeum ad Acta Sanctorum Novembris (Brussels 1902), archive.org DelehayeSynaxariumConstantinopolitanum.
- Repository ids: none registered; the entry cites the edition directly.
- URL: https://archive.org/download/DelehayeSynaxariumConstantinopolitanum/Delehaye%2C%20Synaxarium%20Constantinopolitanum_djvu.txt; page image leaf 76
- Retrieved: 2026-09-30T15:17:43Z
- SHA-256 of the bytes read: df11361ff4d76de50776e24d4ca50e3cd3dc2f54ce16c193ff3decd9c297f62f (5639177 bytes)
- Loci read: 6 Sept. (cols. 19–20); 25 Sept. (cols. 79–80); 8 Nov. (cols. 203–204, also on the page image); Delehaye's prolegomena note on the angel feasts.
- Quoted (Greek transliterated): 6 Sept. phrases (anamnēsin poioumenoi tou thaumatos; chōneuesthai); 25 Sept. sentence; 8 Nov. sentence (Proschōmen; synaxis … henōsis).
- Rights: 1902; public domain.
- Ceiling: OCR; the scan is low resolution; the 8 Nov. entry was checked on the page image. The Synaxarion names the fallen taxiarch; the name is not given in the body.

### Not used
- Metropolitan Cantor Institute, online Menaion 8 November (.scratch/christ-liturgy/nov8.txt; https://mci.archpitt.org/menaion/11-08.html): modern translation, rights unresolved; not quoted, not relied on.

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

## Liturgy, devotion and its regulation, calendar, names

General normalizations in all Latin quotations (not otherwise noted): æ/œ ligatures resolved to ae/oe; accents and diaeresis (Mame, Tours printings: é, Michaël) dropped; long s (PL 25) printed as s; chant syllable hyphens removed (Rituale 1872 In paradisum; 1920 Exsultet). Spelling, j/i, capitals and punctuation otherwise as printed. English quotations exactly as printed, except that `o'ertheazure` etc. were read on the page image.

### Missale Romanum, typical edition of 1920 (Internet Archive scan)
- Witness: Missale Romanum, editio typica Vaticana 1920 (scan of a 1951–54 body / post-1970 appendix printing; see repository artifact record).
- Repository ids: `edition.catholic-church.missale-romanum.vatican-typica-1920` (existing).
- URL: https://archive.org/download/MissaleRomanumBenedettoXV/Missale%20Romanum%20Benedetto%20XV_djvu.txt
- Retrieved: 2026-09-30
- SHA-256 of the bytes read: aa6461961702b5cbae51460a7385f7a982c6f5a2649822d0bb8d5f13b6b387e0 (2918085 bytes)
- Loci read: kalendarium (24 Mar, 8 May, 29 Sept, 2 Oct, 24 Oct); proper headings 8 May and 29 Sept; Sabbato Sancto litany and Exsultet (Benedictio Cerei, p. 233); Canon (Supplices, pp. 338–339); Missae pro defunctis, Offertory.
- Quoted: Supplices (to "majestatis tuae … repleamur"); Exsultet opening; Holy Saturday litany invocations of angels; Requiem Offertory.
- Rights: underlying 1920 typical edition and older text public domain (US, pre-1931; 17 USC 103(b)); only pre-1920 matter quoted, per the artifact record's own list of quotable parts.
- Ceiling: OCR text layer only; not collated with a page image. The kalendarium line for 29 Sept reads "duplex II classis" while the proper heading reads "Duplex I classis" (see Open issues).

### Missale Romanum, Tours: Mame, 1922 (editio quarta iuxta typicam Vaticanam)
- Repository ids: `edition.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam` (existing).
- URL: https://archive.org/download/missaleromanum0000unse/missaleromanum0000unse_djvu.txt
- Retrieved: 2026-09-30
- SHA-256 of the bytes read: e30d731cefbc25b1c806e49365c9cdb0fc54ad4a36ee08e7d544f2f024bbc9f6 (2393514 bytes)
- Loci read: kalendarium (March, May [OCR scrambled], September, October); pp. 552–554 (S. Gabrielis); pp. 592–593 (8 May); pp. 725–729 (29 Sept; 2 Oct); pp. 741–743 (S. Raphaelis).
- Quoted: collects of 24 Mar and 24 Oct; Secret and Postcommunion clauses of 24 Mar, 8 May/29 Sept, 2 Oct, 24 Oct; Alleluia verses; rubric "Missa Benedicite, ut in die 8 Maji … praeter ritum".
- Rights: public domain (US, published 1922).
- Ceiling: OCR only; accents dropped; not page-image collated.

### Missale Romanum 1962 (CMAA facsimile)
- Repository ids: none registered; the entry cites the edition directly.
- Retrieved: local copy (GPT scratch); extracted with pdftotext -layout to work/missale62.txt on 2026-09-30.
- Loci read: kalendarium (March, May, Sept, Oct); pp. 493, 670–672, 695; appendix Missae pro aliquibus locis p. [161] (page image, PDF p. 969).
- Quoted: only the rubric at p. [161] ("Eodem die 8 maii. In Apparitione S. Michaelis Archangeli. Missa Benedicite, ut in Missali, die 29 septembris").
- Rights: 1962 edition not cleared for reproduction; used for facts (dates, ranks, structure) and one short rubric quotation. All other Latin of these Masses quoted from 1920/1922/1898 witnesses.
- Ceiling: text layer + one page image.

### Repository calendar indexes
- Witness: src/sources/calendars/roman-1962/propers.yaml; postconciliar/propers.yaml; roman-pre-1955/propers.yaml and rubrics.yaml (read-only).
- Repository ids: none registered; the entry cites the edition directly.
- Loci read: 1962 entries 1962-03-24, 1962-09-29, 1962-10-02, 1962-10-24; postconciliar pc-09-29 (OLM n. 647), pc-10-02 (OLM n. 650), and absence of angel entries on 03-24, 05-08, 10-24 (10-24 is St Anthony Mary Claret); pre-1955 header (structural projection from 1962; no angel departures).
- Quoted: none (ranks and reading assignments only).
- Rights: facts.
- Ceiling: the pre-1955 index inherits from 1962 uncollated, so pre-1955 ranks were read in the 1920/1922 Missals and the 1898 Breviary instead.

### Cummiskey, The Roman Missal … for the use of the laity (Philadelphia, 1861)
- Repository ids: `edition.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861` (existing).
- URL: repository TSVs (transcribed from IA romanmissaltran00churgoog page images).
- Retrieved: repository tracked artifacts (2026-08-20).
- Loci read: pp. xvi–xix, xxiv–xxv, xxviii–xxxii, xxxvii–xxxviii.
- Quoted: Gloria incipit (Latin/English), Confiteor (abridged), incense prayer, Common Preface, Trinity/Nativity/Pentecost clauses, Sanctus, Supplices (English).
- Rights: public domain (US).
- Ceiling: repository transcriptions from page images (verified by that lane); the book's Latin is a lay missal's, not the altar book.

### Cummiskey, The Roman Missal … (Philadelphia, 1843)
- Repository ids: `edition.eugene-cummiskey.roman-missal-english-laity.philadelphia-1843` (existing).
- Loci read: pp. 666–670 (Michaelmas; Guardian Angels), Holy Saturday blessing of the candle (p. 302/303), Masses for the Dead offertory.
- Quoted: Alleluia verses of Michaelmas (English); "Let now the heavenly troop of angels rejoice"; Requiem Offertory English clause.
- Rights: public domain.
- Ceiling: OCR only (noisy); only clean phrases quoted.

### Breviarium Romanum (Tours: Mame, 1898), Pars autumnalis and Pars verna
- Repository ids: `work.catholic-church.breviarium-romanum` (registered with this publication).
- URL: https://archive.org/download/breviariumromanu18984cath/breviariumromanu18984cath_djvu.txt (autumnalis); https://archive.org/download/breviariumromanu21898cath/breviariumromanu21898cath_djvu.txt (verna)
- Retrieved: 2026-09-30
- SHA-256 of the bytes read: c61dd243e5b6c69a9c753d6c9d66da0bb34c726c2e74e027f64f17938240d5a0 (2529391 bytes)
- Loci read: Autumn pp. 151 (Compline collect), 378–385 (29 Sept), 397–403 (2 Oct); Spring pp. 568–573 (8 May). Page images read: Autumn pp. 381 (leaf 426), 383–385 (leaves 428–430), 387, 399–401 (leaves 444–446), 404.
- Quoted: Compline collect; Te splendor (stanzas 2–3); Christe sanctorum (stanzas 2–4); collect Deus qui miro ordine; Gregory lesson iv (nine orders); Jerome lesson ix sentence; Lauds antiphon 5; Magnificat antiphon Princeps gloriosissime; responsory titles; Custodes hominum stanza 1; Lauds hymn lines; collect of 2 Oct; Bernard lesson v; Hilary lesson ix; 8 May lessons iv–vi (iv entire; phrases of v–vi).
- Rights: public domain (1898).
- Ceiling: OCR plus page images of the Michaelmas and Guardian Angels leaves; Spring volume OCR only.

### The Roman Breviary, translated by John, Marquess of Bute (Edinburgh: Blackwood, 1908), vols II and IV
- Repository ids: none registered; the entry cites the edition directly.
- URL: https://archive.org/download/romanbreviary04unknuoft/romanbreviary04unknuoft_djvu.txt; https://archive.org/download/theromanbreviary02unknuoft/theromanbreviary02unknuoft_djvu.txt
- Retrieved: 2026-09-30
- SHA-256 of the bytes read: cd9ea44377988ffc25d458795aed7b1782ec1e001dd5136a416494f002234f8f (2991278 bytes)
- Loci read: IV kalendar; pp. 209–210 (Compline), 591–600 (Michaelmas), 613–619 (Guardian Angels), 684–686 (St Raphael); II kalendar, pp. 866–871 (8 May).
- Quoted: English of the Compline collect, Michaelmas martyrology, invitatory, Gregory lessons iv–vi, Jerome lesson ix, Lauds antiphon, Copeland's Lauds hymn, collect, Magnificat antiphon, Caswall's Custodes hominum and Lauds hymn lines, Bernard lessons iv–vi, Hilary lesson ix, Guardian Angels collect, 8 May lessons iv–vi, Raphael lesson vi.
- Rights: public domain (US, 1908; translator d. 1900; hymn translators Neale, Copeland, Caswall d. before 1885).
- Ceiling: OCR only; clean passages. Bute renders "in summo circo" (8 May, lesson vi) as "on Hadrian's Mole"; the body quotes the Latin and names Bute's rendering.

### Rituale Romanum (Ratisbon: Pustet, 1872)
- Repository ids: `edition.catholic-church.rituale-romanum.latin-ratisbon-1872` (existing).
- URL: https://archive.org/download/ritualeromanumpa00cath_0/ritualeromanumpa00cath_0_djvu.txt
- Retrieved: 2026-09-30
- SHA-256 of the bytes read: 412f153295e3bc62c35938cdf26c1101ea9d1ccc570bb3f814fc8c4b93c1622d (905571 bytes)
- Loci read: Ordo commendationis animae pp. 115–116; In exspiratione pp. 131–132; Exsequiarum ordo p. 141.
- Quoted: Proficiscere (to "Prophetarum"), "splendidus Angelorum coetus occurrat", Subvenite, In paradisum.
- Rights: public domain.
- Ceiling: OCR only.

### A Manual of Prayers for the Use of the Catholic Laity (New York, 1889)
- Repository ids: `edition.third-plenary-council-of-baltimore.manual-of-prayers.new-york-catholic-publication-society-1889` (existing).
- URL: https://archive.org/download/manualofprayersf00wood/manualofprayersf00wood_djvu.txt
- Retrieved: 2026-09-30
- SHA-256 of the bytes read: eada18d4949720fcef1f031d067136c3dba908d2d3142c62f15bcfe54fc0c33f (1379047 bytes)
- Loci read: pp. 531–532 (page images leaves n538–n539), 583–584.
- Quoted: English of the Subvenite and In paradisum.
- Rights: public domain (US; 1888 copyright expired).
- Ceiling: Subvenite page-image verified; In paradisum OCR only.

### The Raccolta, trans. Ambrose St John (London: Burns & Oates, 1910)
- Repository ids: none registered; the entry cites the edition directly.
- URL: https://archive.org/download/theraccoltaorcol00unknuoft/theraccoltaorcol00unknuoft_djvu.txt
- Retrieved: 2026-09-30
- SHA-256 of the bytes read: 5d6f8c594e1266b941020c510dd8e71d778655833c495f5b3268866fea138e85 (728786 bytes)
- Loci read: nn. 182 (pp. 150–152), 289–297 (pp. 259–267). Page images: pp. 151–152, 259–263, 266–267.
- Quoted: Angelus V/R and collect clause; Te splendor English stanzas; Princeps gloriosissime and collect (English); Angelical Crown (salutations, antiphon, versicle, collect clause); n. 292 opening and closing clauses; n. 293 antiphon; n. 295 prayer to St Raphael (entire); n. 296 Angele Dei (Latin, English, rhymed).
- Rights: public domain (1910).
- Ceiling: page-image verified for every quoted passage.

### Collectio precum piorumque operum (Typis Polyglottis Vaticanis, 1929)
- Repository ids: `work.apostolic-penitentiary.collectio-precum-piorumque-operum-1929` (registered with this publication); `work.apostolic-penitentiary.enchiridion-indulgentiarum` (existing).
- URL: https://archive.org/download/precesetpiaopera0000vari_c6f1/precesetpiaopera0000vari_c6f1_djvu.txt
- Retrieved: 2026-09-30
- SHA-256 of the bytes read: 085be3683d33e8a80b3fcd8adc36a30e215f8bd76eca7417eaf6d7e4f1896c76 (419403 bytes)
- Loci read: n. 331, pp. 327–328 (page image leaf n343), p. 329 (leaf n344).
- Quoted: Latin of the prayer to St Michael after Low Mass; indulgence note (S. Rituum C., 6 Ian. 1884 et 24 Nov. 1915).
- Rights: public domain in the US (published 1929; US term expired 1 Jan 2025).
- Ceiling: page-image verified.

### Key of Heaven (Baltimore: J. Murphy, 1901)
- Repository ids: `work.anonymous.key-of-heaven` (registered with this publication).
- URL: https://archive.org/download/KeyOfHeaven/KeyOfHeaven_djvu.txt
- Retrieved: 2026-09-30
- SHA-256 of the bytes read: d7c06c2714928a4e4d4319d957b451bf72c75f8f56097bbabe30af7bc737ac52 (473013 bytes)
- Loci read: pp. 138–141 (page images leaves n151–n153).
- Quoted: heading, prayer "O God, our refuge" clause, English prayer to St Michael, indulgence line.
- Rights: public domain (1901).
- Ceiling: page-image verified.

### Jacobus de Voragine, The Golden Legend, Caxton's English ed. F. S. Ellis (Temple Classics, London: Dent, 1900), vol. V
- Repository ids: `work.jacobus-de-voragine.legenda-aurea` (registered with this publication).
- URL: https://archive.org/download/goldenlegendorli05jaco/goldenlegendorli05jaco_djvu.txt
- Retrieved: 2026-09-30
- SHA-256 of the bytes read: 5b206a6715b1d484be64f48203f450292acb66cb1d4f9393e69db32ceaf0b1ec (535024 bytes)
- Loci read: "The Feast of S. Michael", pp. 180–186.
- Quoted: Gargano (Michael's words), Tumba (second apparition), tide miracle, Gregory's vision over Hadrian's mausoleum.
- Rights: public domain (Caxton 1483; Ellis ed. 1900).
- Ceiling: OCR only. The Latin (Graesse 1846) fetch failed (HTTP 500); English only.

### Sacramentarium Leonianum, ed. C. L. Feltoe (Cambridge, 1896)
- Repository ids: `edition.catholic-church.sacramentarium-veronense.feltoe-1896` (existing).
- URL: https://archive.org/download/sacramentariumle00cath/sacramentariumle00cath_djvu.txt
- Retrieved: 2026-09-30
- SHA-256 of the bytes read: 7e7e82fe4e8990ec557a914b6ec768c99e174623f8acba606654280845cad21b (672888 bytes)
- Loci read: pp. 106–108 (XXVI Prid. Kal. Oct., N[atale] basilicae Angeli in Salaria) and editor's notes p. 106.
- Quoted: Preface "Vere dignum … ministrorum"; clause "quae etsi humano generi … intuitu"; Secret clause; Postcommunion clause.
- Rights: public domain (ancient text; 1896 edition).
- Ceiling: OCR; abbreviated words (Dne) avoided in quotations.

### Gregorian Sacramentary, ed. H. A. Wilson (HBS, 1915)
- Repository ids: `edition.catholic-church.sacramentarium-gregorianum-hadrianum.wilson-1915` (existing).
- URL: https://archive.org/download/gregoriansacrame00cath/gregoriansacrame00cath_djvu.txt
- Retrieved: 2026-09-30
- SHA-256 of the bytes read: 3613cce6277a9d68a9554457c590affef959023675170d1abc4d8b28ebd76a20 (979250 bytes)
- Loci read: III Kal. Oct., Dedicatio basilicae sancti Angeli, pp. 105–106.
- Quoted: none verbatim beyond the heading words; collect identity, Secret and Postcommunion reading "quos honore prosequimur" reported.
- Rights: public domain.
- Ceiling: OCR.

### Gelasian Sacramentary, ed. H. A. Wilson (1894)
- Repository ids: `edition.catholic-church.sacramentarium-gelasianum-vetus.wilson-1894` (existing).
- URL: https://archive.org/download/gelasiansacrame00wilsgoog/gelasiansacrame00wilsgoog_djvu.txt
- Retrieved: 2026-09-30
- SHA-256 of the bytes read: 039123ca029bf1684b2e8b0dec014cc3fa9057ecb30da3494f7165cb89684d84 (1098845 bytes)
- Loci read: Book II, "Orationes in Sancti Archangeli Michaelis, iii Kal. Octobres" (p. 200); appendix Gerbert list.
- Quoted: none (read as control).
- Rights: public domain. Ceiling: OCR.

### Gregory the Great, Homiliae in Evangelia 34
- Repository ids: `work.gregory-the-great.homiliae-in-evangelia` (existing).
- URL: https://la.wikisource.org/w/index.php?title=Homiliarum_in_Evangelia/XXXIV&action=raw
- Retrieved: 2026-09-30 (shared cache)
- SHA-256 of the bytes read: dfd661ab607de8517fed4ffabddea2bdb80da2591230cb5b9a73efc62d56147f (35028 bytes)
- Loci read: 34.7–34.11.
- Quoted: 34.8 ("angelorum vocabulum…", "sed cum ad nos…"); 34.9 (names; "quia nullus potest…"; "qui se ad Dei similitudinem…"; "quia ad Dei similitudinem…"); 34.10 (Seraphim, Powers clause); 34.11 ("distinctae namque conversationes…", "quorum cor in igne…"). Lessons iv–vi also read in the Breviary and in Bute.
- Rights: public domain. Ceiling: Wikisource transcription of PL 76; not collated with Migne page.

### Gregory the Great, Dialogues IV (English 1608, ed. E. G. Gardner, 1911)
- Repository ids: `work.gregory-the-great.dialogi` (registered with this publication).
- URL: https://www.tertullian.org/fathers/gregory_04_dialogues_book4.htm
- Retrieved: 2026-09-30 (shared cache)
- SHA-256 of the bytes read: c0fcbac5f0d6cbf6a192398f793368cf85d2e26253db4a40d0edd116c43698b1 (202560 bytes)
- Loci read: IV.58. Quoted: IV.58 ("for what right believing Christian … invisible?").
- Rights: public domain. Ceiling: web transcription; p. 256 from the transcription's page marker.

### Jerome, Commentarii in Danielem (PL 25)
- Repository ids: `work.jerome.commentaria-in-danielem` (existing).
- URL: https://archive.org/download/bim_early-english-books-1641-1700_patrologiae-cursus-completus-_1845_25/…_djvu.txt
- SHA-256 of the bytes read: 116c5a253abdc00fd0882e5e102d38d9266b263e4096d0b720b062194cbb4bb9 (4968383 bytes)
- Loci read: on Dan 8:16–17. Quoted: "fortitudo, vel robustus Dei"; "qui praepositus est praeliis"; "Raphael mittitur"; "curatio; vel medicina Dei"; "Michael dirigitur, qui interpretatur quis sicut Deus".
- Rights: public domain. Ceiling: OCR (long s); column number not established.

### Jerome, Hilary, Bernard as read in the Breviary
- Jerome, In Matth. III on 18:10 (work.jerome.commentariorum-in-evangelium-matthaei); Hilary, In Matth. on c. 18 (NEW work.hilary-of-poitiers.commentarius-in-matthaeum); Bernard, Sermon on Ps 90 "Qui habitat" (NEW work.bernard-of-clairvaux.sermones-super-psalmum-qui-habitat). Read and quoted only as the Roman Breviary 1898 prints them (lessons) and in Bute's English; not read at their own editions. Aquinas's s.c. citation of Jerome (I q.113 a.5) read.

### Isidore, Etymologiae VII.5
- Repository ids: `work.isidore.etymologiae` (existing).
- URL: https://www.thelatinlibrary.com/isidore/7.shtml; Retrieved 2026-09-29; Cache text/ll-isidore-etym07.txt
- Loci read: VII.5.1–33. Quoted: VII.5.2, 5.15 ("Vriel interpretatur…"), 5.19 clause.
- Rights: public domain. Ceiling: web transcription.

### Origen, De principiis I.5.5 (trans. Crombie, ANF 4)
- Repository ids: `work.origen.de-principiis` (existing).
- SHA-256 of the bytes read: b9f385a048c18158c2f74dcd37062f48a1c68a5d05bdb07270a93692d172da2e (4237225 bytes)

### Cyril of Jerusalem, Catechetical Lecture 23 (Mystagogical 5).6 (Gifford, NPNF II.7)
- Repository ids: `work.cyril-of-jerusalem.catechetical-lectures` (existing).
- SHA-256 of the bytes read: 56d84cfa94dee313af0139e2d7f3d4b5f7fffca40ce0f34794b5f56264964dfd (3388014 bytes)

### Thomas Aquinas, Summa theologiae (English Dominican 1920, New Advent)
- Repository ids: `work.thomas-aquinas.summa-theologiae` (existing).
- URL: https://www.newadvent.org/summa/4083.htm (fetched 2026-09-30); 1111, 1113 (cache 2026-09-29)
- Loci read: III q.83 a.4 (co., obj. 9, ad 9); I q.111 a.1 co.; I q.113 a.5.
- Quoted: III q.83 a.4 co. (Gloria; Sanctus); ad 9 (entire reply, abridged); ad 9 on missa; I q.111 a.1 co. (two phrases).
- Rights: public domain. Ceiling: New Advent presentation.

### Council of Laodicea, canon 35 (trans. Percival, NPNF II.14)
- Repository ids: `edition.council-of-laodicea.canons.english-percival-npnf2-14-1900-ccel-pdf-2018` (existing).
- SHA-256 of the bytes read: 5b8d0c6518fd71b1de8d626ebf1d6b59c9967d2e7f5d2e0379654b5cbbf0c914 (2570287 bytes)

### Roman synod of 745 (MGH Concilia II/1, ed. A. Werminghoff, 1906)
- Repository ids: none registered; the entry cites the edition directly.
- URL: https://archive.org/download/conciliaaevikaro2pt1werm/conciliaaevikaro2pt1werm_djvu.txt (shared cache, 2026-09-29)
- Loci read: no. 5, Concilium Romanum a. 745, pp. 37–44 (page images pp. 42–44).
- Quoted: Aldebert's invocation (p. 42); the bishops' verdict (p. 43); "sub obtentu angelorum demonum nomina introduxit" (p. 43).
- Rights: public domain. Ceiling: page-image verified.

### Admonitio generalis 789, c. 16 (MGH Capitularia I, ed. A. Boretius, 1883)
- Repository ids: none registered; the entry cites the edition directly.
- URL: https://archive.org/download/capitulariaregum01bore/capitulariaregum01bore_djvu.txt; Retrieved 2026-09-30; Cache text/ia-mgh-capitularia-01-boretius-1883-djvu.txt
- Loci read: Admonitio generalis cc. 12–18, p. 55. Quoted: c. 16 clause.
- Rights: public domain. Ceiling: OCR ("nco", "auctoritato" read as nec, auctoritate by context).

### Directory on Popular Piety and the Liturgy (CDWDS, 17 Dec 2001), English (vatican.va)
- Repository ids: `work.congregation-for-divine-worship-and-the-discipline-of-the-sacraments.directory-on-popular-piety-2001` (registered with this publication).
- SHA-256 of the bytes read: a9d30018f650a6854f3f13d3691a068a6519c2ebdb8d1fc9a2418ad13b90ed38 (531807 bytes)
- Rights: Holy See copyright; short quotations with attribution (brief). Note: 215 prints "spirts" (sic) — that clause is not quoted.

### CDF, Decretum de doctrina et usibus particularibus consociationis "Opus Angelorum" (6 June 1992)
- Repository ids: none registered; the entry cites the edition directly.
- SHA-256 of the bytes read: 81d6d107d271c5220db4dad98bfa8be8f22032d6e91d90490f5c9b64865f1d9b (7696 bytes)
- Rights: Holy See; short quotation. Ceiling: vatican.va HTML; AAS not seen.

### Catechism of the Catholic Church (English, vatican.va)
- Repository ids: `work.catholic-church.catechism` (existing).

### Douay–Rheims (Challoner; Gutenberg 1581) and Douay 1610 appendix
- Repository ids: `work.english-college-of-douay.douay-rheims-bible` (existing).
- SHA-256 of the bytes read: 7d10da78d8ec97db53b4e2bd8719cc01e16106b44937a673ba34aa534a04c007 (5880580 bytes)
- Rights: public domain. Ceiling: Gutenberg transcription.

### R. H. Charles, The Book of Enoch (1917), ch. 20
- Repository ids: none registered; the entry cites the edition directly.
- URL: https://archive.sacred-texts.com/bib/boe/boe023.htm; cache text/st-boe023.txt (2026-09-30). Quoted: "names of the holy angels who watch"; the seven names listed. Rights: public domain (US). Ceiling: web transcription.

### Guéranger, The Liturgical Year, Time after Pentecost V (English, Stanbrook)
- Repository ids: `work.prosper-gueranger.the-liturgical-year` (existing); `edition.prosper-gueranger.the-liturgical-year.english-volume-14` (existing).
- URL: https://archive.org/download/liturgicalyear00gugoog/liturgicalyear00gugoog_djvu.txt; Retrieved 2026-09-30; Cache text/ia-gueranger-lit-year-v14-1903-djvu.txt
- Loci read: September 29; October 2. Quoted: none (paraphrase only: Paul V 1608, Clement X 1670; Chonae 6 Sept, synaxis 8 Nov).
- Rights: public domain. Ceiling: OCR.

### Negative or unused retrievals
- Acta Sanctae Sedis 18 (1885–86) and 19 (1886–87) (IA actasanctaesedis0018iose, 0019iose): searched for the 1886 Michael prayer; not found in OCR.
- Collectio caeremoniarum et precum (Rome 1912): no Leonine prayer.
- Legenda aurea, Graesse 1846: HTTP 500.
- Guéranger Paschal Time III (1909): fetched, not used.

## The saints and the holy angels

### Bonaventure, Legenda maior (Life of Saint Francis), English
- Witness: Bonaventure, *The Life of Saint Francis*, trans. E. Gurney Salter (Temple Classics; London and Toronto: J. M. Dent, 1904).
- Repository ids: `work.bonaventure.legenda-maior-sancti-francisci` (registered with this publication).
- URL: https://archive.org/download/TheLifeOfSaintFrancis/TheLifeOfSaintFrancis_djvu.txt ; collation copy https://archive.org/download/cihm_88134/cihm_88134_djvu.txt
- Retrieved: 2026-09-30T14:56:50Z; 2026-09-30T15:00:37Z
- SHA-256 of the bytes read: e71d92ce5eba87bd250a9aaf4ce4b784b2d5787321d44dad0bbe344bb0a0bfe4 (353433 bytes); 33fad07e6ed41d5b86b2520952cefc10b7bd642c1f50e19d6f8e662ea05f0858 (351094 bytes)
- Loci read: prol. 1–2; II.8; VIII.10; IX.3; XIII.1–5.
- Quoted: prol. 1 ("himself an Angel of the true peace"; "appointed unto angelic ministries … chariot of fire"; "he is thought to be not unmeetly … seal of the Living God"); prol. 2 ("living among men … purity of the Angels"; "faithfully and devoutly held"); II.8 ("Perceiving that Angels ofttimes visited it …"; "commended it unto the Brethren …"); VIII.10 ("there would seem to have been a divine omen … vision of the Seraph"); IX.3 (block); XIII.1 ("like the heavenly spirits on Jacob's ladder …"; "the peaceful ecstasies of contemplation"; "When, according unto his wont …"); XIII.3 (block; "at the gracious aspect …"; "knowing that the infirmity …"; "wholly transformed …"); XIII.4 ("adding that He who had appeared …"); XIII.5 ("when the Feast of Saint Michael Archangel came …").
- Rights: public domain (1904; translator's work out of copyright in US; Temple Classics).
- Ceiling: Google/Canadiana OCR; two independent OCRs collated for every quoted sentence (agreement); marginal glosses stripped; not collated with print page images.

### Bonaventure, Opera omnia (Quaracchi), t. VIII — Legenda S. Francisci (Latin)
- Witness: *Doctoris seraphici S. Bonaventurae opera omnia*, t. VIII, Opusculum XXIII, Legenda S. Francisci (Ad Claras Aquas / Quaracchi).
- Repository ids: `work.bonaventure.opera-omnia-quaracchi` (existing).
- URL: https://archive.org/download/doctorisseraphic08bona/doctorisseraphic08bona_djvu.txt
- Retrieved: 2026-09-30T14:56:55Z
- SHA-256 of the bytes read: ac751f92bb942824d6e7e5fc037dde7f360d387854fbf35c938a5ff7e204a64e (6206733 bytes)
- Loci read: c. 9 n. 3 with notes 9–12 (pp. c. 529–530); c. 13 nn. 1–3 with notes (pp. 542–543); title page.
- Quoted: IX.3 "Beato autem Michaeli Archangelo, eo quod animarum repraesentandarum haberet officium, speciali erat amore devotior"; note 10 (Breviary responsory "Cui tradidit Deus animas Sanctorum, ut perducat eas in paradisum exsultationis" and antiphon "Archangele Michael, constitui te principem super omnes animas suscipiendas", as the note gives them); XIII.1 "Quadragesimam ibidem ad honorem sancti Archangeli Michaelis ieiunare coepisset"; XIII.3 "tam ignitas quam splendidas", "seraphicis desideriorum ardoribus"; title "Doctoris seraphici S. Bonaventurae opera omnia".
- Rights: public domain (19th-c. critical edition; Latin text).
- Ceiling: OCR; obvious OCR errors silently corrected (e.g. autera→autem, ofQcium→officium, salutera→salutem, Archangeh Michaehs→Archangeli Michaelis). Volume date not read.

### Bonaventure, Opera omnia (Quaracchi), t. V — Itinerarium mentis in Deum
- Witness: Quaracchi t. V, *Itinerarium mentis in Deum*, prologue.
- Repository ids: `work.bonaventure.opera-omnia-quaracchi` (existing); `work.bonaventure.itinerarium-mentis-in-deum` (registered with this publication).
- URL: https://archive.org/download/doctorisseraphic05bona/doctorisseraphic05bona_djvu.txt
- Retrieved: 2026-09-30T15:01:11Z
- SHA-256 of the bytes read: 9ba2eecaf747a4fe180a95df21cb536cd3ca8550921de9a4d357138a1aaabc12 (4455576 bytes)
- Loci read: prol. 1 (end)–3 with notes.
- Quoted: prol. 2 "amore quaerendi pacem spiritus"; "inter alia occurrit illud miraculum … ad instar Crucifixi"; prol. 3 "Nam per senas alas … amorem Crucifixi" (block); "quod mens in carne patuit"; "quae a creaturis incipiunt … nisi per Crucifixum"; "Effigies igitur sex alarum seraphicarum insinuat sex illuminationes scalares".
- Rights: public domain.
- Ceiling: OCR (inteUigi→intelligi, sfix→sex corrected); "thirty-three years" and "seventh successor" from prol. 2 and its note (1259).

### Bonaventure, Opera omnia (Quaracchi), t. IX — Sermones de sanctis, De sanctis Angelis 1–5
- Witness: Quaracchi t. IX, *Sermones de sanctis*, "De sanctis Angelis" sermons 1–5 (pp. 609 ff.).
- Repository ids: `work.bonaventure.opera-omnia-quaracchi` (existing).
- URL: https://ia800507.us.archive.org/28/items/doctorisseraphic09bona/doctorisseraphic09bona_djvu.txt (the first attempt at the archive.org/download URL returned HTTP 500 and is in the manifest as ia-bonaventure-opera-t9.txt)
- Retrieved: 2026-09-30T14:57:59Z
- SHA-256 of the bytes read: 77fd92d2f496d6f1bb0639d69466449481de4889e18b99d267a2047f97e566d7 (4918572 bytes)
- Loci read: s. 1 (pp. 609–614, whole); s. 2 opening; s. 3 opening; s. 4 (pp. 620–622, whole); s. 5 opening (division and part I start).
- Quoted: s. 1 "Habemus loqui de hierarchiis angelicis …" (p. 609); "Scala ista, cuius pars est in caelo …" (p. 610); "In prima hierarchia sunt Throni … triumphare" (pp. 612–613); "Et supra se hierarchia angelica habet Virginem gloriosam …" (p. 612); "Concentus caeli est harmonia laudis angelicae …" (p. 612); "Angeli dicunt nobis: Suscipite exempla …" (p. 612); "Magnum est confidere in Angelis" (p. 612); "Loquuntur de caelestibus et affectum habent in terrenis" (p. 612); "ideo eius officium celebratur per universam Ecclesiam" (p. 613). s. 4: "Angeli dicuntur nostri propter tria …"; "Primum remedium ministrat Raphael, qui interpretatur medicina Dei"; "Secundum remedium ministrat Gabriel …"; "Tertium remedium ministrat Michael … Deo facit"; "introducit animas in paradisum exsultationis"; "quis est tam desiderandus ut Deus?"; "tres Angelos solum ex nomine designat sacra Scriptura …"; "imago Dei manifestativa luminis occulti, speculum purum"; "Semper est Angelis cognata virginitas"; "nam generales custodes sunt animarum Angeli". s. 5: "hierarchia nihil aliud est quam sacer principatus".
- Rights: public domain.
- Ceiling: OCR with many errors, silently corrected in quoted phrases (e.g. Virlutiim→Virtutum, Principutuum→Principatuum, supporta7ulum→supportandum, lesum→Iesum); editors state s. 1 is from cod. Trecensis 981 (s. XIII) with "multa et gravia vitia" corrected; "(et)" is the editors' insertion. Garbled first-hierarchy line of s. 1 (p. 610) paraphrased, not quoted.

### William of Tocco and Peter Calo, lives of Thomas Aquinas (ed. Prümmer)
- Witness: D. Prümmer (ed.), *Fontes vitae S. Thomae Aquinatis notis historicis et criticis illustrati* (Toulouse: Privat, 1911 [fasc. containing Calo and Tocco]).
- Repository ids: `work.william-of-tocco.vita-sancti-thomae-aquinatis` (registered with this publication); `work.peter-calo.vita-sancti-thomae-aquinatis` (registered with this publication).
- URL: https://archive.org/download/prummerfontesvitaestho/prummerfontesvitaestho_djvu.txt (also fetched https://archive.org/download/fontesvitaesthom00pr/fontesvitaesthom00pr_djvu.txt, 1912, same texts, used for spot check only)
- Retrieved: 2026-09-30T14:57:03Z; 2026-09-30T14:57:09Z
- SHA-256 of the bytes read: 2ea97fa64ac0d2d0afebbf1b45762de86b60501b587651733b9e75b25305b70d (612331 bytes); f09a430f5266343fe668398aeffcaee8af7ccdc763be9be72717a96de4ff11ce (1633591 bytes)
- Loci read: Prümmer prologue; Calo nn. 6–8 (pp. 23–24) with notes; Tocco cc. 9–11 (pp. 74–76) with notes.
- Quoted: Tocco c. 10 "ecce ad eum duo Angeli coelitus missi sunt … divinae largitatis ex dono" (block); "cui Angelica societas, dum castitate cingitur, non negatur, qui meruit fieri puritate Angelicus"; Calo n. 7 "Cingimus te cingulo perpetue virginitatis, quod nullatenus de cetero dissolvetur"; "quod ex tunc non sensit nec minimum carnis motum". Prümmer note (Tocco's sworn testimony in the canonization process, no. 61) paraphrased.
- Rights: Latin texts public domain; Prümmer edition 1911 (public domain in US).
- Ceiling: Google OCR; castilale→castitate corrected; page order in OCR irregular (p. 79 header before p. 76); body cites by chapter.

### Pius XI, Studiorum Ducem (Latin)
- Witness: Pius XI, encyclical *Studiorum Ducem*, 29 June 1923 (AAS 15 [1923] 309–326, per page footer), Latin, vatican.va.
- Repository ids: `work.pius-xi.studiorum-ducem` (registered with this publication).
- URL: https://www.vatican.va/content/pius-xi/la/encyclicals/documents/hf_p-xi_enc_19230629_studiorum-ducem.html
- Retrieved: 2026-09-30T15:00:03Z
- SHA-256 of the bytes read: 2f7ab30c0fe9164784b9a453bcc5b31197f6d46c684ba9ac0a5eaa6799964944 (70323 bytes)
- Loci read: whole letter and appended ORATIO.
- Quoted (short): "prima omnium occurrit ea virtus … castimoniam dicimus"; "dignus est habitus quem mystica zona angeli cingerent"; "rato Angelici titulo"; "non modo Angelicum, sed etiam Communem seu universalem Ecclesiae Doctorem"; "si Thomae pudicitia … cecidisset, verisimile est nequaquam Ecclesiam suum Doctorem Angelicum habituram fuisse"; "Militiae Angelicae societatem"; "sancti Thomae cum Angelis ei zonam accingentibus"; "qua ipse utebatur"; ORATIO "Creator ineffabilis, qui de thesauris sapientiae tuae tres Angelorum hierarchias designasti, et eas super caelum empyreum miro ordine collocasti".
- Rights: Vatican-site document; short quotations with attribution. The prayer is quoted in Latin as text, not offered as English prayer (no translation of it given).
- Ceiling: web text; not collated with AAS.

### Gertrude the Great, Insinuationes divinae pietatis (Kenmare translation)
- Witness: *The Life and Revelations of Saint Gertrude, Virgin and Abbess, of the Order of St. Benedict* (London: Burns & Oates; New York: Benziger; letter of Bp Moriarty dated 11 Dec. 1870; translator Sister M. Frances Clare, Kenmare), parts II–V translating books II–V of the *Insinuationes*.
- Repository ids: `work.gertrude-the-great.insinuationes-divinae-pietatis` (registered with this publication).
- URL: https://archive.org/download/thelifeandrevela00gertuoft/thelifeandrevela00gertuoft_djvu.txt
- Retrieved: 2026-09-30T14:57:14Z
- SHA-256 of the bytes read: f4a481ea4819992320b497bd4d79a81aea8ebac609ba36e0dd21b2f5bf25ea63 (1230593 bytes)
- Loci read: front matter, contents, Advertisement; pt III ch. 21; pt IV chs. 1–2 (Christmas); pt IV ch. 54 (St Michael) and 55 opening.
- Quoted: pt III ch. 21 ("it appeared to her that her guardian angel took her in his arms … bless Thy little child"); pt IV ch. 2 ("When those who loved God with the greatest fervour … present their homage"; "that when angels are present at our solemnities …"); pt IV ch. 54 ("by meditating on the care …"; "I offer Thee this most august Sacrament …"; block "Thou hast indeed honoured us … utmost vigilance"; "appeared to her as a prince magnificently attired …"; Archangels', Virtues', Powers' promises; "For the prayers of one loving soul …").
- Rights: public domain (1870).
- Ceiling: OCR; "0 most loving"→"O most loving". Latin chapter numbers of the *Insinuationes*/*Legatus* not verified; body cites the translation's part/chapter. The translation conflates Gertrude the Great with the abbess; body does not call her abbess.

### Mechtild, Select Revelations (1875)
- Witness: *Select Revelations of S. Mechtild, Virgin: taken from the five books of her Spiritual Grace, and translated from the Latin by a secular priest* (London: T. Richardson, 1875).
- Repository ids: `work.mechtild-of-hackeborn.liber-specialis-gratiae` (registered with this publication).
- URL: https://archive.org/download/selectrevelation00mech/selectrevelation00mech_djvu.txt ; collation https://archive.org/download/selectrevelatio00mechgoog/selectrevelatio00mechgoog_djvu.txt
- Retrieved: 2026-09-30T14:57:17Z; 2026-09-30T15:03:37Z
- SHA-256 of the bytes read: cc5d201098135ed6247ad0244364a99adb4fdef17551f461f27663d44e8b096c (290555 bytes); 13ac85f1044004f9ef139e8f955f71aa5ba434fad2fb1417114df745377ad1e4 (252170 bytes)
- Loci read: contents; ch. 16 (pp. 72–76) whole.
- Quoted: ch. 16 ("The handmaid of Christ beheld a golden staircase … conversation of men"; "faithfully, and humbly, and devotedly … the poor"; block "And they who love God … no others are found").
- Rights: public domain (1875).
- Ceiling: both OCRs read "Before the heart of S. Michael" at the chapter opening (probably a misprint for "feast"); the phrase is not quoted. Latin locus in the *Liber specialis gratiae* not identified.

### Trial and rehabilitation of Joan of Arc (Murray)
- Witness: T. Douglas Murray (ed. and trans.), *Jeanne d'Arc, Maid of Orleans, Deliverer of France … as attested on oath and set forth in the original documents* (New York: McClure, Phillips, 1902).
- Repository ids: none registered; the entry cites the edition directly.
- URL: https://archive.org/download/jeannedarcmaidof028754mbp/jeannedarcmaidof028754mbp_djvu.txt
- Retrieved: 2026-09-30T14:57:24Z
- SHA-256 of the bytes read: 2b7d8a16ec010a81d1c1cee0bec29b930183bd0b1bef93fa0d025b54d608dbae (790676 bytes)
- Loci read: public sessions 21, 22, 24, 27 Feb., 1 and 3 Mar. 1431 (pp. 1–53 region); private sessions 15 and 17 Mar. (pp. 83–86); rehabilitation depositions of Pierre Lebouchier (1452; pp. 198–199) and Guillaume Delachambre (p. c. 254).
- Quoted: 27 Feb. (block, "What was the first Voice … taken away with them"); 1 Mar. ("Do you think God has not wherewithal to clothe him?"); 3 Mar. ("I saw them with my eyes; and I believe …"); 15 Mar. (block; "so well, and it was so clear …"; "Above all things he told me to be a good child …"); 17 Mar. ("In the form of a true honest man … which he has given me"); Lebouchier ("to Saint Michael that he would direct and counsel her"; "While they were tying her to the stake …"); Delachambre ("cry 'Jesus' and … invoke St. Michael; and then she perished in the flame").
- Rights: public domain (1902; Murray d. 1911).
- Ceiling: English translation only; the Latin/French minute (Quicherat) not read. Lebouchier's day of examination is OCR-garbled ("May %th, 1452"); body gives the year only.

### Fullerton, Life of St. Frances of Rome (1855)
- Witness: Lady Georgiana Fullerton, *The Life of St. Frances of Rome* (London, 1855), with J. M. Capes's essay; Project Gutenberg eBook 8495.
- Repository ids: `work.georgiana-fullerton.life-of-st-frances-of-rome` (registered with this publication).
- URL: https://www.gutenberg.org/cache/epub/8495/pg8495.txt (first attempt at archive.org 8stfr10.txt returned 500)
- Retrieved: 2026-09-30T14:58:01Z
- SHA-256 of the bytes read: 16b83736f7e6187a56f3ac72db3d817b4e2a2498771ec69a46b30a993b3df8f1 (511114 bytes)
- Loci read: preface on authorities (Mattiotti; Bollandists; Fuligatti; Bussière); chs. 3, 7, 14; contents.
- Quoted: ch. 3 ("one day to accompany her … in a visible form"; "At the least imperfection …"); ch. 7 ("There are nine choirs …"; "This my companion is higher …"; "but the archangel remained …"; "His stature … degraded condition of our own"; "At night, and in the most profound darkness …"; "When she committed the slightest fault …"; "Be not afraid, father …"); ch. 14 ("The heavens open! …").
- Rights: public domain (1855).
- Ceiling: Gutenberg transcription; Mattiotti's Latin life (AASS) not read.

### Ignatius of Loyola, Spiritual Exercises (Mullan 1914)
- Witness: *The Spiritual Exercises of St. Ignatius of Loyola, translated from the Autograph* by Father Elder Mullan, S.J. (New York: Kenedy, 1914).
- Repository ids: none registered; the entry cites the edition directly.
- URL: https://archive.org/download/spiritualexercis00ignauoft/spiritualexercis00ignauoft_djvu.txt
- Retrieved: 2026-09-30T14:57:33Z
- SHA-256 of the bytes read: e5d0d89ec40c6a7562f347d090e2280baada61fe4ff858033f8c55a49ec02a3e (223739 bytes)
- Loci read: First Week first and second exercises; Second Week fourth day (Two Standards); Rules for discernment First Week 12–14; Rules for the Second Week 1–8.
- Quoted: first exercise first point (block and two phrases); second exercise fifth point ("the Angels, how, though they are the sword …"); Two Standards first and second points; Second-Week rules 1, 3, 4 (block), 5, 7.
- Rights: public domain (1914; US).
- Ceiling: OCR; standard paragraph numbers not printed in Mullan and not used.

### Teresa of Jesus, Life (Lewis)
- Witness: *The Life of St. Teresa of Jesus … Written by Herself*, trans. David Lewis, 3rd ed. enlarged, with notes by B. Zimmerman (London: Baker, 1904); Project Gutenberg eBook 8120.
- Repository ids: `work.teresa-of-avila.libro-de-la-vida` (registered with this publication).
- URL: https://www.gutenberg.org/cache/epub/8120/pg8120.txt
- Retrieved: 2026-09-30T14:58:02Z
- SHA-256 of the bytes read: 3420485ba9b861cc44ac80833e3d9864683784e93e0f68f6ba5fc44c407a33bc (1116120 bytes)
- Loci read: ch. 29 §§ 15–19 with notes 13–18; ch. 31 §§ 3–4; ch. 39 §§ 31–32.
- Quoted: 29.16 and 29.17 (blocks); 39.32; 31.4 (two sentences). Note 14 (cherubines/seraphim, Báñez) paraphrased.
- Rights: public domain (1904; US).
- Ceiling: Gutenberg transcription; Spanish autograph not read.

### Francis de Sales, Introduction à la vie dévote (French)
- Witness: *Introduction à la vie dévote*, édition corrigée (Lyon and Paris: Périsse frères, 1832); Project Gutenberg eBook 53540.
- Repository ids: `work.francis-de-sales.introduction-a-la-vie-devote` (existing); `edition.francis-de-sales.introduction-a-la-vie-devote.perisse-freres-french-gutenberg` (existing).
- URL: https://www.gutenberg.org/cache/epub/53540/pg53540.txt
- Retrieved: 2026-09-30T14:59:40Z
- SHA-256 of the bytes read: c2d4183f1d937d9ae9c7c73d9a444bf1a7701565d02402a2175c0e1bd0277036 (615203 bytes)
- Loci read: II.16 whole.
- Quoted: II.16 "Puisque c'est par le ministère des anges … nos aspirations"; "Rendez-vous fort familière avec les anges … coopèrent à vos intentions"; "il s'étoit toujours très-bien trouvé de saluer … les anges qui la protégeoient". English glosses are the lane's own (unquoted).
- Rights: public domain.
- Ceiling: Gutenberg transcription of the 1832 edition (spelling "présens", "étoit" as printed).
- Also consulted, not quoted: *Introduction to the Devout Life*, "new edition" (London: Longmans, 1891; https://archive.org/download/IntroductionToTheDevoutLife/IntroductionToTheDevoutLife_djvu.txt; text/ia-desales-devout-life-1891.txt) — its preface states it omits the chapter on honouring and invoking Saints and Angels (numbered there Pt I ch. xvi) and passages invoking the saints; unusable for II.16. *Introduction to the Devout Life, a new translation* (London: Rivingtons, 1876; https://archive.org/download/introductiontod00salegoog/introductiontod00salegoog_djvu.txt; text/ia-desales-devout-life-1876.txt) — II.16 read; free rendering that softens "priez-les souvent"; not quoted.

### Alphonsus Liguori, Sermons for all the Sundays (Grimm)
- Witness: *Sermons for all the Sundays in the Year* / *Abridged Sermons for all Sundays*, Centenary Edition vol. XVI, ed. and trans. Eugene Grimm (New York: Benziger; item dated 1890).
- Repository ids: `work.alphonsus-liguori.sermoni-compendiati` (registered with this publication).
- URL: https://archive.org/download/abridgedsermons16liguuoft/abridgedsermons16liguuoft_djvu.txt
- Retrieved: 2026-09-30T15:11:10Z
- SHA-256 of the bytes read: 4b1ec5ca2a813cabc2e1d9770acb7a97b8ff346f0958d335aac104ef916c8838 (1232231 bytes)
- Loci read: s. 11 (Sixth Sunday after Epiphany, "Death of the Just", pp. 124–126); s. 44 (Fifteenth Sunday after Pentecost, pp. 457–458); series list in front matter.
- Quoted: s. 11 (block, p. 125); s. 44 ("St. Joseph, St. Michael, the archangel, my holy angel-guardian …", p. 458).
- Rights: public domain (Grimm d. 1891).
- Ceiling: OCR of p. 125 is poor; the quoted sentences were reconstructed from legible OCR (`(iod`→God, `whh`→with, `guar dian`→guardian). Recommend collation against another scan (e.g. archive.org sermonsforallsun00liguuoft). Also consulted without quotation: vol. XV *Preaching* (text/ia-liguori-grimm-v15.txt; https://archive.org/download/alphonsusworks15liguuoft/alphonsusworks15liguuoft_djvu.txt) and vol. XVII (text/ia-liguori-grimm-v17.txt).

### Alphonsus Liguori, Glories of Mary (Grimm)
- Witness: *The Glories of Mary*, two volumes in one, Centenary Edition vols. VII–VIII, ed. Grimm, 4th reprint revised (Brooklyn etc.: Redemptorist Fathers, 1931).
- Repository ids: `work.alphonsus-liguori.le-glorie-di-maria` (registered with this publication).
- URL: https://archive.org/download/kpbc.umk.pl.Magazyn_286_07_HD_008_197127/Magazyn_286_07_HD_008_djvu.txt
- Retrieved: 2026-09-30T15:12:23Z
- SHA-256 of the bytes read: b1d891b61ab6b5a88fbe158b5260affc3e208ba380ac8d02bc6cace4c87a2f0c (1353188 bytes)
- Loci read: series list; Pt I ch. II § 3 ("Mary renders death sweet"), pp. c. 100–102 with footnotes.
- Quoted: "sends without delay the prince of the heavenly court … recommended themselves to her"; footnote Latin "Michael, dux et princeps militiæ cœlestis, cum omnibus spiritibus administratoriis, tuis, Virgo, paret præceptis" (Spec. B. V. lect. 3).
- Rights: Grimm's 1888 translation public domain; 1931 reprint adds nothing quoted.
- Ceiling: OCR; the series list announces "Devotion to the Holy Angels" in vol. VIII, but it is not in this reprint nor in the Kenedy 1888 *Glories* (text/ia-liguori-glories-kenedy-1888.txt; https://archive.org/download/thegloriesofmary00liguuoft/thegloriesofmary00liguuoft_djvu.txt), both checked.

### Monnin, The Spirit of the Curé of Ars (1865)
- Witness: Alfred Monnin, *The Spirit of the Curé of Ars*, trans. from the French, ed. J. E. Bowden (London, 1865).
- Repository ids: `work.alfred-monnin.esprit-du-cure-dars` (registered with this publication).
- URL: https://archive.org/download/spiritcurarsstj00monngoog/spiritcurarsstj00monngoog_djvu.txt
- Retrieved: 2026-09-30T14:59:43Z
- SHA-256 of the bytes read: 0a908a99deaec89d8f4ed383306d9a0318933cd36bf3805c41c2059b28340f48 (363473 bytes)
- Loci read: contents; pt I introduction (p. c. 30); Catechisms on the Prerogatives of the Pure Soul, the Priesthood, Frequent Communion, the Cardinal Virtues; Homily on the Cockle.
- Quoted: "We always have two secretaries …"; "What joy is it to the guardian angel to conduct a pure soul!"; "How happy is a guardian angel who leads a beautiful soul to the holy table!"; "If I were to meet a priest and an angel … holds His place"; "When we are going along the streets … by our side".
- Rights: public domain (1865).
- Ceiling: Google OCR; French original not read.

### O'Meara, The Curé of Ars
- Witness: Kathleen O'Meara, *The Curé of Ars* (Notre Dame: Ave Maria Press, [1912?]).
- Repository ids: `work.kathleen-omeara.cure-of-ars` (registered with this publication).
- URL: https://archive.org/download/curofars00omeauoft/curofars00omeauoft_djvu.txt
- Retrieved: 2026-09-30T15:07:29Z
- SHA-256 of the bytes read: 5aa00843c0b86aa16c516510a4a7a90593130676d8c7dace0b27cfd5ede9f6b6 (261134 bytes)
- Loci read: ch. 9 "He is persecuted by the devil" (pp. 77–91).
- Quoted: "commending myself to God, to the Blessed Virgin, and my Guardian Angel"; "to be near me with His angels when the enemy came to torment me"; "The devil is cunning … puts him to flight"; "He is more powerful than the grappin."
- Rights: public domain (author d. 1888).
- Ceiling: OCR.

### Germanus, Life of Gemma Galgani (O'Sullivan 1913)
- Witness: Germanus of St Stanislaus, C.P., *The Life of Saint Gemma Galgani*, trans. A. M. O'Sullivan (St Louis: B. Herder, 1913), as retypeset by Catholic Way Publishing (2014).
- Repository ids: `work.germanus-of-saint-stanislaus.vita-di-gemma-galgani` (registered with this publication).
- URL: https://archive.org/download/the-life-of-saint-gemma-galgani-by-venerable-reverend-germanus-c.-p/The_Life_of_Saint_Gemma_Galgani%20by%20Venerable%20Reverend%20Germanus%2C%20C.P_djvu.txt
- Retrieved: 2026-09-30T14:59:54Z
- SHA-256 of the bytes read: 6e9576903c61bc2e55442235fd11a4ce42d8e7d21865763768a89e295d6391fa (702851 bytes)
- Loci read: ch. 1 opening; ch. 20 whole.
- Quoted: ch. 20 ("as one friend would with another"; "Jesus … has not left me alone …"; angel's reply; "raised in the air with outspread wings …"; "I myself have many times assisted …"; "like a child at school"; dictation block; "My Angel is a little severe …"; "Dear Angel … I so love you!" dialogue; "From this day forward …"; "No, because I am sent by Him …"; "It is my wish that thy conversation …").
- Rights: 1913 translation public domain in US; the retypeset claims typography only; words quoted are the 1913 translation's.
- Ceiling: retypeset e-text, not collated with the 1913 print; small archaisms ("Art you") suggest retyping errors elsewhere; quoted passages avoid visibly corrupt lines. The French *Lettres et extases* (1920; text/ia-gemma-lettres-extases-1920.txt) fetched, not used.

### Thérèse of Lisieux, Histoire d'une âme (1912) — "À mon Ange gardien"
- Witness: Sœur Thérèse de l'Enfant Jésus, *Histoire d'une âme écrite par elle-même; Lettres; Poésies* (Lisieux, 1912 printing, "Cent vingt-cinquième mille"), pp. 427–428, as transcribed on French Wikisource (proofread "à valider").
- Repository ids: none registered; the entry cites the edition directly.
- URL: https://fr.wikisource.org/wiki/Histoire_d%E2%80%99une_%C3%A2me/4/2/5 (also /1/4 read)
- Retrieved: 2026-09-30T15:09:03Z; 15:09:05Z
- SHA-256 of the bytes read: e6028bf3db48db2ce1232da150389b4f31c6975d5485e76708f826c1c94940c3 (70424 bytes); 172b4a7069bc2293f63a9f2bc20e0307d61ddff4ecfc026e143aab393c94953a (147700 bytes)
- Loci read: poem "À mon Ange gardien" (Février 1897) whole; front matter (death date 30 Sept. 1897); ch. 4 searched for the angels.
- Quoted: stanza 1 (block); stanza 2 lines; "plus promptement que les éclairs"; stanza 4 lines; stanza 6 (block). English glosses are the lane's own (unquoted).
- Rights: author d. 1897; text public domain; Wikisource transcription CC BY-SA (source text PD).
- Ceiling: Wikisource transcription of the 1912 printing; not collated with page images or the critical edition.

### Thérèse, Poems (Emery 1907)
- Witness: *Poems of Sr. Teresa, Carmelite of Lisieux*, trans. S. L. Emery (Boston: Angel Guardian Press, 1907).
- Repository ids: `work.therese-of-lisieux.poesies` (registered with this publication).
- URL: https://archive.org/download/poemsofsrteresac00thrs/poemsofsrteresac00thrs_djvu.txt
- Retrieved: 2026-09-30T14:59:47Z
- SHA-256 of the bytes read: 610a90d869ab6c4c0995925babfb9c3d45fb68ca2a96c44e21aed15db7c6ab79 (202392 bytes)
- Loci read: "To My Angel Guardian" (pp. 73–74); "The Angels of the Crib. Fragment." (pp. 134–136).
- Quoted: "The Angels of the Crib" ("O Child, whose light doth blind the sight / … that love of Thine?"; "Thee will I guard by day and night").
- Rights: public domain (1907; US).
- Ceiling: OCR ("divine 1"→"divine!"). The French of "Les Anges à la crèche" not read.
- Also consulted: T. N. Taylor, *Saint Thérèse of Lisieux … a new and complete translation of L'Histoire d'une âme* (1912; text/ia-therese-taylor-1912.txt) — searched for the Association of the Holy Angels; not found; not quoted.

### Newman, Parochial and Plain Sermons II.29 "The Powers of Nature"
- Witness: J. H. Newman, *Parochial and Plain Sermons*, vol. II, sermon 29 (Newman Reader transcription of the uniform edition, pp. 358–367).
- Repository ids: `work.john-henry-newman.parochial-and-plain-sermons` (registered with this publication).
- URL: https://newmanreader.org/works/parochial/volume2/sermon29.html
- Retrieved: 2026-09-30T15:00:00Z
- SHA-256 of the bytes read: e27340a99e1f68590b8c16b56762bfe8d5130eaceb0ce073437f0d93739b7510 (18903 bytes)
- Loci read: whole sermon and notes.
- Quoted: pp. 358–359 (block); p. 360 ("how do the wind and water … work of Angels"); p. 361 ("Nature is not inanimate …"); p. 362 ("Every breath of air …"; "in subordination to that higher view"); p. 363 ("fixed laws, self-caused and self-sustained"; "the thousands and ten thousands of His unseen Servants"); pp. 365–366 ("it is a great comfort to reflect …"; "The very lowest of His Angels …"; "if we attain to heaven …").
- Rights: public domain text; Newman Reader site © NINS for presentation; focused quotation.
- Ceiling: web transcription; not collated with print.

### Newman, The Dream of Gerontius
- Witness: J. H. Newman, *The Dream of Gerontius* (dated "The Oratory. January, 1865"), in *Verses on Various Occasions* (Newman Reader transcription).
- Repository ids: `work.john-henry-newman.dream-of-gerontius` (registered with this publication).
- URL: https://newmanreader.org/works/verses/gerontius.html
- Retrieved: 2026-09-30T15:00:01Z
- SHA-256 of the bytes read: e558097b617acbf4c5be0f88f580fde0505daead16af5cb617d8ce2c6f6486fa (145115 bytes)
- Loci read: §§ 2, 5, 6, 7 (angel passages).
- Quoted: § 2 ("My work is done …" block; "My Father gave … To serve and save"; "a member of that family … he never has known sin"; "More than the Seraph … ransom'd race"); § 5 ("Least and most childlike of the Sons of God"; "Praise to the Holiest …"; "elder race"; "To battle and to win …"); § 6 ("the great Angel of the Agony …"); § 7 (block "Softly and gently … on the morrow").
- Rights: public domain.
- Ceiling: web transcription with hard line-wrap artifacts removed (e.g. "ran- som'd"); line division restored from the verse sense.

### Gregory the Great, Homiliae in Evangelia 34.7 (for the order comparison only)
- Witness: cache copy of Gregory, XL Homiliae in Evangelia.
- Repository ids: none registered; the entry cites the edition directly.
- URL: https://archive.org/download/sanctigregoriim00igoog/sanctigregoriim00igoog_djvu.txt
- Retrieved: 2026-09-29T13:48:47Z
- SHA-256 of the bytes read: 4eb8d78cd432816ff08b76b2549b6015fe29637307a22ee1d7ba79884d68e2f1 (701111 bytes)
- Loci read: 34.7 (list of nine orders).
- Quoted: none (cited for the order only).
- Rights: public domain.
- Ceiling: OCR.

### Denzinger (Lateran IV, DS 800)
- Witness: cache Denzinger (Latin).
- Repository ids: none registered; the entry cites the edition directly.
- URL/Retrieved: see manifest `denz-patristica.txt`.
- SHA-256 of the bytes read: 604f24c46e0bc71c2018f25dc787a9ab421d4b2e9cf7d1cee1f43e910ef2708f (2333435 bytes)
- Loci read: DS 800 (428).
- Quoted: none (cited: "Diabolus enim et alii daemones a Deo quidem natura creati sunt boni, sed ipsi per se facti sunt mali").
- Rights: public domain Latin.
- Ceiling: OCR.

### Catechism of the Catholic Church 335–336
- Witness: CCC, English, vatican.va (cache ccc-en-P1A.txt).
- Repository ids: `work.catholic-church.catechism` (existing).
- URL/Retrieved: per manifest.
- SHA-256 of the bytes read: f5d0972215f47a1bc22e768aa4e51f454db80f32dcbc4e3dd52b4a40ae5254d3 (22605 bytes)
- Loci read: 334–336.
- Quoted: 336 "From infancy to death human life is surrounded by their watchful care and intercession" (short; Vatican English, attributed).
- Rights: Vatican copyright; short quotation with attribution.
- Ceiling: web text.

### Douay–Rheims (Challoner), Gutenberg 1581
- Witness: repository edition edition.english-college-of-douay.douay-rheims-bible.challoner-gutenberg-1581.
- Repository ids: `work.english-college-of-douay.douay-rheims-bible` (existing).
- URL: https://www.gutenberg.org/cache/epub/1581/pg1581.txt
- Retrieved: per manifest
- SHA-256 of the bytes read: 7d10da78d8ec97db53b4e2bd8719cc01e16106b44937a673ba34aa534a04c007 (5880580 bytes)
- Loci read: Ps 90:11–12; 103:4; 137:1; 2 Cor 11:14; Matt 18:10; Gen 28:12; Apoc 7:2; 12:7; Isa 6:2, 6–7; Luke 22:43; Dan 10:13; 12:1; Tob 12:12, 15; Heb 1:14; 4 Kings 6:16–17.
- Quoted: Matt 18:10 (part); Ps 137:1 (part); 2 Cor 11:14 (part).
- Rights: public domain.
- Ceiling: Gutenberg transcription.
