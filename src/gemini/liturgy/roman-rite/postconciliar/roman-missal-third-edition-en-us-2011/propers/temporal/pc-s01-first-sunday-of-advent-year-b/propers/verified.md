# Verified Lectionary Composition — First Sunday of Advent, Year B (`PC-S01-B`)

- **Leaf path:** `src/gemini/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s01-first-sunday-of-advent-year-b`
- **Formula identifier:** `PC-S01-B` (U.S. Lectionary No. 2; *Ordo lectionum Missae* [OLM] n. 2)
- **Occurrence date:** `2026-11-29` (Sunday, 29 November 2026 — Year B / Weekday Cycle I)
- **Canonical shared Missal owner:** `src/gemini/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/shared/formularies/pc-s01-first-sunday-of-advent/propers/verified.md`
  - All Missal-formulary collation records, edition locators, SHA-256 digests, ancient sacramentary antecedents, and Missal rubrics for Entrance Antiphon, Collect, Prayer over the Offerings, Seasonal Preface, Communion Antiphon, Prayer after Communion, and Concluding Blessing are owned exclusively by that shared file and are not duplicated here.
- **Appointed text completeness:** `rights-limited`
- **Collation date:** 2026-11-25

---

## 1. Cycle-Specific Lectionary Witnesses and Bounds

| Control Role | Registered Source ID | Exact Locator / SHA-256 | Verified Scope and Bounds |
| :--- | :--- | :--- | :--- |
| Universal Latin Lectionary schedule (OLM 1981) | `artifact.catholic-church.ordo-lectionum-missae.latin-editio-typica-altera-1981.internet-archive-scan-pdf-ed4bc14e` (catalog lead for full PDF) | Artifact p. 59 / printed p. 5, n. 2 (*Dominica I Adventus*, Annus B); SHA-256 `ed4bc14e6c5f885be9cb220f4edbdd23c1db749b53c1489058d6e54cfaf7fd0d` | Restricted PDF not distributed in Git and not reopened offline; Year B citations were previously verified at 200 dpi in `src/sources/calendars/postconciliar/propers.yaml` (`advent-1`, Year B) and `postconciliar-seasonal-collation-v1.toml` (`Isaiah 64:2b`). |
| Lectionary *Praenotanda* (Latin & English — bound 1-to-1) | `passage.catholic-church.ordo-lectionum-missae.latin-editio-typica-altera-1981.{praenotanda-65,praenotanda-66,praenotanda-69,praenotanda-70-71,praenotanda-76,praenotanda-77,praenotanda-80,praenotanda-82-84}`; `passage.catholic-church.ordo-lectionum-missae.english-liturgy-office-web-2026-07-25.{praenotanda-65-69,praenotanda-74-77}` | Latin OLM nn. 65–66, 69, 70–71, 76, 77, 80 (`inspected`), 82–84; English OLM nn. 65–69, 74–77 | Directly inspected and bound 1-to-1 in `research/source-bindings.toml`: Latin `65` (independence of 3-yr Sunday and 2-yr ferial cycles), `66` (paragraph 2 & fn. 102 fixing Years A/B/C and Advent opening in the preceding civil year), `69` (2-yr Ordinary Time weekday cycle I/II), `70-71` (Proper vs. Common series), `76` (*De textibus difficilioribus*), `77` (*De omissione aliquorum versiculorum*), `80` (longer/shorter forms, `inspected` only), and `82-84` (proper/common memorials and weekday courses — outside Advent Sundays); English `65-69` (Sunday 3-reading structure, harmony vs. semi-continuous principles, non-imposition of organic Sunday themes) and `74-77` (reserving Isaiah to Advent, length forms, difficult texts, verse omissions). |
| U.S. Calendar cycle verification (2026 & 2027) | `passage.united-states-conference-of-catholic-bishops.liturgical-calendar-dioceses-united-states.2026.principal-celebrations-and-cycles`; `passage.united-states-conference-of-catholic-bishops.liturgical-calendar-dioceses-united-states.2027.principal-celebrations-and-cycles` | 2026 PDF `usccb-pdf-4bd9add0` (pp. 7–8, SHA-256 `4bd9add07512396a2323aa977bc4816a5fad6348262e12740bcee97c77372d02`); 2027 PDF `usccb-pdf-d7997b57` (pp. 7–8, SHA-256 `d7997b57de96fdbf6433af917a65597b108c720c930f3c39356bf0f5058074ce`) | Verified front-matter passages establish `2026-11-29` as the First Sunday of Advent opening Liturgical Year 2027 (Sunday Cycle B / Weekday Cycle I). The individual 29 November day-entry page of `2027cal.pdf` was not reopened offline (full PDFs bound as `lead`). |
| U.S. Lectionary day page & Common Psalms (cataloged leads, restricted) | `artifact.united-states-conference-of-catholic-bishops.daily-readings.2026-11-23-page-for-2026-11-29.lectionary-2-27c3cb63`; `artifact.catholic-church.ordo-lectionum-missae.2026-11-23-modern-psalter-us-common-psalms.{psalm-25-html-7c1bbedd,psalm-85-html-1447f8f2}` | Restricted USCCB daily reading page (`112926.cfm`, Lectionary No. 2) and Modern Psalter U.S. Advent Common Psalm pages (Lectionary No. 174: Ps 25[24] and Ps 85[84]) | Restricted payloads not tracked in Git and unavailable offline. No copyrighted NABRE, Abbey Psalms, or ICEL refrain wording is reproduced or paraphrased; exact refrain texts and verse spans of the two U.S. Advent Common Psalms remain an unresolved offline boundary. |
| Public-domain study Bibles (tracked controls — all 12 bound) | `artifact.catholic-church.vulgata-clementina.ebible-latvuc.verse-text-{21-psalms-d20e21f8,27-isaias-0eb1c68d,48-mark-ab7b8b95,53-1-corinthians-82f86d50}`; `artifact.english-college-of-douay.douay-rheims-bible.challoner-gutenberg-1581.verse-text-{21-psalms-578f023d,27-isaias-7c9a1228,48-mark-69b4cb75,53-1-corinthians-ffc4f260}`; `artifact.ebible-org.world-english-bible.catholic-eng-web-c.verse-text-{21-psalms-220b12de,27-isaias-ba3986d7,48-mark-524ad183,53-1-corinthians-b0f0a1e3}` | Full chapters `Is 63–64`, `Ps 24(25)`, `Ps 79(80)`, `Ps 84(85)`, `1Cor 1`, `Mark 13` read directly in tracked artifacts | Public-domain textual controls verifying exact verse boundaries, subverse omissions, and Vulgate vs. Hebrew numbering alignments. Douay–Rheims (Challoner) serves strictly as public-domain study English, never as the approved proclaimed U.S. Lectionary. |

---

## 2. Year B Lectionary Elements, Exact Verse Boundaries, and Numbering Alignments

### 2.1 First Reading (`first-reading`)
- **OLM n. 2 / U.S. Lectionary No. 2 citation (Hebrew/NABRE numbering):** `Isaiah 63:16b–17, 19b; 64:2b–7`
- **Clementine Vulgate / Douay–Rheims alignment:** **`Isaiah 63:16b–17; 64:1, 3b–8`** (whole-verse carrier: `Isaiah 63:16–17; 64:1, 3–8`)
- **Verified verse-boundary shift and exact omissions (cf. OLM *Praenotanda* n. 77 on verse omission):**
  - **Omitted `63:16a`:** Opens at the second half of v. 16 (*Tu, Domine, pater noster, redemptor noster, a saeculo nomen tuum* / "Thou, O Lord, art our father, our redeemer, from everlasting is thy name"), omitting the opening clause comparing God with Abraham and Israel (*Tu enim pater noster: et Abraham nescivit nos, et Israel ignoravit nos*).
  - **Omitted `63:18–19a` (NABRE) = `63:18–19` (Vulgate):** Omits the historical lament over enemies trampling the sanctuary and Israel becoming like those over whom God never ruled.
  - **Chapter-boundary shift (`63:19b` NABRE = `64:1` Vulgate):** In the Hebrew Masoretic Text and NABRE, the plea to rend the heavens and come down stands at the close of chapter 63 (`63:19b`), shifting every subsequent verse of chapter 64 by one compared with the Clementine Vulgate and Douay–Rheims (`64:1` = *Utinam dirumperes caelos, et descenderes; a facie tua montes defluerent*).
  - **Omitted `64:1–2a` (NABRE) = `64:2–3a` (Vulgate):** Omits the fire-and-boiling-water simile, the prayer to make God's name known to enemies, and the opening clause of v. 3 (*Cum feceris mirabilia, non sustinebimus*), resuming directly at the past-tense verb `64:2b` NABRE = `64:3b` Vulgate (*descendisti, et a facie tua montes defluxerunt* / "thou didst come down, and at thy presence the mountains melted away") and continuing unbroken through `64:7` NABRE = `64:8` Vulgate (*et opera manuum tuarum omnes nos* / "and we all are the works of thy hands").
- **Length alternatives:** None (no shorter or longer form is appointed in OLM n. 2; cf. OLM *Praenotanda* n. 80).

### 2.2 Responsorial Psalm (`responsorial-psalm`)
- **OLM n. 2 Latin citation (Vulgate numbering):** `Ps 79, 2ac. 3b. 15-16. 18-19`; Refrain `v. 4` (*Deus, converte nos, et ostende faciem tuam, et salvi erimus*)
- **U.S. Lectionary No. 2 citation (Hebrew / BHS / NABRE numbering):** `Psalm 80:2ac, 3b, 15-16, 18-19`; Refrain `Psalm 80:4`
- **Verified Vulgate/Hebrew alignment and exact omissions:**
  - Because both the Masoretic Text / NABRE (`Ps 80`) and the Clementine Vulgate / Douay–Rheims (`Ps 79`) count the superscription (*In finem, pro iis qui commutabuntur. Testimonium Asaph, psalmus*) as verse 1, the liturgical verse numbers match 1-to-1 between NABRE `Ps 80` and Vulgate `Ps 79` (whereas translations that exclude superscriptions from verse numbering, such as WEB-C, shift vv. 2–20 down by 1 to vv. 1–19).
  - **Stanza 1 (`2ac, 3b`):** Includes `2a` (*Qui regis Israel, intende*) and `2c` (*Qui sedes super cherubim, manifestare*), omitting `2b` (*qui deducis velut ovem Joseph*) and `3a` (*coram Ephraim, Benjamin, et Manasse*), and concluding with `3b` (*Excita potentiam tuam, et veni, ut salvos facias nos*).
  - **Omitted central lament (`vv. 5–14`):** Omits the bread of tears, mocking neighbors, and the extended allegory of the vine transplanted from Egypt and ravaged by the boar.
  - **Stanza 2 (`vv. 15–16`):** *Deus virtutum, convertere, respice de caelo, et vide, et visita vineam istam: et perfice eam quam plantavit dextera tua, et super filium hominis quem confirmasti tibi.*
  - **Omitted imprecation (`v. 17`):** Omits *Incensa igni et suffossa, ab increpatione vultus tui peribunt*.
  - **Stanza 3 (`vv. 18–19`):** *Fiat manus tua super virum dexterae tuae, et super filium hominis quem confirmasti tibi. Et non discedimus a te: vivificabis nos, et nomen tuum invocabimus.*
- **Closed seasonal alternatives (`branch-responsorial-psalm`):** Under GIRM 61, seasonal substitutes may be used when sung (alongside the *Graduale Romanum*, *Graduale Simplex*, or another approved collection, excluding songs/hymns); the registered U.S. Lectionary No. 174 catalog leads identify two Advent Common Psalms — `Psalm 25(24)` and `Psalm 85(84)`. Because the restricted Modern Psalter HTML artifacts (`psalm-25-html-7c1bbedd`, `psalm-85-html-1447f8f2`) could not be reopened offline, their exact U.S. refrain texts and stanza verse spans are neither quoted nor invented here and remain an explicit offline boundary.

### 2.3 Second Reading (`second-reading`)
- **OLM n. 2 / U.S. Lectionary No. 2 citation:** `1 Corinthians 1:3–9`
- **Vulgate / Greek alignment:** Identical verse numbering (`1Cor 1:3–9`).
- **Boundaries and omissions:** Begins after the epistolary prescript (`1:1–2`, Paul and Sosthenes to the sanctified Church at Corinth), opening with the apostolic greeting (`1:3`, *Gratia vobis et pax*) and spanning the complete thanksgiving section (`1:4–9`) right up to the transition into Paul's rebuke of Corinthian factions (`1:10`). No internal verses are omitted; no shorter/longer form exists.

### 2.4 Gospel Acclamation (`gospel-acclamation`)
- **Identifying Latin incipit:** *Ostende nobis, Domine*
- **OLM n. 2 citation (Vulgate):** `Ps 84, 8` (*Ostende nobis, Domine, misericordiam tuam, et salutare tuum da nobis*)
- **U.S. Lectionary No. 2 citation (Hebrew / BHS / NABRE):** `Psalm 85:8` (identical verse number because NABRE/BHS counts the superscription as v. 1; corresponds to `85:7` in translations omitting the superscription from verse numbers).
- **Rubrical note (GIRM 62):** Outside Lent, the acclamation before the Gospel is the *Alleluia*, whose verses are taken from the Lectionary or the *Graduale*. (Note: tracked `GIRM 63.toml` records only the provisions when there is one reading before the Gospel; the specific unsung-omission sub-clause of GIRM 63 was not verified in a tracked passage and remains an open offline boundary.)

### 2.5 Gospel (`gospel`)
- **OLM n. 2 / U.S. Lectionary No. 2 citation:** `Mark 13:33–37`
- **Vulgate / Greek alignment:** Identical verse numbering (`Mark 13:33–37`).
- **Boundaries and omissions:** Forms the closing pericope of Jesus' Olivet Discourse (`Mark 13:1–37`), beginning immediately after the omitted verse `13:32` (*De die autem illo vel hora nemo scit, neque angeli in caelo, neque Filius, nisi Pater*) — an omission directly relevant to OLM *Praenotanda* nn. 76–77 and to patristic reception, because ancient commentators read `13:33–37` continuously out of `13:32`. No internal verses are omitted; no shorter/longer form exists.

---

## 3. Rights Disposition and Study-English Notice

- **Completeness class:** `rights-limited` (under `src/sources/inventories/liturgical-english-rights-v1.toml` and `guidance/liturgy/postconciliar-propers.md`).
- **Mandatory standing distinction:** The approved proclaimed U.S. Lectionary (NABRE / Abbey Psalms) and ICEL 2011 English Missal are protected works and are neither reproduced nor closely paraphrased. All English Scripture quotations in `propers/retrieved.txt` and in the forthcoming study editions come from the tracked public-domain **Douay–Rheims (Challoner)** text and are explicitly identified as **public-domain study English**, never as the approved proclaimed text of the U.S. Lectionary.
- **Public-domain Latin study texts:** Clementine Vulgate Latin texts for all appointed biblical units are transcribed directly from tracked repository witnesses in `propers/retrieved.txt`. Missal-owned antiphon collation and historical sacramentary evidence remain owned by the canonical shared Missal owner.

---

## 4. Open Verification Boundaries (Leaf Level)

1. **USCCB `2027cal.pdf` day-entry line and `112926.cfm` live HTML:** Both restricted artifacts are registered in `src/sources/` without tracked payloads and could not be reopened offline. Cycle confirmation rests on the verified `principal-celebrations-and-cycles` passages of the 2026 and 2027 USCCB calendars; Lectionary pericopes rest on the 200-dpi OLM 1981 verification recorded in `propers.yaml`.
2. **U.S. Advent Common Psalm refrain wordings and verse spans:** Lectionary No. 174 (`Ps 25[24]` and `Ps 85[84]`) are cataloged as Advent Common Psalm leads, while their exact U.S. refrain texts and verse selections remain unverified offline.
3. **GIRM 63 unsung-omission sub-clause:** Not extracted in tracked `63.toml`; left as an open offline rubric boundary.
4. **Missal-owned bounds:** See the canonical shared Missal owner (`shared/formularies/pc-s01-first-sunday-of-advent/propers/verified.md`, §4) for the uncollated 2008 altar-book check, Entrance Antiphon cue boundary, modern Latin oration/Preface/blessing bodies, Appendix Eucharistic Prayers, and unextracted GIRM 346/305/313 rubrics.
