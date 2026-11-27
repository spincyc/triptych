# Source Audit — Postconciliar Illustrated Dictionary of the Roman Sanctuary

- **Owner:** `src/gemini/liturgy/roman-rite/postconciliar/2008-latin-2011-us-english/reference/roman-sanctuary-dictionary`
- **Declared edition-locale:** `2008-latin-2011-us-english` (*Missale Romanum* 2002/2008 + U.S. *Roman Missal, Third Edition* 2011 & USCCB GIRM adaptations emended through 22 October 2021)
- **As-of date:** `2026-11-25`

## 1. Source Verification Strategy and Rights Discipline

Modern official postconciliar liturgical books (LEV Latin *Missale Romanum*, ICEL/USCCB English *Roman Missal* and *General Instruction*, CCD *Lectionary*) are rights-restricted. In compliance with `guidance/sources.md` and `guidance/liturgical-text-publication-policy.md`:

- Locally registered postconciliar source records in `src/sources/works/` carry text-free metadata, hash-bound artifact pointers, segment boundaries, and verified passage records (`storage = "restricted"` or `"remote"`).
- Official postconciliar paragraphs not yet held as local passage TOMLs (specifically GIRM Chapters III–VI, *Redemptionis Sacramentum* 2004, *Caeremoniale Episcoporum* 1984, USCCB *Norms for Communion under Both Kinds* 2002/2011, and *Excerpts from the Roman Missal* 2018) were verified directly against official Holy See (`vatican.va`) and USCCB (`usccb.org`) witnesses on `2026-11-25`.
- Reader-facing dictionary entries use original analytical prose and verified technical Latin headwords rather than reproducing copyrighted liturgical texts, respecting the 29 November 2026 effective date of the 2025 USCCB *Guidelines for the Publication of Liturgical Books*.
- All 1962 counterpart loci, patristic/scholastic witnesses (St. Thomas Aquinas *ST* III q. 83 aa. 3–5; Amalarius of Metz *Liber Officialis* II), and Scripture quotations (Douay–Rheims Challoner revision in `src/sources/bibles/douay-rheims/`) were checked directly against tracked public-domain or registered witnesses inside `src/sources/`.

## 2. Repository-Registered Sources Bound (`src/sources/works/`)

| Source ID | Role | Local State | Verified Contribution |
| --- | --- | --- | --- |
| `edition.catholic-church.institutio-generalis-missalis-romani.latin-missale-romanum-typica-tertia-2002` | Governing Latin GIRM | Text-free (`restricted`); 41 passages incl. 299, 389 | Universal Latin headwords and IGMR structure |
| `edition.catholic-church.institutio-generalis-missalis-romani.english-us-2011-emended-2021` | Governing U.S. GIRM | Text-free (`restricted`); 21 passages incl. 28, 51, 2021 notice | U.S. GIRM adaptations (283, 301, 304, 329, 339, 346e/h) and Oct 2021 emendations |
| `edition.catholic-church.missale-romanum.vatican-typica-tertia-2002` | Governing Latin Missal | Text-free (`restricted`); 513 passages | 2002 third typical edition framework |
| `edition.catholic-church.missale-romanum.vatican-typica-tertia-reimpressio-emendata-2008` | 2008 Emended Reprint | Cataloged edition (`0` local artifacts); verified via *Notitiae* 503–504 | Confirms sanctuary/vessel/vesture IGMR rules unchanged in 2008 |
| `work.holy-see.reimpressio-emendata-missalis-romani-notice-2008` & `work.holy-see.variationes-et-additiones-missalis-romani-2008` | Currentness control | Verified passages (*Notitiae* 44 [2008] 367–388) | Bounds 2008 changes against unchanged IGMR articles |
| `edition.catholic-church.missale-romanum.vatican-typica-1970` | Historical postconciliar control | Text-free (`restricted`); 37 passages | 1970 transitional subdeacon/tunicle & vessel wording |
| `edition.catholic-church.ordo-lectionum-missae.latin-editio-typica-altera-1981` | Lectionary control | Text-free (`restricted`); 50 passages | Three-year/two-year Lectionary & Book of the Gospels |
| `edition.catholic-church.codex-iuris-canonici-1983.english-vatican-web-codex-2026-07-25` | Universal canon law | Text-free (`restricted`); includes can. 230 | Lay ministries, holy oils (847), font (858), Communion (910), tabernacle/lamp (938–940), altars (1235–1239) |
| `edition.second-vatican-council.sacrosanctum-concilium.english-vatican-web-2026-07-23` | Conciliar mandate | Text-free (`restricted`); 20 passages | Nos. 34–35, 50–55, 122–128 reform principles |
| `edition.paul-vi.missale-romanum-constitutio.english-vatican-web-2026-07-25` | Promulgating act | Text-free (`restricted`); verified complete | 3 Apr 1969 Apostolic Constitution promulgating revised Missal |
| `edition.paul-vi.ministeria-quaedam.latin-vatican-web-2026-07-27` | Ministry transition | Text-free (`restricted`); 3 verified passages | 15 Aug 1972 (eff. 1 Jan 1973) suppression of minor orders & subdiaconate |
| `edition.catholic-church.missale-romanum.vatican-typica-1962` & `edition.catholic-church.rubricae-breviarii-et-missalis-romani.latin-aas-52-1960` | 1962 comparison control | Verified passages (RG 131–137, 503, 526–528; RS I–X) | Direct 1962 counterpart collation |
| `edition.adrian-fortescue.ceremonies-of-the-roman-rite-described.seventh-revised-1943` | 1962 ceremonial context | Verified passages (pp. 8–9, 17, 37–40, 71, 78–81, 89–90) | 1962 sedilia, credence, processional cross, asperges, torches |
| `edition.thomas-aquinas.summa-theologiae.english-dominicans-gutenberg-tertia-2006` | Scholastic symbolism | Public-domain local text (`ST` III q. 83 aa. 3–5 read in full) | Grounded theology of altar, chalice, paten, corporal, incense, cross, lavabo |
| `edition.amalarius-of-metz.liber-de-ordine-antiphonarii.latin-migne-pl-105` | Medieval vestment allegory | Public-domain local OCR (*Liber Officialis* II.17–24) | Explicitly labeled medieval devotional tradition (never conflated with GIRM) |
| `edition.catholic-church.catechism.english-usccb-second-2019` | Doctrinal control | Verified passages (nn. 1240, 1300) | Baptismal font and Sacred Chrism theology |
| `work.united-states-conference-of-catholic-bishops.guidelines-publication-liturgical-books` | Rights control | Verified passages (2025 printing, eff. 29 Nov 2026) | Publication & quotation compliance boundary |

## 3. Official External Primary Acts Verified Online (Pending Central Registration)

The following authoritative postconciliar texts do not yet have standalone work or postconciliar edition records in `src/sources/works/` and were verified directly from official Holy See / USCCB sources on `2026-11-25` (with secondary corroboration noted for 1964–1984 older documents):

- **GIRM Chapters III–VI (2002/2008 Latin & 2011 USCCB English, emended 2021):** Verified directly on `usccb.org` and `vatican.va` for every sanctuary, vessel, linen, book, service, and vestment article (nos. 117–198, 274–349, 389–390).
- ***Redemptionis Sacramentum* (CDWDS, 25 March 2004; AAS 96:549–601):** Verified on `vatican.va` for nos. 47, 93, 106, 117–128, 130–131, 154–160.
- **USCCB *Norms for the Distribution and Reception of Holy Communion under Both Kinds* (2002/2011) & Oct 2006 CDWDS Non-Renewal Letter:** Verified for nos. 32–38, 52–55 (strict reservation of purification to priest, deacon, or instituted acolyte; prohibition on post-consecration flagon pouring).
- **USCCB *Excerpts from the Roman Missal* ("Book of the Chair", 2018):** Verified on `usccb.org` as the CDWDS-confirmed U.S. companion volume for GIRM 118a.
- ***Caeremoniale Episcoporum*, *editio typica* (14 Sept 1984):** Verified for no. 56 (pontifical dalmatic without separate tunicle), no. 65 (surplice always over cassock), and no. 274 (Chrism Mass). *(Note: `src/sources/works/catholic-church/caeremoniale-episcoporum` currently holds only the preconciliar 1948 edition.)*
- **CDWDS Response on GIRM 299 (25 Sept 2000, Prot. N. 2036/00/L; *Notitiae* 36:171–173):** Clarifies that *expedit* expresses desirability rather than an absolute juridical prohibition of wall-attached altars or *ad orientem* celebration.
- **1964–1973 Postconciliar Acts:** *Inter Oecumenici* (26 Sept 1964, nn. 91–96), *Tres abhinc annos* (4 May 1967, nn. 25–26), *Ordo benedicendi oleum* (3 Dec 1970), *Immensae caritatis* (29 Jan 1973), and *De sacra communione et de cultu mysterii eucharistici extra Missam* (21 June 1973, nn. 91–92).

## 4. Material Source Corrections Caught During Audit

1. **Chalice veil vs. burse in GIRM 118c:** 2002/2008 GIRM 118c restores explicit praise of the **chalice veil** (*velum calicis*), but does **not** name the **burse** (*bursa*), which remains customary.
2. **Formal USCCB adaptations vs. universal Roman norms:** Under GIRM 390 collation, nos. **283, 301, 304, 329, 339, 346(e), and 346(h)** carry explicit USCCB adaptations, while nos. **307, 309, 315, 316, and 336** are universal Roman norms without U.S.-specific textual insertions.
3. **Latin *pyxis* / *urceoli* terminology:** The Latin IGMR (118c, 306, 329) uses *pyxis* / *pyxides* where English GIRM translates "ciboria", and *urceoli* (rather than 1962 *ampullae*) for cruets.
4. **Baptismal font legal basis and patristic locus:** Governed by CIC 1983 can. 858, *Ordo Baptismi Parvulorum*, and the Easter Vigil rubrics rather than GIRM 311–318. St. Cyril of Jerusalem's "tomb and womb" baptismal catechesis stands in *Mystagogical Catechesis* 2.4 (*Catechesis* 20, §4) — verified against the NPNF2-7 Gifford edition (not *Procatechesis* 9, which treats exorcism).
5. **Anti-allegory control:** Purely practical furnishings and service items (`credence-table`, `ciborium`, `pyx`, `cruets`, `flagon`, `purificator`, `pall`, `lavabo-towel`, `book-of-the-chair`, `missal-stand`, `incense-boat`, `sanctuary-bells`, `cope`, `cassock-surplice`) are explicitly recorded without invented symbolism.
