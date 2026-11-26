# Source Audit — The Dwelling of the Living God (Gemini Ark of the Covenant Monograph)

- **Publication leaf:** `src/gemini/theology/mariology/ark-of-the-covenant/`
- **As-of date:** 2026-11-25
- **Source boundary:** All primary quotations, lexical counts, textual variants, and liturgical appointments were verified directly from tracked files in `src/sources/` (`bibles/`, `works/`, `calendars/`, `chronology/`). No authored prose was copied from sibling provider leaves (`src/gpt/` or `src/claude/`).

## 1. Scriptural and Lexical Controls Verified Locally

### 1.1 English, Latin, and Comparative Biblical Editions
- **Douay-Rheims Bible (Challoner revision, Gutenberg 1581)** (`edition.english-college-of-douay.douay-rheims-bible.challoner-gutenberg-1581`, public domain): Primary English quotation witness across Exodus, Numbers, Deuteronomy, Josue (Joshua), Judges, 1--3 Kings (1--2 Samuel, 1 Kings), 1--2 Paralipomenon (1--2 Chronicles), Psalms, Jeremias, 2 Machabees, Matthew, Luke, Hebrews, and Apocalypse, plus Bishop Challoner's notes on 1 Kgs 6:19, 3 Kgs 8:9, and Apoc 12:1 (`pg1581.txt`). Checked against the **1899 American Douay-Rheims** (`engDRA`, public domain).
- **Clementine Vulgate (1598, `latVUC`)** (`edition.catholic-church.vulgata-clementina.ebible-latvuc`, public domain): Controlling Latin witness for Gallican Psalter (*arca sanctificationis tuae* at Ps 131:8; *obumbrabit tibi* at Ps 90:4 and Luke 1:35), Vulgate Exodus 40:32--33 (*operiente*/*operuerat* rather than *obumbro*), Judges 20:18 (*hoc est, in Silo*), 1 Chr 13:14 and Luke 1:56 (*mansit ... tribus mensibus*), and Rev 11:19--12:3 (*visa est* / *apparuit* / *visum est*).
- **Brenton English Septuagint (1851, `eng-Brenton`)** (`edition.lancelot-brenton.septuagint-english-translation.ebible-eng-brenton`, public domain): Complete tracked English LXX witness establishing Exod 16:33 (*a golden pot*), Exod 40:35 (*because the cloud overshadowed it*), Num 9:18--22 and 10:36 (*overshadowed*), Judg 20:18, 26 (*Baethel*), 1 Sam 5:10 & 6:16 (*Ascalon* vs. MT/Vg *Ekron*, while naming all five cities at 6:17), 2 Sam 6:14, 16 (*sounded with well-tuned instruments* / *dancing and playing*), 1 Chr 15--16 & 2 Chr 5:13 Levitical vocal proclamation, and Ps 131:8 (*ark of thine holiness*).
- **Swete Greek Old Testament** (`edition.swete.old-testament-in-greek.first1kgreek-github-digitisation-2026-09-05`, CC BY-SA 4.0): Locally tracked for Psalms (`27-psalmi.txt`) and 3--4 Kingdoms (`13-regnorum-iii.txt`), directly verifying Greek *episkiasei soi* at Ps 90:4, *skirtao* at Ps 113:4, 6, *he kibotos tou hagiasmatos sou* at Ps 131:8, and 3 Kingdoms 6 & 8 (*dabeir*, and *nothing in the ark except the two stone tablets* at 8:9).
- **Masoretic-Base English Controls:** World English Bible Catholic Edition (`eng-web-c`, public domain), Revised Version 1895 (`eng-rv`, US public domain), and King James Version (`eng-kjv`, US public domain), controlling Hebrew-base readings at Judg 20:18, 26 (Bethel), 1 Sam 5:10 (Ekron), 2 Sam 6:2 (Baale of Judah), and Ps 132:8 (``ark of thy strength'').

### 1.2 Greek New Testament and MorphGNT Replay Controls
- **SBLGNT v1.2** (`edition.society-of-biblical-literature.sbl-greek-new-testament.faithlife-v1.2-c4d241a`, CC BY 4.0): Tracked surface Greek for Luke (`Luke.txt`: 1:26--56, 6:23, 9:34) and Revelation (`Rev.txt`: 11:19--12:6).
- **RP2018 Byzantine Textform** (`edition.robinson-pierpont.greek-new-testament-byzantine-textform.rp2018-byztxt-unicode-csv`, public domain): Tracked surface Greek for Matthew, Mark, Luke, Acts, and Revelation, documenting textual variants at Luke 1:28, 1:42 (*krauge* vs. *phone*), 1:44, 1:56, and Rev 11:19 (*autou* vs. *tou kyriou*, *kai brontai*).
- **MorphGNT-SBLGNT v6.12 Lemma-Field Projection** (`artifact.james-tauber.morphgnt-sblgnt.version-6.12-aaed91e.lemma-field-projection-9135bfb2`, CC BY-SA 3.0; 137,554 tokens): Exact New Testament lemma counts replayed directly:
  - *episkiazo* = **5** (Matt 17:5; Mark 9:7 [Vg 9:6]; Luke 1:35; Luke 9:34; Acts 5:15)
  - *anaphoneo* = **1** (Luke 1:42 — exact NT hapax legomenon)
  - *skirtao* = **3** (Luke 1:41, 1:44, 6:23 — exclusively Lukan; NOT shared by 2 Sam 6)
  - *kibotos* = **6** (4 Noah: Matt 24:38, Luke 17:27, Heb 11:7, 1 Pet 3:20; 2 Ark of the Covenant: Heb 9:4, Rev 11:19)
  - *kataskiazo* = **1** (Heb 9:5 — exact NT hapax legomenon)
  - *charitoo* = **2** (Luke 1:28; Eph 1:6)

## 2. Patristic, Scholastic, Liturgical, and Magisterial Witnesses

### 2.1 Verbatim Tracked Primary Witnesses (Public Domain)
- **Justin Martyr**, *Dialogue with Trypho* 100 (`ANF` Vol. 1, CCEL tracked text).
- **Irenaeus of Lyons**, *Adversus haereses* III.22.4 & V.19.1 (`ANF` Vol. 1 + Buffalo 1887 passage witness).
- **Athanasius of Alexandria**, *Orations against the Arians* III.14, 29, 33 (`NPNF` Series II, Vol. 4).
- **Cyril of Jerusalem**, *Catechesis* X.19 & **Gregory of Nazianzus**, *Epistle 101* (`NPNF` Series II, Vol. 7).
- **Gregory of Nyssa**, *Life of Moses* on Luke 1:35, plus a shadow reflection transmitted under his name (*In Diem Natalem*) via Aquinas, *Catena Aurea in Lucam*, Oxford 1843/1865 (where the Oxford margin flags `non occ.` beside the *In Diem Natalem* extract).
- **Ambrose of Milan**, *De Spiritu Sancto* III.11.79--80, *De Virginibus* II.2.15--18, *De Officiis* I.50.260 (`NPNF` Series II, Vol. 10), and *Expositio Evangelii secundum Lucam* Book II (CSEL 32/4 checked texts II.19, II.26; Migne PL 15 II.1, 5--7, 23, 25, 29).
- **Jerome**, *Commentary on Matthew* (on Matt 1:25) and *Contra Helvidium* cc. 5, 8, 10 (via Aquinas, *Catena Aurea in Matthaeum*, Oxford 1842).
- **Augustine of Hippo**, *Enarrationes in Psalmos* on Ps 131(132):8 (`NPNF` I, Vol. 8), *De natura et gratia* 36(42) & *De nuptiis et concupiscentia* I.12--13 (`NPNF` I, Vol. 5), *De consensu Evangelistarum* II.1.3 & *Sermon 51* §§18, 30 (`NPNF` I, Vol. 6), *Sermo* 185.1 (Migne PL 38 checked text).
- **Cyril of Alexandria**, *Commentary on Luke* Sermon I (Payne Smith, Oxford 1859).
- **Gregory the Great**, *Homiliae in Evangelia* VIII.1 (`8.1-bethlehem-checked-text-3f9b22a4`, Migne PL 76 col. 1104 A--B, Garnier 1878).
- **John of Damascus**, *De fide orthodoxa* III.12 & IV.14 (`NPNF` II, Vol. 9).
- **Venerable Bede**, *Explanatio Apocalypsis* Book II on Rev 11:19--12:1 (Marshall, Oxford/London 1878), and exposition of Luke 1:35 (via Aquinas, *Catena Aurea in Lucam*, Oxford 1843/1865).
- **Bernard of Clairvaux**, *Super Missus est* II.7 & IV.8 and *Vigil of the Nativity* (Washbourne, London 1909).
- **Thomas Aquinas**, *Summa theologiae* III, qq. 27--30 & q. 35 (English Dominicans, 1920).
- **Robert Bellarmine**, *Commentary on the Psalms* on Ps 131(132):7--8 (O'Sullivan, Dublin 1866).
- **Cornelius a Lapide**, *Commentaria in Quatuor Evangelia* Vol. 4 on Luke 1:35, 43, 46, 56 (Mossman, Edinburgh 1908).
- **Second Council of Constantinople (553)** Canons VI & XIV (via Hefele, Vol. 4, 1895); **Council of Trent (1546--1547)** Sess. V §6 & Sess. VI Canon XXIII (Devin-Adair 1912); **Pius IX**, *Ineffabilis Deus* (1854 Roman Latin & 1855 Murphy Baltimore bilingual); **Leo XIII**, *Quamquam pluries* (1889 Latin, ASS 22).
- **Liturgical Books and Received Prayers:** `src/sources/calendars/roman-1962/propers.yaml`, `src/sources/calendars/postconciliar/propers.yaml`, Pustet 1862 Assumption chants, Lasance New Roman Missal, and *The Raccolta* (1910: No. 75, *Mysteries of the Holy Childhood*, pp. 61--62; No. 189, *Litany of Loreto*, pp. 167--170).
- **Secondary Reference:** 1910 *Catholic Encyclopedia* Vol. 7 ("Immaculate Conception") for the historical summary of Bl. John Duns Scotus (*III Sent.*, d. 3).

### 2.2 Cataloged / Metadata-Only Witnesses (No Local Tracked Bytes; Summarized Without Fabricated Quotations)
- Councils of Ephesus (431), Chalcedon (451), and Lateran (649) standalone acts (though Ephesus and Chalcedon are reaffirmed verbatim in Constantinople II Canons VI & XIV).
- Pius XII, *Munificentissimus Deus* (1 Nov 1950, AAS 42, pp. 753--771, §44).
- Second Vatican Council, *Lumen gentium* (21 Nov 1964, §§52--69, esp. 53, 56, 60--62) and *Dei Verbum* (18 Nov 1965, §§11--12).
- Catechism of the Catholic Church (§§65--67, 499, 963--975, esp. 970).
- Paul VI (*Marialis Cultus*), John Paul II (*Redemptoris Custos*), Francis (*Patris Corde*).
- Dicastery for the Doctrine of the Faith, *Mater Populi Fidelis* (approved by Pope Leo XIV 7 Oct 2025; published 4 Nov 2025).
- John of Damascus, *Homilies on the Dormition* (Allies 1898 — catalog-only; no local artifact).

## 3. Consequential Negative Results and Attribution Boundaries

1. **Restricted Greek LXX Archives:** Full Greek LXX morphological archives (`catss`, `centerblc`, `eliran-wong`) are access-restricted and excluded from Git; Greek LXX Exodus 40:35, 2 Sam 6, and 1--2 Chronicles are therefore controlled via tracked Brenton English LXX, while tracked Swete Greek verifies Psalms (including Ps 90:4 *episkiasei soi* and Ps 131:8) and 3 Kingdoms (1 Kings 6 & 8).
2. **Spurious Patristic Attributions Excluded:** The Coptic encomium on the Papyrus of Turin often attributed to Athanasius (*"O noble Virgin... ark of the covenant"*) and the Marian Annunciation homilies printed under Gregory Thaumaturgus are neither locally tracked nor authentic third/fourth-century works of those Fathers, and are explicitly excluded as authentic early witnesses.
3. **Absent Patristic/Modern Works:** Ephrem's Hymns, Hesychius of Jerusalem, Proclus of Constantinople, Severus of Antioch, Romanos, Andrew of Crete, Germanus of Constantinople, Bernard's *Assumption Sermons*, Bonaventure's *III Sent.*, Scotus's *Ordinatio*, Alphonsus's *Le glorie di Maria*, Louis de Montfort, Newman's Marian writings, and Scheeben have no tracked Marian texts in `src/sources/` and carry no fabricated quotations.
4. **Honest Exegetical Boundaries:** Neither St. Ambrose (*In Lucam* II.29) nor Cornelius a Lapide (Vol. 4 on Luke 1:56) draws the 2 Samuel 6 / Obed-edom parallel at Luke 1:56; St. Augustine reads Ps 131(132):8 ecclesiologically and Christologically rather than directly Mariologically; and 2 Sam 6:14, 16 does not share the Greek verb *skirtao* with Luke 1:41, 44. All four facts are preserved transparently in body prose and synopsis tables.
